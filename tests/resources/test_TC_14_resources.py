"""
TC-14: Resources page - automated tests.

Covers: page load 200, containers (heading + text), resources content blocks,
last updated year, footer, top menu, links and images (API check),
console, UX, navigation, and scaling.
"""

import re
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from playwright.sync_api import Page

from tests.conftest import (
    BASE_URL,
    RESOURCES_URL,
    get_console_error_allowlist,
)
from tests.footer_checks import assert_footer_structure_and_contacts_ok
from tests.link_checks import check_url_not_broken_and_not_empty

BASE_URL_NORMALIZED = BASE_URL.rstrip("/")
RESOURCES_PAGE_HTTP_TIMEOUT = 15
RESOURCES_PAGE_HTTP_RETRIES = 2
RESOURCES_PAGE_HTTP_RETRY_DELAY = 2
DESKTOP_VIEWPORT = {"width": 1280, "height": 720}
MOBILE_VIEWPORT = {"width": 375, "height": 667}


def _ensure_resources(page: Page, step_logger, viewport: dict | None = None):
    if viewport:
        step_logger.start_step(f"Set viewport to {viewport['width']}x{viewport['height']}")
        page.set_viewport_size(viewport)
    step_logger.start_step("Open Resources page")
    page.goto(RESOURCES_URL, wait_until="domcontentloaded")


def _get_containers_with_headings(page: Page):
    """
    Return list of (heading_text, container_locator) for content blocks with heading.

    Some pages (e.g. Resources) have <section> elements that do not wrap h1/h2/h3.
    In that case the section-based pass yields nothing; fall back to each heading's parent.
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


def _is_allowlisted_console_error(message: str, allowlist: list[str]) -> bool:
    lower = message.lower()
    return any(term in lower for term in allowlist)


def test_TC_14_1_resources_returns_200(step_logger):
    """TC-14-01: Resources page returns HTTP 200."""
    step_logger.start_step("Send GET request to Resources (with retry on timeout)")
    response = None
    for attempt in range(RESOURCES_PAGE_HTTP_RETRIES + 1):
        try:
            response = requests.get(RESOURCES_URL, timeout=RESOURCES_PAGE_HTTP_TIMEOUT)
            break
        except requests.Timeout as e:
            if attempt < RESOURCES_PAGE_HTTP_RETRIES:
                step_logger.log_text(
                    f"[Retry] attempt {attempt + 1} timed out; "
                    f"waiting {RESOURCES_PAGE_HTTP_RETRY_DELAY}s"
                )
                time.sleep(RESOURCES_PAGE_HTTP_RETRY_DELAY)
            else:
                raise e

    step_logger.log_text(f"[Request] GET {RESOURCES_URL}")
    step_logger.log_text(f"[Response] {response.status_code} {RESOURCES_URL}")
    step_logger.start_step("Check response status is 200")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    step_logger.checkpoint("Resources response status is 200")


def test_TC_14_2_containers_have_non_empty_heading_and_text(page: Page, step_logger):
    """TC-14-02: Containers have non-empty headings and body text."""
    _ensure_resources(page, step_logger)

    step_logger.start_step("Find all containers with headings")
    containers = _get_containers_with_headings(page)
    print(f"\n[test_TC_14_2] containers count = {len(containers)}")
    assert len(containers) > 0, "Expected at least one container with a heading"

    for idx, (heading_text, container) in enumerate(containers):
        body = container.inner_text().strip()
        print(f"[test_TC_14_2] container {idx} heading={heading_text!r}, body len={len(body)}")
        assert heading_text, f"Container {idx} should have non-empty heading"
        assert body, f"Container {idx} should have non-empty body text"

    step_logger.checkpoint(f"All {len(containers)} containers have non-empty heading and text")


def test_TC_14_3_resources_content_has_expected_keywords(page: Page, step_logger):
    """TC-14-03: Resources page contains key resource topics and links."""
    _ensure_resources(page, step_logger)

    step_logger.start_step("Check H1 indicates Resources")
    h1 = page.locator("h1").first
    assert h1.is_visible(), "H1 should be visible"
    h1_text = h1.inner_text().strip()
    print(f"\n[test_TC_14_3] h1_text = {h1_text!r}")
    assert "resource" in h1_text.lower(), f"H1 should mention Resources, got: {h1_text!r}"

    step_logger.start_step("Check key keywords in page text")
    page_text = page.locator("main, body").first.inner_text()
    required_keywords = ["library", "camping tips", "photo archive", "eagle projects"]
    missing = [kw for kw in required_keywords if kw not in page_text.lower()]
    print(f"[test_TC_14_3] missing keywords = {missing}")
    assert not missing, f"Expected keyword(s) missing in Resources content: {missing}"

    step_logger.checkpoint("Resources content has key topics and links")


def test_TC_14_4_last_updated_year_current_or_recent(page: Page, step_logger):
    """TC-14-04: Last updated contains a recent year (current/prev/prev-2)."""
    _ensure_resources(page, step_logger)

    step_logger.start_step("Locate Last updated element and extract year")
    last_updated = page.get_by_text("Last updated", exact=False).first
    assert last_updated.count() > 0, '"Last updated" element should be present'

    text = last_updated.inner_text()
    years = re.findall(r"\b(20\d{2})\b", text)
    print(f"\n[test_TC_14_4] last_updated text = {text!r}, years = {years}")
    assert years, f'"Last updated" should contain a 4-digit year, got: {text!r}'

    year = int(years[0])
    now = datetime.now().year
    allowed = {now, now - 1, now - 2}
    assert year in allowed, f"Year should be one of {allowed}, got: {year}"
    step_logger.checkpoint(f"Last updated year {year} is current or recent ({allowed})")


def test_TC_14_5_footer_structure_and_contacts_on_resources(page: Page, step_logger):
    """TC-14-05: Footer structure and contacts on Resources."""
    _ensure_resources(page, step_logger)
    assert_footer_structure_and_contacts_ok(page, step_logger=step_logger, scope="resources")


def test_TC_14_6_top_menu_visible_and_has_links(page: Page, step_logger):
    """TC-14-06: Top menu is visible and contains links."""
    _ensure_resources(page, step_logger)

    step_logger.start_step("Locate top nav or header with links")
    nav = page.locator("nav").first
    if nav.count() == 0:
        nav = page.locator("header").first
    assert nav.count() > 0, "Expected at least one nav or header"
    assert nav.is_visible(), "Nav/header should be visible"

    links = nav.locator("a[href]")
    n = links.count()
    print(f"\n[test_TC_14_6] nav/header links count = {n}")
    assert n > 0, "Top menu should contain at least one link"

    resources_link = nav.locator("a[href*='resources']").first
    assert resources_link.count() > 0, "Top menu should contain a Resources link"
    step_logger.checkpoint("Top menu is visible and contains a Resources link")


def test_TC_14_7_all_links_and_images_not_broken(page: Page, step_logger):
    """TC-14-07: Same-origin links and images on Resources are healthy via API checks."""
    _ensure_resources(page, step_logger)

    step_logger.start_step("Collect all in-scope links (a[href]) and images (img[src])")
    seen = set()
    to_check = []

    for loc, kind in [(page.locator("a[href]"), "link"), (page.locator("img[src]"), "image")]:
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
                full_url = urljoin(RESOURCES_URL, href_or_src)

            if not full_url.startswith(BASE_URL_NORMALIZED):
                continue
            if full_url in seen:
                continue

            seen.add(full_url)
            label = (el.inner_text() or el.get_attribute("alt") or "").strip() or kind
            to_check.append((full_url, f"{kind}: {label}"))
            print(f"[test_TC_14_7] in-scope {kind}: url={full_url!r}, label={label!r}")

    step_logger.checkpoint(f"Found {len(to_check)} in-scope links and images (same-origin, unique)")
    assert len(to_check) > 0, "Expected at least one in-scope link or image on Resources"

    step_logger.start_step("Check each URL via API")
    failed = []
    for full_url, label in to_check:
        ok, msg = check_url_not_broken_and_not_empty(full_url)
        print(f"[test_TC_14_7] {label} url={full_url!r} -> {msg!r}")
        step_logger.log_text(f"GET {full_url} ({label}) -> {msg}")
        if not ok:
            failed.append({"url": full_url, "label": label, "reason": msg})
        else:
            step_logger.checkpoint(f"OK: {full_url}")

    assert not failed, f"Some links/images failed (not 2xx or empty): {failed!r}"
    step_logger.checkpoint(f"All {len(to_check)} links and images are not broken and not empty")


def test_TC_14_8_no_critical_console_errors_on_load(page: Page, step_logger):
    """TC-14-08: No critical console errors on Resources load (allowlist as on main)."""
    console_errors = []

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", on_console)
    step_logger.start_step("Open Resources and wait for network idle")
    page.goto(RESOURCES_URL, wait_until="networkidle")

    step_logger.start_step("Check no critical console errors")
    allowlist = get_console_error_allowlist()
    blocking = [e for e in console_errors if not _is_allowlisted_console_error(e, allowlist)]
    assert not blocking, f"Unexpected console errors ({len(blocking)}): {blocking[:5]}"
    step_logger.checkpoint("No critical console errors on Resources load")


def test_TC_14_9_ux_desktop_mobile_viewports_and_readable(page: Page, step_logger):
    """TC-14-09: UX on desktop/mobile (visibility, no horizontal overflow, readable text)."""
    _ensure_resources(page, step_logger, viewport=DESKTOP_VIEWPORT)

    step_logger.start_step("Check key content visible on desktop")
    h1 = page.locator("h1").first
    library_link = page.get_by_role("link", name=re.compile("library", re.IGNORECASE)).first
    assert h1.is_visible(), "H1 should be visible on desktop"
    assert library_link.is_visible(), "Library link should be visible on desktop"

    scroll_width = page.evaluate("document.body.scrollWidth")
    vw = page.viewport_size["width"]
    assert scroll_width <= vw + 20, f"Body scroll width ({scroll_width}) should not exceed viewport ({vw})"
    step_logger.checkpoint("Desktop: key sections visible, no horizontal scroll")

    _ensure_resources(page, step_logger, viewport=MOBILE_VIEWPORT)
    step_logger.start_step("Check key content accessible on mobile")
    h1.scroll_into_view_if_needed()
    assert h1.is_visible(), "H1 should be visible on mobile"

    font_size = page.evaluate("getComputedStyle(document.body).fontSize")
    font_px = int(float(str(font_size).replace("px", "")))
    assert font_px >= 12, f"Body font size should be at least 12px, got: {font_px}"
    step_logger.checkpoint("Mobile: key content accessible and text readable")


def test_TC_14_10_navigation_from_homepage_to_resources_and_back(page: Page, step_logger):
    """TC-14-10: Navigate from homepage to Resources and back."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Find and click link to Resources")
    resources_link = page.locator("a[href*='resources']").first
    assert resources_link.count() > 0, "Expected a link to Resources on homepage"
    assert resources_link.is_visible(), "Resources link should be visible"
    href = resources_link.get_attribute("href") or ""
    assert href, "Resources link should have href"

    resources_link.click()
    step_logger.take_screenshot("resources_after_navigation")
    assert "resources" in page.url, f"URL should contain 'resources', got: {page.url}"
    step_logger.checkpoint("Navigated to Resources and screenshot captured")

    step_logger.start_step("Return to homepage")
    page.go_back(wait_until="domcontentloaded")
    step_logger.take_screenshot("homepage_after_back")
    assert "resources" not in page.url or page.url.rstrip("/").endswith("t23b.org"), "After back, should be on homepage"
    step_logger.checkpoint("Returned to homepage")


def test_TC_14_11_scaling_viewports_key_content_visible(page: Page, step_logger):
    """TC-14-11: Scaling on multiple viewports with no horizontal overflow."""
    viewports = [
        {"width": 1920, "height": 1080},
        {"width": 1024, "height": 768},
        {"width": 375, "height": 667},
    ]

    for vp in viewports:
        step_logger.start_step(f"Viewport {vp['width']}x{vp['height']}")
        page.set_viewport_size(vp)
        page.goto(RESOURCES_URL, wait_until="domcontentloaded")

        h1 = page.locator("h1").first
        assert h1.is_visible(), f"H1 should be visible at {vp}"

        scroll_width = page.evaluate("document.body.scrollWidth")
        vw = page.viewport_size["width"]
        assert scroll_width <= vw + 30, f"At {vp}: scroll width {scroll_width} should not exceed viewport {vw}"

    step_logger.checkpoint("Key content visible and no horizontal overflow at all viewports")
