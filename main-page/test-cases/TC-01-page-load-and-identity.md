# Test Cases: TC-01 — Page Load and Identity

**Test Case:** TC-01 (Page Load and Identity)  
**Scope:** https://www.t23b.org/

---

## TC-01-01: Homepage returns successful HTTP status

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Send GET request to `https://www.t23b.org/`. | Response status code is 200 (or 200–299 for success). |

**Automation notes:** HTTP/API check; no browser required. Use HTTP client (e.g., axios, fetch, requests).

---

## TC-01-02: Page title contains Troop 23 and BSA

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/` in browser. | Page loads. |
| 2 | Get document `<title>`. | Title text contains "Troop 23" and "BSA" (or "Boy Scouts of America"). |

**Automation notes:** `document.title` or `driver.getTitle()`; assert substring or regex.

---

## TC-01-03: Main heading (H1) is visible and contains Troop 23

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate the first `h1` element. | Element exists and is displayed. |
| 3 | Get H1 text. | Text contains "Troop 23"; optionally contains "Brooklyn" or "BSA". |

**Automation notes:** Selector `h1` or `[data-testid="main-heading"]` if present. Use visibility check before text assertion.

---

## TC-01-04: No critical console errors on load

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/` with console/network monitoring. | Page loads. |
| 2 | Collect browser console errors (e.g., uncaught exceptions, failed resources). | No errors that prevent above-the-fold content from rendering (or define allowlist of known non-blocking errors). |

**Automation notes:** Browser DevTools protocol or `driver.getLog("browser")`; filter by level "SEVERE" or equivalent. Define policy for acceptable vs critical errors.
