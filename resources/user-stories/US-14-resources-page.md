# US-14: Resources Page

## User Story

**As a** scout, parent, or troop volunteer  
**I want** the Resources page to provide clear, working links to key troop materials and reference pages  
**So that** I can quickly find information and use it without broken links or confusing navigation.

## Acceptance Criteria

- [ ] The Resources page loads successfully (HTTP 200 or equivalent).
- [ ] The browser title and main heading clearly indicate this is the Resources page for Troop 23.
- [ ] The page has at least one visible content container with a non-empty heading and non-empty text.
- [ ] The page content includes key resource topics such as library, camping tips/guides, photo archive, and Eagle projects.
- [ ] The page contains a visible "Last updated" indicator with a year.
- [ ] The year in "Last updated" is current year, previous year, or two years ago.
- [ ] The top menu (nav/header) is visible and contains links, including a Resources link.
- [ ] The footer is present and contains at least one section heading, email and phone contact, and a copyright line.
- [ ] All same-origin links (`a[href]`) on the Resources page are not broken and not empty by API checks.
- [ ] All same-origin image URLs (`img[src]`) on the Resources page are not broken and not empty by API checks.
- [ ] Redirects for `/events` links are accepted only if the final destination returns 2xx.
- [ ] No critical console errors appear on page load (allowlist policy same as main page).
- [ ] On desktop viewport, key content is visible and horizontal scrolling is not required.
- [ ] On mobile viewport, key content remains reachable/readable and body font size is at least 12px.
- [ ] Navigation from homepage to Resources and back to homepage works.
- [ ] Across multiple viewports (desktop/tablet/mobile), key content remains visible and no horizontal overflow appears.

## Notes

- Scope: https://www.t23b.org/resources/  
- Related automated tests: TC-14 - Resources Page.
