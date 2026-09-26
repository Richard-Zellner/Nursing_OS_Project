"""Command-line entry point for Nurse Handoff."""

import sys

from .generator import render_handoff, render_warnings
from .loader import PatientFileError, load_patient
from .rules import collect_warnings
from .validator import validate


USAGE = "Usage: python -m nurse_handoff <patient.json>"


def _write(stream, text: str) -> None:
    """Write UTF-8 text with LF line endings, whatever the console code page."""
    buffer = getattr(stream, "buffer", None)
    if buffer is None:
        stream.write(text)
        return
    stream.flush()
    buffer.write(text.encode("utf-8"))
    buffer.flush()


def main(argv: list[str] | None = None) -> int:
    """Print a handoff and its warnings; return the documented exit code.

    Exit 0 on success, 1 on validation errors, and 2 on usage, file, or JSON
    errors. No handoff is printed when any error occurs.
    """
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        _write(sys.stderr, f"{USAGE}\n")
        return 2

    try:
        record = load_patient(args[0])
    except PatientFileError as error:
        _write(sys.stderr, f"ERROR: {error}\n")
        return 2

    errors = validate(record)
    if errors:
        _write(sys.stderr, "".join(f"ERROR: {error}\n" for error in errors))
        return 1

    warnings = collect_warnings(record)
    _write(sys.stdout, render_handoff(record) + "\n" + render_warnings(warnings) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
