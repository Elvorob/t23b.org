# Test Cases: TC-19 — Date Model Validation

**Test Case:** TC-19 (Date Model Validation)  
**Scope:** https://www.t23b.org/events/

---

## TC-19-01: All display dates parse successfully to known formats

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded in card view. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `.event-card`, extract the visible date text from the date label (e.g. `.card-text` element containing the date). | All cards have a non-empty date string. |
| 2 | Attempt to parse each display date against known format patterns: `Month DD, YYYY`, `Month DD-DD, YYYY`, `Q[1-4] YYYY (tentative)`, `Week of Month DD, YYYY (tentative)`. | Each date matches at least one pattern. |
| 3 | Log all successfully parsed dates and their format. | Informational for debugging. |

**Automation notes:** Maintain a list of regex patterns for accepted date formats. Use a `_parse_display_date()` helper that returns the canonical date or raises on failure. Log each card's event name alongside its parsed date for traceability.

---

## TC-19-02: ISO data-attribute dates are valid

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each `.event-card`, read `data-event-date` attribute. | Non-empty ISO date string (YYYY-MM-DD). |
| 2 | Parse each as a date object. | All parse successfully. |
| 3 | For each `.events-timeline-event`, read `data-event-start` and `data-event-end`. | Both are valid ISO dates. |

**Automation notes:** Use `datetime.strptime(value, "%Y-%m-%d")`. Fail with event ID and raw value if any parse error.

---

## TC-19-03: Display date is consistent with ISO data attribute

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events with both display date and ISO `data-event-date`. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each event card, extract displayed date text and `data-event-date` ISO value. | Both collected. |
| 2 | Parse display date to extract month, day, year. | Parse succeeds. |
| 3 | Compare: the month and year from display date must match the ISO date. Day must match start day. | No mismatches found. |

**Automation notes:** For multi-day events (e.g. "July 5-11, 2025"), the display start day should match the ISO date day. For tentative events ("Q1 2025" or "Week of ..."), validate that the ISO date falls within the described range. Log mismatches as failures with full context.

---

## TC-19-04: No single-day event has start ≠ end

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Timeline visible with data attributes. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each event with a display date showing a single day (e.g. "March 15, 2025"), check `data-event-start` and `data-event-end`. | start == end for single-day display dates. |

**Automation notes:** Parse display date; if no range separator (dash) exists, it is a single-day event. Compare ISO start and end — they should be equal.

---

## TC-19-05: Multi-day events have correct date span

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Timeline visible; multi-day events present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each event whose display date contains a range (e.g. "July 5-11, 2025"), parse start and end days. | start_day < end_day. |
| 2 | Compute expected span: end_day - start_day + 1. | Span is ≥ 2 days. |
| 3 | Compare with `data-event-start` and `data-event-end`. | ISO start = first day of range. ISO end = last day of range. |

**Automation notes:** Handle cross-month ranges (rare but possible, e.g. "June 28 - July 3, 2025") by parsing both dates fully.

---

## TC-19-06: No date has drifted day (off-by-one detection)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events collected with both display dates and ISO dates. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each event, compute absolute difference between display date and ISO date. | Difference is 0 days (exact match). |
| 2 | If difference is ±1 day, log as WARNING (possible timezone conversion drift). | No ±1 day drifts found. |

**Automation notes:** This is the key regression test for date conversion bugs. Timezone conversions (UTC → America/New_York) can shift a date to the previous or next day. Any non-zero difference should be flagged. Log the event name, display date, ISO date, and delta for any mismatch.
