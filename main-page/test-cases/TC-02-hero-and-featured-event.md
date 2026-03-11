# Test Cases: TC-02 — Hero and Featured Event (Next Big Thing)

**Test Case:** TC-02 (Hero and Featured Event)  
**Scope:** https://www.t23b.org/

---

## TC-02-01: Next Big Thing section is visible

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate section containing text "Next Big Thing". | Element is present and visible. |

**Automation notes:** XPath `//*[contains(text(),'Next Big Thing')]` or CSS by heading/label. Prefer stable id/aria-label if available.

---

## TC-02-02: Featured event name is displayed

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads; "Next Big Thing" section present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Within "Next Big Thing" section, locate event name element. | Event name text is non-empty and displayed. |

**Automation notes:** Content may change (e.g., "Pinewood Derby"); assert presence and non-empty, or match against known list of event names.

---

## TC-02-03: Event date is shown in readable format

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads; "Next Big Thing" section present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Next Big Thing" section, locate date element (e.g., "When:" or date text). | Date text is present and matches a reasonable date format (e.g., contains month and day or ISO date). |

**Automation notes:** Regex for date pattern (e.g., month name + day, or MM/DD/YYYY) to allow dynamic content.

---

## TC-02-04: Event time range is shown

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Homepage loads; "Next Big Thing" section present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Next Big Thing" section, locate time element (e.g., "7:00 pm — 9:00 pm"). | Time or time range text is present and non-empty. |

**Automation notes:** Assert presence; optional regex for time pattern (e.g., \d{1,2}:\d{2}\s*[ap]m).

---

## TC-02-05: Read more link is present and navigates to event page

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads; "Next Big Thing" section present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Next Big Thing" section, locate link with text "Read more" (or equivalent). | Link is present and visible. |
| 2 | Get link `href`. | `href` contains "/events/" (event detail path). |
| 3 | Click the link (or navigate to `href`). | Destination page loads (HTTP 200); URL matches event path. |

**Automation notes:** Selector by link text or `a[href*="/events/"]` within hero. Store `href` and assert URL after navigation.
