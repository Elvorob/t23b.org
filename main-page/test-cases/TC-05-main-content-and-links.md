# Test Cases: TC-05 — Main Content and Links

**Test Case:** TC-05 (Main content and links)  
**Scope:** https://www.t23b.org/

Covers the main text block (Welcome, What is Scouting, Why Choose, New to Scouting) as one area and all homepage links.

---

## TC-05-01: Main content is visible and has text; links in it are visually recognizable

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate the main content area (e.g. `<main>` or central content container). | Element is present and visible. |
| 3 | Get text of that area. | Text is non-empty. |
| 4 | For each link inside the main content, check computed style. | Every link is visually recognizable as a link (different color from body text or underlined). |

**Automation notes:** Use `main` if present, else a container that includes the main text blocks. No per-section split; one block, one check. Link visibility: same logic as before (color vs section color, or underline).

---

## TC-05-02: All links on homepage are non-empty, clickable, and each destination has a full-page screenshot

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Find all links (`a[href]`) on the page; filter to same-origin, non-empty, non-mailto/tel. | List of links. |
| 3 | For each unique URL: navigate, take full-page screenshot, return to homepage. | One screenshot per link destination in the results folder. |

**Automation notes:** Deduplicate by URL; skip external/mailto/tel. Full-page screenshot per destination.
