# Test Cases: TC-04 — What's Due Soon

**Test Case:** TC-04 (What's Due Soon)  
**Scope:** https://www.t23b.org/

---

## TC-04-01: What's Due Soon section is visible

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate section containing text "What's Due Soon". | Element is present and visible. |

**Automation notes:** XPath or CSS by text content; prefer stable container id/class if available.

---

## TC-04-02: At least one due-soon item is displayed

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads; "What's Due Soon" section present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "What's Due Soon" section, locate due items (rows/cards) with event name and due link. | At least one due item (row/card with link to an event) is present and visible. |

**Automation notes:** Select by table/list structure inside the section; assert that at least one row has an event name and a link to `/events/...`.

---

## TC-04-03: Due-soon items correspond to event pages (names)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | "What's Due Soon" section has at least one due item with link to an event. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each due item, read the event name from the second column (e.g., "Summer Camp", "Bear Mountain Day Hike"). | Event name text is non-empty. |
| 2 | Click the due link for that item to open the event page. | Event page loads (HTTP 200). |
| 3 | On the event page, get the main event title (H1). | H1 title contains the key words from the due item event name (case-insensitive substring/word match). |

**Automation notes:** For each due item, compare event name from the "What's Due Soon" row with the event page title by lowercasing and checking word overlap (ignore very short words).

---

## TC-04-04: Due-soon items correspond to event pages (nearest date name)

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | "What's Due Soon" section has at least one due item with link to an event. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each due item, read the nearest-date name from the first text column (e.g., "Deposit Fee", "RSVP"). | Nearest-date name text is non-empty. |
| 2 | Click the due link for that item to open the event page. | Event page loads (HTTP 200). |
| 3 | On the event page, locate the sub-section for that nearest-date name (e.g., "💲 Deposit Fee", "🙋🏻‍♂️ RSVP"). | Matching sub-section exists and is visible; its heading contains the same nearest-date name text as in the due item. |

**Automation notes:** Use text match for the nearest-date name to locate the corresponding sub-block on the event page (heading + its container), and assert name equality (case-insensitive).

---

## TC-04-05: Due-soon dates match event page dates

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | "What's Due Soon" section has at least one due item with link to an event and nearest-date name. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each due item, read the due date text in the due column (e.g., "Feb 28 3d ago", "Mar 22 in 2w"). | Due date text contains a readable date (month+day or similar). |
| 2 | Click the due link for that item to open the event page. | Event page loads (HTTP 200). |
| 3 | On the event page, in the sub-section for the nearest-date name (from TC-04-04), get the "When:" date text. | "When:" text contains a date. |
| 4 | Compare the date from the due item with the date from the event page sub-section. | Dates match (after normalizing format, e.g., both map to the same calendar date). |

**Automation notes:** Extract date fragments from both the due item text and the event page "When:" text using a regex or date parser, normalize them (e.g., `Feb 28` vs `02/28/2026`), and assert they represent the same date. Log both values in the automation report so mismatches are easy to debug.
