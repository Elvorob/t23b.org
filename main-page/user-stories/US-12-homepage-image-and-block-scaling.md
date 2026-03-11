# US-12: Homepage Image and Block Scaling

## User Story

**As a** visitor using desktop or mobile devices  
**I want** homepage images and content blocks to scale and reflow correctly when viewport size changes  
**So that** the page remains readable, visually stable, and usable across screen sizes and orientations.

## Acceptance Criteria

- [ ] On desktop, the homepage scales correctly at 1920x1080, 1366x768, and 1024x768.
- [ ] On desktop resize, images preserve aspect ratio and do not appear stretched or critically cropped.
- [ ] On desktop resize, key content blocks reflow without overlap, clipping, or layout breakage.
- [ ] On mobile viewports (360x800, 390x844, 393x873), images and blocks adapt to screen width and remain readable.
- [ ] On mobile portrait and landscape, layout remains stable and key content stays visible and accessible.
- [ ] No horizontal overflow appears due to responsive layout defects in tested desktop/mobile sizes.

## Notes

- Scope: https://www.t23b.org/
- Manual execution only at this stage; automation can be added later.
- Optional extended desktop check: 1536x864.
- Related test case: `main-page/test-cases/TC-12-image-and-block-scaling.md`.
