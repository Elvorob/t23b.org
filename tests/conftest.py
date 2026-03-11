"""
Pytest configuration and shared fixtures for t23b.org tests.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import TextIO

import pytest
from playwright.sync_api import sync_playwright, Browser, Page

from tests.step_logger import StepLogger

BASE_URL = "https://www.t23b.org/"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
TESTS_DIR = Path(__file__).resolve().parent

# Path to console error allowlist (one substring per line; # and empty lines ignored).
CONSOLE_ALLOWLIST_PATH = TESTS_DIR / "console_allowlist.txt"


def get_console_error_allowlist() -> list[str]:
    """Load console error allowlist from config file; return list of lowercase substrings."""
    terms = []
    if CONSOLE_ALLOWLIST_PATH.exists():
        for line in CONSOLE_ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line.lower())
    if not terms:
        # Fallback if file missing or empty
        terms = ["cookie", "tracking", "analytics", "gtag", "facebook", "cloudflare"]
    return terms


def _unescape_teamcity_for_file(s: str) -> str:
    """Make TeamCity protocol lines readable in run_log: restore newlines and quotes (|n -> \\n, |' -> ')."""
    return (
        s.replace("|n", "\n")
        .replace("|r", "\r")
        .replace("|'", "'")
        .replace("||", "|")
        .replace("|[", "[")
        .replace("|]", "]")
        .replace("|p", "|")
    )


class _Tee:
    """Writes to both the original stream and a file (for run_log.txt). Accepts str or bytes (PyCharm runner may pass bytes)."""

    def __init__(self, stream: TextIO, file: TextIO) -> None:
        self._stream = stream
        self._file = file

    def write(self, data: str | bytes) -> int:
        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="replace")
        n = self._stream.write(data)
        try:
            file_data = _unescape_teamcity_for_file(data)
            self._file.write(file_data)
            self._file.flush()
        except (ValueError, OSError):
            pass  # file may already be closed by pytest_sessionfinish/unconfigure
        return n

    def flush(self) -> None:
        self._stream.flush()
        try:
            self._file.flush()
        except (ValueError, OSError):
            pass

    def writable(self) -> bool:
        return True

    def isatty(self) -> bool:
        return getattr(self._stream, "isatty", lambda: False)()


def pytest_configure(config: pytest.Config) -> None:
    """Create run folder and tee stdout/stderr to run_log.txt as early as possible."""
    run_dir = RESULTS_DIR / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    config.run_dir = run_dir

    log_path = run_dir / "run_log.txt"
    config._run_log_file = open(log_path, "w", encoding="utf-8")  # noqa: SIM115
    config._run_log_stdout_orig = sys.stdout
    config._run_log_stderr_orig = sys.stderr
    sys.stdout = _Tee(sys.stdout, config._run_log_file)
    sys.stderr = _Tee(sys.stderr, config._run_log_file)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Do not close here: other plugins (e.g. TerminalReporter) still write to the Tee. See pytest_unconfigure."""

def pytest_unconfigure(config: pytest.Config) -> None:
    """Restore stdout/stderr and close run_log.txt after all sessionfinish hooks have run."""
    if hasattr(config, "_run_log_file"):
        sys.stdout = getattr(config, "_run_log_stdout_orig", sys.stdout)
        sys.stderr = getattr(config, "_run_log_stderr_orig", sys.stderr)
        config._run_log_file.close()
        del config._run_log_file
        del config._run_log_stdout_orig
        del config._run_log_stderr_orig


@pytest.fixture(scope="session")
def run_dir(pytestconfig: pytest.Config):
    """Return the run folder for this session (created in pytest_configure)."""
    return getattr(pytestconfig, "run_dir", None) or (
        RESULTS_DIR / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    )


@pytest.fixture
def step_logger(request, run_dir: Path):
    """Per-test: capture console/network by step, write log file, one full-page screenshot at end."""
    page = None
    if "page" in request.fixturenames:
        page = request.getfixturevalue("page")
    logger = StepLogger(run_dir=run_dir, test_name=request.node.name, page=page)
    yield logger
    logger.finalize()


@pytest.fixture(scope="module")
def browser():
    """Launch browser once per test module; close after all tests in module."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser):
    """New page (tab) per test; closed after each test."""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def homepage_url():
    """Base URL of the site (homepage)."""
    return BASE_URL
