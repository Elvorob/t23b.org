"""
TC-US-02: Hero and Featured Event (Next Big Thing) — automated tests.

User Story US-02: Visitor wants to see the featured event with date, time, and Read more.
Test cases: TC-US-02-01 .. TC-US-02-05.
"""

import re

import pytest
from playwright.sync_api import Page

from tests.conftest import BASE_URL


def _hero_section(page: Page):
    """Section that contains both 'Next Big Thing' and 'Read more'."""
    return page.locator("section, div").filter(has_text="Next Big Thing").filter(has_text="Read more").first


def test_TC_02_1_next_big_thing_section_visible(page: Page, step_logger):
    """TC-US-02-01: Next Big Thing section is visible."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check Next Big Thing section is visible")
    section = page.get_by_text("Next Big Thing").first
    is_visible = section.is_visible()
    print(f"\n[test_next_big_thing_section_visible] section.is_visible() = {is_visible}")
    assert is_visible, "Next Big Thing section should be visible"
    step_logger.checkpoint("Next Big Thing section is visible")


def test_TC_02_2_featured_event_name_displayed(page: Page, step_logger):
    """TC-US-02-02: Featured event name is displayed."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check featured event name is displayed in hero")
    hero = _hero_section(page)
    assert hero.is_visible(), "Hero section should be visible"
    step_logger.checkpoint("Hero section is visible")
    event_heading = hero.locator("h2, h3, h4").first
    assert event_heading.is_visible(), "Event name (heading) should be visible"
    name_text = event_heading.inner_text().strip()
    print(f"\n[test_featured_event_name_displayed] name_text (event name) = {name_text!r}")
    assert len(name_text) > 0, "Event name should be non-empty"
    step_logger.checkpoint("Event name is displayed and non-empty")


def test_TC_02_3_event_date_shown_in_readable_format(page: Page, step_logger):
    """TC-US-02-03: Event date is shown in readable format."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check event date is shown in hero")
    hero = _hero_section(page)
    assert hero.is_visible(), "Hero section should be visible"
    text = hero.inner_text()
    print(f"\n[test_event_date_shown_in_readable_format] hero.inner_text() (excerpt) = {text[:300]!r}...")
    date_pattern = (
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s*\d{4}"
        r"|\d{1,2}/\d{1,2}/\d{2,4}"
        r"|\d{4}-\d{2}-\d{2}"
    )
    assert re.search(date_pattern, text, re.IGNORECASE), (
        f"Hero should contain a date, got excerpt: {text[:200]}"
    )
    step_logger.checkpoint("Event date is shown in readable format")


def test_TC_02_4_event_time_range_shown(page: Page, step_logger):
    """TC-US-02-04: Event time range is shown."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check event time range is shown in hero")
    hero = _hero_section(page)
    assert hero.is_visible(), "Hero section should be visible"
    text = hero.inner_text()
    print(f"\n[test_event_time_range_shown] hero.inner_text() (excerpt) = {text[:300]!r}...")
    time_pattern = r"\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)"
    assert re.search(time_pattern, text), (
        f"Hero should contain time (e.g. 7:00 pm), got excerpt: {text[:200]}"
    )
    step_logger.checkpoint("Event time range is shown")


def test_TC_02_5_read_more_link_present_and_navigates_to_event_page(page: Page, step_logger):
    """TC-US-02-05: Read more link is present and navigates to event page."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check Read more link is present and has correct href")
    hero = _hero_section(page)
    assert hero.is_visible(), "Hero section should be visible"
    read_more = hero.get_by_role("link", name="Read more")
    assert read_more.is_visible(), "Read more link should be visible"
    href = read_more.get_attribute("href") or ""
    print(f"\n[test_read_more_link] href = {href!r}")
    assert "/events/" in href, f"Read more href should contain '/events/', got: {href}"
    step_logger.checkpoint("Read more link href contains '/events/'")
    step_logger.start_step("Click Read more and check destination")
    read_more.click()
    # Capture destination page for report
    step_logger.take_screenshot("event_page")
    final_url = page.url
    print(f"\n[test_read_more_link] page.url after click = {final_url!r}")
    assert "/events/" in final_url, f"After click URL should contain '/events/', got: {final_url}"
    step_logger.checkpoint("Destination URL contains '/events/' and screenshot captured")
