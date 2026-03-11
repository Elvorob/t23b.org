# Main Page — Test Cases

Test cases derived from main page user stories, written for test automation (UI and/or API).

## Naming

- **Folder:** `test-cases` (standard US Agile term).
- **Files:** One file per test case set: `TC-NN-<short-name>.md`.
- **Case ID:** `TC-NN-MM` (e.g., TC-01-01 = first test case in set 01).

## Test Case Format

Each test case includes:

- **ID** — Unique identifier (TC-NN-MM).
- **Title** — Short, actionable summary.
- **Priority** — High / Medium / Low.
- **Preconditions** — State or data required before execution.
- **Steps** — Numbered actions; expected result can be per step or at the end.
- **Expected Result** — What must be true for the test to pass.
- **Automation Notes** — Suggested approach (UI selector, API, viewport, etc.).

## Scope

- **Base URL:** https://www.t23b.org/
- **Page:** Homepage (main page).

## Index

| TC   | Test Case File |
|------|-----------------|
| TC-01 | TC-01-page-load-and-identity.md |
| TC-02 | TC-02-hero-and-featured-event.md |
| TC-03 | TC-03-join-ctas.md |
| TC-04 | TC-04-whats-due-soon.md |
| TC-05 | TC-05-main-content-and-links.md |
| TC-06 | TC-06-what-is-scouting-and-patrol-links.md (covered by TC-05) |
| TC-07 | TC-07-why-choose-troop-23-and-links.md (covered by TC-05) |
| TC-08 | TC-08-new-to-scouting-cta.md (covered by TC-05) |
| TC-09 | TC-09-footer-and-last-updated.md |
| TC-10 | TC-10-responsive-and-ux.md |
| TC-11 | TC-11-accessibility-and-seo.md |
