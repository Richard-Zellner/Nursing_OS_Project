# Handoff

## Implementation handoff — ticket 004

Ticket 004 adds `load_patient(path) -> dict` and `PatientFileError`.
The loader reads UTF-8 JSON objects and preserves all supplied values,
including missing keys, null, false, empty lists, and unknown keys.
Missing files, malformed JSON/UTF-8, non-object roots, and read failures
produce useful path-bearing errors. Required-field validation remains 005.

Verification in this run: baseline pytest passed (6 tests); final pytest
passed (27 tests); `tests/verify.ps1` passed. No open questions.
This was owner-authorized delegated work; parent code review and an
independent `tests/verify.ps1` run passed (27 tests).
The ignored STOP marker remains under the parent session's control.

Next ticket: 005 — Validator. It is unblocked by ticket 002.

## Portfolio setup — 2026-09-24

Owner delegated the private NurseBench repository setup to Codex. P1-M0-1
and P1-M0-2 are complete in the separate Desktop/nursebench repository.
It is registered as nursebench; remote private visibility and the first
pushed commit were checked. Local locked dependency and scaffold checks
passed. All clinical content and releases remain pending owner work.
Next interactive task: P1-M0-3 shared item schema and validator. See
plans/PROGRESS.md and the new repository's memory/HANDOFF.md. P0 is unchanged.
