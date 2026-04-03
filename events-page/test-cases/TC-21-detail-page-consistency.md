# Test Cases: TC-21 — Event Detail Page Consistency

**Test Case:** TC-21 (Event Detail Page Consistency)  
**Scope:** https://www.t23b.org/events/ → individual event pages

---

## TC-21-01: Clicking event card navigates to event detail page

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loaded in card view; at least one event visible. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click the first visible `.event-card` link. | Browser navigates to a new URL. |
| 2 | Check final URL. | URL contains `/events/` and a slug (not the season listing page). |
| 3 | Page returns HTTP 200 (no 404). | Page content loads. |
| 4 | Take screenshot of event detail page. | Screenshot captured. |
| 5 | Go back to events listing. | Events listing page restored. |

**Automation notes:** Use `page.click()` on the card link. After navigation, assert URL matches pattern `/events/YYYY-YYYY/<slug>/`. Take full-page screenshot. Use `page.go_back(wait_until="domcontentloaded")`.

---

## TC-21-02: Event detail page has an H1 title

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Event detail page loaded from TC-21-01. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate `h1` on the event detail page. | H1 is visible. |
| 2 | Get H1 text. | Text is non-empty. |

**Automation notes:** Selector `h1`. Do not assert specific event name — only that it is present and non-empty.

---

## TC-21-03: Detail page title matches listing card title

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Event listing and detail page accessible. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | On events listing, record the title text from a `.event-card .card-title`. | Title captured. |
| 2 | Click the card to navigate to the detail page. | Detail page loads. |
| 3 | Read H1 text on detail page. | H1 text matches the card title (after whitespace normalization). |
| 4 | Go back to listing. | Listing restored. |

**Automation notes:** Trim and normalize whitespace. Test a sample of events (e.g. first 3) to keep runtime reasonable while catching systemic issues.

---

## TC-21-04: Detail page date matches listing date

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Same sample events as TC-21-03. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | On listing, record the `data-event-date` for a card. | ISO date recorded. |
| 2 | Navigate to detail page. | Detail page loads. |
| 3 | Find a date element on the detail page (search for first parseable date text). | A date is found. |
| 4 | Compare detail page date with listing ISO date. | Dates match (same month, day, year). |
| 5 | Go back. | Listing restored. |

**Automation notes:** The detail page date may be in display format ("July 5-11, 2025") while listing has ISO. Parse both and compare the start date. Use the `_parse_date_to_canonical()` helper from TC-04 experience.

---

## TC-21-05: Detail page has breadcrumb back to events listing

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Event detail page loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate breadcrumb navigation on detail page. | Breadcrumb container is visible. |
| 2 | Find a link in the breadcrumb that points to `/events/`. | Link href contains `/events/`. |
| 3 | Click the breadcrumb link. | Browser navigates back to the events listing page. |
| 4 | Take screenshot. | Screenshot of listing page captured. |

**Automation notes:** Breadcrumb selector may be `.breadcrumb` or `nav[aria-label="breadcrumb"]`. Validate link navigation completes without 404.

---

## TC-21-06: Sample of event detail pages return 200 (no broken links)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events listing loaded. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Collect all unique event URLs from `.event-card` links. | URL list collected. |
| 2 | For each URL (or a sample of up to 10), send an HTTP GET request. | All return status 200. |

**Automation notes:** HTTP-only check; no browser needed for this sub-test. Use `requests.get()` with redirect follow. Log any non-200 responses with URL and status code.
