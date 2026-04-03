# Test Cases: TC-17 — Category Filtering Behavior

**Test Case:** TC-17 (Category Filtering Behavior)  
**Scope:** https://www.t23b.org/events/

---

## TC-17-01: Filter buttons are visible with text

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport; events page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page. | Page loads. |
| 2 | Locate all `.filter-category` elements. | At least 1 filter button found. |
| 3 | For each button, get inner text. | Text is non-empty (e.g. "Camping", "Hiking"). |

**Automation notes:** Selector `.filter-category`. Categories are dynamically sorted by frequency via Alpine.js — do not assert specific order.

---

## TC-17-02: Default state has no filters active

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded; no user interaction. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Check all `.filter-category` elements for `active` class. | None have `active` class. |
| 2 | Check all `.event-card` elements for `filtered-out` class. | None have `filtered-out` class. |
| 3 | Read Overview count N from heading. | N equals total event count. |

**Automation notes:** Use `.filter-category.active` selector — expect 0 matches. Use `.event-card.filtered-out` — expect 0 matches.

---

## TC-17-03: Activating a single filter hides non-matching events

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded; no filters active. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click the first visible `.filter-category` button. Record its category key from the class name. | Button receives `active` class. |
| 2 | Check `.event-card` elements. | Cards whose `data-event-categories` does NOT contain the selected category have `filtered-out` class. Cards with the category remain visible. |
| 3 | Read updated Overview count. | Count is less than or equal to total N. |

**Automation notes:** Extract category key from button class (e.g. `category-camping` → `camping`). Use `data-event-categories` attribute on `.event-card` to verify filtering logic. Do not rely on Bootstrap layout classes for visibility — check `filtered-out` class presence.

---

## TC-17-04: Filtered count matches visible cards

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | One or more filters active. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Count `.event-card` elements without `filtered-out` class. | Count is a positive number. |
| 2 | Read the filtered count from Overview heading. | Displayed count matches actual visible card count. |

**Automation notes:** Parse the filtered count from text like `(12 of 44, filtered by 1 category)` using regex.

---

## TC-17-05: Deactivating a filter restores all events

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | One filter active from TC-17-03. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click the same category button again (the one with `active` class). | `active` class removed from button. |
| 2 | Check `.event-card` elements. | No cards have `filtered-out` class. |
| 3 | Read Overview count. | Count returns to total N. |

**Automation notes:** This tests the toggle behavior of `toggleCategory()`.

---

## TC-17-06: Multiple filters use OR logic

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded; no filters active. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click two different `.filter-category` buttons. | Both buttons have `active` class. |
| 2 | Check visible events. | Events matching EITHER category are visible (no `filtered-out`). Events matching NEITHER category have `filtered-out`. |
| 3 | Read Overview count. | Count reflects the union of both categories. |

**Automation notes:** Select two categories that have some non-overlapping events. For each visible card, verify that `data-event-categories` contains at least one of the two selected keys. This validates the OR (union) logic implemented in `isEventVisible()`.

---

## TC-17-07: Clearing all filters restores default state

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Two filters active from TC-17-06. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click both active category buttons to deactivate them. | No buttons have `active` class. |
| 2 | Check events. | All events visible (no `filtered-out`). |
| 3 | Read Overview count. | Count equals total N. |

**Automation notes:** State should return to exactly the same as TC-17-02 default.
