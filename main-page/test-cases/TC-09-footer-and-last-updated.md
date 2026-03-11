# Test Cases: TC-09 — Footer and Last Updated

**Test Case:** TC-09 (Footer and Last Updated)  
**Scope:** https://www.t23b.org/

---

## TC-09-01: Last updated indicator is visible

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate element containing "Last updated" (or equivalent). | Element is present and visible. |

**Automation notes:** XPath `//*[contains(text(),'Last updated')]` or similar; case-insensitive if needed.

---

## TC-09-02: Last updated date is in valid format

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | "Last updated" element present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Get text of "Last updated" element (e.g., full string "Last updated on May 07, 2025"). | Text contains a date pattern: month (name or number), day, year (e.g., MMM DD, YYYY or MM/DD/YYYY). |

**Automation notes:** Regex for date (e.g., month name + day + year, or \d{1,2}/\d{1,2}/\d{4}). Do not assert fixed date value.

---

## TC-09-03: Last updated date is non-empty and readable

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | "Last updated" element present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Get date portion of "Last updated" text. | Date substring is non-empty and has at least 5 characters (e.g., "May 07" or "05/07/2025"). |

**Automation notes:** Trivial sanity check; can be merged with TC-09-02.
