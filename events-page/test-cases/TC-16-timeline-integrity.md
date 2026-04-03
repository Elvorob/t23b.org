# Test Cases: TC-16 — Events Timeline Integrity (Desktop)

**Test Case:** TC-16 (Events Timeline Integrity)  
**Scope:** https://www.t23b.org/events/

---

## TC-16-01: Timeline is visible on desktop viewport

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport (>= 992px width). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page on desktop viewport. | Page loads. |
| 2 | Locate `.events-timeline` container. | Container is visible (not hidden by `d-none`). |

**Automation notes:** Set viewport to 1280x800. Selector `.events-timeline`. The element has `d-none d-lg-block` classes — visible only at lg+ breakpoint.

---

## TC-16-02: All 12 months are present in correct order

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport; events page loaded; timeline visible. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Collect all `.events-timeline-month-header` elements. | Exactly 12 elements found. |
| 2 | Read text from each header. | Texts are: Sep, Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug — in that order. |

**Automation notes:** Selector `.events-timeline-month-header`. Compare extracted list with expected school-year month order.

---

## TC-16-03: Timeline events have required data attributes

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Desktop viewport; timeline visible. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Collect all `.events-timeline-event` elements. | At least 1 event found. |
| 2 | For each event, read `data-event-id`. | Non-empty string (UUID format). |
| 3 | For each event, read `data-event-start`. | Valid ISO date (YYYY-MM-DD). |
| 4 | For each event, read `data-event-end`. | Valid ISO date (YYYY-MM-DD). |
| 5 | For each event, read `data-event-categories`. | String present (may be empty for uncategorized events). |
| 6 | For each event, read `data-event-status`. | One of: `confirmed`, `postponed`, `tentative`, `cancelled`. |

**Automation notes:** Iterate all timeline event elements. Parse dates with `datetime.strptime`. Log each event's attributes for debugging.

---

## TC-16-04: Start date is not after end date for all events

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Timeline events collected with data attributes. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each timeline event, parse `data-event-start` and `data-event-end`. | Both parse as valid dates. |
| 2 | Compare start and end. | `start_date <= end_date` for every event. |

**Automation notes:** Fail with event title and dates if any violation found.

---

## TC-16-05: Timeline events are clickable links to event pages

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Timeline visible; events present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `.events-timeline-event`, check tag name. | Element is `<a>`. |
| 2 | Get `href` attribute. | href contains `/events/`. |

**Automation notes:** Selector `.events-timeline-event`. Check `tag_name` property and href substring.

---

## TC-16-06: Overview count matches timeline event count

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Desktop viewport; timeline visible; no filters active. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the number N from "Overview (N)" heading text. | N is a positive integer. |
| 2 | Count all `.events-timeline-event` elements in the DOM. | Count equals N. |
| 3 | Log which events (if any) have `data-hidden="true"` or `data-dimmed="true"`. | Informational — no assertion on hidden/dimmed count. |

**Automation notes:** Parse N from heading text using regex `\((\d+)\)`. The Overview count represents total events including hidden/dimmed. Verify on real DOM before hardcoding expectations about visibility states.
