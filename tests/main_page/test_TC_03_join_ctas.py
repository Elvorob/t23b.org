"""
TC-US-03: Join CTAs (Become a Boy Scout / Become a Cub Scout) — automated tests.

User Story US-03: Parent or youth wants to see how to join as Boy or Cub Scout.
"""

import re

from playwright.sync_api import Page

from tests.conftest import BASE_URL


def _boy_block(page: Page):
    title = page.get_by_text("Become a Boy Scout").first
    return title.locator("xpath=ancestor::section|ancestor::div").first


def _cub_block(page: Page):
    title = page.get_by_text("Become a Cub Scout").first
    return title.locator("xpath=ancestor::section|ancestor::div").first


def test_TC_03_1_boy_scout_block_visible(page: Page, step_logger):
    """TC-US-03-01: Become a Boy Scout block is visible."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check Become a Boy Scout block is visible")
    block = _boy_block(page)
    visible = block.is_visible()
    print(f"\n[test_boy_scout_block_visible] visible = {visible}")
    assert visible, "Become a Boy Scout block should be visible"
    step_logger.checkpoint("Become a Boy Scout block is visible")


def test_TC_03_2_cub_scout_block_visible(page: Page, step_logger):
    """TC-US-03-02: Become a Cub Scout block is visible."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check Become a Cub Scout block is visible")
    block = _cub_block(page)
    visible = block.is_visible()
    print(f"\n[test_cub_scout_block_visible] visible = {visible}")
    assert visible, "Become a Cub Scout block should be visible"
    step_logger.checkpoint("Become a Cub Scout block is visible")


def _block_has_phone_with_correct_digit_count(text: str) -> bool:
    """Check that text contains a phone number: 10 digits, or 11 digits with leading 1 (format-agnostic)."""
    digits_only = re.sub(r"\D", "", text)
    for i in range(len(digits_only) - 9):
        if i + 10 <= len(digits_only):
            run10 = digits_only[i : i + 10]
            if run10.isdigit():
                return True
        if i + 11 <= len(digits_only) and digits_only[i] == "1":
            run11 = digits_only[i : i + 11]
            if run11.isdigit():
                return True
    return False


def test_TC_03_3_boy_scout_block_has_contact_name_and_phone(page: Page, step_logger):
    """TC-US-03-03: Boy Scout block shows contact name and contact method."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check contact info in Boy Scout block")
    block = _boy_block(page)
    text = block.inner_text()
    print(f"\n[test_boy_scout_block_has_contact_name_and_phone] block text excerpt = {text[:200]!r}...")
    assert "Contact" in text, "Boy Scout block should contain 'Contact'"
    assert _block_has_phone_with_correct_digit_count(text), (
        "Boy Scout block should contain a phone number (10 digits, or 11 with leading 1)"
    )
    step_logger.checkpoint("Boy Scout block has contact label and phone")


def test_TC_03_4_cub_scout_block_has_contact_name_and_phone(page: Page, step_logger):
    """TC-US-03-04: Cub Scout block shows contact name and contact method."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Check contact info in Cub Scout block")
    block = _cub_block(page)
    text = block.inner_text()
    print(f"\n[test_cub_scout_block_has_contact_name_and_phone] block text excerpt = {text[:200]!r}...")
    assert "Contact" in text, "Cub Scout block should contain 'Contact'"
    assert _block_has_phone_with_correct_digit_count(text), (
        "Cub Scout block should contain a phone number (10 digits, or 11 with leading 1)"
    )
    step_logger.checkpoint("Cub Scout block has contact label and phone")


def test_TC_03_5_learn_more_links_go_to_how_to_join(page: Page, step_logger):
    """TC-US-03-05/06: Learn more links go to How to Join."""
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    step_logger.start_step("Locate all Learn more links and verify href")
    links = page.get_by_role("link", name="Learn more")
    count = links.count()
    print(f"\n[test_learn_more_links_go_to_how_to_join] Learn more count = {count}")
    assert count >= 2, "Expected at least two 'Learn more' links (Boy and Cub Scout)"
    for i in range(count):
        link = links.nth(i)
        href = link.get_attribute("href") or ""
        print(f"[test_learn_more_links_go_to_how_to_join] link {i} href = {href!r}")
        assert "how-to-join" in href, (
            f"'Learn more' href should contain 'how-to-join', got: {href}"
        )
        step_logger.checkpoint(
            f"Learn more link {i + 1} href points to How to Join"
        )
        step_logger.start_step(
            f"Click Learn more link {i + 1} and check destination"
        )
        link.click()
        # Capture destination page for report
        step_logger.take_screenshot(f"how_to_join_link_{i + 1}")
        final_url = page.url
        print(
            f"[test_learn_more_links_go_to_how_to_join] final_url for link {i} = {final_url!r}"
        )
        assert "how-to-join" in final_url, (
            f"After click URL for link {i} should contain 'how-to-join', got: {final_url}"
        )
        step_logger.checkpoint(
            f"Learn more link {i + 1} navigates to How to Join and screenshot captured"
        )
        if i < count - 1:
            # Go back to homepage for the next link
            page.go_back(wait_until="domcontentloaded")
    step_logger.checkpoint("All Learn more links point to and open How to Join")

