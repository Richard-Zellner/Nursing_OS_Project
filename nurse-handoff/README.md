# Nurse Handoff

**Nurse Handoff** is an educational prototype exploring how structured
clinical information can be converted into a standardized nursing
shift-report summary.

Nursing handoff requires clinicians to synthesize information scattered
throughout the medical record. This project explores a deterministic
approach to organizing that information while explicitly preserving
missing or unknown data.

The initial version intentionally does not use artificial intelligence.
Its primary design principle is: *the system may organize documented
information, but it must not invent undocumented information.*

All patient records included in this repository are synthetic and the
software is not intended for clinical use.

Version 0.1.0. Python standard library only; `pytest` is the single test
dependency. The specification lives in
[`docs/NURSE-HANDOFF-SPEC.md`](../docs/NURSE-HANDOFF-SPEC.md), with the field
list in [`PATIENT-SCHEMA.md`](../docs/PATIENT-SCHEMA.md) and the exact report
layout in [`OUTPUT-FORMAT.md`](../docs/OUTPUT-FORMAT.md).

## Install

Requires Python 3.10 or newer. From this `nurse-handoff/` directory:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Activate the virtual environment before `pip install` (`source .venv/bin/activate`
on macOS/Linux, `.venv\Scripts\Activate.ps1` in PowerShell), or call its
interpreter directly, for example
`.venv\Scripts\python.exe -m pip install -r requirements.txt` on Windows.

## Usage

```bash
python -m nurse_handoff data/chf_patient.json
```

The program loads the JSON record, validates it, prints the handoff, and then
prints a `WARNINGS` block (`None` when there are no warnings). Output is UTF-8
plain text with LF line endings and is byte-identical for identical input.

| Exit code | Meaning | Output |
|---|---|---|
| 0 | Handoff generated | Handoff and `WARNINGS` block on stdout |
| 1 | Validation error (missing required field or wrong type) | One `ERROR:` line per problem on stderr; no handoff |
| 2 | Missing file, invalid JSON, or wrong arguments | `ERROR:` line or usage text on stderr; no handoff |

Required fields are `patient_id`, `age`, and `primary_problem`. A missing one
stops the program:

```text
ERROR: primary_problem is required
```

## Sample output

Patient B (`data/chf_patient.json`):

```text
NURSING HANDOFF
---------------

72-year-old — Full Code
Primary problem: CHF exacerbation

ASSESSMENT
Neuro: Alert and oriented x4
Cardiac: Normal sinus rhythm on telemetry
Respiratory: 2 L/min nasal cannula
Mobility: 1-person assist
Diet: Cardiac diet

ACCESS
- 20G peripheral IV, left forearm

MEDICATIONS OF NOTE
- Furosemide 40 mg IV BID

THIS SHIFT
- Furosemide given at 1800
- Intake 700 mL; urine output 900 mL this shift
- Daily weight completed

PENDING
- Morning BMP
- Daily weight

WARNINGS
--------
None
```

## Known versus unknown

A documented fact and a missing value are different things, and the program
keeps them apart.

```json
"respiratory": {"oxygen": false}
```

is **known**: the patient is documented as not receiving supplemental oxygen.
It renders `Respiratory: No supplemental oxygen documented` with no warning.

```json
"respiratory": null
```

is **unknown**: respiratory status was not provided. An absent key means the
same. It renders `Respiratory: Not documented` and adds the warning
`⚠ Respiratory assessment not documented`.

The program never turns unknown into an assumed value. It does not print
"Room air" unless the input says so. Lists follow the same rule: a missing or
`null` list renders `Not documented`, while an explicitly empty list `[]` is a
documented "nothing" and renders `None`.

## Synthetic patients

| File | ID | Scenario | Expected warnings |
|---|---|---|---|
| `data/simple_patient.json` | SYNTH-001 | Patient A. Routine postoperative recovery; every field present, no supplemental oxygen. | None |
| `data/chf_patient.json` | SYNTH-002 | Patient B. CHF exacerbation on telemetry with 2 L/min oxygen, IV diuretic, intake and output, daily weight, and pending labs. | None |
| `data/incomplete_patient.json` | SYNTH-003 | Patient C. Omits code status, mobility, and the respiratory assessment. | `⚠ Code status not documented`, `⚠ Respiratory assessment not documented`, `WARNING: Mobility status not documented.` |
| `data/complex_patient.json` | SYNTH-004 | Patient D. Oxygen documented without device or flow, and an IV medication with no vascular access. | Rule 1 and Rule 2 warnings |

Patient IDs use the `SYNTH-###` form. No names, dates of birth, MRNs, or
facility names appear anywhere, and a test scans `data/` to keep it that way.

## Rules

Warnings never stop the handoff. The block lists important-field warnings
first, in schema order, then rule warnings in rule order.

Important-field warnings fire when one of these fields is absent or `null`:

- `⚠ Code status not documented`
- `⚠ Neuro assessment not documented`
- `⚠ Respiratory assessment not documented`
- `⚠ Mobility status not documented` (replaced by Rule 3's wording)
- `⚠ Vascular access not documented`
- `⚠ Pending tasks not documented`

Clinical consistency rules are deterministic and intentionally simple:

1. **Oxygen.** `respiratory.oxygen` is `true` but `device` or `flow_lpm` is
   missing:
   `WARNING: Supplemental oxygen documented but device/flow information is incomplete.`
2. **IV medication.** A `medications_of_note` entry contains the
   word-bounded, case-sensitive token `IV` and `access` is missing or empty:
   `WARNING: IV medication listed but no vascular access documented.`
   `IVF` and `Ivabradine` do not match.
3. **Mobility.** `mobility` is missing:
   `WARNING: Mobility status not documented.`
   This replaces the mobility important-field warning so the same fact is not
   reported twice.
4. **Pending tasks.** A missing `pending_tasks` is never read as "nothing
   pending": the `PENDING` section shows `Not documented` and the
   important-field warning fires. An explicit `[]` shows `None` with no
   warning.

## Running tests

From this directory, with the virtual environment's interpreter:

```bash
python -m pytest -q
```

On Windows without activating: `.venv\Scripts\python.exe -m pytest -q`. The
suite covers the loader, validator, generator, rules, and CLI, byte-for-byte
snapshots of patients A and B in `tests/snapshots/`, a scan of `data/` for
real-patient identifiers, and a map from every test listed in spec section 12
to a named test. The hub's `tests/verify.ps1` runs the suite and the CLI on
patient B.

## Roadmap

| Version | Scope | Status |
|---|---|---|
| v0.1 | Deterministic handoff | This release |
| v0.2 | More clinical validation rules | Planned next |
| v0.3 | Simple web interface | Needs the owner's decision |
| v0.4 | FHIR resources | Later |
| v0.5 | LLM handoff generation | Later |
| v0.6 | Deterministic evaluation of AI output | Later |

The eventual research question: can an AI-generated nursing handoff be
automatically checked against the source clinical record to detect omissions,
hallucinations, and changes in clinical meaning?

## Disclaimer

Educational project. Every patient record here is synthetic; none describes a
real person. The generated text is not medical advice and must not be used to
care for a real patient. This software is not a medical device and is not
intended for clinical use.
