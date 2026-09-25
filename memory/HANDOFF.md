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

## Portfolio setup — 2026-09-24

Owner delegated the private NurseBench repository setup to Codex. P1-M0-1
and P1-M0-2 are complete in the separate Desktop/nursebench repository.
It is registered as nursebench; remote private visibility and the first
pushed commit were checked. Local locked dependency and scaffold checks
passed. All clinical content and releases remain pending owner work.
Next interactive task: P1-M0-3 shared item schema and validator. See
plans/PROGRESS.md and the new repository's memory/HANDOFF.md. P0 is unchanged.
