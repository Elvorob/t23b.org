"""
TC-13: About Us page — automated tests.

Covers: page load 200, containers (heading + text), Leadership block,
About the Troop (Troop size, Scouting season), last updated year,
footer, top menu, links and images (API check), console, UX, navigation, scaling.
"""

import re
import time
from datetime import datetime
from urllib.parse import urljoin

import pytest
import requests
from playwright.sync_api import Page

from tests.conftest import (
    ABOUT_US_URL,
    BASE_URL,
    get_console_error_allowlist,
)
from tests.footer_checks import assert_footer_structure_and_contacts_ok
from tests.link_checks import check_url_not_broken_and_not_empty

BASE_URL_NORMALIZED = BASE_URL.rstrip("/")
ABOUT_US_PAGE_HTTP_TIMEOUT = 15
ABOUT_US_PAGE_HTTP_RETRIES = 2
ABOUT_US_PAGE_HTTP_RETRY_DELAY = 2
DESKTOP_VIEWPORT = {"width": 1280, "height": 720}
MOBILE_VIEWPORT = {"width": 375, "height": 667}
SCOUTING_SEASON_EXACT_PHRASE = "Scouting season: September to June"


def _ensure_about_us(page: Page, step_logger, viewport: dict | None = None):
    if viewport:
        step_logger.start_step(f"Set viewport to {viewport['width']}x{viewport['height']}")
        page.set_viewport_size(viewport)
    step_logger.start_step("Open About Us page")
    page.goto(ABOUT_US_URL, wait_until="domcontentloaded")


def test_TC_13_1_about_us_returns_200(step_logger):
    """TC-13-01: About Us page returns HTTP 200."""
    step_logger.start_step("Send GET request to About Us (with retry on timeout)")
    response = None
    for attempt in range(ABOUT_US_PAGE_HTTP_RETRIES + 1):
        try:
            response = requests.get(ABOUT_US_URL, timeout=ABOUT_US_PAGE_HTTP_TIMEOUT)
            break
        except requests.Timeout as e:
            if attempt < ABOUT_US_PAGE_HTTP_RETRIES:
                step_logger.log_text(
                    f"[Retry] attempt {attempt + 1} timed out; "
                    f"waiting {ABOUT_US_PAGE_HTTP_RETRY_DELAY}s"
                )
                time.sleep(ABOUT_US_PAGE_HTTP_RETRY_DELAY)
            else:
                raise e
    step_logger.log_text(f"[Request] GET {ABOUT_US_URL}")
    step_logger.log_text(f"[Response] {response.status_code} {ABOUT_US_URL}")
    step_logger.start_step("Check response status is 200")
    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )
    step_logger.checkpoint("About Us response status is 200")


def _get_containers_with_headings(page: Page):
    """
    Return list of (heading_text, container_locator) for each content block
    that has a heading (h1, h2, h3) and body. Uses section or heading parent.

    If <section> exists but does not wrap headings (empty pass), fall back to
    each h1/h2/h3 and its parent — same as Resources page layout edge case.
    """
    result = []
    sections = page.locator("section")
    if sections.count() > 0:
        for i in range(sections.count()):
            sec = sections.nth(i)
            h = sec.locator("h1, h2, h3").first
            if h.count() > 0:
                result.append((h.inner_text().strip(), sec))

    if not result:
        headings = page.locator("h1, h2, h3")
        for i in range(headings.count()):
            h = headings.nth(i)
            parent = h.locator("xpath=..")
            result.append((h.inner_text().strip(), parent))
    return result


def test_TC_13_2_containers_have_non_empty_heading_and_text(page: Page, step_logger):
    """TC-13-02: Every container on the page has non-empty heading and non-empty text."""
    _ensure_about_us(page, step_logger)

    step_logger.start_step("Find all containers with headings")
    containers = _get_containers_with_headings(page)
    print(f"\n[test_TC_13_2] containers count = {len(containers)}")
    assert len(containers) > 0, "Expected at least one container with a heading"

    for idx, (heading_text, container) in enumerate(containers):
        body = container.inner_text().strip()
        print(f"[test_TC_13_2] container {idx} heading = {heading_text!r}, body len = {len(body)}")
        assert heading_text, f"Container {idx} should have non-empty heading, got: {heading_text!r}"
        assert body, f"Container {idx} should have non-empty text, got empty body"
    step_logger.checkpoint(f"All {len(containers)} containers have non-empty heading and text")


def test_TC_13_3_leadership_container_scoutmaster_and_scoutmasters_on_same_line(
    page: Page, step_logger
):
    """TC-13-03: In Leadership container, 'Scoutmaster:' and 'Scoutmasters:' have text on same line."""
    _ensure_about_us(page, step_logger)

    step_logger.start_step("Find container whose heading contains 'Leadership'")
    containers = _get_containers_with_headings(page)
    leadership_container = None
    for heading_text, container in containers:
        if "leadership" in heading_text.lower():
            leadership_container = container
            break
    assert leadership_container is not None, (
        "Expected a container with heading containing 'Leadership'"
    )
    full_text = leadership_container.inner_text()
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]

    step_logger.start_step("Check 'Scoutmaster:' has text on same line")
    scoutmaster_ok = False
    for line in lines:
        if "Scoutmaster:" in line:
            after = line.split("Scoutmaster:", 1)[-1].strip()
            if after:
                scoutmaster_ok = True
                break
    assert scoutmaster_ok, (
        "In Leadership container, a line containing 'Scoutmaster:' must have "
        "non-empty text immediately after it on the same line"
    )
    step_logger.checkpoint("'Scoutmaster:' has text on same line")

    step_logger.start_step("Check 'Scoutmasters:' or 'Assistant Scoutmasters:' has text on same line")
    scoutmasters_ok = False
    for line in lines:
        if "Scoutmasters:" in line or "Assistant Scoutmasters:" in line:
            if "Assistant Scoutmasters:" in line:
                after = line.split("Assistant Scoutmasters:", 1)[-1].strip()
            else:
                after = line.split("Scoutmasters:", 1)[-1].strip()
            if after:
                scoutmasters_ok = True
                break
    assert scoutmasters_ok, (
        "In Leadership container, a line containing 'Scoutmasters:' or 'Assistant Scoutmasters:' "
        "must have non-empty text immediately after it on the same line"
    )
    step_logger.checkpoint("'Scoutmasters:'/Assistant Scoutmasters:' has text on same line")


def test_TC_13_4_about_troop_container_troop_size_and_season_phrase(page: Page, step_logger):
    """TC-13-04: In About the Troop container, Troop size has text on same line; exact season phrase."""
    _ensure_about_us(page, step_logger)

    step_logger.start_step("Find container whose heading contains 'About' and 'Troop'")
    containers = _get_containers_with_headings(page)
    about_troop = None
    for heading_text, container in containers:
        if "about" in heading_text.lower() and "troop" in heading_text.lower():
            about_troop = container
            break
    assert about_troop is not None, (
        "Expected a container with heading containing 'About' and 'Troop'"
    )
    full_text = about_troop.inner_text()
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]

    step_logger.start_step("Check 'Troop size:' has text on same line")
    troop_size_ok = False
    for line in lines:
        if "Troop size:" in line:
            after = line.split("Troop size:", 1)[-1].strip()
            if after:
                troop_size_ok = True
                break
    assert troop_size_ok, (
        "In About the Troop container, 'Troop size:' must have non-empty text on the same line"
    )
    step_logger.checkpoint("'Troop size:' has text on same line")

    step_logger.start_step("Check exact phrase 'Scouting season: September to June'")
    assert SCOUTING_SEASON_EXACT_PHRASE in full_text, (
        f"Container must contain exact phrase: {SCOUTING_SEASON_EXACT_PHRASE!r}"
    )
    step_logger.checkpoint("Exact phrase 'Scouting season: September to June' present")


def test_TC_13_5_last_updated_year_current_or_recent(page: Page, step_logger):
    """TC-13-05: Last updated block contains a year that is current, previous, or two years ago."""
    _ensure_about_us(page, step_logger)

    step_logger.start_step("Locate Last updated element and extract year")
    last_updated = page.get_by_text("Last updated", exact=False).first
    assert last_updated.count() > 0, '"Last updated" element should be present'
    text = last_updated.inner_text()
    years = re.findall(r"\b(20\d{2})\b", text)
    print(f"\n[test_TC_13_5] last_updated text = {text!r}, years = {years}")
    assert years, f'"Last updated" text should contain a 4-digit year, got: {text!r}'
    year = int(years[0])
    now = datetime.now().year
    allowed = {now, now - 1, now - 2}
    assert year in allowed, (
        f"Year in last updated should be one of {allowed}, got: {year}"
    )
    step_logger.checkpoint(f"Last updated year {year} is current or recent ({allowed})")


def test_TC_13_6_footer_structure_and_contacts_on_about_us(page: Page, step_logger):
    """TC-13-06: Footer structure and contacts on About Us (same as homepage)."""
    _ensure_about_us(page, step_logger)
    assert_footer_structure_and_contacts_ok(
        page, step_logger=step_logger, scope="about-us"
    )


def test_TC_13_7_top_menu_visible_and_has_links(page: Page, step_logger):
    """TC-13-07: Top menu (nav/header) is visible and contains links."""
    _ensure_about_us(page, step_logger)

    step_logger.start_step("Locate top nav or header with links")
    nav = page.locator("nav").first
    if nav.count() == 0:
        nav = page.locator("header").first
    assert nav.count() > 0, "Expected at least one nav or header"
    assert nav.is_visible(), "Nav/header should be visible"
    links = nav.locator("a[href]")
    n = links.count()
    print(f"\n[test_TC_13_7] nav/header links count = {n}")
    assert n > 0, "Top menu should contain at least one link"
    step_logger.checkpoint("Top menu is visible and has links")


def test_TC_13_8_all_links_and_images_not_broken(page: Page, step_logger):
    """TC-13-08: All links and image src URLs on About Us are checked via API (2xx, not empty)."""
    _ensure_about_us(page, step_logger)

    step_logger.start_step("Collect all in-scope links (a[href]) and images (img[src])")
    seen = set()
    to_check = []  # (full_url, index_or_neg, label)

    for loc, kind in [
        (page.locator("a[href]"), "link"),
        (page.locator("img[src]"), "image"),
    ]:
        n = loc.count()
        for i in range(n):
            el = loc.nth(i)
            href_or_src = (el.get_attribute("href") or el.get_attribute("src") or "").strip()
            if not href_or_src or href_or_src.startswith("#"):
                continue
            if href_or_src.lower().startswith(("javascript:", "mailto:", "tel:", "data:")):
                continue
            if href_or_src.startswith("/"):
                full_url = BASE_URL_NORMALIZED + href_or_src
            elif href_or_src.startswith(("http://", "https://")):
                full_url = href_or_src
            else:
                full_url = urljoin(ABOUT_US_URL, href_or_src)
            if not full_url.startswith(BASE_URL_NORMALIZED):
                continue
            if full_url in seen:
                continue
            seen.add(full_url)
            label = (el.inner_text() or el.get_attribute("alt") or "").strip() or kind
            to_check.append((full_url, i if kind == "link" else -i, f"{kind}: {label}"))
            print(f"[test_TC_13_8] in-scope {kind}: url={full_url!r}, label={label!r}")

    step_logger.checkpoint(f"Found {len(to_check)} in-scope links and images (same-origin, unique)")
    assert len(to_check) > 0, "Expected at least one in-scope link or image on About Us"

    step_logger.start_step("Check each URL via API")
    failed = []
    for full_url, dom_index, label in to_check:
        ok, msg = check_url_not_broken_and_not_empty(full_url)
        print(f"[test_TC_13_8] {label} url={full_url!r} -> {msg!r}")
        step_logger.log_text(f"GET {full_url} ({label}) -> {msg}")
        if not ok:
            failed.append({"url": full_url, "label": label, "reason": msg})
        else:
            step_logger.checkpoint(f"OK: {full_url}")
    assert not failed, (
        "Some links or images failed (not 2xx or empty). " f"Failed: {failed!r}"
    )
    step_logger.checkpoint(f"All {len(to_check)} links and images are not broken and not empty")


def _is_allowlisted_console_error(message: str, allowlist: list[str]) -> bool:
    lower = message.lower()
    return any(term in lower for term in allowlist)


def test_TC_13_9_no_critical_console_errors_on_load(page: Page, step_logger):
    """TC-13-09: No critical console errors on About Us load (allowlist as on main)."""
    console_errors = []

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", on_console)
    step_logger.start_step("Open About Us and wait for network idle")
    page.goto(ABOUT_US_URL, wait_until="networkidle")
    step_logger.start_step("Check no critical console errors")
    allowlist = get_console_error_allowlist()
    blocking = [
        e for e in console_errors
        if not _is_allowlisted_console_error(e, allowlist)
    ]
    assert not blocking, (
        f"Unexpected console errors ({len(blocking)}): {blocking[:5]}"
    )
    step_logger.checkpoint("No critical console errors on About Us load")


def test_TC_13_10_ux_desktop_mobile_viewports_and_readable(page: Page, step_logger):
    """TC-13-10: UX — desktop/mobile viewports, key content visible, no horizontal scroll, readable text."""
    _ensure_about_us(page, step_logger, viewport=DESKTOP_VIEWPORT)

    step_logger.start_step("Check key content visible on desktop")
    h1 = page.locator("h1").first
    leadership = page.get_by_text("Troop Leadership", exact=False).first
    assert h1.is_visible(), "H1 should be visible on desktop"
    assert leadership.is_visible(), "'Troop Leadership' section should be visible on desktop"
    scroll_width = page.evaluate("document.body.scrollWidth")
    vw = page.viewport_size["width"]
    assert scroll_width <= vw + 20, (
        f"Body scroll width ({scroll_width}) should not exceed viewport ({vw})"
    )
    step_logger.checkpoint("Desktop: key sections visible, no horizontal scroll")

    _ensure_about_us(page, step_logger, viewport=MOBILE_VIEWPORT)
    step_logger.start_step("Check key content accessible on mobile")
    h1.scroll_into_view_if_needed()
    leadership.scroll_into_view_if_needed()
    assert h1.is_visible(), "H1 visible on mobile"
    assert leadership.is_visible(), "'Troop Leadership' visible on mobile"
    font_size = page.evaluate("getComputedStyle(document.body).fontSize")
    font_px = int(float(str(font_size).replace("px", "")))
    assert font_px >= 12, f"Body font size should be at least 12px, got: {font_px}"
    step_logger.checkpoint("Mobile: key sections accessible, text readable")


def test_TC_13_11_navigation_from_homepage_to_about_us_and_back(page: Page, step_logger):
    """TC-13-11: From homepage (or menu) navigate to About Us and back."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Find and click link to About Us")
    about_link = page.locator("a[href*='about-us']").first
    assert about_link.count() > 0, "Expected a link to About Us on the page"
    assert about_link.is_visible(), "About Us link should be visible"
    href = about_link.get_attribute("href") or ""
    assert href, "About Us link should have href"
    about_link.click()
    step_logger.take_screenshot("about_us_after_navigation")
    assert "about-us" in page.url, (
        f"After clicking About Us link, URL should contain 'about-us', got: {page.url}"
    )
    step_logger.checkpoint("Navigated to About Us and screenshot captured")

    step_logger.start_step("Return to homepage (back or Home link)")
    page.go_back(wait_until="domcontentloaded")
    step_logger.take_screenshot("homepage_after_back")
    assert "about-us" not in page.url or page.url.rstrip("/").endswith("t23b.org"), (
        "After going back, should be on homepage"
    )
    step_logger.checkpoint("Returned to homepage")


def test_TC_13_12_scaling_viewports_key_content_visible(page: Page, step_logger):
    """TC-13-12: Scaling — multiple viewports; key content visible, no horizontal overflow."""
    viewports = [
        {"width": 1920, "height": 1080},
        {"width": 1024, "height": 768},
        {"width": 375, "height": 667},
    ]
    for vp in viewports:
        step_logger.start_step(f"Viewport {vp['width']}x{vp['height']}")
        page.set_viewport_size(vp)
        page.goto(ABOUT_US_URL, wait_until="domcontentloaded")
        h1 = page.locator("h1").first
        assert h1.is_visible(), f"H1 should be visible at {vp}"
        scroll_width = page.evaluate("document.body.scrollWidth")
        vw = page.viewport_size["width"]
        assert scroll_width <= vw + 30, (
            f"At {vp}: scroll width {scroll_width} should not exceed viewport {vw}"
        )
    step_logger.checkpoint("Key content visible and no horizontal overflow at all viewports")
