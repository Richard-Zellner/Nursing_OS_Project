"""Clinical consistency rules emit exact spec wording and never infer facts."""

from pathlib import Path

import pytest

from nurse_handoff.generator import render_handoff
from nurse_handoff.loader import load_patient
from nurse_handoff.rules import (
    IV_ACCESS_WARNING,
    MOBILITY_WARNING,
    NPO_CONFLICT_WARNING,
    OXYGEN_WARNING,
    CODE_STATUS_WARNING,
    DIURETIC_WARNING,
    TELEMETRY_WARNING,
    check_code_status,
    check_diuretic_output,
    check_important_fields,
    check_iv_access,
    check_mobility,
    check_npo_conflict,
    check_oxygen,
    check_telemetry,
    collect_warnings,
)


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MINIMAL_RECORD = {
    "patient_id": "SYNTH-900",
    "age": 48,
    "primary_problem": "Synthetic test condition",
}
PENDING_WARNING = "⚠ Pending tasks not documented"
CODE_STATUS_FIELD_WARNING = "⚠ Code status not documented"


def test_oxygen_warning_uses_exact_spec_wording():
    spec_wording = "WARNING: Supplemental oxygen documented but device/flow information is incomplete."

    assert OXYGEN_WARNING == spec_wording


@pytest.mark.parametrize(
    "respiratory",
    [
        {"oxygen": True, "device": None, "flow_lpm": 2},
        {"oxygen": True, "flow_lpm": 2},
    ],
    ids=["device-null", "device-absent"],
)
def test_oxygen_without_device_warns(respiratory):
    assert check_oxygen({"respiratory": respiratory}) == [OXYGEN_WARNING]


@pytest.mark.parametrize(
    "respiratory",
    [
        {"oxygen": True, "device": "nasal cannula", "flow_lpm": None},
        {"oxygen": True, "device": "nasal cannula"},
    ],
    ids=["flow-null", "flow-absent"],
)
def test_oxygen_without_flow_warns(respiratory):
    assert check_oxygen({"respiratory": respiratory}) == [OXYGEN_WARNING]


@pytest.mark.parametrize(
    "respiratory",
    [
        {"oxygen": True, "device": None, "flow_lpm": None},
        {"oxygen": True},
    ],
    ids=["both-null", "both-absent"],
)
def test_oxygen_without_device_or_flow_warns_once(respiratory):
    assert check_oxygen({"respiratory": respiratory}) == [OXYGEN_WARNING]


def test_oxygen_with_device_and_flow_does_not_warn():
    record = {
        "respiratory": {"oxygen": True, "device": "nasal cannula", "flow_lpm": 2}
    }

    assert check_oxygen(record) == []


@pytest.mark.parametrize(
    "respiratory",
    [
        {"oxygen": False},
        {"oxygen": False, "device": None, "flow_lpm": None},
    ],
    ids=["false-only", "false-with-null-details"],
)
def test_oxygen_false_does_not_warn(respiratory):
    assert check_oxygen({"respiratory": respiratory}) == []


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"respiratory": None},
        {"respiratory": {}},
        {"respiratory": {"oxygen": None, "device": None, "flow_lpm": None}},
    ],
    ids=["respiratory-absent", "respiratory-null", "oxygen-absent", "oxygen-null"],
)
def test_unknown_oxygen_status_does_not_warn(record):
    assert check_oxygen(record) == []


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("simple_patient.json", []),
        ("chf_patient.json", []),
        ("incomplete_patient.json", []),
        ("complex_patient.json", [OXYGEN_WARNING]),
    ],
)
def test_oxygen_rule_on_synthetic_patients(filename, expected):
    assert check_oxygen(load_patient(DATA_DIR / filename)) == expected


def test_iv_access_warning_uses_exact_spec_wording():
    spec_wording = "WARNING: IV medication listed but no vascular access documented."

    assert IV_ACCESS_WARNING == spec_wording


@pytest.mark.parametrize(
    "access_fields",
    [{}, {"access": None}, {"access": []}],
    ids=["access-absent", "access-null", "access-empty"],
)
@pytest.mark.parametrize(
    "medication",
    [
        "Furosemide 40 mg IV BID",
        "IV fluids at 75 mL/hr",
        "Synthetic medication given IV.",
        "Synthetic medication (IV) once",
        "Synthetic medication IV/PO",
    ],
    ids=["middle", "start", "before-period", "parenthesized", "slash"],
)
def test_iv_medication_without_access_warns(medication, access_fields):
    record = {"medications_of_note": ["Oral synthetic medication", medication]}
    record.update(access_fields)

    assert check_iv_access(record) == [IV_ACCESS_WARNING]


def test_several_iv_medications_warn_once():
    record = {
        "medications_of_note": ["Synthetic A 1 mg IV", "Synthetic B 2 mg IV"],
        "access": [],
    }

    assert check_iv_access(record) == [IV_ACCESS_WARNING]


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"medications_of_note": None},
        {"medications_of_note": []},
        {"medications_of_note": [], "access": []},
    ],
    ids=["meds-absent", "meds-null", "meds-empty", "meds-and-access-empty"],
)
def test_no_medications_do_not_warn(record):
    assert check_iv_access(record) == []


def test_medications_without_iv_do_not_warn():
    record = {
        "medications_of_note": ["Synthetic medication 10 mg PO daily"],
        "access": [],
    }

    assert check_iv_access(record) == []


@pytest.mark.parametrize(
    "medication",
    [
        "IVF at 75 mL/hr",
        "Ivabradine 5 mg PO BID",
        "IVIG infusion scheduled",
        "PIV flush",
        "Synthetic medication iv once",
        "Synthetic medication Iv once",
    ],
    ids=["ivf", "ivabradine", "ivig", "piv", "lowercase", "mixed-case"],
)
def test_iv_false_positives_do_not_warn(medication):
    record = {"medications_of_note": [medication], "access": []}

    assert check_iv_access(record) == []


def test_iv_medication_with_access_does_not_warn():
    record = {
        "medications_of_note": ["Furosemide 40 mg IV BID"],
        "access": ["20G peripheral IV, left forearm"],
    }

    assert check_iv_access(record) == []


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("simple_patient.json", []),
        ("chf_patient.json", []),
        ("incomplete_patient.json", []),
        ("complex_patient.json", [IV_ACCESS_WARNING]),
    ],
)
def test_iv_access_rule_on_synthetic_patients(filename, expected):
    assert check_iv_access(load_patient(DATA_DIR / filename)) == expected


def test_mobility_warning_uses_exact_spec_wording():
    assert MOBILITY_WARNING == "WARNING: Mobility status not documented."


@pytest.mark.parametrize(
    "record",
    [{}, {"mobility": None}],
    ids=["mobility-absent", "mobility-null"],
)
def test_missing_mobility_warns(record):
    assert check_mobility(record) == [MOBILITY_WARNING]


def test_documented_mobility_does_not_warn():
    assert check_mobility({"mobility": "1-person assist"}) == []


def test_code_status_warning_uses_exact_rule_5_wording():
    assert (
        CODE_STATUS_WARNING
        == "WARNING: Code status not documented; confirm before handoff."
    )


@pytest.mark.parametrize(
    "record",
    [{}, {"code_status": None}],
    ids=["code-status-absent", "code-status-null"],
)
def test_missing_code_status_emits_rule_5_warning(record):
    assert check_code_status(record) == [CODE_STATUS_WARNING]


def test_documented_code_status_does_not_emit_rule_5_warning():
    assert check_code_status({"code_status": "Full Code"}) == []


def test_telemetry_warning_uses_exact_rule_6_wording():
    assert (
        TELEMETRY_WARNING
        == "WARNING: Telemetry documented but no cardiac rhythm documented."
    )


@pytest.mark.parametrize(
    "monitoring",
    ["telemetry", "Continuous telemetry monitoring", "Telemetry"],
    ids=["exact-token", "in-sentence", "capitalized-token"],
)
def test_telemetry_without_cardiac_rhythm_warns(monitoring):
    assert check_telemetry({"monitoring": monitoring}) == [TELEMETRY_WARNING]


def test_null_cardiac_rhythm_with_telemetry_warns():
    assert check_telemetry(
        {"monitoring": "Telemetry monitoring", "cardiac": None}
    ) == [TELEMETRY_WARNING]


@pytest.mark.parametrize(
    "monitoring",
    ["telemetric monitoring", "nontelemetry monitoring"],
    ids=["longer-word", "embedded-token"],
)
def test_telemetry_rule_requires_a_whole_token(monitoring):
    assert check_telemetry({"monitoring": monitoring}) == []


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"monitoring": None},
        {"monitoring": "continuous cardiac monitoring"},
        {"monitoring": "Telemetry monitoring", "cardiac": "Normal sinus rhythm"},
    ],
    ids=["monitoring-absent", "monitoring-null", "other-monitoring", "rhythm-documented"],
)
def test_telemetry_rule_does_not_warn_without_both_conditions(record):
    assert check_telemetry(record) == []


def test_diuretic_warning_uses_exact_rule_7_wording():
    assert (
        DIURETIC_WARNING
        == "WARNING: Diuretic listed but no urine output documented this shift."
    )


@pytest.mark.parametrize(
    "medication",
    [
        "Furosemide 40 mg daily",
        "BUMETANIDE 1 mg daily",
        "Torsemide 20 mg daily",
    ],
    ids=["furosemide", "bumetanide-case-insensitive", "torsemide"],
)
@pytest.mark.parametrize(
    "recent_event_fields",
    [{}, {"recent_events": None}, {"recent_events": []}],
    ids=["events-absent", "events-null", "events-empty"],
)
def test_diuretic_without_recent_output_warns(medication, recent_event_fields):
    record = {"medications_of_note": [medication], **recent_event_fields}

    assert check_diuretic_output(record) == [DIURETIC_WARNING]


@pytest.mark.parametrize(
    "event",
    [
        "900 mL urine output this shift",
        "UO 900 mL this shift",
    ],
    ids=["phrase", "abbreviation"],
)
def test_documented_urine_output_suppresses_diuretic_warning(event):
    record = {
        "medications_of_note": ["Furosemide 40 mg IV"],
        "recent_events": ["Synthetic event", event],
    }

    assert check_diuretic_output(record) == []


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"medications_of_note": None},
        {"medications_of_note": []},
        {"medications_of_note": ["Synthetic medication 1 mg daily"]},
        {
            "medications_of_note": ["Synthetic medication 1 mg daily"],
            "recent_events": [],
        },
    ],
    ids=["meds-absent", "meds-null", "meds-empty", "non-diuretic", "no-diuretic"],
)
def test_no_diuretic_does_not_warn(record):
    assert check_diuretic_output(record) == []


def test_unrelated_recent_event_does_not_suppress_diuretic_warning():
    record = {
        "medications_of_note": ["Furosemide 40 mg daily"],
        "recent_events": ["Daily weight completed"],
    }

    assert check_diuretic_output(record) == [DIURETIC_WARNING]


def test_uo_is_matched_as_a_contained_abbreviation():
    record = {
        "medications_of_note": ["Torsemide 20 mg daily"],
        "recent_events": ["Synthetic UOstatus reviewed"],
    }

    assert check_diuretic_output(record) == []


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("simple_patient.json", []),
        ("chf_patient.json", []),
        ("incomplete_patient.json", []),
        ("complex_patient.json", []),
    ],
)
def test_diuretic_rule_on_synthetic_patients(filename, expected):
    assert check_diuretic_output(load_patient(DATA_DIR / filename)) == expected


def test_npo_conflict_warning_uses_exact_rule_8_wording():
    assert (
        NPO_CONFLICT_WARNING
        == "WARNING: NPO diet documented but a meal-related task is pending."
    )


@pytest.mark.parametrize(
    ("diet", "pending_tasks"),
    [
        ("NPO", ["Confirm meal delivery"]),
        ("Strict npo", ["Prepare a tray"]),
        ("NPO after midnight", ["Review MEAL order", "Other task"]),
    ],
    ids=["meal-task", "tray-task-case-insensitive", "match-once"],
)
def test_npo_with_meal_related_pending_task_warns(diet, pending_tasks):
    assert check_npo_conflict(
        {"diet": diet, "pending_tasks": pending_tasks}
    ) == [NPO_CONFLICT_WARNING]


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"diet": None, "pending_tasks": ["Prepare tray"]},
        {"diet": "Regular diet", "pending_tasks": ["Prepare tray"]},
        {"diet": "NPO", "pending_tasks": None},
        {"diet": "NPO", "pending_tasks": []},
        {"diet": "NPO", "pending_tasks": ["Obtain morning weight"]},
        {"diet": "NPO", "pending_tasks": [None, 42]},
    ],
    ids=[
        "both-absent",
        "diet-null",
        "non-npo-diet",
        "tasks-null",
        "tasks-empty",
        "unrelated-task",
        "non-string-tasks",
    ],
)
def test_npo_rule_does_not_warn_without_both_conditions(record):
    assert check_npo_conflict(record) == []


def test_rule_8_follows_rule_7_in_collected_warnings():
    record = {
        **MINIMAL_RECORD,
        "diet": "NPO",
        "medications_of_note": ["Furosemide 40 mg daily"],
        "pending_tasks": ["Arrange meal tray"],
    }

    assert collect_warnings(record)[-2:] == [
        DIURETIC_WARNING,
        NPO_CONFLICT_WARNING,
    ]


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("simple_patient.json", []),
        ("chf_patient.json", []),
        ("incomplete_patient.json", [MOBILITY_WARNING]),
        ("complex_patient.json", []),
    ],
)
def test_mobility_rule_on_synthetic_patients(filename, expected):
    assert check_mobility(load_patient(DATA_DIR / filename)) == expected


@pytest.mark.parametrize(
    "pending_fields",
    [{}, {"pending_tasks": None}],
    ids=["pending-absent", "pending-null"],
)
def test_missing_pending_tasks_render_not_documented_and_warn(pending_fields):
    record = {**MINIMAL_RECORD, **pending_fields}

    assert render_handoff(record).endswith("\n\nPENDING\nNot documented\n")
    assert PENDING_WARNING in check_important_fields(record)


def test_empty_pending_tasks_render_none_without_warning():
    record = {**MINIMAL_RECORD, "pending_tasks": []}

    assert render_handoff(record).endswith("\n\nPENDING\nNone\n")
    assert PENDING_WARNING not in check_important_fields(record)


def test_all_missing_important_fields_warn_in_schema_order():
    assert check_important_fields(MINIMAL_RECORD) == [
        "⚠ Code status not documented",
        "⚠ Neuro assessment not documented",
        "⚠ Respiratory assessment not documented",
        "⚠ Mobility status not documented",
        "⚠ Vascular access not documented",
        "⚠ Pending tasks not documented",
    ]


def test_null_important_fields_warn_like_absent_fields():
    record = {
        **MINIMAL_RECORD,
        "code_status": None,
        "neuro": None,
        "respiratory": None,
        "mobility": None,
        "access": None,
        "pending_tasks": None,
    }

    assert check_important_fields(record) == check_important_fields(MINIMAL_RECORD)


def test_documented_or_explicitly_empty_important_fields_do_not_warn():
    record = {
        **MINIMAL_RECORD,
        "code_status": "Full Code",
        "neuro": "Alert and oriented",
        "respiratory": {"oxygen": False},
        "mobility": "Independent",
        "access": [],
        "pending_tasks": [],
    }

    assert check_important_fields(record) == []


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("simple_patient.json", []),
        ("chf_patient.json", []),
        (
            "incomplete_patient.json",
            [
                CODE_STATUS_FIELD_WARNING,
                "⚠ Respiratory assessment not documented",
                MOBILITY_WARNING,
                CODE_STATUS_WARNING,
            ],
        ),
        ("complex_patient.json", [OXYGEN_WARNING, IV_ACCESS_WARNING]),
    ],
)
def test_collect_warnings_on_synthetic_patients(filename, expected):
    assert collect_warnings(load_patient(DATA_DIR / filename)) == expected


def test_collect_warnings_lists_field_warnings_before_rule_warnings():
    record = {
        **MINIMAL_RECORD,
        "respiratory": {"oxygen": True},
        "medications_of_note": [
            "Synthetic medication 1 mg IV once",
            "Furosemide 40 mg daily",
        ],
        "monitoring": "Telemetry",
    }

    assert collect_warnings(record) == [
        "⚠ Code status not documented",
        "⚠ Neuro assessment not documented",
        "⚠ Vascular access not documented",
        "⚠ Pending tasks not documented",
        OXYGEN_WARNING,
        IV_ACCESS_WARNING,
        MOBILITY_WARNING,
        CODE_STATUS_WARNING,
        TELEMETRY_WARNING,
        DIURETIC_WARNING,
    ]


def test_missing_mobility_prints_only_the_rule_wording():
    warnings = collect_warnings(MINIMAL_RECORD)

    assert MOBILITY_WARNING in warnings
    assert "⚠ Mobility status not documented" not in warnings
    assert warnings == [
        "⚠ Code status not documented",
        "⚠ Neuro assessment not documented",
        "⚠ Respiratory assessment not documented",
        "⚠ Vascular access not documented",
        "⚠ Pending tasks not documented",
        MOBILITY_WARNING,
        CODE_STATUS_WARNING,
    ]


def test_missing_code_status_keeps_both_field_and_rule_warnings():
    warnings = collect_warnings(MINIMAL_RECORD)

    assert warnings.count(CODE_STATUS_FIELD_WARNING) == 1
    assert warnings.count(CODE_STATUS_WARNING) == 1
    assert (
        warnings.index(CODE_STATUS_FIELD_WARNING)
        < warnings.index(CODE_STATUS_WARNING)
    )
    assert warnings[-1] == CODE_STATUS_WARNING
