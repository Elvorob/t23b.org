# Test Cases: TC-18 — Cross-View Consistency (Cards, Table, Timeline)

**Test Case:** TC-18 (Cross-View Consistency)  
**Scope:** https://www.t23b.org/events/

---

## TC-18-01: Collect event models from timeline

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport; events page loaded; no filters active. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `.events-timeline-event`, extract `data-event-id`, `data-event-title` (from `title` attribute), `data-event-start`, `href`. | All events collected into a dict keyed by `data-event-id`. |

**Automation notes:** Use `get_event_model_from_timeline()` helper. The `title` HTML attribute contains event name and categories in format "Name (Cat1, Cat2)".

---

## TC-18-02: Collect event models from cards

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Card view active (default). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `.event-card`, extract `data-event-id`, `.card-title` inner text, `data-event-date`, `data-href`. | All cards collected into a dict keyed by `data-event-id`. |

**Automation notes:** Use `get_event_model_from_card()` helper. Trim whitespace from title text.

---

## TC-18-03: Collect event models from table

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Switch to table view by clicking the table toggle button. | Table view becomes visible. |
| 2 | For each `.event-row`, extract `data-event-id`, `.event-title-link` inner text, `data-event-date`, link href. | All rows collected into a dict keyed by `data-event-id`. |

**Automation notes:** Use `get_event_model_from_table_row()` helper. Skip the `.event-table-divider` row (past events separator).

---

## TC-18-04: Event count matches across all three views

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Models collected from TC-18-01, TC-18-02, TC-18-03. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Compare counts: timeline events, cards, table rows. | All three counts are equal. |

**Automation notes:** If counts differ, log which event IDs are missing from which view.

---

## TC-18-05: Title consistency across views

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Models collected. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `data-event-id`, compare title from timeline, card, and table. | Titles match after trim and whitespace normalization. |

**Automation notes:** Timeline title is extracted from the `title` attribute which includes categories (e.g. "Summer Camp (Camping, Advancement)") — extract only the name part before the parenthesis. Use `assert_event_consistency()` helper.

---

## TC-18-06: Start date consistency across views

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Models collected. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `data-event-id`, compare: timeline `data-event-start` = card `data-event-date` = table `data-event-date`. | All three start dates match. |

**Automation notes:** All values are ISO date strings (YYYY-MM-DD). Direct string comparison is sufficient.

---

## TC-18-07: URL consistency across views

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Models collected. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `data-event-id`, compare URLs from timeline (`href`), card (`data-href`), table (link `href`). | All three URLs point to the same event detail path after normalizing trailing slashes. |

**Automation notes:** Use `normalize_url()` helper. URLs may differ by trailing slash or scheme — normalize before comparison.
