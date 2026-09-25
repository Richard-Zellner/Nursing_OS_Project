# Handoff

## Nurse Handoff — ticket 006 accepted

Added `render_overview(record)` for the NURSING HANDOFF heading and overview
lines, including the exact em dash and the missing-code-status text. Added
byte-exact tests for documented and missing code status; explicit `null` is
also covered. The section has no trailing LF so later assembly can control
section spacing and the single final LF.

Verification this run: pytest passed (39 tests); `tests/verify.ps1` passed.
No spec discrepancy. No open questions. No milestone or release completed.
Next ticket: 007 Assessment section; its prerequisite 006 is satisfied.
Human action: none.
