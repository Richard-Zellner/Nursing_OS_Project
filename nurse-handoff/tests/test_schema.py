"""Schema metadata stays aligned with the patient schema document."""

from nurse_handoff.schema import (
    FIELD_TYPES,
    IMPORTANT_FIELDS,
    OPTIONAL_FIELDS,
    REQUIRED_FIELDS,
)


def test_required_fields_match_patient_schema():
    assert REQUIRED_FIELDS == ["patient_id", "age", "primary_problem"]


def test_important_fields_and_warnings_match_patient_schema():
    assert list(IMPORTANT_FIELDS.items()) == [
        ("code_status", "⚠ Code status not documented"),
        ("neuro", "⚠ Neuro assessment not documented"),
        ("respiratory", "⚠ Respiratory assessment not documented"),
        ("mobility", "⚠ Mobility status not documented"),
        ("access", "⚠ Vascular access not documented"),
        ("pending_tasks", "⚠ Pending tasks not documented"),
    ]


def test_optional_fields_and_expected_types_are_documented():
    assert OPTIONAL_FIELDS == ["cardiac", "diet", "medications_of_note", "recent_events"]
    assert FIELD_TYPES == {
        "patient_id": str,
        "age": int,
        "primary_problem": str,
        "code_status": str,
        "neuro": str,
        "cardiac": str,
        "respiratory": dict,
        "respiratory.oxygen": bool,
        "respiratory.device": str,
        "respiratory.flow_lpm": (int, float),
        "mobility": str,
        "diet": str,
        "access": list,
        "medications_of_note": list,
        "recent_events": list,
        "pending_tasks": list,
    }
