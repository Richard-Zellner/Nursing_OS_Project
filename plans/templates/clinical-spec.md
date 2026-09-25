# Template: clinical specification (owner-authored)

Copy to `docs/clinical-spec.md` (or `docs/clinical-spec-<track>.md`). The
owner fills in every section. An agent may create this empty file and list
questions, but never writes the answers.

```markdown
# <Project / track>: clinical specification

Author: <owner>, RN · Version: <x.y> · Date: <YYYY-MM-DD>

## 1. Clinical problem
What goes wrong at the bedside, and who notices.

## 2. Scope
In scope. Out of scope (be explicit, e.g. "no pediatric patients").

## 3. Sources and licensing
| Source | Citation | What is used | License / permission status |
Paraphrase; never copy forms or licensed item text.

## 4. Definitions
Every term the code relies on (e.g. "critical error", "unable to screen", "hospital day").

## 5. Decision logic
Tables or rules exact enough to implement without guessing.
Units, rounding, caps and tolerances stated.

## 6. Missing and contradictory data
What happens when data is absent, ambiguous or conflicting.
Absent never means normal.

## 7. Edge cases
Numbered list; each becomes at least one test or gold item.

## 8. Gold-answer and labeling rules
How gold answers are produced and reviewed; who adjudicates.

## 9. Evaluation thresholds
Pass criteria, error thresholds and kappa minimums, each with its justification.

## 10. Known limitations
What this cannot represent (real workflows, institutional variation).

## Changelog
```

Before an agent implements from the spec, check that:
- every rule has units and boundaries (inclusive or exclusive)
- every source has its license status filled in
- sections 6 and 7 are not empty
