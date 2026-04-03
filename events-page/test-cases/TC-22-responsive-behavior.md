# Test Cases: TC-22 — Responsive Behavior

**Test Case:** TC-22 (Responsive Behavior)  
**Scope:** https://www.t23b.org/events/

---

## TC-22-01: Desktop layout shows timeline and card/table switcher

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport (width ≥ 992px). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page with viewport 1280×800. | Page loads. |
| 2 | Check `.events-timeline` visibility. | Timeline is visible (has `d-lg-block` but not `d-none` on lg+). |
| 3 | Check view switcher buttons (card / table toggles). | Switcher buttons are visible. |
| 4 | Take screenshot. | Screenshot of desktop layout captured. |

**Automation notes:** Set viewport via `page.set_viewport_size({"width": 1280, "height": 800})`. Use `is_visible()` for assertions.

---

## TC-22-02: Mobile layout hides timeline

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Mobile viewport (width < 992px). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page with viewport 375×812 (iPhone-sized). | Page loads. |
| 2 | Check `.events-timeline` visibility. | Timeline is NOT visible (hidden by Bootstrap `d-none` on small screens). |
| 3 | Check event cards. | Cards are still visible and stacked vertically. |
| 4 | Take screenshot. | Screenshot of mobile layout captured. |

**Automation notes:** Set viewport via `page.set_viewport_size({"width": 375, "height": 812})`. Timeline uses `d-none d-lg-block` — should be hidden below 992px.

---

## TC-22-03: Filter buttons wrap correctly on mobile

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Mobile viewport; events page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate `.filter-category` elements on mobile viewport. | Filter buttons are visible. |
| 2 | Verify all buttons are within the viewport width (no horizontal overflow). | No horizontal scrollbar. Page width equals viewport width. |

**Automation notes:** Use `page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")` to check for overflow. Alternatively check each button's bounding box is within viewport.

---

## TC-22-04: Season navigation visible on mobile

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Mobile viewport; events page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | On mobile viewport, locate season navigation links (prev/next). | Both links are visible. |
| 2 | Check links are tappable (not overlapping, visible bounding box). | Links have positive width and height. |

**Automation notes:** Selector `a.year-nav-prev`, `a.year-nav-next`. Use `bounding_box()` to confirm non-zero dimensions.

---

## TC-22-05: Subscribe to Calendar button visible on mobile

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Mobile viewport; events page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate the Subscribe button (`button[data-bs-target='#icalModal']`). | Button is visible. |
| 2 | Click the button. | Modal opens (`.modal-title` becomes visible). |
| 3 | Take screenshot of modal on mobile. | Screenshot captured. |
| 4 | Close the modal. | Modal closes. |

**Automation notes:** Same flow as TC-15-04 but on mobile viewport. Validates modal works on small screens.

---

## TC-22-06: Tablet viewport — intermediate breakpoint

| Field | Value |
|-------|--------|
| **Priority** | Low |
| **Preconditions** | Tablet viewport (width 768px). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page with viewport 768×1024. | Page loads. |
| 2 | Check timeline visibility. | Timeline is hidden (768 < 992 lg breakpoint). |
| 3 | Check cards layout. | Cards display in a 2-column grid (or similar medium layout). |
| 4 | Take screenshot. | Screenshot of tablet layout captured. |

**Automation notes:** Set viewport 768×1024. Timeline should still be hidden. Card layout may differ from mobile — take screenshot for visual verification.
