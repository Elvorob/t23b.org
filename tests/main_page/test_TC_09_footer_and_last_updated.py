"""
TC-09: Footer and Last Updated — automated tests.

Test Case TC-09: Last updated indicator visibility and date format.
"""

import re

from playwright.sync_api import Page

from tests.conftest import BASE_URL
from tests.footer_checks import assert_footer_structure_and_contacts_ok


def _last_updated_element(page: Page):
    return page.get_by_text("Last updated", exact=False).first


def test_TC_09_1_last_updated_indicator_visible(page: Page, step_logger):
    """TC-09-01: Last updated indicator is visible."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Locate Last updated indicator")
    elem = _last_updated_element(page)
    visible = elem.is_visible()
    print(f"\n[test_last_updated_indicator_visible] visible = {visible}")
    assert visible, '"Last updated" indicator should be visible'
    step_logger.checkpoint('"Last updated" indicator is visible')


def test_TC_09_2_last_updated_date_has_valid_format_and_non_empty(
    page: Page, step_logger
):
    """TC-09-02/03: Last updated date is in valid format and non-empty."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step("Get Last updated text and validate date format")
    elem = _last_updated_element(page)
    text = elem.inner_text()
    print(
        "\n[test_last_updated_date_has_valid_format_and_non_empty] "
        f"text = {text!r}"
    )
    # Accept common date formats: "May 07, 2025", "05/07/2025", etc.
    date_pattern = (
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s*\d{4}"
        r"|\d{1,2}/\d{1,2}/\d{4}"
        r"|\d{4}-\d{2}-\d{2}"
    )
    m = re.search(date_pattern, text, re.IGNORECASE)
    assert m, (
        f'"Last updated" text should contain a date, got: {text!r}'
    )
    date_substring = m.group(0)
    print(
        "[test_last_updated_date_has_valid_format_and_non_empty] "
        f"date_substring = {date_substring!r}"
    )
    assert len(date_substring.strip()) >= 5, (
        f"Date substring should be non-empty and readable, got: {date_substring!r}"
    )
    step_logger.checkpoint(
        '"Last updated" date has valid date pattern and is non-empty'
    )


def test_TC_09_3_footer_structure_and_contacts_on_homepage(
    page: Page, step_logger
):
    """
    TC-09-03: Footer structure and contacts are present on the homepage.

    - Footer exists and is visible
    - At least one section heading (h5) in footer
    - At least one email and one phone contact in footer
    - Copyright line with year and brand
    """
    step_logger.start_step("Open homepage for footer checks")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    assert_footer_structure_and_contacts_ok(
        page, step_logger=step_logger, scope="homepage"
    )

