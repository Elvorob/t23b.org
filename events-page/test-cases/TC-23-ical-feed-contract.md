# Test Cases: TC-23 — iCal Feed Contract

**Test Case:** TC-23 (iCal Feed Contract)  
**Scope:** https://www.t23b.org/events.ics and https://www.t23b.org/events/

---

## TC-23-01: iCal feed returns valid VCALENDAR response

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Send GET request to `https://www.t23b.org/events.ics`. | HTTP status 200. |
| 2 | Check `Content-Type` header. | Contains `text/calendar`. |
| 3 | Check response body starts with `BEGIN:VCALENDAR`. | True. |
| 4 | Check response body ends with `END:VCALENDAR`. | True. |
| 5 | Body is not empty (length > 100 bytes). | True. |

**Automation notes:** HTTP-only test; no browser. Use `requests.get()`. Strip trailing whitespace from body before checking `END:VCALENDAR`.

---

## TC-23-02: iCal feed is not empty — contains at least one VEVENT

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | iCal response from TC-23-01. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Count occurrences of `BEGIN:VEVENT` in the iCal body. | Count ≥ 1. |
| 2 | Count occurrences of `END:VEVENT`. | Count equals `BEGIN:VEVENT` count (all events properly closed). |

**Automation notes:** Simple string count. Log the total VEVENT count for informational purposes.

---

## TC-23-03: Each VEVENT has required fields

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | iCal parsed. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Parse each VEVENT block. | All blocks extracted. |
| 2 | For each VEVENT, check presence of: `SUMMARY`, `DTSTART`, `DTEND`, `UID`, `URL`. | All five fields present in every VEVENT. |
| 3 | For each, check `STATUS` field. | `STATUS` is one of: `CONFIRMED`, `TENTATIVE`, `CANCELLED`. |

**Automation notes:** Parse iCal manually (split by `BEGIN:VEVENT` / `END:VEVENT`, then extract fields with regex). Do not use icalendar library to avoid adding a dependency.

---

## TC-23-04: VEVENT dates are valid and start ≤ end

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | VEVENTs parsed from TC-23-03. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each VEVENT, parse `DTSTART` and `DTEND` as dates. | Both parse successfully (format `YYYYMMDD` or `YYYYMMDDTHHmmssZ`). |
| 2 | Compare start and end. | `DTSTART <= DTEND`. |

**Automation notes:** Handle both all-day events (`VALUE=DATE:YYYYMMDD`) and timed events (`YYYYMMDDTHHMMSSZ`). For UTC timestamps, convert to `America/New_York` before date comparison if needed.

---

## TC-23-05: VEVENT URLs point to valid event pages

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | VEVENTs parsed. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each VEVENT, extract `URL` field. | URL is non-empty. |
| 2 | URL contains `/events/`. | True. |
| 3 | For a sample of URLs (up to 5), send HTTP GET request. | All return status 200. |

**Automation notes:** HTTP-only validation. Log any non-200 responses with VEVENT SUMMARY and URL.

---

## TC-23-06: iCal event count matches website event count

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | iCal parsed; events page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Count VEVENTs in iCal feed. | N_ical. |
| 2 | Count `.event-card` elements on the events page. | N_page. |
| 3 | Compare. | N_ical == N_page, OR log the difference. |

**Automation notes:** The counts may differ if the iCal feed includes events from all seasons while the page shows only the current season. If counts differ, log both counts and the event lists for analysis — use a soft assertion (warning, not failure) unless the difference is confirmed to be a bug.

---

## TC-23-07: iCal event titles match website event titles

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Both iCal and page events collected. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each VEVENT, extract `SUMMARY` field (event title). | Title list from iCal. |
| 2 | For each `.event-card`, extract `.card-title` text. | Title list from page. |
| 3 | Match by URL slug or title text. | All page titles have a corresponding iCal SUMMARY. |
| 4 | Log any titles present in iCal but not on the page (could be other seasons). | Informational. |

**Automation notes:** Normalize titles (strip whitespace, lowercase) before comparison. Match using the event URL as the key (extract slug from both VEVENT URL and card href). Titles may have minor formatting differences — use fuzzy matching or slug-based matching as primary strategy.

---

## TC-23-08: iCal event dates match website ISO dates

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events matched between iCal and page (by URL slug). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each matched event, extract `DTSTART` from iCal and `data-event-date` from the page. | Both dates obtained. |
| 2 | Convert iCal `DTSTART` to `YYYY-MM-DD` (handling UTC → Eastern if needed). | Conversion succeeds. |
| 3 | Compare: iCal start date == page ISO date. | Dates match. |

**Automation notes:** Critical test for date consistency between iCal feed and website. UTC timestamps like `20250705T040000Z` convert to `2025-07-05` in Eastern time. Use `pytz` or `zoneinfo` for conversion. This test directly catches the timezone drift bug where iCal shows a different day than the website.

---

## TC-23-09: Leading zeros consistency in iCal dates

| Field | Value |
|-------|--------|
| **Priority** | Low |
| **Preconditions** | VEVENTs parsed. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each VEVENT, extract raw `DTSTART` string. | String obtained. |
| 2 | Verify format matches `YYYYMMDD` or `YYYYMMDDTHHmmssZ` exactly (8 or 16 chars). | Format matches — no missing leading zeros. |

**Automation notes:** Soft check — log inconsistencies but do not fail. Leading zero issues in iCal dates are cosmetic in most clients but could signal backend formatting bugs.
