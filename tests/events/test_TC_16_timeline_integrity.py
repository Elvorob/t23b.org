"""
TC-16: Events Timeline Integrity (Desktop) — automated tests.

Verify that the timeline is visible on desktop viewport (lg breakpoint),
all 12 months are present in school-year order, events have valid data
attributes, start <= end invariant holds, events are clickable links,
and the Overview count matches unique event IDs.
"""
from __future__ import annotations

import re
from datetime import datetime

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.conftest import EVENTS_URL

SEASON_URL_PATTERN = re.compile(r"/events/\d{4}-\d{4}/?")
DESKTOP_VIEWPORT = {"width": 992, "height": 800}

EXPECTED_MONTHS = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
VALID_STATUSES = {"confirmed", "tentative", "postponed", "cancelled"}


def _goto_events_desktop(page: Page) -> str:
    """Set desktop viewport and navigate to events page. Returns final URL."""
    page.set_viewport_size(DESKTOP_VIEWPORT)
    page.goto(EVENTS_URL, wait_until="domcontentloaded")
    page.wait_for_url(SEASON_URL_PATTERN, timeout=10_000)
    return page.url


def _collect_timeline_events(page: Page) -> list[dict]:
    """Extract data attributes from all timeline event elements."""
    elements = page.locator(".events-timeline-event").all()
    events = []
    for el in elements:
        events.append({
            "id": el.get_attribute("data-event-id") or "",
            "title": el.get_attribute("data-event-title") or "",
            "start": el.get_attribute("data-event-start") or "",
            "end": el.get_attribute("data-event-end") or "",
            "categories": el.get_attribute("data-event-categories") or "",
            "status": el.get_attribute("data-event-status") or "",
            "hidden": el.get_attribute("data-hidden") or "",
            "dimmed": el.get_attribute("data-dimmed") or "",
            "href": el.get_attribute("href") or "",
            "tag": el.evaluate("el => el.tagName.toLowerCase()"),
        })
    return events


@allure.epic("Events Page")
@allure.feature("Timeline Integrity")
@allure.story("Timeline visibility")
@allure.title("TC-16-01: Timeline is visible on desktop viewport (992px)")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_16_1_timeline_visible_on_desktop(page: Page, step_logger):
    """TC-16-01: Timeline container is visible at the lg breakpoint (992px)."""
    with allure.step("Open events page with 992px viewport"):
        step_logger.start_step("Open events page with 992px viewport")
        final_url = _goto_events_desktop(page)
        step_logger.log_text(f"[Navigation] final URL = {final_url}")
        print(f"\n[test_TC_16_1] viewport = {DESKTOP_VIEWPORT}, url = {final_url!r}")

    with allure.step("Check .events-timeline is visible"):
        step_logger.start_step("Check .events-timeline is visible")
        timeline = page.locator(".events-timeline")
        assert timeline.is_visible(), (
            "Timeline (.events-timeline) should be visible at 992px (lg breakpoint)"
        )
        allure.attach(
            f"Viewport: {DESKTOP_VIEWPORT}\nTimeline visible: True",
            name="Timeline visibility",
            attachment_type=allure.attachment_type.TEXT,
        )
        step_logger.checkpoint("Timeline is visible at 992px viewport")

    with allure.step("Take screenshot"):
        step_logger.take_screenshot("timeline_desktop")


@allure.epic("Events Page")
@allure.feature("Timeline Integrity")
@allure.story("Month headers")
@allure.title("TC-16-02: All 12 months present in school-year order")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_16_2_twelve_months_in_order(page: Page, step_logger):
    """TC-16-02: Timeline has 12 month headers in Sep..Aug order."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events_desktop(page)

    with allure.step("Collect month headers"):
        step_logger.start_step("Collect month headers")
        headers = page.locator(".events-timeline-month-header").all_inner_texts()
        months = [m.strip() for m in headers]
        print(f"\n[test_TC_16_2] months = {months!r}")
        allure.attach(
            "\n".join(f"{i+1}. {m}" for i, m in enumerate(months)),
            name="Month headers",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Assert exactly 12 months"):
        step_logger.start_step("Assert exactly 12 months")
        assert len(months) == 12, f"Expected 12 month headers, got {len(months)}: {months}"
        step_logger.checkpoint(f"Found {len(months)} month headers")

    with allure.step("Assert correct order (Sep through Aug)"):
        step_logger.start_step("Assert correct order (Sep through Aug)")
        assert months == EXPECTED_MONTHS, (
            f"Month order mismatch.\nExpected: {EXPECTED_MONTHS}\nGot:      {months}"
        )
        step_logger.checkpoint("Months are in correct school-year order: Sep..Aug")


@allure.epic("Events Page")
@allure.feature("Timeline Integrity")
@allure.story("Data attributes")
@allure.title("TC-16-03: Timeline events have required data attributes")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_16_3_events_have_required_data_attributes(page: Page, step_logger):
    """TC-16-03: Every timeline event has valid id, dates, categories, and status."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events_desktop(page)

    with allure.step("Collect all timeline events"):
        step_logger.start_step("Collect all timeline events")
        events = _collect_timeline_events(page)
        assert len(events) >= 1, "Expected at least 1 timeline event"
        print(f"\n[test_TC_16_3] total_timeline_events = {len(events)}")

    errors = []
    status_counts: dict[str, int] = {}

    with allure.step("Validate data attributes for each event"):
        step_logger.start_step("Validate data attributes for each event")
        for i, ev in enumerate(events):
            label = f"[{i}] {ev['title']!r}"

            if not ev["id"]:
                errors.append(f"{label}: data-event-id is empty")

            for field in ("start", "end"):
                val = ev[field]
                if not val:
                    errors.append(f"{label}: data-event-{field} is empty")
                else:
                    try:
                        datetime.strptime(val, "%Y-%m-%d")
                    except ValueError:
                        errors.append(f"{label}: data-event-{field} = {val!r} is not a valid YYYY-MM-DD date")

            if ev["status"] not in VALID_STATUSES:
                errors.append(f"{label}: data-event-status = {ev['status']!r} not in {VALID_STATUSES}")

            status_counts[ev["status"]] = status_counts.get(ev["status"], 0) + 1

            step_logger.log_text(
                f"  event {i}: id={ev['id'][:8]}… title={ev['title']!r} "
                f"start={ev['start']} end={ev['end']} status={ev['status']} cats={ev['categories']!r}"
            )

    summary = (
        f"Total events: {len(events)}\n"
        f"Status breakdown: {status_counts}\n"
        f"Errors: {len(errors)}"
    )
    print(f"\n[test_TC_16_3] {summary}")
    allure.attach(summary, name="Validation summary", attachment_type=allure.attachment_type.TEXT)

    if errors:
        allure.attach("\n".join(errors), name="Validation errors", attachment_type=allure.attachment_type.TEXT)

    assert not errors, f"{len(errors)} validation error(s):\n" + "\n".join(errors)
    step_logger.checkpoint(f"All {len(events)} events have valid data attributes")


@allure.epic("Events Page")
@allure.feature("Timeline Integrity")
@allure.story("Date invariant")
@allure.title("TC-16-04: Start date is not after end date for all events")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_16_4_start_not_after_end(page: Page, step_logger):
    """TC-16-04: For every timeline event, start_date <= end_date."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events_desktop(page)

    with allure.step("Collect timeline events"):
        step_logger.start_step("Collect timeline events")
        events = _collect_timeline_events(page)
        assert len(events) >= 1, "Expected at least 1 timeline event"

    violations = []

    with allure.step("Check start <= end for each event"):
        step_logger.start_step("Check start <= end for each event")
        for ev in events:
            try:
                start = datetime.strptime(ev["start"], "%Y-%m-%d")
                end = datetime.strptime(ev["end"], "%Y-%m-%d")
            except ValueError:
                violations.append(f"{ev['title']!r}: unparseable dates start={ev['start']!r} end={ev['end']!r}")
                continue

            if start > end:
                violations.append(
                    f"{ev['title']!r}: start ({ev['start']}) > end ({ev['end']})"
                )

        print(f"\n[test_TC_16_4] checked {len(events)} events, violations = {len(violations)}")

    if violations:
        allure.attach("\n".join(violations), name="Date violations", attachment_type=allure.attachment_type.TEXT)

    assert not violations, f"{len(violations)} date violation(s):\n" + "\n".join(violations)
    step_logger.checkpoint(f"All {len(events)} events satisfy start <= end")


@allure.epic("Events Page")
@allure.feature("Timeline Integrity")
@allure.story("Clickable links")
@allure.title("TC-16-05: Timeline events are clickable links to event pages")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_16_5_events_are_clickable_links(page: Page, step_logger):
    """TC-16-05: Each timeline event is an <a> tag with href containing /events/."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events_desktop(page)

    with allure.step("Collect timeline events"):
        step_logger.start_step("Collect timeline events")
        events = _collect_timeline_events(page)
        assert len(events) >= 1, "Expected at least 1 timeline event"

    errors = []

    with allure.step("Validate tag and href for each event"):
        step_logger.start_step("Validate tag and href for each event")
        for i, ev in enumerate(events):
            label = f"[{i}] {ev['title']!r}"

            if ev["tag"] != "a":
                errors.append(f"{label}: tag is <{ev['tag']}>, expected <a>")

            if "/events/" not in ev["href"]:
                errors.append(f"{label}: href={ev['href']!r} does not contain '/events/'")

            step_logger.log_text(f"  event {i}: tag=<{ev['tag']}> href={ev['href']}")

        print(f"\n[test_TC_16_5] checked {len(events)} events, errors = {len(errors)}")

    if errors:
        allure.attach("\n".join(errors), name="Link errors", attachment_type=allure.attachment_type.TEXT)

    assert not errors, f"{len(errors)} link error(s):\n" + "\n".join(errors)
    step_logger.checkpoint(f"All {len(events)} events are <a> tags with valid /events/ hrefs")


@allure.epic("Events Page")
@allure.feature("Timeline Integrity")
@allure.story("Overview count")
@allure.title("TC-16-06: Overview count matches unique timeline event IDs")
@allure.severity(allure.severity_level.NORMAL)
def test_TC_16_6_overview_count_matches_timeline(page: Page, step_logger):
    """TC-16-06: The number in 'Overview (N)' equals the count of unique event IDs in the timeline."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events_desktop(page)

    with allure.step("Extract Overview count from heading"):
        step_logger.start_step("Extract Overview count from heading")
        title_el = page.locator(".events-timeline-title")
        title_text = title_el.inner_text().strip()
        print(f"\n[test_TC_16_6] overview_title_text = {title_text!r}")

        m = re.search(r"\((\d+)\)", title_text)
        assert m, f"Could not find (N) in Overview heading: {title_text!r}"
        overview_n = int(m.group(1))
        allure.attach(str(overview_n), name="Overview N", attachment_type=allure.attachment_type.TEXT)
        step_logger.log_text(f"Overview count N = {overview_n}")

    with allure.step("Count timeline events and unique IDs"):
        step_logger.start_step("Count timeline events and unique IDs")
        events = _collect_timeline_events(page)
        total_elements = len(events)
        unique_ids = set(ev["id"] for ev in events if ev["id"])
        unique_count = len(unique_ids)

        hidden_count = sum(1 for ev in events if ev["hidden"] == "true")
        dimmed_count = sum(1 for ev in events if ev["dimmed"] == "true")

        summary = (
            f"Total timeline elements: {total_elements}\n"
            f"Unique event IDs: {unique_count}\n"
            f"Overview N: {overview_n}\n"
            f"Hidden (data-hidden=true): {hidden_count}\n"
            f"Dimmed (data-dimmed=true): {dimmed_count}"
        )
        print(f"\n[test_TC_16_6] {summary}")
        allure.attach(summary, name="Count breakdown", attachment_type=allure.attachment_type.TEXT)
        step_logger.log_text(summary)

    with allure.step("Assert Overview count equals unique event IDs"):
        step_logger.start_step("Assert Overview count equals unique event IDs")
        assert overview_n == unique_count, (
            f"Overview says {overview_n} but found {unique_count} unique event IDs "
            f"({total_elements} total elements). "
            f"Difference may be due to multi-day occurrences sharing the same event ID."
        )
        step_logger.checkpoint(
            f"Overview count ({overview_n}) matches unique timeline event IDs ({unique_count})"
        )
