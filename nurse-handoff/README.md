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

## Usage

```text
python -m nurse_handoff <patient.json>
```

The command-line interface is under construction.
