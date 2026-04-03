# Test Cases: TC-20 — Upcoming vs Past Events Partition

**Test Case:** TC-20 (Upcoming vs Past Events Partition)  
**Scope:** https://www.t23b.org/events/

---

## TC-20-01: Past events divider exists in table view

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded in table view. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Switch to table view. | Table view visible. |
| 2 | Locate `.event-table-divider` row. | Divider row found with text like "Past Events". |

**Automation notes:** Selector `.event-table-divider`. Exact text may vary — assert non-empty text.

---

## TC-20-02: All events above divider are upcoming (date >= today)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Table view with divider. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Collect all `.event-row` elements before the `.event-table-divider`. | At least 0 rows (could be 0 if season is fully past). |
| 2 | For each, read `data-event-date`. | Date is today or in the future. |

**Automation notes:** Use timezone-aware comparison with `America/New_York` to avoid midnight edge cases. The server uses Eastern time for the upcoming/past split.

---

## TC-20-03: All events below divider are past (date < today)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Table view with divider. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Collect all `.event-row` elements after the `.event-table-divider`. | At least 0 rows. |
| 2 | For each, read `data-event-date`. | Date is before today. |

**Automation notes:** Same timezone handling as TC-20-02.

---

## TC-20-04: Invariant — max(past dates) < min(upcoming dates)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Both past and upcoming events present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Collect all past event ISO dates. Find the maximum (most recent past). | A date is found. |
| 2 | Collect all upcoming event ISO dates. Find the minimum (soonest upcoming). | A date is found. |
| 3 | Compare: max(past) < min(upcoming). | Invariant holds. |

**Automation notes:** This is a robust, timezone-independent check. If violated, past and upcoming are incorrectly partitioned. Skip if either partition is empty (beginning or end of season).

---

## TC-20-05: Card view applies dimming/opacity to past events

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Card view active; past events present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each event card with a past `data-event-date`, check computed CSS `opacity` or presence of a `.past-event` or dimming class. | Past cards have reduced opacity or a specific class indicator. |
| 2 | For each upcoming event card, check the same. | Upcoming cards have full opacity (1.0) or no dimming class. |

**Automation notes:** Verify on real DOM first — the exact dimming mechanism may be via Alpine.js `:class` binding or inline style. Log findings before creating hard assertions. Use `page.evaluate()` to read `getComputedStyle().opacity` if class-based detection is insufficient.
