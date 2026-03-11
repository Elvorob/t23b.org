# Test Cases: TC-10 — Responsive and Basic UX

**Test Case:** TC-10 (Responsive and Basic UX)  
**Scope:** https://www.t23b.org/

**Viewports (suggested):** Desktop 1280×720 (or 1024×768); Mobile 375×667 (or 320×568). Adjust in automation config.

---

## TC-10-01: Desktop viewport — key sections visible without horizontal scroll

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Set viewport to desktop (e.g., width 1024px or 1280px). | Viewport is set. |
| 2 | Open `https://www.t23b.org/`. | Page loads. |
| 3 | Check that main sections (e.g., H1, Next Big Thing, Welcome) are visible. | All key sections are in view; no required horizontal scroll (or scroll width equals body width). |
| 4 | Optionally measure body/document scroll width. | Scroll width ≤ viewport width (or within acceptable threshold). |

**Automation notes:** Resize window or use device emulation; assert visibility of section landmarks; optional `document.body.scrollWidth <= viewportWidth`.

---

## TC-10-02: Mobile viewport — page readable and key sections accessible

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Set viewport to mobile (e.g., 375×667). | Viewport is set. |
| 2 | Open `https://www.t23b.org/`. | Page loads. |
| 3 | Verify H1 and at least "Next Big Thing" and "Welcome to Troop 23" are present and visible (after scroll if needed). | Key content is present and not permanently hidden or cut off. |

**Automation notes:** Same as desktop; use scroll into view if needed before assertion.

---

## TC-10-03: Primary CTAs (Read more, Learn more) are clickable

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads in any viewport. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate at least one "Read more" link and one "Learn more" link. | Elements are present. |
| 2 | Assert each is displayed and not disabled. | `display` not none; element is enabled. |
| 3 | Click "Read more" (or first instance). | Navigation occurs or event detail page loads. |
| 4 | Return to homepage; click "Learn more" (or first instance). | Navigation occurs or How to Join (or target) loads. |

**Automation notes:** Use `isDisplayed()` and `isEnabled()`; click and assert URL change or new page load.

---

## TC-10-04: No permanent overlay blocking main content or CTAs

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Wait for page load (and optional dismiss of cookie/modal if applicable). | Page in steady state. |
| 2 | Locate main content container and primary CTA links. | Elements are present. |
| 3 | Check that no fixed/full-screen overlay covers main content or CTAs (or overlay is dismissible). | Main H1 and at least one CTA are clickable/visible. |

**Automation notes:** Optional; check `position: fixed` overlays and z-index, or assert clickability of key elements.

---

## TC-10-05: Text is readable in desktop and mobile viewports

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | None. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load homepage at desktop viewport; get computed font-size of body or main content. | Font size is at least 12px (or project standard). |
| 2 | Load homepage at mobile viewport; get computed font-size. | Font size is at least 12px (or project standard); no critical text at &lt;10px. |

**Automation notes:** Get computed style `fontSize`; optional contrast check via a11y APIs if needed.
