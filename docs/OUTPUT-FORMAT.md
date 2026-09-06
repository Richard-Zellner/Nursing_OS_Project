# Handoff output format (v0.1)

Plain text, UTF-8, LF line endings, no trailing whitespace. Byte-identical
for identical input. The em dash in the overview line is U+2014; the
warning glyph is U+26A0 followed by one space.

## Full layout

```text
NURSING HANDOFF
---------------

<age>-year-old — <code_status or "Code status: Not documented">
Primary problem: <primary_problem>

ASSESSMENT
Neuro: <neuro | Not documented>
Cardiac: <cardiac | Not documented>
Respiratory: <see PATIENT-SCHEMA.md respiratory table>
Mobility: <mobility | Not documented>
Diet: <diet | Not documented>

ACCESS
- <item>                       (or "Not documented" / "None")

MEDICATIONS OF NOTE
- <item>

THIS SHIFT
- <item>

PENDING
- <item>

WARNINGS
--------
None                            (or one line per warning, in rule order)
```

Section order is fixed. Every section always prints, even when empty.
Exactly one blank line between sections. The file ends with a single LF.

## Overview line

- Code status present: `72-year-old — Full Code`
- Code status missing: `72-year-old — Code status: Not documented`

## Warnings block

Two kinds of warnings, printed in this order:

1. Important-field warnings, in schema order:
   `⚠ Code status not documented`, `⚠ Neuro assessment not documented`,
   `⚠ Respiratory assessment not documented`, `⚠ Mobility status not
   documented`, `⚠ Vascular access not documented`, `⚠ Pending tasks not
   documented`.
2. Rule warnings, in rule order, prefixed `WARNING: ` exactly as worded in
   the spec. Rule 3 and the mobility important-field warning describe the
   same fact; print only the rule wording
   (`WARNING: Mobility status not documented.`), not both.

When there are no warnings the block body is the single word `None`.

## Errors

Validation failures print to stderr, one per line, and exit 1:

```text
ERROR: primary_problem is required
```

File and JSON failures print to stderr and exit 2:

```text
ERROR: file not found: data/missing.json
ERROR: invalid JSON in data/bad.json: Expecting ',' delimiter: line 4 column 3
```

No handoff is printed on any error.
