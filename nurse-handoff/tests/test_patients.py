"""The checked-in synthetic patient records follow the v0.1 constraints."""

import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
PATIENT_FILES = (
    "simple_patient.json",
    "chf_patient.json",
    "incomplete_patient.json",
    "complex_patient.json",
)
FORBIDDEN_KEYS = {"name", "dob", "mrn", "facility"}


def _all_keys(value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield key
            yield from _all_keys(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from _all_keys(nested_value)


def test_four_synthetic_patients_parse_with_sequential_ids():
    records = [
        json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
        for filename in PATIENT_FILES
    ]

    assert [record["patient_id"] for record in records] == [
        "SYNTH-001",
        "SYNTH-002",
        "SYNTH-003",
        "SYNTH-004",
    ]


def test_synthetic_patients_contain_no_forbidden_keys():
    for filename in PATIENT_FILES:
        record = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
        assert FORBIDDEN_KEYS.isdisjoint(key.casefold() for key in _all_keys(record))


def test_incomplete_patient_omits_code_status_mobility_and_respiratory():
    record = json.loads(
        (DATA_DIR / "incomplete_patient.json").read_text(encoding="utf-8")
    )

    assert {"code_status", "mobility", "respiratory"}.isdisjoint(record)
