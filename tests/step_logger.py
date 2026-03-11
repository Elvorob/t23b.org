"""
Step logger: captures page console/network by step, writes one log file per test,
takes one full-page screenshot at end of test. Supports checkpoints for proof of passed checks.
"""

from pathlib import Path
from typing import List, Optional, Tuple

from playwright.sync_api import Page

try:
    import allure  # type: ignore

    _HAVE_ALLURE = True
except Exception:  # pragma: no cover - optional dependency
    allure = None  # type: ignore
    _HAVE_ALLURE = False


def _sanitize_segment(name: str) -> str:
    return (
        name.replace("/", "_")
        .replace("::", "_")
        .replace(" ", "_")
        .strip("_")
        or "part"
    )


def _split_test_name(test_name: str) -> Tuple[str, str]:
    """
    Split pytest function name into:
    - case_id folder (e.g. TC_03)
    - per-function base name (e.g. 1_boy_scout_block_visible)

    Expected pattern: test_TC_03_1_boy_scout_block_visible
    Fallback: case_id="misc", base_name=<sanitized original>.
    """
    base = test_name
    if base.startswith("test_"):
        base = base[5:]
    parts = base.split("_", 3)
    if (
        len(parts) >= 3
        and parts[0].upper() == "TC"
        and parts[1].isdigit()
        and parts[2].isdigit()
    ):
        case_id = f"TC_{parts[1]}"
        tail = parts[3] if len(parts) > 3 else ""
        local = f"{parts[2]}_{tail}".strip("_")
        return _sanitize_segment(case_id), _sanitize_segment(local)
    return "misc", _sanitize_segment(test_name)


class StepLogger:
    """One log file + one full-page screenshot (end) per test function, grouped by case folder."""

    def __init__(
        self,
        run_dir: Path,
        test_name: str,
        page: Optional[Page] = None,
    ):
        self.run_dir = Path(run_dir)
        self.test_name = test_name
        self.page = page
        case_id, _ = _split_test_name(test_name)
        self._case_dir = self.run_dir / case_id
        self._case_dir.mkdir(parents=True, exist_ok=True)
        # Use full test function name for artefact base name
        self._base_name = _sanitize_segment(test_name)
        self._shot_index: int = 0
        self._steps: List[Tuple[str, List[str]]] = []
        self._current_step: Optional[str] = None
        self._current_entries: List[str] = []

        if page:
            self._attach_listeners(page)

    def _attach_listeners(self, page: Page) -> None:
        def on_console(msg):
            self._current_entries.append(f"[Console] {msg.type}: {msg.text}")

        def on_request(req):
            self._current_entries.append(f"[Request] {req.method} {req.url}")

        def on_response(resp):
            self._current_entries.append(f"[Response] {resp.status} {resp.url}")

        page.on("console", on_console)
        page.on("request", on_request)
        page.on("response", on_response)

    def start_step(self, description: str) -> None:
        if self._current_step is not None:
            self._steps.append((self._current_step, list(self._current_entries)))
            self._current_entries.clear()
        self._current_step = description

    def log_text(self, line: str) -> None:
        self._current_entries.append(line)

    def checkpoint(self, message: str) -> None:
        """Record a passed check for proof in the log."""
        self._current_entries.append(f"[Checkpoint] {message} — OK")

    def take_screenshot(self, suffix: str, full_page: bool = True) -> None:
        if not self.page:
            return
        self._shot_index += 1
        label = _sanitize_segment(suffix)
        path = self._case_dir / f"{self._base_name}_{self._shot_index:02d}_{label}.png"
        # Always capture full-page screenshots for consistency in reports
        self.page.screenshot(path=str(path), full_page=True)
        if _HAVE_ALLURE:
            try:
                allure.attach.file(
                    str(path),
                    name=f"{self._base_name}_{self._shot_index:02d}_{label}",
                    attachment_type=allure.attachment_type.PNG,  # type: ignore[attr-defined]
                )
            except Exception:
                # Allure is optional; ignore attachment errors so tests still pass.
                pass

    def finalize(self) -> None:
        if self._current_step is not None:
            self._steps.append((self._current_step, list(self._current_entries)))
        if self.page:
            self.take_screenshot("end", full_page=True)
        self._write_log()

    def _write_log(self) -> None:
        path = self._case_dir / f"{self._base_name}_log.txt"
        lines = []
        for step_name, entries in self._steps:
            lines.append(f"\n[Step] {step_name}")
            lines.append("-" * 60)
            for e in entries:
                lines.append(e)
            lines.append("")
        text = "\n".join(lines)
        path.write_text(text, encoding="utf-8")

        if _HAVE_ALLURE:
            try:
                allure.attach(
                    text,
                    name=f"{self._base_name}_log",
                    attachment_type=allure.attachment_type.TEXT,  # type: ignore[attr-defined]
                )
            except Exception:
                pass
