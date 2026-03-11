"""
Shared footer checks for t23b.org pages.

These helpers do NOT verify footer links via HTTP (covered elsewhere).
They only assert that the footer exists, has at least one section,
contains contact information (email + phone), and has a copyright line.
"""

import re
from typing import Optional

from playwright.sync_api import Page


def _footer_locator(page: Page):
    """Return the main footer locator (first <footer> element)."""
    return page.locator("footer").first


def _has_visible_email(footer) -> bool:
    """Check that footer contains at least one visible email element."""
    # Cloudflare-protected emails
    cf_email = footer.locator("a[href*='/cdn-cgi/l/email-protection'], span.__cf_email__")
    if cf_email.count() > 0 and cf_email.first.is_visible():
        return True
    # Standard mailto links
    mailto = footer.locator("a[href^='mailto:']")
    return mailto.count() > 0 and mailto.first.is_visible()


def _has_visible_phone(footer) -> bool:
    """Check that footer contains at least one visible phone link (tel:)."""
    tel_links = footer.locator("a[href^='tel:']")
    return tel_links.count() > 0 and tel_links.first.is_visible()


def _extract_footer_text(footer) -> str:
    """Get normalized inner text of footer for simple text checks."""
    try:
        text = footer.inner_text()
    except Exception:
        return ""
    return (text or "").strip()


def _has_reasonable_copyright(text: str) -> bool:
    """
    Check that footer text contains a copyright-like line:
    - '©' or 'Copyright'
    - a 4-digit year (optionally a range)
    - 'Troop 23' or 'Scouting America' (brand)
    """
    if not text:
        return False
    lower = text.lower()
    if "©" not in text and "copyright" not in lower:
        return False

    year_pattern = re.compile(r"\b(\d{4})(?:\s*-\s*(\d{4}))?\b")
    if not year_pattern.search(text):
        return False

    if "troop 23" not in lower and "scouting america" not in lower:
        return False

    return True


def assert_footer_structure_and_contacts_ok(
    page: Page,
    step_logger: Optional[object] = None,
    scope: str = "page",
) -> None:
    """
    Assert that the current page footer exists, has at least one section,
    contains contact information (email + phone), and a copyright.

    - Footer: first <footer> is present and visible.
    - Sections: at least one <h5> heading inside footer.
    - Contacts: at least one email and one phone link in footer.
    - Copyright: footer text contains ©/Copyright, year, and brand.
    """
    if step_logger:
        step_logger.start_step(f"[footer] Check footer structure and contacts on {scope}")

    footer = _footer_locator(page)
    assert footer.count() > 0, f"[footer] No <footer> element found on {scope}"
    assert footer.is_visible(), f"[footer] Footer should be visible on {scope}"

    # At least one section heading (e.g., Navigate the Trail, Troop Hub, About)
    headings = footer.locator("h5")
    count_h5 = headings.count()
    if step_logger:
        step_logger.log_text(f"[footer] h5 section headings count = {count_h5}")
    assert count_h5 >= 1, f"[footer] Expected at least one section heading (h5) in footer on {scope}"

    # Contact information: email + phone somewhere in footer (Troop Hub)
    has_email = _has_visible_email(footer)
    has_phone = _has_visible_phone(footer)
    if step_logger:
        step_logger.log_text(f"[footer] has_email={has_email}, has_phone={has_phone}")
    assert has_email, f"[footer] Expected at least one visible email contact in footer on {scope}"
    assert has_phone, f"[footer] Expected at least one visible phone contact in footer on {scope}"

    # Copyright line
    text = _extract_footer_text(footer)
    if step_logger:
        snippet = text.replace("\n", " ")[:200]
        step_logger.log_text(f"[footer] footer text snippet = {snippet!r}")
    assert _has_reasonable_copyright(text), (
        f"[footer] Expected a copyright line with year "
        f"and brand (Troop 23 / Scouting America) in footer on {scope}"
    )

    if step_logger:
        step_logger.checkpoint(f"[footer] Footer structure and contacts OK on {scope}")

