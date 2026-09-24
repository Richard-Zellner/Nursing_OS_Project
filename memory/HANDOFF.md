# Handoff

## Implementation handoff — ticket 003

Ticket 003 adds all four synthetic patient JSON records and tests that they
parse, use IDs `SYNTH-001` through `SYNTH-004`, contain no forbidden keys,
and that patient C omits `code_status`, `mobility`, and `respiratory`.
Patient B includes telemetry, oxygen, IV diuretic and access, intake/output,
daily weight, and pending labs. Patient D retains the two contradictory
conditions required by the spec.

Verification in this run: pytest passed (6 tests); `tests/verify.ps1` passed.
No open questions. No human action is needed before the next ticket.

Next ticket: 004 — Loader. It is unblocked by tickets 001 and 003.
