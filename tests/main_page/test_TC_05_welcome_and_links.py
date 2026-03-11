"""
TC-05: Main Content and Links — automated tests.

One test for the whole main text block (Welcome, What is Scouting, Why Choose, New to Scouting):
  - main content area is visible and has text;
  - all links inside it are visually recognizable.
Second test: all links on homepage — check via API that each destination is not broken and not empty
(status 2xx, minimum body length, HTML structure, non-empty title). No browser navigation or screenshots.
"""

import re
from urllib.parse import urljoin, urlparse

import requests
from playwright.sync_api import Page

from tests.conftest import BASE_URL
from tests.main_page.link_visibility import report_links_visually_recognizable

# API check: minimum response body length (bytes) to consider page "not empty".
LINK_CHECK_MIN_BODY_LENGTH = 500
LINK_CHECK_TIMEOUT = 15

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


def _is_media_resource_url(url: str, content_type: str | None) -> bool:
    """True if URL or Content-Type indicates image/media (no HTML expected)."""
    path = urlparse(url).path.lower()
    if path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".pdf")):
        return True
    if content_type and content_type.split(";")[0].strip().lower().startswith(("image/", "application/pdf")):
        return True
    return False


def _check_link_not_broken_and_not_empty(url: str) -> tuple[bool, str]:
    """
    Check via GET that the URL is not broken and not empty.
    Returns (success, message).
    - Not broken: final status code 2xx after redirects.
    - For HTML pages: body length, </body> or <html, non-empty <title>.
    - For media (image/pdf): 2xx and non-empty body only.
    """
    # Internal links to t23b.org are expected to respond directly (no redirects).
    # Treat any 3xx as an error here; external links are excluded earlier.
    try:
        response = requests.get(
            url,
            allow_redirects=False,
            timeout=LINK_CHECK_TIMEOUT,
        )
    except requests.RequestException as e:
        return False, f"request failed: {e!s}"

    status = response.status_code
    if 300 <= status < 400:
        # For internal links, redirects are unexpected. Build a redirect chain for reporting.
        try:
            follow = requests.get(
                url,
                allow_redirects=True,
                timeout=LINK_CHECK_TIMEOUT,
            )
            chain_parts = []
            all_resps = list(follow.history) + [follow]
            prev_url = url
            for r in all_resps:
                chain_parts.append(f"{prev_url} ({r.status_code})")
                prev_url = r.headers.get("Location", prev_url)
            chain = " -> ".join(chain_parts)
            return False, f"unexpected redirect status {status}; chain: {chain}"
        except requests.RequestException as e:
            return False, f"unexpected redirect status {status}; redirect follow failed: {e!s}"

    if status not in range(200, 300):
        return False, f"status {status}"

    content = response.content
    content_type = response.headers.get("Content-Type") or ""

    if _is_media_resource_url(url, content_type):
        if len(content) < 100:
            return False, f"media body too short ({len(content)} bytes)"
        return True, "OK"

    if len(content) < LINK_CHECK_MIN_BODY_LENGTH:
        return False, f"body too short ({len(content)} bytes)"

    content_lower = content.lower()
    if b"</body>" not in content_lower and b"<html" not in content_lower:
        return False, "body lacks </body> or <html"

    title_match = re.search(
        rb"<title[^>]*>([^<]*)</title>",
        content,
        re.IGNORECASE | re.DOTALL,
    )
    if not title_match:
        return False, "no <title> found"
    title_text = title_match.group(1).decode("utf-8", errors="replace").strip()
    if not title_text:
        return False, "empty <title>"

    return True, "OK"


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
        ok, msg = _check_link_not_broken_and_not_empty(full_url)
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
