"""
TC-10: Responsive and Basic UX — automated tests.

Test Case TC-10: Desktop/mobile viewports, CTA clickability, overlays, and readable text.
"""

from playwright.sync_api import Page

from tests.conftest import BASE_URL


DESKTOP_VIEWPORT = {"width": 1280, "height": 720}
MOBILE_VIEWPORT = {"width": 375, "height": 667}


def _ensure_homepage(page: Page, viewport: dict, step_logger) -> None:
    step_logger.start_step(f"Set viewport to {viewport['width']}x{viewport['height']}")
    page.set_viewport_size(viewport)
    step_logger.start_step("Open homepage")
    page.goto(BASE_URL, wait_until="domcontentloaded")


def test_TC_10_1_desktop_viewport_key_sections_visible_without_horizontal_scroll(
    page: Page, step_logger
):
    """TC-10-01: Desktop viewport — key sections visible without horizontal scroll."""
    _ensure_homepage(page, DESKTOP_VIEWPORT, step_logger)

    step_logger.start_step("Check key sections are visible on desktop")
    h1 = page.locator("h1").first
    next_big_thing = page.get_by_text("Next Big Thing", exact=False).first
    welcome = page.get_by_text("Welcome to Troop 23", exact=False).first

    h1_visible = h1.is_visible()
    nbt_visible = next_big_thing.is_visible()
    welcome_visible = welcome.is_visible()
    print(
        "\n[test_desktop_viewport_key_sections_visible] "
        f"h1_visible={h1_visible}, nbt_visible={nbt_visible}, "
        f"welcome_visible={welcome_visible}"
    )
    assert h1_visible, "H1 should be visible on desktop"
    assert nbt_visible, '"Next Big Thing" section should be visible on desktop'
    assert welcome_visible, '"Welcome to Troop 23" section should be visible on desktop'

    step_logger.start_step("Check horizontal scroll is not required on desktop")
    scroll_width = page.evaluate("document.body.scrollWidth")
    viewport_width = page.viewport_size["width"]
    print(
        "\n[test_desktop_viewport_key_sections_visible] "
        f"scroll_width={scroll_width}, viewport_width={viewport_width}"
    )
    assert scroll_width <= viewport_width + 20, (
        f"Body scroll width ({scroll_width}) should not significantly exceed "
        f"viewport width ({viewport_width})"
    )
    step_logger.checkpoint(
        "Desktop viewport shows key sections without horizontal scroll"
    )


def test_TC_10_2_mobile_viewport_page_readable_and_key_sections_accessible(
    page: Page, step_logger
):
    """TC-10-02: Mobile viewport — page readable and key sections accessible."""
    _ensure_homepage(page, MOBILE_VIEWPORT, step_logger)

    step_logger.start_step("Ensure key sections are accessible on mobile")
    h1 = page.locator("h1").first
    next_big_thing = page.get_by_text("Next Big Thing", exact=False).first
    welcome = page.get_by_text("Welcome to Troop 23", exact=False).first

    h1.scroll_into_view_if_needed()
    next_big_thing.scroll_into_view_if_needed()
    welcome.scroll_into_view_if_needed()

    h1_visible = h1.is_visible()
    nbt_visible = next_big_thing.is_visible()
    welcome_visible = welcome.is_visible()
    print(
        "\n[test_mobile_viewport_page_readable_and_key_sections_accessible] "
        f"h1_visible={h1_visible}, nbt_visible={nbt_visible}, "
        f"welcome_visible={welcome_visible}"
    )
    assert h1_visible, "H1 should be visible on mobile (after scroll)"
    assert nbt_visible, '"Next Big Thing" should be visible on mobile (after scroll)'
    assert welcome_visible, (
        '"Welcome to Troop 23" should be visible on mobile (after scroll)'
    )
    step_logger.checkpoint(
        "Mobile viewport has key sections accessible and readable"
    )


def test_TC_10_3_primary_ctas_are_clickable(page: Page, step_logger):
    """TC-10-03: Primary CTAs (Read more, Learn more) are clickable."""
    _ensure_homepage(page, DESKTOP_VIEWPORT, step_logger)

    step_logger.start_step("Locate primary CTAs: Read more and Learn more")
    read_more = page.get_by_role("link", name="Read more").first
    learn_more = page.get_by_role("link", name="Learn more").first

    read_more_visible = read_more.is_visible()
    learn_more_visible = learn_more.is_visible()
    print(
        "\n[test_primary_ctas_are_clickable] "
        f"read_more_visible={read_more_visible}, learn_more_visible={learn_more_visible}"
    )
    assert read_more_visible, '"Read more" link should be visible'
    assert learn_more_visible, '"Learn more" link should be visible'
    step_logger.checkpoint("Primary CTAs are visible")

    step_logger.start_step('Click "Read more" and check destination')
    read_more.click()
    step_logger.take_screenshot("read_more_event_page")
    read_more_url = page.url
    print(f"[test_primary_ctas_are_clickable] read_more_url = {read_more_url!r}")
    assert "/events/" in read_more_url, (
        f'"Read more" should navigate to event page, got: {read_more_url}'
    )
    step_logger.checkpoint(
        '"Read more" navigates to event page and screenshot captured'
    )

    step_logger.start_step("Return to homepage for Learn more CTA")
    page.goto(BASE_URL, wait_until="domcontentloaded")

    step_logger.start_step('Click "Learn more" and check destination')
    learn_more = page.get_by_role("link", name="Learn more").first
    learn_more.click()
    step_logger.take_screenshot("learn_more_how_to_join_page")
    learn_more_url = page.url
    print(f"[test_primary_ctas_are_clickable] learn_more_url = {learn_more_url!r}")
    assert "how-to-join" in learn_more_url, (
        f'"Learn more" should navigate to How to Join, got: {learn_more_url}'
    )
    step_logger.checkpoint(
        '"Learn more" navigates to How to Join and screenshot captured'
    )


def test_TC_10_4_no_permanent_overlay_blocking_main_content_or_ctas(
    page: Page, step_logger
):
    """TC-10-04: No permanent overlay blocking main content or CTAs."""
    _ensure_homepage(page, DESKTOP_VIEWPORT, step_logger)

    step_logger.start_step("Check H1 and primary CTA are clickable (no blocking overlay)")
    h1 = page.locator("h1").first
    read_more = page.get_by_role("link", name="Read more").first

    # Use trial clicks to ensure elements are clickable (Playwright will throw if obscured)
    h1.click(trial=True)
    read_more.click(trial=True)
    step_logger.checkpoint(
        "H1 and primary CTA are clickable; no permanent overlay blocking main content"
    )


def test_TC_10_5_text_is_readable_in_desktop_and_mobile_viewports(
    page: Page, step_logger
):
    """TC-10-05: Text is readable in desktop and mobile viewports."""
    # Desktop
    _ensure_homepage(page, DESKTOP_VIEWPORT, step_logger)
    step_logger.start_step("Check desktop font size")
    desktop_font_size = page.evaluate(
        "getComputedStyle(document.body).fontSize"
    )
    print(
        f"\n[test_text_is_readable] desktop_font_size = {desktop_font_size!r}"
    )
    desktop_px = int(float(desktop_font_size.replace("px", "")))
    assert desktop_px >= 12, (
        f"Desktop font size should be at least 12px, got: {desktop_px}"
    )

    # Mobile
    _ensure_homepage(page, MOBILE_VIEWPORT, step_logger)
    step_logger.start_step("Check mobile font size")
    mobile_font_size = page.evaluate(
        "getComputedStyle(document.body).fontSize"
    )
    print(
        f"[test_text_is_readable] mobile_font_size = {mobile_font_size!r}"
    )
    mobile_px = int(float(mobile_font_size.replace("px", "")))
    assert mobile_px >= 12, (
        f"Mobile font size should be at least 12px, got: {mobile_px}"
    )
    step_logger.checkpoint(
        "Body text font size is readable on both desktop and mobile viewports"
    )

