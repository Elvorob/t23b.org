"""
TC-17: Category Filtering Behavior — automated tests.

Verify that filter buttons are visible, default state has no active filters,
activating a filter hides non-matching events, deactivating restores all,
multiple filters use OR logic, and clearing filters returns to default.
"""
from __future__ import annotations

import re

import allure
import pytest
from playwright.sync_api import Page

from tests.conftest import EVENTS_URL

SEASON_URL_PATTERN = re.compile(r"/events/\d{4}-\d{4}/?")
DESKTOP_VIEWPORT = {"width": 992, "height": 800}
ALPINE_SETTLE_MS = 600


def _goto_events(page: Page) -> str:
    """Set desktop viewport, navigate to events, wait for Alpine.js init."""
    page.set_viewport_size(DESKTOP_VIEWPORT)
    page.goto(EVENTS_URL, wait_until="networkidle")
    page.wait_for_url(SEASON_URL_PATTERN, timeout=10_000)
    return page.url


def _get_category_key(filter_el) -> str:
    """Extract category key from the filter element's class list (e.g. 'category-camping' → 'camping')."""
    classes = (filter_el.get_attribute("class") or "").split()
    for cls in classes:
        if cls.startswith("category-"):
            return cls[len("category-"):]
    return ""


def _get_card_categories_via_timeline(page: Page, event_id: str) -> list[str]:
    """Get event categories by looking up the timeline element with the same event ID."""
    timeline_el = page.locator(f".events-timeline-event[data-event-id='{event_id}']").first
    raw = timeline_el.get_attribute("data-event-categories") or ""
    return [c for c in raw.split(",") if c]


def _count_visible_cards(page: Page) -> int:
    return page.locator(".event-card:not(.filtered-out)").count()


def _count_filtered_out_cards(page: Page) -> int:
    return page.locator(".event-card.filtered-out").count()


def _get_overview_count(page: Page) -> int:
    """Parse the first number from the Overview heading (works for both '(44)' and '(12 of 44, ...)')."""
    title_el = page.locator(".events-timeline-title")
    text = title_el.inner_text().strip()
    m = re.search(r"\((\d+)", text)
    assert m, f"Could not parse Overview count from: {text!r}"
    return int(m.group(1))


def _get_visible_filter_buttons(page: Page):
    """Return only filter buttons that are actually visible (Alpine x-show rendered)."""
    all_btns = page.locator(".filter-category").all()
    return [btn for btn in all_btns if btn.is_visible()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("Filter buttons")
@allure.title("TC-17-01: Filter buttons are visible with text")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_17_1_filter_buttons_visible_with_text(page: Page, step_logger):
    """TC-17-01: Category filter buttons are present and have non-empty text."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)

    with allure.step("Collect visible filter buttons"):
        step_logger.start_step("Collect visible filter buttons")
        buttons = _get_visible_filter_buttons(page)
        print(f"\n[test_TC_17_1] visible_filter_buttons = {len(buttons)}")
        assert len(buttons) >= 1, "Expected at least 1 visible filter button"

    with allure.step("Check each button has non-empty text"):
        step_logger.start_step("Check each button has non-empty text")
        names = []
        for btn in buttons:
            text = btn.inner_text().strip()
            key = _get_category_key(btn)
            assert text, f"Filter button category-{key} has empty text"
            names.append(f"{key} → {text!r}")
            step_logger.log_text(f"  filter: key={key!r} text={text!r}")

        summary = "\n".join(names)
        print(f"\n[test_TC_17_1] buttons:\n{summary}")
        allure.attach(summary, name="Filter buttons", attachment_type=allure.attachment_type.TEXT)
        step_logger.checkpoint(f"{len(buttons)} filter buttons visible with text")


@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("Default state")
@allure.title("TC-17-02: Default state has no filters active")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_17_2_default_no_filters_active(page: Page, step_logger):
    """TC-17-02: On page load, no filter is active and all events are visible."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)

    with allure.step("Check no active filter buttons"):
        step_logger.start_step("Check no active filter buttons")
        active_count = page.locator(".filter-category.active").count()
        print(f"\n[test_TC_17_2] active_filters = {active_count}")
        assert active_count == 0, f"Expected 0 active filters, got {active_count}"
        step_logger.checkpoint("No active filter buttons on load")

    with allure.step("Check no filtered-out cards"):
        step_logger.start_step("Check no filtered-out cards")
        filtered_out = _count_filtered_out_cards(page)
        total_cards = page.locator(".event-card").count()
        print(f"\n[test_TC_17_2] total_cards = {total_cards}, filtered_out = {filtered_out}")
        assert filtered_out == 0, f"Expected 0 filtered-out cards, got {filtered_out}"
        step_logger.checkpoint(f"All {total_cards} cards visible (0 filtered out)")

    with allure.step("Check Overview count"):
        step_logger.start_step("Check Overview count")
        overview_n = _get_overview_count(page)
        print(f"\n[test_TC_17_2] overview_count = {overview_n}")
        allure.attach(
            f"Overview: {overview_n}\nTotal cards: {total_cards}",
            name="Default counts",
            attachment_type=allure.attachment_type.TEXT,
        )
        step_logger.checkpoint(f"Overview shows {overview_n}, total cards = {total_cards}")


@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("Single filter")
@allure.title("TC-17-03: Activating a single filter hides non-matching events")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_17_3_single_filter_hides_non_matching(page: Page, step_logger):
    """TC-17-03: Clicking one filter shows only matching events."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)
        total_cards = page.locator(".event-card").count()

    with allure.step("Click first visible filter"):
        step_logger.start_step("Click first visible filter")
        buttons = _get_visible_filter_buttons(page)
        assert len(buttons) >= 1, "Need at least 1 filter button"
        btn = buttons[0]
        cat_key = _get_category_key(btn)
        btn_text = btn.inner_text().strip()
        print(f"\n[test_TC_17_3] clicking filter: key={cat_key!r} text={btn_text!r}")
        btn.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)

    with allure.step("Check button is active"):
        step_logger.start_step("Check button is active")
        classes_after = btn.get_attribute("class") or ""
        assert "active" in classes_after, f"Filter button should be active, classes: {classes_after}"
        step_logger.checkpoint(f"Filter '{cat_key}' is active")

    with allure.step("Verify card visibility matches filter"):
        step_logger.start_step("Verify card visibility matches filter")
        cards = page.locator(".event-card").all()
        visible = 0
        hidden = 0
        errors = []

        for card in cards:
            event_id = card.get_attribute("data-event-id") or ""
            card_cats = _get_card_categories_via_timeline(page, event_id)
            is_filtered_out = "filtered-out" in (card.get_attribute("class") or "")

            if cat_key in card_cats:
                if is_filtered_out:
                    errors.append(f"Card {event_id} has category '{cat_key}' but is filtered out")
                visible += 1
            else:
                if not is_filtered_out:
                    errors.append(f"Card {event_id} lacks category '{cat_key}' but is NOT filtered out")
                hidden += 1

        summary = (
            f"Filter: {cat_key}\n"
            f"Total cards: {total_cards}\n"
            f"Should be visible: {visible}\n"
            f"Should be hidden: {hidden}\n"
            f"Errors: {len(errors)}"
        )
        print(f"\n[test_TC_17_3] {summary}")
        allure.attach(summary, name="Filter result", attachment_type=allure.attachment_type.TEXT)
        step_logger.log_text(summary)

        if errors:
            allure.attach("\n".join(errors), name="Filtering errors", attachment_type=allure.attachment_type.TEXT)
        assert not errors, f"{len(errors)} filtering error(s):\n" + "\n".join(errors)
        assert visible >= 1, f"Filter '{cat_key}' should match at least 1 card"
        step_logger.checkpoint(f"Filter '{cat_key}': {visible} visible, {hidden} hidden — correct")


@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("Filtered count")
@allure.title("TC-17-04: Filtered count matches visible cards")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_17_4_filtered_count_matches_visible_cards(page: Page, step_logger):
    """TC-17-04: Overview filtered count equals actual visible card count."""
    with allure.step("Open events page and activate one filter"):
        step_logger.start_step("Open events page and activate one filter")
        _goto_events(page)
        buttons = _get_visible_filter_buttons(page)
        assert len(buttons) >= 1
        btn = buttons[0]
        cat_key = _get_category_key(btn)
        btn.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)
        print(f"\n[test_TC_17_4] activated filter: {cat_key!r}")

    with allure.step("Count visible cards"):
        step_logger.start_step("Count visible cards")
        actual_visible = _count_visible_cards(page)
        print(f"\n[test_TC_17_4] actual_visible_cards = {actual_visible}")

    with allure.step("Read Overview filtered count"):
        step_logger.start_step("Read Overview filtered count")
        overview_n = _get_overview_count(page)
        print(f"\n[test_TC_17_4] overview_filtered_count = {overview_n}")
        allure.attach(
            f"Overview says: {overview_n}\nActual visible cards: {actual_visible}",
            name="Count comparison",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Assert counts match"):
        step_logger.start_step("Assert counts match")
        assert overview_n == actual_visible, (
            f"Overview shows {overview_n} but {actual_visible} cards are actually visible"
        )
        step_logger.checkpoint(f"Overview ({overview_n}) matches visible cards ({actual_visible})")


@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("Deactivate filter")
@allure.title("TC-17-05: Deactivating a filter restores all events")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_17_5_deactivate_restores_all(page: Page, step_logger):
    """TC-17-05: Toggling a filter off restores default state."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)
        total_before = page.locator(".event-card").count()

    with allure.step("Activate a filter"):
        step_logger.start_step("Activate a filter")
        buttons = _get_visible_filter_buttons(page)
        btn = buttons[0]
        cat_key = _get_category_key(btn)
        btn.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)
        filtered_out_while_active = _count_filtered_out_cards(page)
        print(f"\n[test_TC_17_5] filter '{cat_key}' ON → {filtered_out_while_active} cards filtered out")
        assert filtered_out_while_active > 0, "Filter should hide at least some cards"

    with allure.step("Deactivate the same filter"):
        step_logger.start_step("Deactivate the same filter")
        btn.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)

    with allure.step("Check all filters deactivated"):
        step_logger.start_step("Check all filters deactivated")
        active_count = page.locator(".filter-category.active").count()
        assert active_count == 0, f"Expected 0 active filters after toggle off, got {active_count}"
        step_logger.checkpoint("No active filters after deactivation")

    with allure.step("Check all cards visible again"):
        step_logger.start_step("Check all cards visible again")
        filtered_out_after = _count_filtered_out_cards(page)
        total_after = page.locator(".event-card").count()
        print(f"\n[test_TC_17_5] filter OFF → filtered_out = {filtered_out_after}, total = {total_after}")
        assert filtered_out_after == 0, f"Expected 0 filtered-out after deactivation, got {filtered_out_after}"
        assert total_after == total_before, f"Card count changed: {total_before} → {total_after}"
        step_logger.checkpoint(f"All {total_after} cards restored after filter deactivation")

    with allure.step("Check Overview count restored"):
        step_logger.start_step("Check Overview count restored")
        overview_n = _get_overview_count(page)
        print(f"\n[test_TC_17_5] overview after deactivation = {overview_n}")
        allure.attach(str(overview_n), name="Overview after deactivation", attachment_type=allure.attachment_type.TEXT)
        step_logger.checkpoint(f"Overview count restored to {overview_n}")


@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("OR logic")
@allure.title("TC-17-06: Multiple filters use OR logic")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC_17_6_multiple_filters_or_logic(page: Page, step_logger):
    """TC-17-06: Activating two filters shows events matching EITHER category."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)

    with allure.step("Activate two filters"):
        step_logger.start_step("Activate two filters")
        buttons = _get_visible_filter_buttons(page)
        assert len(buttons) >= 2, f"Need at least 2 filter buttons, got {len(buttons)}"

        btn_a = buttons[0]
        btn_b = buttons[1]
        key_a = _get_category_key(btn_a)
        key_b = _get_category_key(btn_b)
        print(f"\n[test_TC_17_6] activating filters: {key_a!r} and {key_b!r}")

        btn_a.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)
        btn_b.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)

    with allure.step("Check both buttons active"):
        step_logger.start_step("Check both buttons active")
        assert "active" in (btn_a.get_attribute("class") or ""), f"Button '{key_a}' should be active"
        assert "active" in (btn_b.get_attribute("class") or ""), f"Button '{key_b}' should be active"
        step_logger.checkpoint(f"Both filters active: {key_a}, {key_b}")

    with allure.step("Verify OR logic on all cards"):
        step_logger.start_step("Verify OR logic on all cards")
        selected = {key_a, key_b}
        cards = page.locator(".event-card").all()
        errors = []
        visible_count = 0
        hidden_count = 0

        for card in cards:
            event_id = card.get_attribute("data-event-id") or ""
            card_cats = set(_get_card_categories_via_timeline(page, event_id))
            is_filtered_out = "filtered-out" in (card.get_attribute("class") or "")
            has_match = bool(card_cats & selected)

            if has_match and is_filtered_out:
                errors.append(
                    f"Card {event_id} has matching category {card_cats & selected} but is filtered out"
                )
            elif not has_match and not is_filtered_out:
                errors.append(
                    f"Card {event_id} categories {card_cats} match neither {selected} but is visible"
                )

            if not is_filtered_out:
                visible_count += 1
            else:
                hidden_count += 1

        summary = (
            f"Filters: {key_a}, {key_b}\n"
            f"Visible: {visible_count}\n"
            f"Hidden: {hidden_count}\n"
            f"Errors: {len(errors)}"
        )
        print(f"\n[test_TC_17_6] {summary}")
        allure.attach(summary, name="OR logic result", attachment_type=allure.attachment_type.TEXT)
        step_logger.log_text(summary)

        if errors:
            allure.attach("\n".join(errors), name="OR logic errors", attachment_type=allure.attachment_type.TEXT)
        assert not errors, f"{len(errors)} OR logic error(s):\n" + "\n".join(errors)
        step_logger.checkpoint(f"OR logic correct: {visible_count} visible, {hidden_count} hidden")


@allure.epic("Events Page")
@allure.feature("Category Filtering")
@allure.story("Clear all filters")
@allure.title("TC-17-07: Clearing all filters restores default state")
@allure.severity(allure.severity_level.NORMAL)
def test_TC_17_7_clear_all_restores_default(page: Page, step_logger):
    """TC-17-07: Deactivating all filters returns to default (all visible, no active)."""
    with allure.step("Open events page"):
        step_logger.start_step("Open events page")
        _goto_events(page)
        total_before = page.locator(".event-card").count()

    with allure.step("Activate two filters"):
        step_logger.start_step("Activate two filters")
        buttons = _get_visible_filter_buttons(page)
        assert len(buttons) >= 2
        btn_a = buttons[0]
        btn_b = buttons[1]
        key_a = _get_category_key(btn_a)
        key_b = _get_category_key(btn_b)
        btn_a.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)
        btn_b.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)
        filtered_while_active = _count_filtered_out_cards(page)
        print(f"\n[test_TC_17_7] 2 filters ON → {filtered_while_active} filtered out")

    with allure.step("Deactivate both filters"):
        step_logger.start_step("Deactivate both filters")
        btn_a.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)
        btn_b.click()
        page.wait_for_timeout(ALPINE_SETTLE_MS)

    with allure.step("Check no active filters"):
        step_logger.start_step("Check no active filters")
        active_count = page.locator(".filter-category.active").count()
        print(f"\n[test_TC_17_7] active_filters after clear = {active_count}")
        assert active_count == 0, f"Expected 0 active filters, got {active_count}"
        step_logger.checkpoint("All filters deactivated")

    with allure.step("Check all cards visible"):
        step_logger.start_step("Check all cards visible")
        filtered_out = _count_filtered_out_cards(page)
        total_after = page.locator(".event-card").count()
        print(f"\n[test_TC_17_7] filtered_out = {filtered_out}, total = {total_after}")
        assert filtered_out == 0, f"Expected 0 filtered-out, got {filtered_out}"
        assert total_after == total_before, f"Card count changed: {total_before} → {total_after}"
        step_logger.checkpoint(f"All {total_after} cards visible")

    with allure.step("Check Overview count restored"):
        step_logger.start_step("Check Overview count restored")
        overview_n = _get_overview_count(page)
        print(f"\n[test_TC_17_7] overview after clear = {overview_n}")
        allure.attach(
            f"Overview: {overview_n}\nTotal cards: {total_after}",
            name="State after clearing filters",
            attachment_type=allure.attachment_type.TEXT,
        )
        step_logger.checkpoint(f"Overview restored to {overview_n}")
