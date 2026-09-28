# Handoff

## Nurse Handoff - v0.2 in development

Ticket 106 complete: Rule 9 warns when `fall_risk` is `true` and `mobility`
is absent or `null`. Added the optional boolean to v0.2 schema metadata,
validation, tests, and the README. Rule 9 follows Rule 8.

Checks this run: pytest passed (306 tests); `tests/verify.ps1` passed,
including its CLI checks. No synthetic patient data was added. The v0.2
Definition of Done is pending ticket 110, so no `DONE` file was created.

Next ticket: 107, remove the Rule 10 placeholder and record why in DECISIONS.md.

Open questions: Q-002 (optional empty strings); Q-003 (newline list items,
whitespace-only strings, and UTF-8 BOM). No human action is needed for ticket
106.
