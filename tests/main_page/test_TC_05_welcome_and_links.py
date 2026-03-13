"""
TC-05: Main Content and Links — automated tests.

One test for the whole main text block (Welcome, What is Scouting, Why Choose, New to Scouting):
  - main content area is visible and has text;
  - all links inside it are visually recognizable.
Second test: all links on homepage — check via API that each destination is not broken and not empty
(status 2xx, minimum body length, HTML structure, non-empty title). No browser navigation or screenshots.
"""

from urllib.parse import urljoin

from playwright.sync_api import Page

from tests.conftest import BASE_URL
from tests.link_checks import check_url_not_broken_and_not_empty
from tests.main_page.link_visibility import report_links_visually_recognizable

BASE_URL_NORMALIZED = BASE_URL.rstrip("/")

MAIN_CONTENT_SECTION_NAME = "Main content (Welcome / What is Scouting / Why Choose / New to Scouting)"


def _main_content(page: Page):
    """Main content block: <main> if present and visible, else a container that has Welcome and New to Scouting."""
    main_loc = page.locator("main")
    if main_loc.count() > 0 and main_loc.first.is_visible():
        return main_loc.first
    # Fallback: container that spans the whole text block (has both Welcome and New to Scouting)
    return (
        page.locator("div")
        .filter(has=page.get_by_text("Welcome to Troop 23", exact=False))
        .filter(has=page.get_by_text("New to Scouting", exact=False))
        .first
    )


def test_TC_05_1_main_content_visible_and_links_recognizable(page: Page, step_logger):
    """TC-05-01: Main content block is visible, has text, and all links in it are visually recognizable."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Locate main content area")
    section = _main_content(page)
    visible = section.is_visible()
    print(f"\n[test_main_content_visible_and_links_recognizable] visible = {visible}")
    assert visible, f"'{MAIN_CONTENT_SECTION_NAME}' should be visible"
    step_logger.checkpoint("Main content area is visible")

    step_logger.start_step("Check main content has non-empty text")
    text = section.inner_text().strip()
    print(f"[test_main_content_visible_and_links_recognizable] section text length = {len(text)}")
    assert len(text) > 0, "Main content should contain some text"
    step_logger.checkpoint("Main content has non-empty text")

    report_links_visually_recognizable(
        page, section, MAIN_CONTENT_SECTION_NAME, step_logger
    )


def test_TC_05_2_all_links_on_homepage_not_broken_and_not_empty(page: Page, step_logger):
    """
    TC-05-02: All links on homepage are checked via API: each destination returns 2xx,
    has minimum body length, HTML structure (</body> or <html), and non-empty <title>.
    No browser navigation or screenshots.
    """
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Collect all in-scope links with non-empty href")
    links = page.locator("a[href]")
    n = links.count()
    print(f"\n[test_all_links_on_homepage] total links with href = {n}")

    seen_urls = set()
    to_check = []  # list of (full_url, index_in_dom, link_text)
    for i in range(n):
        link = links.nth(i)
        href = (link.get_attribute("href") or "").strip()
        if not href or href.startswith("#") or href.lower().startswith(("javascript:", "mailto:", "tel:")):
            continue
        if href.startswith("/"):
            full_url = BASE_URL_NORMALIZED + href
        elif href.startswith(("http://", "https://")):
            full_url = href
        else:
            full_url = urljoin(BASE_URL, href)
        if not full_url.startswith(BASE_URL_NORMALIZED):
            continue
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)
        link_text = (link.inner_text() or "").strip()
        to_check.append((full_url, i, link_text))
        print(
            "[test_all_links_on_homepage] in-scope link: "
            f"index={i}, url={full_url!r}, text={link_text!r}"
        )

    step_logger.checkpoint(f"Found {len(to_check)} in-scope links (same-origin, unique)")
    assert len(to_check) > 0, "Expected at least one in-scope link on the homepage"

    step_logger.start_step("Check each link via API (not broken, not empty)")
    failed = []
    for idx, (full_url, dom_index, link_text) in enumerate(to_check, start=1):
        ok, msg = check_url_not_broken_and_not_empty(full_url)
        print(
            "[test_all_links_on_homepage] "
            f"{idx}/{len(to_check)} index={dom_index} url={full_url!r} text={link_text!r} -> {msg!r}"
        )
        step_logger.log_text(
            f"GET {full_url} (index={dom_index}, text={link_text!r}) -> {msg}"
        )
        if not ok:
            failed.append(
                {
                    "url": full_url,
                    "index": dom_index,
                    "text": link_text,
                    "reason": msg,
                }
            )
        else:
            step_logger.checkpoint(f"Link OK: {full_url}")

    assert not failed, (
        "Links failed (not 2xx or empty/invalid). "
        "Each item includes url, index in DOM, link text, and reason: "
        f"{failed!r}"
    )
    step_logger.checkpoint(f"All {len(to_check)} links are not broken and not empty")
