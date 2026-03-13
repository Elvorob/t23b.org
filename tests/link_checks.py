"""
Shared helpers for checking links and image URLs via HTTP (2xx, body, HTML/media).
Used by main page (TC-05) and about-us (TC-13) tests; supports both <a href> and <img src>.
"""

import re
from urllib.parse import urlparse

import requests

LINK_CHECK_MIN_BODY_LENGTH = 500
LINK_CHECK_TIMEOUT = 15


def is_media_resource_url(url: str, content_type: str | None) -> bool:
    """True if URL or Content-Type indicates image/media (no HTML expected)."""
    path = urlparse(url).path.lower()
    if path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".pdf")):
        return True
    if content_type and content_type.split(";")[0].strip().lower().startswith(
        ("image/", "application/pdf")
    ):
        return True
    return False


def _is_events_path(url: str) -> bool:
    """Return True for internal /events... paths which are allowed to redirect."""
    path = urlparse(url).path
    return path.startswith("/events")


def check_url_not_broken_and_not_empty(url: str) -> tuple[bool, str]:
    """
    Check via GET that the URL is not broken and not empty.
    Returns (success, message).

    - Default: expect direct 2xx (no redirects). Any 3xx is treated as error, and
      the whole redirect chain is reported for debugging.
    - Exception: internal /events... URLs are allowed to redirect; for them we
      follow redirects and require that the final response is 2xx.
    - For HTML pages: body length, </body> or <html, non-empty <title>.
    - For media (image/pdf): 2xx and non-empty body only.
    """
    try:
        response = requests.get(
            url,
            allow_redirects=False,
            timeout=LINK_CHECK_TIMEOUT,
        )
    except requests.RequestException as e:
        return False, f"request failed: {e!s}"

    status = response.status_code
    if 300 <= status < 400:
        # Special case: /events... links are allowed to redirect;
        # check the final destination instead of failing on 3xx.
        if _is_events_path(url):
            try:
                follow = requests.get(
                    url,
                    allow_redirects=True,
                    timeout=LINK_CHECK_TIMEOUT,
                )
                all_resps = list(follow.history) + [follow]
                chain_parts = []
                prev_url = url
                for r in all_resps:
                    chain_parts.append(f"{prev_url} ({r.status_code})")
                    prev_url = r.headers.get("Location", prev_url)
                chain = " -> ".join(chain_parts)
                if follow.status_code in range(200, 300):
                    return True, f"redirect OK; chain: {chain}"
                return (
                    False,
                    f"events redirect chain did not end in 2xx; "
                    f"final status {follow.status_code}; chain: {chain}",
                )
            except requests.RequestException as e:
                return (
                    False,
                    f"unexpected redirect status {status}; redirect follow failed: {e!s}",
                )

        # Default behaviour for other internal URLs: redirects are unexpected.
        try:
            follow = requests.get(
                url,
                allow_redirects=True,
                timeout=LINK_CHECK_TIMEOUT,
            )
            chain_parts = []
            all_resps = list(follow.history) + [follow]
            prev_url = url
            for r in all_resps:
                chain_parts.append(f"{prev_url} ({r.status_code})")
                prev_url = r.headers.get("Location", prev_url)
            chain = " -> ".join(chain_parts)
            return False, f"unexpected redirect status {status}; chain: {chain}"
        except requests.RequestException as e:
            return (
                False,
                f"unexpected redirect status {status}; redirect follow failed: {e!s}",
            )

    if status not in range(200, 300):
        return False, f"status {status}"

    content = response.content
    content_type = response.headers.get("Content-Type") or ""

    if is_media_resource_url(url, content_type):
        if len(content) < 100:
            return False, f"media body too short ({len(content)} bytes)"
        return True, "OK"

    if len(content) < LINK_CHECK_MIN_BODY_LENGTH:
        return False, f"body too short ({len(content)} bytes)"

    content_lower = content.lower()
    if b"</body>" not in content_lower and b"<html" not in content_lower:
        return False, "body lacks </body> or <html"

    title_match = re.search(
        rb"<title[^>]*>([^<]*)</title>",
        content,
        re.IGNORECASE | re.DOTALL,
    )
    if not title_match:
        return False, "no <title> found"
    title_text = title_match.group(1).decode("utf-8", errors="replace").strip()
    if not title_text:
        return False, "empty <title>"

    return True, "OK"
