# Homepage Analysis & User Story Topics for Testing

**Page:** https://www.t23b.org/  
**Purpose:** Content and element analysis to derive testable user story topics.

---

## 1. Content Overview

| Section | Description |
|--------|-------------|
| **Page title / meta** | Troop 23, Bay Ridge, Brooklyn, New York, Boy Scouts of America, BSA |
| **Hero (H1)** | "Troop 23, Brooklyn, New York, Boy Scouts of America, BSA" |
| **Next Big Thing** | Featured event (e.g. Pinewood Derby) with date, time, "Read more" link |
| **Join CTAs** | Two blocks: "Become a Boy Scout" and "Become a Cub Scout" with contact (name, email, phone) and "Learn more" link |
| **What's Due Soon** | Upcoming deadlines (e.g. deposit fee, Summer Camp) with date and link to event |
| **Welcome to Troop 23** | Intro text, history, diversity, service hours, meeting time/place, links to History, Trips, community service, Our Lady of Angels Church, About Us |
| **What is Scouting?** | Explanation of scouting, Scout Oath/Law, Patrol Method; links to Patrols, Patrol Scoring |
| **Why Choose Troop 23?** | Value propositions: patrol leadership, scoring, advancement, merit badges, Eagle Scouts, Procedures, outdoor activities, 50 Miler; multiple internal links |
| **New to Scouting?** | CTA to join/transfer; links to How to Join, Advancements, What is Scouting? |
| **Footer** | "Last updated on [date]" |

---

## 2. Key UI Elements

- **Headings:** H1 (main title), H2 (section titles), H5 ("Next Big Thing", "What's Due Soon")
- **Links:** Internal navigation (events, about-us, locations, patrols, procedures, advancements, etc.)
- **Contact elements:** Email (possibly obfuscated), phone numbers
- **Event block:** Event name, date, time range, "Read more" CTA
- **Due-soon block:** Table/card with icon, label, event name, deadline text, link
- **CTA buttons/links:** "Read more", "Learn more" (repeated in several sections)

---

## 3. Suggested User Story Topics for Testing

### 3.1 Page load & identity
- **US:** As a visitor, I want the homepage to load and show the correct title and Troop 23 branding so that I know I am on the right site.
- **Topics:** Page load, title/meta, main H1 visible and correct.

### 3.2 Hero & featured event
- **US:** As a visitor, I want to see the "Next Big Thing" event with date, time, and a way to read more so that I can learn about the next big activity.
- **Topics:** Hero section visible, event name/date/time correct, "Read more" link present and goes to the correct event page.

### 3.3 Join CTAs (Boy Scout / Cub Scout)
- **US:** As a parent or youth, I want to see how to join as Boy Scout or Cub Scout and get contact info and "Learn more" so that I can reach out or get details.
- **Topics:** Both CTAs visible, contact name/email/phone present (or masked as expected), "Learn more" links work and go to How to Join.

### 3.4 What's Due Soon
- **US:** As a scout or parent, I want to see what is due soon (e.g. deposit, Summer Camp) with deadline and link so that I don’t miss deadlines.
- **Topics:** Due-soon block visible, deadline text and link to event page correct.

### 3.5 Welcome section & key links
- **US:** As a visitor, I want to read about Troop 23 and use links to History, Trips, community service, location, and About Us so that I can explore further.
- **Topics:** Welcome text visible, all listed internal links present and navigable.

### 3.6 What is Scouting & Patrol links
- **US:** As a visitor, I want to understand what scouting is and follow links to Patrols and Patrol Scoring so that I can learn about the program and structure.
- **Topics:** "What is Scouting?" section visible, Patrols and Patrol Scoring links work.

### 3.7 Why Choose Troop 23 & value links
- **US:** As a visitor, I want to see why Troop 23 is a good choice and follow links to Patrol Method, scoring, merit badges, Eagle Scouts, Procedures, events, and awards so that I can dig deeper.
- **Topics:** Section visible, all linked pages (Patrol Method, Patrol Scoring, Merit Badge Counselors, Eagle Scouts, Procedures, events, 50 Miler) reach correct destinations.

### 3.8 New to Scouting CTA
- **US:** As someone new to scouting, I want a clear invitation to join and links to How to Join, Advancements, and What is Scouting so that I can take the next step.
- **Topics:** "New to Scouting?" block visible, How to Join / Advancements / What is Scouting links work.

### 3.9 Footer & last updated
- **US:** As a visitor, I want to see when the page was last updated so that I have a sense of content freshness.
- **Topics:** "Last updated" text visible and date format reasonable.

### 3.10 Responsive & basic UX
- **US:** As a visitor on mobile or desktop, I want the homepage to display correctly and key actions (links, CTAs) to be usable so that I can use the site on my device.
- **Topics:** Layout and readability on different viewports, links and buttons clickable/tappable.

### 3.11 Accessibility & SEO (optional)
- **US:** As a user with assistive tech or a search engine, I want the page to have sensible structure and semantics so that the content is accessible and indexable.
- **Topics:** Heading hierarchy, link text, basic ARIA/alt if applicable; optional meta/SEO checks.

---

## 4. Summary

- **Content:** One hero, two join CTAs, one due-soon block, four main text sections with many internal links, plus footer.
- **Elements:** Headings, text, internal links, contact info, event block, due-soon block, CTA links.
- **User story topics:** Page identity, hero/featured event, join CTAs, due soon, welcome + links, What is Scouting + patrol links, Why Choose Troop 23 + value links, New to Scouting CTA, footer/last updated, responsiveness, optional accessibility/SEO.

Use these topics to write concrete user stories and test cases (e.g. in Given/When/Then or checklist form) for the t23b.org homepage.
