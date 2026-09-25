# Handoff

## Nurse Handoff — ticket 008 accepted

Added `render_list_section(title, items)` with distinct output for missing or
null lists, explicitly empty lists, and populated lists in their original
order. Added `render_handoff(record)` to render ACCESS, MEDICATIONS OF NOTE,
THIS SHIFT, and PENDING in fixed order with the overview and assessment.
Added tests for all list states and a byte-exact handoff section-order check.

Verification this run: pytest passed (54 tests); `tests/verify.ps1` passed.
No spec discrepancy. No open questions. No milestone or release completed.
Next ticket: 009 Missing-data pass; prerequisites 007 and 008 are satisfied.
Human action: none.
