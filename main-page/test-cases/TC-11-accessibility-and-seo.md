# Test Cases: TC-11 — Accessibility and SEO (Optional)

**Test Case:** TC-11 (Accessibility and SEO)  
**Scope:** https://www.t23b.org/

---

## TC-11-01: Heading hierarchy is logical

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Query all heading elements `h1`–`h6` in document order. | At least one `h1` exists. |
| 2 | Check sequence of heading levels. | No skip in hierarchy (e.g., no h1 → h4 without h2/h3); or document has only h1 and h2/h5 as per design. |

**Automation notes:** Get all `h1..h6`, map to levels, assert no level skip (e.g., level[i+1] <= level[i] + 1). Adjust if design uses h5 under h2.

---

## TC-11-02: Links have descriptive text or accessible names

**Automation:** Disabled in test run until the site implements descriptive link text / accessible names (aria-label, title) for all main links.

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Query main content links (e.g., within main or above footer). | List of links. |
| 2 | For each link, get visible text or aria-label. | No link has only generic text like "click here" or "read more" without context (or allowlist "Read more" / "Learn more" where context is clear). |

**Automation notes:** Optional: flag links with text length &lt; 3 or exact match "click here"; allowlist known CTAs.

---

## TC-11-03: Images in main content have alt text or are decorative

**Automation:** Disabled in test run until the site adds `alt` attributes to all images in main content (meaningful or empty for decorative).

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Query `img` elements in main content. | List of images. |
| 2 | For each image, check `alt` attribute. | Each image has `alt` present: either non-empty (meaningful) or empty string `alt=""` (decorative). |

**Automation notes:** `img[alt]` or assert no `img` without `alt` in scope. Empty `alt=""` is valid for decorative images.

---

## TC-11-04: Page has meaningful title and meta description for SEO

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Get `<title>` text. | Non-empty; contains "Troop 23" or key brand term. |
| 2 | Get `<meta name="description" content="...">`. | Meta description exists and is non-empty (length &gt; 0). |

**Automation notes:** `document.title`; query `meta[name="description"]` and get `content`. Optional: length in range 50–160 chars.

---

## TC-11-05: Keyboard navigation reaches main links and CTAs (optional)

| Field | Value |
|-------|--------|
| **Priority** | Low |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Focus page body; tab through focusable elements. | Focus moves through interactive elements (links, buttons). |
| 2 | Tab until "Read more" or "Learn more" receives focus. | At least one main CTA is focusable and reachable by keyboard. |

**Automation notes:** Use keyboard driver (Tab, Enter); or check `tabIndex` and non-disabled focusable elements. Can be expanded in dedicated a11y suite.
