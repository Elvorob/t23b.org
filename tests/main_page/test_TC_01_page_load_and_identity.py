"""
TC-US-01: Page Load and Identity — automated tests.

User Story US-01: Visitor wants homepage to load with correct title and Troop 23 branding.
Test cases: TC-US-01-01 .. TC-US-01-04.
"""

import time

import pytest
import requests
from playwright.sync_api import Page

from tests.conftest import BASE_URL, get_console_error_allowlist

# HTTP request: timeout in seconds; retries on timeout (5B).
HOME_PAGE_HTTP_TIMEOUT = 15
HOME_PAGE_HTTP_RETRIES = 2
HOME_PAGE_HTTP_RETRY_DELAY = 2


def test_TC_01_1_homepage_returns_200(step_logger):
    """TC-US-01-01: Homepage returns successful HTTP status (no browser)."""
    step_logger.start_step("Send GET request to homepage (with retry on timeout)")
    response = None
    for attempt in range(HOME_PAGE_HTTP_RETRIES + 1):
        try:
            response = requests.get(BASE_URL, timeout=HOME_PAGE_HTTP_TIMEOUT)
            break
        except requests.Timeout as e:
            if attempt < HOME_PAGE_HTTP_RETRIES:
                step_logger.log_text(f"[Retry] attempt {attempt + 1} timed out; waiting {HOME_PAGE_HTTP_RETRY_DELAY}s")
                time.sleep(HOME_PAGE_HTTP_RETRY_DELAY)
            else:
                raise e
    step_logger.log_text(f"[Request] GET {BASE_URL}")
    step_logger.log_text(f"[Response] {response.status_code} {BASE_URL}")
    step_logger.start_step("Check response status is 200")
    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )
    step_logger.checkpoint("Response status is 200")


def test_TC_01_2_page_title_contains_troop23_and_bsa(page: Page, step_logger):
    """TC-US-01-02: Page title contains Troop 23 and BSA."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check page title contains Troop 23 and BSA")
    title = page.title()
    assert "Troop 23" in title, f"Title should contain 'Troop 23', got: {title}"
    step_logger.checkpoint("Page title contains 'Troop 23'")
    assert "BSA" in title or "Boy Scouts of America" in title, (
        f"Title should contain 'BSA' or 'Boy Scouts of America', got: {title}"
    )
    step_logger.checkpoint("Page title contains 'BSA' or 'Boy Scouts of America'")


def test_TC_01_3_h1_visible_and_contains_troop23(page: Page, step_logger):
    """TC-US-01-03: Main heading (H1) is visible and contains Troop 23."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check H1 is visible and contains Troop 23")
    h1 = page.locator("h1").first
    assert h1.is_visible(), "H1 should be visible"
    step_logger.checkpoint("H1 is visible")
    text = h1.inner_text()
    assert "Troop 23" in text, f"H1 should contain 'Troop 23', got: {text}"
    step_logger.checkpoint("H1 text contains 'Troop 23'")


def test_TC_01_4_no_critical_console_errors_on_load(page: Page, step_logger):
    """TC-US-01-04: No critical console errors on load."""
    console_errors = []

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", on_console)
    step_logger.start_step("Open homepage and wait for network idle")
    page.goto(BASE_URL, wait_until="networkidle")
    step_logger.start_step("Check no critical console errors")
    allowlist = get_console_error_allowlist()
    blocking = [
        e for e in console_errors
        if not _is_allowlisted_console_error(e, allowlist)
    ]
    assert not blocking, (
        f"Unexpected console errors ({len(blocking)}): {blocking[:5]}"
    )
    step_logger.checkpoint("No critical console errors on load")


def _is_allowlisted_console_error(message: str, allowlist: list[str]) -> bool:
    """Treat some console errors as non-blocking (e.g. analytics, extensions)."""
    lower = message.lower()
    return any(term in lower for term in allowlist)
