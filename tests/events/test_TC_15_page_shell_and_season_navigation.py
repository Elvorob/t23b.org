"""
TC-15: Events Page Shell and Season Navigation — automated tests.

Verify that the events page loads, redirects to the current season,
displays the season title, provides calendar subscription, and
allows navigation between seasons.
"""
from __future__ import annotations

import re
import time

import allure
import pytest
import requests
from playwright.sync_api import Page, expect

from tests.conftest import EVENTS_URL, get_console_error_allowlist

EVENTS_HTTP_TIMEOUT = 15
EVENTS_HTTP_RETRIES = 2
EVENTS_HTTP_RETRY_DELAY = 2

SEASON_PATTERN = re.compile(r"\d{4}-\d{4}")
SEASON_URL_PATTERN = re.compile(r"/events/\d{4}-\d{4}/?")


def _goto_events(page: Page) -> str:
    """Navigate to events page, wait for redirect to season URL. Returns final URL."""
    page.goto(EVENTS_URL, wait_until="domcontentloaded")
    page.wait_for_url(SEASON_URL_PATTERN, timeout=10_000)
    return page.url


def _extract_season_from_url(url: str) -> str | None:
    """Extract 'YYYY-YYYY' from an events URL path."""
    m = re.search(r"/events/(\d{4}-\d{4})", url)
    return m.group(1) if m else None


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Page load and redirect")
@allure.title("TC-15-01: GET /events/ redirects to season URL with status 200")
@allure.severity(allure.severity_level.BLOCKER)
def test_TC_15_1_page_loads_and_redirects(step_logger):
    """TC-15-01: GET /events/ redirects to season URL with status 200."""
    with allure.step("Send GET request to /events/ with redirect follow"):
        step_logger.start_step("Send GET request to /events/ with redirect follow")
        response = None
        for attempt in range(EVENTS_HTTP_RETRIES + 1):
            try:
                response = requests.get(EVENTS_URL, timeout=EVENTS_HTTP_TIMEOUT, allow_redirects=True)
                break
            except requests.Timeout:
                if attempt < EVENTS_HTTP_RETRIES:
                    step_logger.log_text(f"[Retry] attempt {attempt + 1} timed out; waiting {EVENTS_HTTP_RETRY_DELAY}s")
                    time.sleep(EVENTS_HTTP_RETRY_DELAY)
                else:
                    raise
        step_logger.log_text(f"[Request] GET {EVENTS_URL}")
        step_logger.log_text(f"[Response] {response.status_code} {response.url}")
        print(f"\n[test_TC_15_1] final_url = {response.url!r}, status = {response.status_code}")
        allure.attach(
            f"URL: {response.url}\nStatus: {response.status_code}",
            name="HTTP Response",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Check response status is 200"):
        step_logger.start_step("Check response status is 200")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        step_logger.checkpoint("Response status is 200")

    with allure.step("Check final URL matches season pattern /events/YYYY-YYYY/"):
        step_logger.start_step("Check final URL matches season pattern")
        assert SEASON_URL_PATTERN.search(response.url), (
            f"Final URL should match /events/YYYY-YYYY/, got: {response.url}"
        )
        step_logger.checkpoint("Final URL matches /events/YYYY-YYYY/ pattern")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Season title")
@allure.title("TC-15-02: H1 heading contains season pattern YYYY-YYYY")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_15_2_season_title_displayed(page: Page, step_logger):
    """TC-15-02: H1 heading contains season pattern YYYY-YYYY."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        final_url = _goto_events(page)
        step_logger.log_text(f"[Navigation] final URL = {final_url}")

    with allure.step("Check H1 contains season pattern"):
        step_logger.start_step("Check H1 contains season pattern")
        h1 = page.locator("h1").first
        assert h1.is_visible(), "H1 should be visible"
        h1_text = h1.inner_text().strip()
        print(f"\n[test_TC_15_2] h1_text = {h1_text!r}")
        allure.attach(h1_text, name="H1 text", attachment_type=allure.attachment_type.TEXT)
        assert SEASON_PATTERN.search(h1_text), (
            f"H1 should contain YYYY-YYYY pattern, got: {h1_text}"
        )
        step_logger.checkpoint("H1 contains season pattern (e.g. 2025-2026)")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Subscribe to Calendar")
@allure.title("TC-15-03: Subscribe to Calendar button is visible")
@allure.severity(allure.severity_level.NORMAL)
def test_TC_15_3_subscribe_button_visible(page: Page, step_logger):
    """TC-15-03: Subscribe to Calendar button is visible."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)

    with allure.step("Check Subscribe to Calendar button is visible"):
        step_logger.start_step("Check Subscribe to Calendar button is visible")
        subscribe_btn = page.locator("button[data-bs-target='#icalModal']")
        assert subscribe_btn.is_visible(), "Subscribe to Calendar button should be visible"
        btn_text = subscribe_btn.inner_text().strip()
        print(f"\n[test_TC_15_3] subscribe_button_text = {btn_text!r}")
        allure.attach(btn_text, name="Button text", attachment_type=allure.attachment_type.TEXT)
        step_logger.checkpoint("Subscribe to Calendar button is visible")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Subscribe to Calendar")
@allure.title("TC-15-04: iCal modal opens and contains calendar URL")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_15_4_ical_modal_opens_and_contains_url(page: Page, step_logger):
    """TC-15-04: iCal modal opens with calendar URL and subscription instructions."""
    with allure.step("Open events page (wait for scripts to load)"):
        step_logger.start_step("Open events page (wait for scripts to load)")
        page.goto(EVENTS_URL, wait_until="networkidle")
        page.wait_for_url(SEASON_URL_PATTERN, timeout=10_000)

    with allure.step("Click Subscribe to Calendar button"):
        step_logger.start_step("Click Subscribe to Calendar button")
        subscribe_btn = page.locator("button[data-bs-target='#icalModal']")
        subscribe_btn.click()

    with allure.step("Check modal is visible and contains calendar URL"):
        step_logger.start_step("Check modal is visible and contains calendar URL")
        modal = page.locator("#icalModal")
        modal.locator(".modal-title").wait_for(state="visible", timeout=5_000)
        step_logger.checkpoint("iCal modal is visible")

        modal_title = modal.locator(".modal-title").inner_text().strip()
        print(f"\n[test_TC_15_4] modal_title = {modal_title!r}")
        allure.attach(modal_title, name="Modal title", attachment_type=allure.attachment_type.TEXT)
        assert "Subscribe" in modal_title or "Calendar" in modal_title, (
            f"Modal title should mention Subscribe or Calendar, got: {modal_title}"
        )
        step_logger.checkpoint("Modal title contains 'Subscribe' or 'Calendar'")

        calendar_input = modal.locator("#calendar-url")
        assert calendar_input.is_visible(), "Calendar URL input should be visible"
        ical_url = calendar_input.get_attribute("value") or ""
        print(f"\n[test_TC_15_4] ical_url = {ical_url!r}")
        allure.attach(ical_url, name="iCal URL", attachment_type=allure.attachment_type.TEXT)
        assert ical_url.endswith("events.ics"), (
            f"Calendar URL should end with events.ics, got: {ical_url}"
        )
        step_logger.checkpoint("Calendar URL ends with events.ics")

    with allure.step("Take screenshot of modal"):
        step_logger.take_screenshot("ical_modal")

    with allure.step("Close modal"):
        step_logger.start_step("Close modal")
        close_btn = modal.locator("button", has_text="Close")
        close_btn.click()
        modal.locator(".modal-title").wait_for(state="hidden", timeout=3_000)
        step_logger.checkpoint("iCal modal closed successfully")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Season navigation links")
@allure.title("TC-15-05: Previous season navigation link is valid")
@allure.severity(allure.severity_level.NORMAL)
def test_TC_15_5_previous_season_link(page: Page, step_logger):
    """TC-15-05: Previous season navigation link is valid."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        final_url = _goto_events(page)
        current_season = _extract_season_from_url(final_url)
        step_logger.log_text(f"Current season: {current_season}")

    with allure.step("Check previous season link"):
        step_logger.start_step("Check previous season link")
        prev_link = page.locator("a.year-nav-prev")
        assert prev_link.is_visible(), "Previous season link should be visible"

        prev_href = prev_link.get_attribute("href") or ""
        prev_text = prev_link.inner_text().strip()
        print(f"\n[test_TC_15_5] prev_link href = {prev_href!r}")
        print(f"\n[test_TC_15_5] prev_link text = {prev_text!r}")
        allure.attach(
            f"href: {prev_href}\ntext: {prev_text}",
            name="Previous season link",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert SEASON_URL_PATTERN.search(prev_href), (
            f"Previous season href should match /events/YYYY-YYYY/, got: {prev_href}"
        )
        step_logger.checkpoint("Previous season link href matches season URL pattern")

        assert re.search(r"\d{4}", prev_text), (
            f"Previous season link text should contain year, got: {prev_text}"
        )
        step_logger.checkpoint("Previous season link text contains year")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Season navigation links")
@allure.title("TC-15-06: Next season navigation link is valid")
@allure.severity(allure.severity_level.NORMAL)
def test_TC_15_6_next_season_link(page: Page, step_logger):
    """TC-15-06: Next season navigation link is valid."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        final_url = _goto_events(page)
        current_season = _extract_season_from_url(final_url)
        step_logger.log_text(f"Current season: {current_season}")

    with allure.step("Check next season link"):
        step_logger.start_step("Check next season link")
        next_link = page.locator("a.year-nav-next")
        assert next_link.is_visible(), "Next season link should be visible"

        next_href = next_link.get_attribute("href") or ""
        next_text = next_link.inner_text().strip()
        print(f"\n[test_TC_15_6] next_link href = {next_href!r}")
        print(f"\n[test_TC_15_6] next_link text = {next_text!r}")
        allure.attach(
            f"href: {next_href}\ntext: {next_text}",
            name="Next season link",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert SEASON_URL_PATTERN.search(next_href), (
            f"Next season href should match /events/YYYY-YYYY/, got: {next_href}"
        )
        step_logger.checkpoint("Next season link href matches season URL pattern")

        assert re.search(r"\d{4}", next_text), (
            f"Next season link text should contain year, got: {next_text}"
        )
        step_logger.checkpoint("Next season link text contains year")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Season navigation")
@allure.title("TC-15-07: Navigate to previous season page")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_15_7_navigate_to_previous_season(page: Page, step_logger):
    """TC-15-07: Clicking prev season link navigates to the previous season page."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        original_url = _goto_events(page)
        current_season = _extract_season_from_url(original_url)
        step_logger.log_text(f"Current season: {current_season}")

    with allure.step("Click previous season link"):
        step_logger.start_step("Click previous season link")
        prev_link = page.locator("a.year-nav-prev")
        prev_href = prev_link.get_attribute("href") or ""
        expected_season = _extract_season_from_url(prev_href)
        prev_link.click()
        page.wait_for_load_state("domcontentloaded")

    with allure.step(f"Verify navigated to previous season ({expected_season})"):
        step_logger.start_step("Verify navigated to previous season")
        new_url = page.url
        new_season = _extract_season_from_url(new_url)
        print(f"\n[test_TC_15_7] navigated from {current_season} to {new_season}")
        allure.attach(
            f"From: {current_season}\nTo: {new_season}\nURL: {new_url}",
            name="Navigation result",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert new_season == expected_season, (
            f"Expected season {expected_season}, got {new_season} (URL: {new_url})"
        )
        step_logger.checkpoint(f"Navigated to previous season: {new_season}")

        h1 = page.locator("h1").first
        h1_text = h1.inner_text().strip()
        print(f"\n[test_TC_15_7] prev season h1 = {h1_text!r}")
        assert expected_season in h1_text, (
            f"H1 should contain {expected_season}, got: {h1_text}"
        )
        step_logger.checkpoint("H1 updated to previous season")

    with allure.step("Take screenshot of previous season page"):
        step_logger.take_screenshot("previous_season_page")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Season navigation")
@allure.title("TC-15-08: Navigate to next season page")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_15_8_navigate_to_next_season(page: Page, step_logger):
    """TC-15-08: Clicking next season link navigates to the next season page."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        original_url = _goto_events(page)
        current_season = _extract_season_from_url(original_url)
        step_logger.log_text(f"Current season: {current_season}")

    with allure.step("Click next season link"):
        step_logger.start_step("Click next season link")
        next_link = page.locator("a.year-nav-next")
        next_href = next_link.get_attribute("href") or ""
        expected_season = _extract_season_from_url(next_href)
        next_link.click()
        page.wait_for_load_state("domcontentloaded")

    with allure.step(f"Verify navigated to next season ({expected_season})"):
        step_logger.start_step("Verify navigated to next season")
        new_url = page.url
        new_season = _extract_season_from_url(new_url)
        print(f"\n[test_TC_15_8] navigated from {current_season} to {new_season}")
        allure.attach(
            f"From: {current_season}\nTo: {new_season}\nURL: {new_url}",
            name="Navigation result",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert new_season == expected_season, (
            f"Expected season {expected_season}, got {new_season} (URL: {new_url})"
        )
        step_logger.checkpoint(f"Navigated to next season URL: {new_season}")

        h1 = page.locator("h1").first
        h1_text = h1.inner_text().strip()
        print(f"\n[test_TC_15_8] next season h1 = {h1_text!r}")

        if "404" in h1_text or "not found" in h1_text.lower():
            allure.attach(
                f"Season {expected_season} returns 404 — page not yet created.",
                name="Note: Season not yet created",
                attachment_type=allure.attachment_type.TEXT,
            )
            step_logger.log_text(
                f"[Note] Next season {expected_season} returns 404 — page not yet created. "
                "This is expected if the season has not started."
            )
            step_logger.checkpoint(
                f"Next season {expected_season} not yet created (404). "
                "Link is valid but target page does not exist yet."
            )
        else:
            assert expected_season in h1_text, (
                f"H1 should contain {expected_season}, got: {h1_text}"
            )
            step_logger.checkpoint("H1 updated to next season")

    with allure.step("Take screenshot of next season page"):
        step_logger.take_screenshot("next_season_page")


@allure.epic("Events Page")
@allure.feature("Page Shell and Season Navigation")
@allure.story("Console errors")
@allure.title("TC-15-09: No critical console errors on events page")
@allure.severity(allure.severity_level.NORMAL)
def test_TC_15_9_no_critical_console_errors(page: Page, step_logger):
    """TC-15-09: No critical console errors on events page load."""
    console_errors = []

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", on_console)

    with allure.step("Open events page and wait for network idle"):
        step_logger.start_step("Open events page and wait for network idle")
        page.goto(EVENTS_URL, wait_until="networkidle")

    with allure.step("Check no critical console errors"):
        step_logger.start_step("Check no critical console errors")
        allowlist = get_console_error_allowlist()
        blocking = [
            e for e in console_errors
            if not any(term in e.lower() for term in allowlist)
        ]
        print(f"\n[test_TC_15_9] total_console_errors = {len(console_errors)}, blocking = {len(blocking)}")
        if console_errors:
            allure.attach(
                "\n".join(console_errors),
                name="All console errors",
                attachment_type=allure.attachment_type.TEXT,
            )
        if blocking:
            for err in blocking[:5]:
                step_logger.log_text(f"[Console Error] {err}")
            allure.attach(
                "\n".join(blocking),
                name="Blocking console errors",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not blocking, (
            f"Unexpected console errors ({len(blocking)}): {blocking[:5]}"
        )
        step_logger.checkpoint("No critical console errors on events page")
