# Test Cases: TC-14 - Resources Page

**Test Case:** TC-14 (Resources Page)  
**Scope:** https://www.t23b.org/resources/

---

## TC-14-01: Resources page returns HTTP 200

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Send GET request to Resources URL; assert status 200 (with retry on timeout).

---

## TC-14-02: All containers have non-empty heading and non-empty text

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Find content containers (sections or blocks with h1/h2/h3). For each container, assert heading text is non-empty and body text is non-empty.

---

## TC-14-03: Resources content includes expected key topics

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Verify H1 indicates Resources; verify page text includes key topics: library, camping tips/guides, photo archive, and Eagle projects.

---

## TC-14-04: Last updated year is current or recent

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Locate last-updated element; extract year; assert year is current year, previous year, or two years ago.

---

## TC-14-05: Footer structure and contacts

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Same as homepage: footer exists, at least one section heading (h5), at least one email and one phone, and copyright line with year and brand. Use shared `assert_footer_structure_and_contacts_ok` with scope "resources".

---

## TC-14-06: Top menu visible and has links

| Field | Value |
|-------|--------|
| **Priority** | Medium |

**Steps:** Locate nav or header; assert it is visible and contains at least one link; assert a Resources link is present.

---

## TC-14-07: All links and images not broken

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Collect same-origin links (`a[href]`) and image URLs (`img[src]`). For each URL, call API check helper and assert not broken/not empty. For `/events` URLs, allow redirects only when final destination returns 2xx.

---

## TC-14-08: No critical console errors

| Field | Value |
|-------|--------|
| **Priority** | Medium |

**Steps:** Open Resources page and wait for network idle; collect console errors; filter by allowlist (same policy as main page); assert no blocking errors.

---

## TC-14-09: UX - desktop/mobile viewports and readable text

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** On desktop viewport, verify H1/key content visible and no horizontal scroll. On mobile viewport, verify key content remains reachable and body font size is at least 12px.

---

## TC-14-10: Navigation from homepage to Resources and back

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Open homepage; find and click Resources link; verify URL contains `resources`; take screenshot; go back to homepage and verify navigation worked.

---

## TC-14-11: Scaling - viewports and no horizontal overflow

| Field | Value |
|-------|--------|
| **Priority** | Medium |

**Steps:** Set multiple viewports (e.g., 1920x1080, 1024x768, 375x667). For each viewport, open Resources page; assert H1 visible and body scroll width does not exceed viewport width (within threshold).
