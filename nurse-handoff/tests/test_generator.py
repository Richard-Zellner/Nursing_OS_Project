"""Exact overview formatting, including undocumented code status."""

import json
from pathlib import Path

import pytest

from nurse_handoff.generator import render_assessment, render_overview


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
