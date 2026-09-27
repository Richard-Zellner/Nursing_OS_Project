# Handoff

## Nurse Handoff — v0.2 in development

Ticket 104 is complete. Rule 7 warns when a medication contains furosemide,
bumetanide, or torsemide (case-insensitive) and no recent event contains the
literal `urine output` phrase or `UO` abbreviation. README and tests cover the
new warning and its order after Rule 6.

Checks this run: pytest passed (286 tests); `tests/verify.ps1` passed,
including its CLI checks. No new synthetic patient data was needed.

Next ticket: 105, Rule 8 NPO conflict. It is unblocked by ticket 101.

Open questions: Q-002 (optional empty strings); Q-003 (newline list items,
whitespace-only strings, and UTF-8 BOM). No human action is needed for ticket
104.
