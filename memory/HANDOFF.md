# Handoff

## Nurse Handoff — v0.2 in development

Ticket 102 is complete. Rule 5 emits the additional code-status warning for
absent or null `code_status`, alongside the important-field glyph warning.
Tests cover both missing forms, documented status, warning order, README, and
the incomplete-patient CLI output.

Verification this run: pytest passed (251 tests); `tests/verify.ps1` passed,
including the CLI check. No new durable decision or human action is needed.

Next ticket: 103, Rule 6 telemetry without rhythm. It is unblocked by ticket
101. Preserve the v0.1 patient schema text when adding the v0.2 field.

Open questions: Q-002 (optional empty strings); Q-003 (newline list items,
whitespace-only strings, and UTF-8 BOM). Their handling remains undecided.
