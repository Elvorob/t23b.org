# Test Cases: TC-13 — About Us Page

**Test Case:** TC-13 (About Us Page)  
**Scope:** https://www.t23b.org/about-us/

---

## TC-13-01: About Us page returns HTTP 200

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** GET About Us URL; assert status 200 (with retry on timeout).

---

## TC-13-02: All containers have non-empty heading and non-empty text

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Find all content containers (sections or blocks with h1/h2/h3). For each container, assert heading text is non-empty and body text is non-empty.

---

## TC-13-03: Leadership container — Scoutmaster and Scoutmasters on same line

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** In the container whose heading contains "Leadership", find lines containing "Scoutmaster:" and "Scoutmasters:" (or "Assistant Scoutmasters:"). Assert that on each such line there is non-empty text immediately after the label on the same line.

---

## TC-13-04: About the Troop — Troop size and exact season phrase

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** In the container whose heading contains "About" and "Troop": (1) Assert "Troop size:" has non-empty text on the same line. (2) Assert the exact phrase "Scouting season: September to June" is present in the container text.

---

## TC-13-05: Last updated year is current or recent

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Locate the last-updated element; extract a 4-digit year from its text. Assert the year is current year, previous year, or two years ago (e.g. 2026 → allow 2026, 2025, 2024).

---

## TC-13-06: Footer structure and contacts

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Same as homepage: footer exists, at least one section heading (h5), at least one email and one phone, copyright line with year and brand. Use shared `assert_footer_structure_and_contacts_ok` with scope "about-us".

---

## TC-13-07: Top menu visible and has links

| Field | Value |
|-------|--------|
| **Priority** | Medium |

**Steps:** Locate nav or header; assert it is visible and contains at least one link.

---

## TC-13-08: All links and images not broken

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Collect all same-origin links (a[href]) and image URLs (img[src]). For each URL, GET via API; assert 2xx, non-empty body; for HTML, assert structure and non-empty title; for media, 2xx and minimum length. Same logic as main page link check; images are included.

---

## TC-13-09: No critical console errors

| Field | Value |
|-------|--------|
| **Priority** | Medium |

**Steps:** Open About Us, wait for network idle; collect console errors; filter by allowlist (same as main page); assert no blocking errors.

---

## TC-13-10: UX — desktop/mobile viewports and readable text

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Desktop viewport: key sections (H1, Troop Leadership) visible, no horizontal scroll. Mobile viewport: same sections accessible after scroll; body font size at least 12px.

---

## TC-13-11: Navigation from homepage to About Us and back

| Field | Value |
|-------|--------|
| **Priority** | High |

**Steps:** Open homepage; find and click link to About Us (href contains "about-us"); assert URL contains "about-us", take screenshot; go back (or click Home); assert back on homepage, take screenshot.

---

## TC-13-12: Scaling — viewports and no horizontal overflow

| Field | Value |
|-------|--------|
| **Priority** | Medium |

**Steps:** Set viewports (e.g. 1920x1080, 1024x768, 375x667); for each, open About Us and assert H1 visible and body scroll width does not exceed viewport width (within threshold).
