# Handoff

## 2026-09-24 — Owner-requested directory organization

Codex moved seven root-level planning documents into `docs/portfolio/`, using
consistent repo-based filenames. Start at `docs/portfolio/README.md`; the hub
README and `docs/README.md` provide navigation to plans, specs, and code.
All seven moved documents retained their exact contents (SHA-256 checked).
All 32 original source files were accounted for. Existing code, specs,
controller entry points, task checkboxes, and Git configuration stayed in place.

Verification: `tests/verify.ps1` passed, including 3 pytest tests and CLI usage;
28 local Markdown links across 10 documents resolved. No ticket was advanced.
The portfolio plans do not replace the current implementation ledger.

## Implementation handoff — ticket 002

The previous worker completed ticket 002. It added `schema.py` with ordered
required, important, and optional fields, exact important-field warning lines,
and expected Python types for every documented field. Added schema metadata
tests aligned with `docs/PATIENT-SCHEMA.md`.

Next ticket: 003 — Four synthetic patients. It is unblocked by completed
ticket 001. Q-001 is answered: public GitHub setup and automated controller Git sync
are authorized. See `memory/GIT-SETUP-2026-09-24.md`.
