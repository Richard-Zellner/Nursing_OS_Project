"""Exact handoff formatting, including undocumented and missing data."""

import copy
import json
from pathlib import Path

import pytest

from nurse_handoff.generator import (
    render_assessment,
    render_handoff,
    render_list_section,
    render_overview,
    render_warnings,
)
from nurse_handoff.loader import load_patient


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_ROOT / "data"
SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"
PATIENT_FILES = (
    "simple_patient.json",
    "chf_patient.json",
    "incomplete_patient.json",
    "complex_patient.json",
)
SECTION_TITLES = (
    "NURSING HANDOFF",
    "ASSESSMENT",
    "ACCESS",
    "MEDICATIONS OF NOTE",
    "THIS SHIFT",
    "PENDING",
)
MINIMAL_RECORD = {
    "patient_id": "SYNTH-900",
    "age": 48,
    "primary_problem": "Synthetic test condition",
}


def test_render_overview_with_code_status_is_byte_exact():
    record = {
        "age": 72,
        "code_status": "Full Code",
        "primary_problem": "CHF exacerbation",
    }

    assert render_overview(record) == (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        "72-year-old — Full Code\n"
        "Primary problem: CHF exacerbation"
    )


def test_render_overview_with_missing_code_status_is_byte_exact():
    record = {
        "age": 48,
        "primary_problem": "Synthetic test condition",
    }

    assert render_overview(record) == (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        "48-year-old — Code status: Not documented\n"
        "Primary problem: Synthetic test condition"
    )


def test_null_code_status_is_not_documented():
    record = {
        "age": 48,
        "code_status": None,
        "primary_problem": "Synthetic test condition",
    }

    assert render_overview(record).splitlines()[3] == (
        "48-year-old — Code status: Not documented"
    )


@pytest.mark.parametrize(
    ("respiratory", "expected"),
    [
        (
            {"oxygen": True, "device": "nasal cannula", "flow_lpm": 2},
            "Respiratory: 2 L/min nasal cannula",
        ),
        (
            {"oxygen": True, "device": None, "flow_lpm": 2},
            "Respiratory: Supplemental oxygen (device not documented)",
        ),
        (
            {"oxygen": True, "flow_lpm": 2},
            "Respiratory: Supplemental oxygen (device not documented)",
        ),
        (
            {"oxygen": True, "device": "nasal cannula", "flow_lpm": None},
            "Respiratory: nasal cannula (flow not documented)",
        ),
        (
            {"oxygen": True, "device": "nasal cannula"},
            "Respiratory: nasal cannula (flow not documented)",
        ),
        (
            {"oxygen": False, "device": None, "flow_lpm": None},
            "Respiratory: No supplemental oxygen documented",
        ),
        ({}, "Respiratory: Not documented"),
        ({"oxygen": None}, "Respiratory: Not documented"),
        (None, "Respiratory: Not documented"),
    ],
    ids=[
        "oxygen-device-and-flow",
        "oxygen-null-device",
        "oxygen-missing-device",
        "oxygen-null-flow",
        "oxygen-missing-flow",
        "oxygen-false",
        "oxygen-missing",
        "oxygen-null",
        "respiratory-null",
    ],
)
def test_respiratory_rendering_table(respiratory, expected):
    assert render_assessment({"respiratory": respiratory}).splitlines()[3] == expected


def test_assessment_renders_each_line_and_keeps_null_data_unknown():
    assert render_assessment(
        {
            "neuro": "Alert and oriented x4",
            "cardiac": None,
            "respiratory": None,
            "mobility": "Independent",
            "diet": "Regular diet",
        }
    ) == (
        "ASSESSMENT\n"
        "Neuro: Alert and oriented x4\n"
        "Cardiac: Not documented\n"
        "Respiratory: Not documented\n"
        "Mobility: Independent\n"
        "Diet: Regular diet"
    )


def test_room_air_is_never_assumed_for_any_synthetic_patient_or_missing_data():
    data_dir = Path(__file__).parents[1] / "data"
    for patient_path in data_dir.glob("*.json"):
        record = json.loads(patient_path.read_text(encoding="utf-8"))
        assert "Room air" not in render_assessment(record)

    assert "Room air" not in render_assessment(
        {"neuro": "Not documented"}
    )


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        (None, "DETAILS\nNot documented"),
        ([], "DETAILS\nNone"),
        (["second", "first"], "DETAILS\n- second\n- first"),
    ],
    ids=["unknown", "explicitly-empty", "preserve-input-order"],
)
def test_render_list_section_distinguishes_unknown_empty_and_populated(items, expected):
    assert render_list_section("DETAILS", items) == expected


def test_render_handoff_uses_all_list_sections_in_fixed_order():
    handoff = render_handoff(
        {
            "age": 72,
            "code_status": "Full Code",
            "primary_problem": "Synthetic test condition",
            "neuro": "Alert and oriented x4",
            "cardiac": "Normal sinus rhythm",
            "respiratory": {"oxygen": False},
            "mobility": "Independent",
            "diet": "Regular diet",
            "access": ["20G peripheral IV", "18G peripheral IV"],
            "medications_of_note": ["Synthetic medication"],
            "recent_events": ["Synthetic event"],
            "pending_tasks": ["Synthetic task"],
        }
    )

    assert handoff == (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        "72-year-old — Full Code\n"
        "Primary problem: Synthetic test condition\n"
        "\n"
        "ASSESSMENT\n"
        "Neuro: Alert and oriented x4\n"
        "Cardiac: Normal sinus rhythm\n"
        "Respiratory: No supplemental oxygen documented\n"
        "Mobility: Independent\n"
        "Diet: Regular diet\n"
        "\n"
        "ACCESS\n"
        "- 20G peripheral IV\n"
        "- 18G peripheral IV\n"
        "\n"
        "MEDICATIONS OF NOTE\n"
        "- Synthetic medication\n"
        "\n"
        "THIS SHIFT\n"
        "- Synthetic event\n"
        "\n"
        "PENDING\n"
        "- Synthetic task\n"
    )


def _assert_report_layout(handoff):
    """Check the whole-report spacing rules from OUTPUT-FORMAT.md."""
    assert handoff.endswith("\n")
    assert not handoff.endswith("\n\n")
    assert "\r" not in handoff
    assert "\n\n\n" not in handoff

    lines = handoff.split("\n")[:-1]
    assert all(line == line.rstrip() for line in lines)

    title_indexes = [lines.index(title) for title in SECTION_TITLES]
    assert title_indexes == sorted(title_indexes)
    assert title_indexes[0] == 0
    for index in title_indexes[1:]:
        assert lines[index - 1] == ""
        assert lines[index - 2] != ""


@pytest.mark.parametrize("filename", PATIENT_FILES)
def test_render_handoff_runs_for_every_synthetic_patient(filename):
    handoff = render_handoff(load_patient(DATA_DIR / filename))

    _assert_report_layout(handoff)


def test_minimal_record_renders_not_documented_for_every_optional_line():
    handoff = render_handoff(MINIMAL_RECORD)

    _assert_report_layout(handoff)
    assert handoff == (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        "48-year-old — Code status: Not documented\n"
        "Primary problem: Synthetic test condition\n"
        "\n"
        "ASSESSMENT\n"
        "Neuro: Not documented\n"
        "Cardiac: Not documented\n"
        "Respiratory: Not documented\n"
        "Mobility: Not documented\n"
        "Diet: Not documented\n"
        "\n"
        "ACCESS\n"
        "Not documented\n"
        "\n"
        "MEDICATIONS OF NOTE\n"
        "Not documented\n"
        "\n"
        "THIS SHIFT\n"
        "Not documented\n"
        "\n"
        "PENDING\n"
        "Not documented\n"
    )


def test_null_optional_fields_render_like_absent_fields():
    null_record = {
        **MINIMAL_RECORD,
        "code_status": None,
        "neuro": None,
        "cardiac": None,
        "respiratory": None,
        "mobility": None,
        "diet": None,
        "access": None,
        "medications_of_note": None,
        "recent_events": None,
        "pending_tasks": None,
    }

    assert render_handoff(null_record) == render_handoff(MINIMAL_RECORD)


@pytest.mark.parametrize(
    ("filename", "snapshot"),
    [
        ("simple_patient.json", "simple_patient.txt"),
        ("chf_patient.json", "chf_patient.txt"),
    ],
    ids=["patient-a-simple", "patient-b-chf"],
)
def test_handoff_matches_snapshot_byte_for_byte(filename, snapshot):
    handoff = render_handoff(load_patient(DATA_DIR / filename))

    assert handoff.encode("utf-8") == (SNAPSHOT_DIR / snapshot).read_bytes()


@pytest.mark.parametrize(
    ("field", "expected_line"),
    [
        ("code_status", "72-year-old — Code status: Not documented"),
        ("neuro", "Neuro: Not documented"),
        ("cardiac", "Cardiac: Not documented"),
        ("respiratory", "Respiratory: Not documented"),
        ("mobility", "Mobility: Not documented"),
        ("diet", "Diet: Not documented"),
        ("access", "ACCESS\nNot documented"),
        ("medications_of_note", "MEDICATIONS OF NOTE\nNot documented"),
        ("recent_events", "THIS SHIFT\nNot documented"),
        ("pending_tasks", "PENDING\nNot documented"),
    ],
)
def test_missing_optional_field_does_not_crash(field, expected_line):
    record = load_patient(DATA_DIR / "chf_patient.json")
    del record[field]

    handoff = render_handoff(record)

    _assert_report_layout(handoff)
    assert f"\n{expected_line}\n" in handoff


def test_unknown_data_displays_not_documented():
    handoff = render_handoff(MINIMAL_RECORD)

    assert handoff.count("Not documented") == 10
    assert "None" not in handoff


@pytest.mark.parametrize(
    "respiratory",
    [None, {}, {"oxygen": None}, {"device": None, "flow_lpm": None}],
    ids=["null", "empty-object", "oxygen-null", "oxygen-missing"],
)
def test_unknown_oxygen_status_does_not_become_room_air(respiratory):
    handoff = render_handoff({**MINIMAL_RECORD, "respiratory": respiratory})

    assert "Room air" not in handoff
    assert "room air" not in handoff.casefold()
    assert "\nRespiratory: Not documented\n" in handoff


def test_render_handoff_is_deterministic_and_leaves_the_record_unchanged():
    record = load_patient(DATA_DIR / "incomplete_patient.json")
    original = copy.deepcopy(record)

    first = render_handoff(record)
    second = render_handoff(record)

    assert first == second
    assert record == original


def test_render_warnings_without_warnings_prints_none():
    assert render_warnings([]) == "WARNINGS\n--------\nNone"


def test_render_warnings_prints_one_line_per_warning_in_order():
    assert render_warnings(
        ["⚠ Code status not documented", "WARNING: Mobility status not documented."]
    ) == (
        "WARNINGS\n"
        "--------\n"
        "⚠ Code status not documented\n"
        "WARNING: Mobility status not documented."
    )


def test_age_appears():
    handoff = render_handoff({**MINIMAL_RECORD, "age": 0})

    assert "\n0-year-old — Code status: Not documented\n" in handoff


def test_diagnosis_appears():
    handoff = render_handoff(load_patient(DATA_DIR / "chf_patient.json"))

    assert "\nPrimary problem: CHF exacerbation\n" in handoff


@pytest.mark.parametrize(
    ("respiratory", "expected_line"),
    [
        (
            {"oxygen": True, "device": "nasal cannula", "flow_lpm": 2},
            "Respiratory: 2 L/min nasal cannula",
        ),
        (
            {"oxygen": True, "device": "high-flow nasal cannula", "flow_lpm": 2.5},
            "Respiratory: 2.5 L/min high-flow nasal cannula",
        ),
        ({"oxygen": False}, "Respiratory: No supplemental oxygen documented"),
    ],
    ids=["whole-number-flow", "decimal-flow", "oxygen-false"],
)
def test_oxygen_information_appears_correctly(respiratory, expected_line):
    handoff = render_handoff({**MINIMAL_RECORD, "respiratory": respiratory})

    assert f"\n{expected_line}\n" in handoff


def test_medications_appear():
    handoff = render_handoff(
        {
            **MINIMAL_RECORD,
            "medications_of_note": [
                "Furosemide 40 mg IV BID",
                "Synthetic medication 10 mg PO daily",
            ],
        }
    )

    assert (
        "\n\nMEDICATIONS OF NOTE\n"
        "- Furosemide 40 mg IV BID\n"
        "- Synthetic medication 10 mg PO daily\n\n"
    ) in handoff


def test_pending_tasks_appear():
    handoff = render_handoff(
        {**MINIMAL_RECORD, "pending_tasks": ["Morning BMP", "Daily weight"]}
    )

    assert handoff.endswith("\n\nPENDING\n- Morning BMP\n- Daily weight\n")
