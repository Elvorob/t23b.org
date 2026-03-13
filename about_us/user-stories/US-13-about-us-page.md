# US-13: About Us Page

## User Story

**As a** prospective or current scout or parent  
**I want** to visit an About Us page that clearly describes who Troop 23 is, who leads the troop, what the troop does, and how active it is  
**So that** I can quickly understand whether this troop is trustworthy, active, and a good fit for my family.

## Acceptance Criteria

- [ ] The About Us page loads successfully (HTTP 200 or equivalent).
- [ ] The browser title and main heading clearly indicate Boy Scout Troop 23 in Brooklyn, New York.
- [ ] The page states that the troop is located in Bay Ridge, Brooklyn, NY and belongs to Greater New York Councils (Lenape Bay District), with a link to the council site.
- [ ] There is a clearly labeled **Troop Leadership** section.
- [ ] The leadership section contains a line starting with `Scoutmaster:` followed by a non-empty name on the same line.
- [ ] The leadership section contains a line with either `Scoutmasters:` or `Assistant Scoutmasters:` followed by non-empty names on the same line.
- [ ] The Committee Chair is listed by name.
- [ ] There are links to detailed leadership/history information: History, Scoutmasters, awards, and Merit Badge Counselors.
- [ ] There is an **About the Troop** section whose heading contains both “About” and “Troop”.
- [ ] The About the Troop section contains a line starting with `Troop size:` followed by non-empty text on the same line.
- [ ] The About the Troop section contains the exact phrase `Scouting season: September to June`.
- [ ] The About the Troop section mentions Eagle Scouts and Eagle Scout projects and links to their lists.
- [ ] There is a **Camping** section that describes how often the troop camps and that the troop is an active troop.
- [ ] The Camping section lists Alpine Scout Camp, Ten Mile River Scout Camps (TMR), and William H. Pouch Scout Camp / Camp Pouch as campgrounds, each linked to a location page.
- [ ] The Camping section links to a resource page with camping tips or guides.
- [ ] The page displays a “Last updated” label with a human-readable date; the year is current, previous, or two years ago.
- [ ] The page includes a link to a contact-us page for the troop.
- [ ] The global footer with email and phone contact is present and consistent with the homepage.
- [ ] The About Us page is reachable from the main navigation (top menu link).
- [ ] From the About Us page, users can reach key related pages: History, Scoutmasters list, awards, Merit Badge Counselors, Eagle Scouts/Eagle projects, Events, Locations, and Resources.
- [ ] On common desktop viewports, key sections (About Us heading, Troop Leadership, About the Troop, Camping) are visible without horizontal scrolling.
- [ ] On common mobile viewports, the same sections are reachable by vertical scroll and remain readable; body text has a reasonable font size (e.g., at least 12px).

## Notes

- Scope: https://www.t23b.org/about-us/  
- Related automated tests: TC-13 — About Us Page.

### 1. Troop identity and context

- **Branding and heading**
  - The browser title and main heading clearly indicate that this is Boy Scout Troop 23 in Brooklyn, New York.
  - The page content mentions that the troop is located in Bay Ridge, Brooklyn, NY.
- **History and charter**
  - The page briefly states that Troop 23 has a long history and is chartered by Greater New York Councils (Lenape Bay District).
  - There is a link to a dedicated **History** page with more details.
- **Council and district**
  - The page mentions Greater New York Councils and Lenape Bay District and links to the council website.

### 2. Leadership transparency

- **Leadership section**
  - There is a clearly labeled section such as “Troop Leadership”.
  - The section is visually grouped as a single content block (heading plus text).
- **Scoutmaster information**
  - The section contains at least one line that starts with `Scoutmaster:` followed by a non‑empty name on the same line.
- **Assistant Scoutmasters and committee**
  - The section contains a line with either `Scoutmasters:` or `Assistant Scoutmasters:` followed by non‑empty names on the same line.
  - The Committee Chair is listed by name.
- **Related leadership links**
  - There are links to more detailed information about leadership and recognition:
    - Past Scoutmasters,
    - Awards received by people of the troop,
    - Merit badge counselors.

### 3. Troop size and activity level

- **About the Troop section**
  - There is a section with a heading that contains both “About” and “Troop”.
  - This section explains the approximate size of the troop, including number of scouts and patrols.
- **Stable season wording**
  - The section contains the exact phrase `Scouting season: September to June`.
- **Evidence of activity**
  - The section mentions Eagle Scouts and Eagle Scout projects and links to their lists.
  - The section states that the troop is active (for example, mentions service hours or number of events) and links to:
    - Events,
    - Service projects from previous years.

### 4. Camping and locations

- **Camping section**
  - There is a “Camping” section that describes how often the troop camps and that the troop is an “active troop”.
- **Campground links**
  - The Camping section lists the main GNYC campgrounds used by the troop:
    - Alpine Scout Camp,
    - Ten Mile River Scout Camps (TMR),
    - William H. Pouch Scout Camp / Camp Pouch.
  - Each campground name is a link to a more detailed location page on the troop site.
- **Camping guidance**
  - The section links to a resource page with camping tips or guides.

### 5. Freshness and contact

- **Last updated indicator**
  - The page shows a “Last updated” label with a human‑readable date string.
  - The year in this date is reasonably recent (current year, previous year, or two years ago).
- **Contact**
  - The page includes a link to a contact‑us page for the troop.
  - The global footer with troop contact info (email and phone) is present and consistent with the homepage.

### 6. Usability and navigation

- **Navigation to and from About Us**
  - The About Us page is reachable from the main navigation (e.g. top menu link).
  - From About Us, users can navigate to key related pages:
    - History,
    - Scoutmasters list,
    - Awards,
    - Merit badge counselors,
    - Eagle Scouts and Eagle projects,
    - Events and locations,
    - Resources and camping tips.
- **Basic UX and responsiveness**
  - The layout is usable on common desktop and mobile viewports:
    - On desktop, key sections (About Us heading, Troop Leadership, About the Troop, Camping) are visible without horizontal scrolling.
    - On mobile, the same sections are reachable by vertical scroll and remain readable.
  - Body text has a reasonable font size (at least a typical baseline such as 12px).

---

## Traceability to Test Case TC-13

- **TC-13-01** verifies that the About Us URL returns HTTP 200.
- **TC-13-02** verifies that all main content containers have non‑empty headings and text, covering content structure.
- **TC-13-03** and **TC-13-04** verify leadership and “About the Troop” details, including the exact `Scouting season: September to June` phrase and troop size line.
- **TC-13-05** verifies that the “Last updated” year is current or reasonably recent.
- **TC-13-06** verifies footer presence and contact details on the About Us page.
- **TC-13-07** verifies that the top navigation is visible and contains links.
- **TC-13-08** verifies that all same‑origin links and images on About Us are not broken (including special handling of /events redirects).
- **TC-13-09** verifies that there are no unexpected console errors on page load.
- **TC-13-10** verifies UX aspects for desktop and mobile viewports (visibility of key sections and readable text).
- **TC-13-11** verifies navigation from the homepage to About Us and back.
- **TC-13-12** verifies that the page scales across multiple viewport sizes without horizontal overflow while keeping key content visible.

