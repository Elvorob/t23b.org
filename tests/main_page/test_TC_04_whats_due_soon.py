"""
TC-04: What's Due Soon — automated tests.

User Story US-04: Scout or parent wants to see what is due soon with deadline and link,
and that each due item is consistent with its event page (names and dates).
"""

import re

from playwright.sync_api import Page

from tests.conftest import BASE_URL


def _due_section(page: Page):
    """Locate the due section by the word 'Due' (heading text may change, e.g. What's Due / What's Due Soon)."""
    return page.get_by_text("Due", exact=False).first


def _due_container(page: Page):
    section = _due_section(page)
    return section.locator("xpath=ancestor::section|ancestor::div").first


# Month name (and common abbrev) -> number 1-12 for parsing.
_MONTH_TO_NUM = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def _parse_date_to_canonical(text: str) -> tuple[int, int] | None:
    """
    Parse a date from free text into a canonical (month, day) form for comparison.
    Supports: "Jan 5", "January 5", "5 Jan", "July 5-11", "Mar 1 5d ago",
    "01/05/2026", "1/5/26", "2026-01-05", "5.1.2026", "05.01".
    Returns (month, day) with month 1-12, day 1-31, or None if no date found.
    """
    if not text or not text.strip():
        return None
    text = text.strip()
    # 1) Month name + day (optionally with range or suffix): "July 5", "July 5-11, 2026", "Mar 1\n5d ago"
    month_names = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    m = re.search(rf"(?i){month_names}\s+(\d{{1,2}})(?:-\d{{1,2}})?(?:,\s*\d{{4}})?", text)
    if m:
        month_str, day_str = m.group(1).lower(), m.group(2)
        month = _MONTH_TO_NUM.get(month_str) or next((v for k, v in _MONTH_TO_NUM.items() if month_str.startswith(k[:3])), None)
        if month and month <= 12:
            day = int(day_str)
            if 1 <= day <= 31:
                return (month, day)
    # 2) Day + month name: "5 July", "15 January"
    m = re.search(rf"(\d{{1,2}})\s+{month_names}(?:\s+\d{{4}})?", text, re.IGNORECASE)
    if m:
        day_str, month_str = m.group(1), m.group(2).lower()
        month = _MONTH_TO_NUM.get(month_str) or next((v for k, v in _MONTH_TO_NUM.items() if month_str.startswith(k[:3])), None)
        if month and month <= 12:
            day = int(day_str)
            if 1 <= day <= 31:
                return (month, day)
    # 3) ISO: YYYY-MM-DD
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if m:
        month, day = int(m.group(2)), int(m.group(3))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return (month, day)
    # 4) US numeric: MM/DD or MM/DD/YY(YY)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", text)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return (month, day)
    # 5) DD.MM or DD.MM.YYYY
    m = re.search(r"\b(\d{1,2})\.(\d{1,2})(?:\.(\d{2,4}))?\b", text)
    if m:
        day, month = int(m.group(1)), int(m.group(2))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return (month, day)
    return None


def _canonical_date_str(pair: tuple[int, int] | None) -> str:
    """Format (month, day) for messages; return empty if None."""
    if pair is None:
        return ""
    return f"{pair[0]:02d}-{pair[1]:02d}"


def _collect_due_items(page: Page):
    """
    Collect due items from the Due section table.

    Table structure: col0 = icon, col1 = milestone (with link to event), col2 = event name, col3 = due date.
    Link to event page is in the milestone column (col1), not in the due column.

    Returns list of dicts:
    - milestone_name: text from milestone column (e.g. "Deposit Fee", "RSVP")
    - event_name: event name column (e.g. "Summer Camp")
    - due_text: text from due column (e.g. "Mar 1 5d ago")
    - href: link to the event page (from milestone column)
    """
    container = _due_container(page)
    rows = container.locator("tr")
    row_count = rows.count()
    print(f"\n[_collect_due_items] table row count = {row_count}")

    items = []
    for i in range(row_count):
        row = rows.nth(i)
        cells = row.locator("td")
        cell_count = cells.count()
        if cell_count < 4:
            continue
        milestone_cell = cells.nth(1)
        link = milestone_cell.locator("a").first
        if not link.count() or not link.is_visible():
            continue
        href = (link.get_attribute("href") or "").strip()
        if "/events/" not in href:
            continue
        milestone_name = (link.inner_text() or milestone_cell.inner_text()).strip()
        event_name = cells.nth(2).inner_text().strip()
        due_text = cells.nth(3).inner_text().strip()
        print(
            f"[_collect_due_items] row {i}: milestone={milestone_name!r}, "
            f"event_name={event_name!r}, due_text={due_text!r}, href={href!r}"
        )
        items.append(
            {
                "milestone_name": milestone_name,
                "event_name": event_name,
                "due_text": due_text,
                "href": href,
            }
        )
    return items


def test_TC_04_1_whats_due_soon_section_visible(page: Page, step_logger):
    """TC-04-01: Due section (contains word 'Due') is visible."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check Due section is visible (section containing 'Due')")
    section = _due_section(page)
    visible = section.is_visible()
    print(f"\n[test_whats_due_soon_section_visible] visible = {visible}")
    assert visible, "Section containing 'Due' should be visible"
    step_logger.checkpoint("Due section is visible")


def test_TC_04_2_whats_due_soon_has_events(page: Page, step_logger):
    """TC-04-02: At least one due-soon item (event) is displayed."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Collect due events from Due section")
    items = _collect_due_items(page)
    count = len(items)
    print(f"\n[test_whats_due_soon_has_events] due event count = {count}")
    assert count > 0, "Expected at least one due event in Due section"
    step_logger.checkpoint(
        f"Found {count} due events in Due section"
    )


def test_TC_04_3_due_events_match_event_pages(page: Page, step_logger):
    """
    TC-04-03/04/05: Due events match their event pages (names and dates).

    For each due item:
    - Event name (second column) matches event page title (keywords overlap).
    - Nearest-date name (first column) matches the corresponding sub-section heading.
    - Due date in the due column matches the date in the event page sub-section.
    """
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Collect due events from Due section")
    due_items = _collect_due_items(page)
    count = len(due_items)
    print(f"\n[test_due_events_match_event_pages] due_items = {due_items!r}")
    assert count > 0, "Expected at least one due event to validate against event pages"
    step_logger.checkpoint(f"Prepared {count} due events for detailed validation")

    for idx, item in enumerate(due_items, start=1):
        milestone_name = item["milestone_name"].strip()
        due_event_name = item["event_name"].strip()
        due_text = item["due_text"].strip()
        href = item["href"].strip()
        print(
            f"\n[test_due_events_match_event_pages] row {idx}: "
            f"milestone_name={milestone_name!r}, due_event_name={due_event_name!r}, "
            f"due_text={due_text!r}, href={href!r}"
        )

        step_logger.start_step(
            f"Open homepage and click due event {idx} ({due_event_name})"
        )
        page.goto(BASE_URL, wait_until="domcontentloaded")
        link = page.locator(f"a[href='{href}']").first
        assert link.is_visible(), (
            f"Due event {idx}: link with href {href!r} should be visible in Due section"
        )
        link.click()
        # Capture full-page screenshot of the event page
        step_logger.take_screenshot(f"due_event_{idx}_event_page")

        # 1) Compare event name (due section second column) with event page title (H1)
        step_logger.start_step(
            f"Compare due event name with event page title for due event {idx}"
        )
        event_title = page.locator("h1").first.inner_text().strip()
        print(
            f"[test_due_events_match_event_pages] row {idx}: "
            f"event_title={event_title!r}"
        )
        due_words = [
            w.lower()
            for w in re.split(r"\s+", due_event_name)
            if len(w) > 2
        ]
        title_lower = event_title.lower()
        matching_words = [w for w in due_words if w in title_lower]
        print(
            f"[test_due_events_match_event_pages] row {idx}: "
            f"due_words={due_words!r}, matching_words={matching_words!r}"
        )
        assert matching_words, (
            f"Due event {idx}: expected event page title {event_title!r} "
            f"to contain keywords from due event name {due_event_name!r}"
        )
        step_logger.checkpoint(
            f"Due event {idx}: event title matches due event name keywords"
        )

        # 2) Compare nearest-date name (first column) with sub-section heading on event page
        step_logger.start_step(
            f"Locate milestone '{milestone_name}' on event page for due event {idx}"
        )
        milestone_heading = page.get_by_text(
            milestone_name, exact=False
        ).first
        assert milestone_heading.is_visible(), (
            f"Due event {idx}: expected to find milestone heading containing "
            f"{milestone_name!r} on event page"
        )
        milestone_heading_text = milestone_heading.inner_text().strip()
        print(
            f"[test_due_events_match_event_pages] row {idx}: "
            f"milestone_heading_text={milestone_heading_text!r}"
        )
        assert milestone_name.lower() in milestone_heading_text.lower(), (
            f"Due event {idx}: milestone name {milestone_name!r} from Due section "
            f"should match heading {milestone_heading_text!r} on event page"
        )
        step_logger.checkpoint(
            f"Due event {idx}: milestone name matches event page sub-section heading"
        )

        # 3) Compare due date (due column) with date in the milestone sub-section on event page
        step_logger.start_step(
            f"Compare due date text with event page milestone date for due event {idx}"
        )
        # Find the first block *after* the milestone heading that contains a parseable date.
        # No dependency on label text (e.g. "When:") — works even if the site changes wording.
        when_text = ""
        for i in range(50):
            candidate = milestone_heading.locator("xpath=following::*").nth(i)
            if candidate.count() == 0:
                break
            text = (candidate.inner_text() or "").strip()
            if text and _parse_date_to_canonical(text) is not None:
                when_text = text
                break
        when_text = when_text.strip()
        print(
            f"[test_due_events_match_event_pages] row {idx}: "
            f"due_text={due_text!r}, when_text={when_text!r}"
        )
        assert when_text, (
            f"Due event {idx}: no block with a parseable date found after milestone heading on event page"
        )
        due_canonical = _parse_date_to_canonical(due_text)
        event_canonical = _parse_date_to_canonical(when_text)
        print(
            f"[test_due_events_match_event_pages] row {idx}: "
            f"due_canonical={_canonical_date_str(due_canonical)!r}, "
            f"event_canonical={_canonical_date_str(event_canonical)!r}"
        )
        assert due_canonical, (
            f"Due event {idx}: could not parse date from due text {due_text!r}"
        )
        assert event_canonical, (
            f"Due event {idx}: could not parse date from event page block {when_text!r}"
        )
        assert due_canonical == event_canonical, (
            f"Due event {idx}: due date (normalized {_canonical_date_str(due_canonical)}) from Due section "
            f"should match event page date (normalized {_canonical_date_str(event_canonical)}) "
            f"(due_text={due_text!r}, when_text={when_text!r})"
        )
        step_logger.checkpoint(
            f"Due event {idx}: due date in Due section matches event page date"
        )

