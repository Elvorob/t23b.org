"""
Helper: check that links inside a text section are visually recognizable as links
(not the same plain text style with no underline/color difference).
Reports findings in the test report without failing the test.
"""

import re
from typing import List, Tuple

from playwright.sync_api import Page, Locator


def _sentence_containing(block_text: str, link_text: str, max_length: int = 300) -> str:
    """Extract one sentence from block_text that contains link_text, or first sentence."""
    if not block_text or not block_text.strip():
        return "(no surrounding text)"
    block_text = block_text.strip()
    link_text = (link_text or "").strip()
    # Split into sentences (break on . ! ? followed by space or end)
    sentences = re.split(r"(?<=[.!?])\s+", block_text)
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if link_text and link_text in s:
            return s[:max_length] + ("..." if len(s) > max_length else "")
        if not link_text:
            return s[:max_length] + ("..." if len(s) > max_length else "")
    return sentences[0][:max_length] + ("..." if len(sentences[0]) > max_length else "") if sentences else block_text[:max_length]


def _normalize_rgb(color: str | None) -> str:
    """
    Normalize computed color string for comparison.
    - Strips spaces and lowercases.
    - Converts rgba(r,g,b,1) to rgb(r,g,b) so it matches browser rgb() output.
    """
    if not color:
        return ""
    s = color.replace(" ", "").lower()
    # rgba(r,g,b,1) or rgba(r,g,b,1.0) -> rgb(r,g,b) for consistent comparison
    m = re.match(r"rgba\((\d+),(\d+),(\d+),1(?:\.0)?\)", s)
    if m:
        return f"rgb({m.group(1)},{m.group(2)},{m.group(3)})"
    return s


def get_visually_hidden_links_in_section(
    page: Page, section: Locator, section_name: str
) -> List[Tuple[str, str, str]]:
    """
    Find links inside the section that look like plain text: same color as section
    and no underline. Returns list of (link_text_excerpt, href, context_sentence).
    """
    links = section.locator("a[href]")
    n = links.count()
    if n == 0:
        return []

    section_color = section.evaluate(
        "el => getComputedStyle(el).color"
    )
    section_color_norm = _normalize_rgb(section_color)

    hidden = []
    for i in range(n):
        link = links.nth(i)
        if not link.is_visible():
            continue
        href = (link.get_attribute("href") or "").strip()
        if not href or href.startswith("#"):
            continue
        styles = link.evaluate(
            "el => ({ color: getComputedStyle(el).color, textDecoration: getComputedStyle(el).textDecoration })"
        )
        link_color_norm = _normalize_rgb(styles.get("color") or "")
        decoration = (styles.get("textDecoration") or "").lower()
        has_underline = "underline" in decoration
        same_color = link_color_norm == section_color_norm and link_color_norm
        if same_color and not has_underline:
            text = (link.inner_text() or "").strip()[:50]
            block_text = link.evaluate(
                "el => { const block = el.closest('p, li, td, div'); return block ? block.innerText || '' : ''; }"
            )
            context_sentence = _sentence_containing(block_text or "", text)
            hidden.append((text, href, context_sentence))
    return hidden


def report_links_visually_recognizable(
    page: Page, section: Locator, section_name: str, step_logger
) -> None:
    """
    Check links in the section for visual recognizability (different color or underline).
    Does not fail the test; writes each finding to the report with the surrounding sentence.
    """
    hidden = get_visually_hidden_links_in_section(page, section, section_name)
    step_logger.start_step(
        f"Check that links in '{section_name}' are visually recognizable (not plain-text style)"
    )
    for text_excerpt, href, context_sentence in hidden:
        msg = (
            f"Non-visualizable link found in this text: \"{context_sentence}\" "
            f"(link text: {text_excerpt!r}, href: {href})"
        )
        print(f"[link_visibility] {section_name}: {msg}")
        step_logger.log_text(msg)
    if hidden:
        step_logger.checkpoint(
            f"Found {len(hidden)} link(s) in '{section_name}' not visually recognizable (see above)"
        )
    else:
        step_logger.checkpoint(
            f"All links in '{section_name}' are visually recognizable as links"
        )
