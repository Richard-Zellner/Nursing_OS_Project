"""Command-line entry point for Nurse Handoff."""

import sys


USAGE = "Usage: python -m nurse_handoff <patient.json>"


def main() -> int:
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
