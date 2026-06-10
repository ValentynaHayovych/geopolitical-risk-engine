"""
pipeline_logger.py
------------------
A reusable logger for ETL pipelines.

Usage
-----
    from src.pipeline_logger import PipelineLogger

    log = PipelineLogger(pipeline_name="Geopolitical Risk Engine ETL", total_phases=4)

    log.start()

    log.phase(1, "Extract & load → raw")
    log.kv("source rows", 1088)
    log.kv("source columns", 61)
    log.kv("loaded", f"{len(df)} rows → raw.global_conflicts")
    log.ok("Extract & load complete")

    log.phase(2, "Validate & load → staging")
    log.kv("source rows", 1088)
    log.kv("duplicates removed", 0)
    log.warn("Nullable columns detected", detail={
        "Alliance_A": "359 nulls",
        "Alliance_B": "366 nulls",
        "Resource_Dispute": "300 nulls",
    })
    log.kv("rows", f"{init_rows} → {final_rows}")
    log.kv("duplicates removed", dup_removed)
    log.kv("null rows removed", nulls_removed)
    log.kv("loaded", f"{len(df)} rows → staging.global_conflicts")
    log.ok("Validation & load complete")

    log.finish(
        summary={
            "raw ingested":       (1088, None),
            "fact rows loaded":   (881, None), 
            "predictions loaded": (872, None),
            "warnings":           (1,    "nullable columns — see [2/4]")
        }
    )
"""

import time
from datetime import datetime


# ── ANSI colour codes ─────────────────────────────────────────────────────────
# Set USE_COLOUR = False if your environment doesn't support ANSI
# (e.g. some Windows terminals, plain file logs).
USE_COLOUR = True

_R = "\033[0m"          # reset
_BLUE   = "\x1b[38;5;14m"    # phase headers
_GREEN  = "\033[38;2;135;191;78m"    # ✓ success
_YELLOW = "\x1b[38;5;178m"    # ⚠ warning
_GREY   = "\033[90m"    # dim detail / notes
_BOLD   = "\033[1m"     # headings


def _c(code: str, text: str) -> str:
    """Wrap text in an ANSI colour code, or return plain text if disabled."""
    return f"{code}{text}{_R}" if USE_COLOUR else text


# ── PipelineLogger ────────────────────────────────────────────────────────────

class PipelineLogger:
    """
    Structured console logger for multi-phase ETL pipelines.

    Parameters
    ----------
    pipeline_name : str
        Displayed in the header and footer banners.
    total_phases : int
        Total number of phases — used in the [n/total] label.
    width : int
        Width of the separator line (default 58).
    show_timestamps : bool
        If True, each phase header shows a HH:MM:SS timestamp.
    """

    def __init__(
        self,
        pipeline_name: str,
        total_phases: int,
        pipeline_type: str = "ETL Pipeline",
        width: int = 58,
        show_timestamps: bool = True,
    ):
        self.pipeline_name  = pipeline_name
        self.pipeline_type = pipeline_type
        self.total_phases   = total_phases
        self.width          = width
        self.show_timestamps = show_timestamps

        self._current_phase = 0
        self._warning_phases = []
        self._warnings = property(lambda self: len(self._warning_phases))
        self._start_time    = None

    # ── internal helpers ──────────────────────────────────────────────────────

    # property
    def warning_count(self) -> int:
        return len(self._warning_phases)
    
    def _sep(self) -> str:
        return _c(_GREY, "─" * self.width)

    def _print_kv(self, key: str, value, note: str = "") -> None:
        note_str = _c(_GREY, f"  ({note})") if note else ""
        print(f"  {_c(_GREY, f'{key:<18}')}  {value}{note_str}")

    # ── public API ────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Print the opening banner. Call once before any phases."""
        self._start_time = time.time()
        print(self._sep())
        title = f"{self.pipeline_name}  ·  {self.pipeline_type}"
        print(_c(_BOLD, title.center(self.width)))
        print(self._sep())

    def phase(self, number: int, label: str) -> None:
        """
        Print a phase header.

        Parameters
        ----------
        number : int   Phase number (1-based).
        label  : str   Short description, e.g. "Extract & load → raw".
        """
        self._current_phase = number
        ts = ""
        if self.show_timestamps:
            ts = _c(_GREY, f"  {datetime.now().strftime('%H:%M:%S')}")
        header = f"[{number}/{self.total_phases}]  {label}"
        print(f"\n{_c(_BLUE, header)}{ts}")

    def kv(self, key: str, value, note: str = "") -> None:
        """
        Print a key-value metric row.

        Parameters
        ----------
        key   : str        Label (left column).
        value : any        Value (right column) — int, str, float all work.
        note  : str        Optional parenthetical note shown in grey.
        """
        if isinstance(value, int):
            value = f"{value:,}"          # thousands separator: 1,088
        self._print_kv(key, value, note)

    def ok(self, message: str) -> None:
        """Print a green success confirmation line."""
        print(_c(_GREEN, f"  ✓  {message}"))

    def warn(self, message: str, detail: dict | None = None) -> None:
        """
        Print a yellow warning line, with optional indented detail rows.

        Parameters
        ----------
        message : str
            The warning summary line.
        detail  : dict | None
            Optional {label: value} pairs printed as indented sub-rows.
        """
        self._warning_phases.append((self._current_phase, message))
        print(_c(_YELLOW, f"  ⚠  {message}"))
        if detail:
            for k, v in detail.items():
                print(_c(_GREY, f"     {k:<18} {v}"))

    def finish(self, summary: dict | None = None) -> None:
        """
        Print the closing summary block and footer banner.

        Parameters
        ----------
        summary : dict | None
            Optional {label: (value, note)} mapping.
            - value : int | str   Shown as the right column.
            - note  : str | None  Shown in grey if provided.

        Example
        -------
            log.finish(
                summary={
                    "raw ingested":       (1088, None),
                    "fact rows loaded":   (881, None),
                    "predictions loaded": (872, None),
                    "warnings":           (1,    "nullable columns — see [2/4]"),
                }
            )
        """
        elapsed = f"{time.time() - self._start_time:.1f}s" if self._start_time else "—"

        print(f"\n{self._sep()}")
        print(_c(_BOLD, f"{self.pipeline_type} Summary".center(self.width)))
        print(self._sep())

        if summary:
            for key, item in summary.items():

                if isinstance(item, tuple):
                    value, note = item
                else:
                    value, note = item, ""

                self.kv(key, value, note)

        self.kv("elapsed", elapsed)
        warning_count = len(self._warning_phases)
        if warning_count == 0:
            self.kv("warnings", 0)
        else:
            for i, (phase, message) in enumerate(self._warning_phases):
                label = "warnings" if i == 0 else ""
                self._print_kv(label, warning_count if i == 0 else "", 
                            f"{message} — see [{phase}/{self.total_phases}]")

        status = "✓  Pipeline complete" if len(self._warning_phases) == 0 else f"✓  Pipeline complete  ({len(self._warning_phases)} warning(s))"
        print(_c(_GREEN, f"  {status}"))
        print(self._sep())

log = PipelineLogger("Geopolitical Risk Engine", total_phases=4, pipeline_type="ETL Pipeline")
