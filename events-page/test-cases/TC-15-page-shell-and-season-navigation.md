# Test Cases: TC-15 — Page Shell and Season Navigation

**Test Case:** TC-15 (Page Shell and Season Navigation)  
**Scope:** https://www.t23b.org/events/

---

## TC-15-01: Events page loads and redirects to current season

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Send GET request to `https://www.t23b.org/events/` with redirect follow. | Response status code is 200. |
| 2 | Check final URL. | Final URL matches pattern `/events/YYYY-YYYY/` (e.g. `/events/2025-2026/`). |

**Automation notes:** HTTP-only check; no browser required. Use `requests.get()` with `allow_redirects=True`. Assert status 200 and regex on final URL.

---

## TC-15-02: Season title is displayed in H1

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/events/` in browser. | Page redirects and loads. |
| 2 | Locate the first `<h1>` element. | H1 is visible. |
| 3 | Get H1 text. | Text matches pattern `YYYY-YYYY` (e.g. "2025-2026"). |

**Automation notes:** Navigate, wait for URL to match season pattern. Selector `h1`; regex `\d{4}-\d{4}`.

---

## TC-15-03: Subscribe to Calendar button is visible

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Events page loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page. | Page loads. |
| 2 | Locate button with `data-bs-target="#icalModal"`. | Button is visible and contains calendar icon. |

**Automation notes:** Selector `button[data-bs-target='#icalModal']`. Assert visibility and non-empty text.

---

## TC-15-04: iCal modal opens and contains calendar URL

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loads; all scripts loaded (use `networkidle`). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page with `wait_until="networkidle"`. | Page loads with Bootstrap JS initialized. |
| 2 | Click "Subscribe to Calendar" button. | Modal dialog appears. |
| 3 | Check modal title. | Title contains "Subscribe" or "Calendar". |
| 4 | Locate `#calendar-url` input. | Input is visible; its `value` ends with `events.ics`. |
| 5 | Take screenshot of the modal. | Screenshot captured. |
| 6 | Click "Close" button in modal. | Modal disappears. |

**Automation notes:** Wait for `.modal-title` to become visible after click (Bootstrap animation). Use `wait_for(state="visible")` instead of `expect().to_be_visible()` for reliability with Cloudflare Rocket Loader deferred scripts.

---

## TC-15-05: Previous season navigation link is valid

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Events page loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page. | Page loads. |
| 2 | Locate `a.year-nav-prev` link. | Link is visible. |
| 3 | Get link `href`. | href matches pattern `/events/YYYY-YYYY/`. |
| 4 | Get link text. | Text contains a 4-digit year. |

**Automation notes:** Selector `a.year-nav-prev`. The link text uses em-dashes (e.g. "2024—2025") while the href uses hyphens.

---

## TC-15-06: Next season navigation link is valid

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Events page loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page. | Page loads. |
| 2 | Locate `a.year-nav-next` link. | Link is visible. |
| 3 | Get link `href`. | href matches pattern `/events/YYYY-YYYY/`. |
| 4 | Get link text. | Text contains a 4-digit year. |

**Automation notes:** Selector `a.year-nav-next`. Same approach as TC-15-05.

---

## TC-15-07: Navigate to previous season page

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loads; previous season link present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page. Record current season from URL. | Current season noted. |
| 2 | Click previous season link. Wait for page load. | URL changes to previous season path. |
| 3 | Check H1 on the new page. | H1 contains the previous season (e.g. "2024-2025"). |
| 4 | Take screenshot. | Screenshot of previous season page captured. |

**Automation notes:** Extract expected season from link `href` before clicking. Compare URL and H1 after navigation.

---

## TC-15-08: Navigate to next season page

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Events page loads; next season link present. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page. Record current season from URL. | Current season noted. |
| 2 | Click next season link. Wait for page load. | URL changes to next season path. |
| 3 | Check H1 on the new page. | H1 contains the next season, OR page returns 404 if the season is not yet created. |
| 4 | Take screenshot. | Screenshot of next season page captured. |

**Automation notes:** Next season page may not exist yet (404). Handle gracefully: if H1 contains "404" or "Not Found", log as informational note (season not yet created), do not fail. The test validates that the link is functional and URL is correct.

---

## TC-15-09: No critical console errors on events page

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open events page with console monitoring, wait for `networkidle`. | Page loads. |
| 2 | Collect browser console errors. | No errors that are outside the allowlist (cookie, tracking, analytics, etc.). |

**Automation notes:** Attach console listener before navigation. Filter errors against allowlist from `console_allowlist.txt`. Assert no blocking errors remain.
