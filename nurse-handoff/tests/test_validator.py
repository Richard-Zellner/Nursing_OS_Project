"""Required values and field types are checked without changing the record."""

from nurse_handoff.schema import REQUIRED_FIELDS
from nurse_handoff.validator import validate


VALID_RECORD = {
    "patient_id": "SYNTH-900",
    "age": 48,
    "primary_problem": "Synthetic test condition",
    "code_status": "Full Code",
    "neuro": "Alert",
    "cardiac": "Regular rhythm",
    "respiratory": {"oxygen": False, "device": None, "flow_lpm": None},
    "mobility": "Independent",
    "diet": "Regular diet",
    "access": [],
    "medications_of_note": [],
    "recent_events": [],
    "pending_tasks": [],
}


def test_each_required_field_is_reported_when_missing():
    for field in REQUIRED_FIELDS:
        record = {key: value for key, value in VALID_RECORD.items() if key != field}
        assert validate(record) == [f"{field} is required"]


def _without(field):
    return {key: value for key, value in VALID_RECORD.items() if key != field}


def test_missing_patient_id_fails():
    assert validate(_without("patient_id")) == ["patient_id is required"]


def test_missing_age_fails():
    assert validate(_without("age")) == ["age is required"]


def test_missing_primary_problem_fails():
    assert validate(_without("primary_problem")) == ["primary_problem is required"]


def test_null_and_empty_required_fields_are_reported_as_required():
    for field in REQUIRED_FIELDS:
        for missing_value in (None, ""):
            record = {**VALID_RECORD, field: missing_value}
            assert validate(record) == [f"{field} is required"]


def test_all_missing_required_fields_are_reported_in_schema_order():
    assert validate({}) == [f"{field} is required" for field in REQUIRED_FIELDS]


def test_wrong_type_age_is_reported_as_integer_error():
    record = {**VALID_RECORD, "age": "forty-eight"}

    assert validate(record) == ["age must be an integer"]


def test_boolean_is_not_accepted_as_an_integer_age():
    record = {**VALID_RECORD, "age": True}

    assert validate(record) == ["age must be an integer"]


def test_wrong_types_in_other_schema_fields_are_reported():
    record = {**VALID_RECORD, "access": "20G"}

    assert validate(record) == ["access must be a list"]


def test_nested_respiratory_type_error_is_reported():
    record = {
        **VALID_RECORD,
        "respiratory": {"oxygen": "false", "device": None, "flow_lpm": None},
    }

    assert validate(record) == ["respiratory.oxygen must be a boolean"]


def test_missing_optional_values_and_unknown_keys_are_accepted():
    record = {
        "patient_id": "SYNTH-900",
        "age": 48,
        "primary_problem": "Synthetic test condition",
        "respiratory": None,
        "future_extension": {"value": "ignored"},
    }

    assert validate(record) == []


def test_clean_record_returns_no_errors():
    assert validate(VALID_RECORD) == []
