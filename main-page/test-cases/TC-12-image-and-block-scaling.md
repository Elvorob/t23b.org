# Test Cases: TC-12 — Image and Block Scaling on Homepage

**Test Case:** TC-12 (Image and Block Scaling on Homepage)  
**Scope:** https://www.t23b.org/  
**Execution mode:** Manual only (automation is not implemented in this test case yet).  
**Recommended viewport set:**  
- Desktop (3 sizes): 1920x1080, 1366x768, 1024x768.  
- Desktop (optional extended check): 1536x864.  
- Mobile (common coverage): 360x800, 390x844, 393x873 (optional compatibility check: 320x568).

---

## TC-12-01: Desktop window resize — homepage images scale with viewport width

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Open homepage in a desktop browser. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/` at desktop size 1920x1080. | Page loads normally. |
| 2 | Identify visible content images on the homepage (hero image, section images, cards, if present). | Images are visible and rendered correctly. |
| 3 | Switch viewport from 1920x1080 to 1366x768, then to 1024x768, and back to 1920x1080. | Image width/height adapts smoothly at each size; images stay proportional (no distortion), no critical cropping of important content, no overlap with text or controls. |
| 4 | Repeat the same check while increasing and decreasing height (if layout depends on viewport height). | Images remain aligned inside their containers and do not overflow outside section boundaries. |

**Manual evidence to capture:** Screenshots at all three desktop sizes (1920x1080, 1366x768, 1024x768).

---

## TC-12-02: Desktop window resize — homepage content blocks scale and reflow correctly

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage is open in a desktop browser. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Starting from a wide desktop viewport, review key homepage blocks/sections (hero, featured/event block, welcome/content blocks, CTA blocks). | All key blocks are visible and properly aligned. |
| 2 | Switch viewport sizes in this order: 1920x1080 -> 1366x768 -> 1024x768. | Blocks resize and/or reflow to fit available width; no horizontal scrollbar appears due to broken layout; text remains readable and not clipped. |
| 3 | Expand width back to desktop maximum. | Blocks return to wide-layout state without broken spacing, overlap, or hidden content. |
| 4 | Scroll through the full homepage at each of the three desktop sizes. | No block is cut off, collapsed unexpectedly, or rendered outside viewport boundaries. |

**Manual evidence to capture:** Full-page screenshots for each of the three desktop sizes.

---

## TC-12-03: Mobile viewport emulation — images and blocks adapt to narrow screens

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Browser with device emulation is available (DevTools or equivalent). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open homepage and switch to mobile emulation using 360x800, 390x844, and 393x873 (optionally add 320x568 for small-screen compatibility). | Page remains usable in each tested mobile viewport. |
| 2 | Verify homepage images in each viewport while scrolling top to bottom. | Images fit container width, keep aspect ratio, and are not stretched or cut in a way that hides critical content. |
| 3 | Verify key content blocks and CTA areas in each viewport. | Blocks stack/reflow for mobile layout; content remains readable; no overlap between text, images, and buttons/links. |
| 4 | Rotate to landscape mode (if supported by emulation) and repeat quick visual check. | Layout updates correctly for landscape width/height; no broken block structure. |

**Manual evidence to capture:** Screenshots for portrait and landscape at 360x800, 390x844, and 393x873 (plus 320x568 if optional step is executed).

---

## TC-12-04: Real mobile device check — responsive behavior matches expected layout

| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Preconditions** | At least one physical mobile device is available (iOS or Android). |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/` on a real mobile browser. | Homepage loads without layout crash. |
| 2 | Scroll through homepage and inspect images and major blocks. | Images and blocks scale to device width; no horizontal scrolling caused by broken layout. |
| 3 | Rotate device portrait <-> landscape and re-check key sections. | Layout responds to orientation changes; content remains visible and aligned. |
| 4 | Repeat on a second device or browser if possible. | Behavior is consistent across tested mobile environments. |

**Manual evidence to capture:** Device screenshots in portrait and landscape.

---

## Acceptance Criteria

1. Homepage images resize with viewport/device width while preserving visual integrity (no distortion or critical cropping).
2. Homepage blocks/sections resize or reflow according to available screen size without overlap, clipping, or broken alignment.
3. Desktop resize and mobile usage do not introduce horizontal overflow caused by layout defects.
4. Responsive behavior is stable during window resize and orientation changes.
