"""The package README keeps every required section and an accurate sample."""

import re
from pathlib import Path

import pytest

from nurse_handoff.rules import (
    CODE_STATUS_WARNING,
    FALL_RISK_WARNING,
    IV_ACCESS_WARNING,
    MOBILITY_WARNING,
    OXYGEN_WARNING,
    TELEMETRY_WARNING,
)
from nurse_handoff.schema import IMPORTANT_FIELDS
from nurse_handoff import __version__


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
README = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"
REQUIRED_SECTIONS = (
    "## Install",
    "## Usage",
    "## Sample output",
    "## Known versus unknown",
    "## Synthetic patients",
    "## Rules",
    "## Running tests",
    "## Version history",
    "## Roadmap",
    "## Disclaimer",
)


def _flatten(text):
    return " ".join(text.split())


@pytest.mark.parametrize("heading", REQUIRED_SECTIONS)
def test_readme_has_required_section(heading):
    assert f"\n{heading}\n" in README


def test_readme_opens_with_the_spec_opening():
    assert README.startswith("# Nurse Handoff\n\n**Nurse Handoff** is an educational prototype")
    assert _flatten(
        "Its primary design principle is: *the system may organize documented "
        "information, but it must not invent undocumented information.*"
    ) in _flatten(README)
    assert _flatten(
        "All patient records included in this repository are synthetic and the "
        "software is not intended for clinical use."
    ) in _flatten(README)


def test_readme_install_uses_venv_and_requirements():
    assert "python -m venv .venv\n" in README
    assert "pip install -r requirements.txt\n" in README


def test_readme_version_history_matches_package_version():
    assert __version__ == "0.2.0-dev"
    assert "Version 0.2.0-dev." in README
    assert "| 0.1.0 | Released 2026-09-26 | Deterministic handoff |" in README
    assert "| 0.2.0-dev | In development | More clinical validation rules |" in README


def test_readme_sample_output_matches_patient_b_cli_output():
    match = re.search(r"\n## Sample output\n.*?```text\n(.*?)```\n", README, re.DOTALL)
    expected = (SNAPSHOT_DIR / "chf_patient.txt").read_bytes().decode("utf-8") + (
        "\nWARNINGS\n--------\nNone\n"
    )

    assert match is not None
    assert match.group(1) == expected


def test_readme_explains_oxygen_false_versus_respiratory_null():
    assert '"respiratory": {"oxygen": false}' in README
    assert '"respiratory": null' in README
    assert "Respiratory: No supplemental oxygen documented" in README
    assert "Respiratory: Not documented" in README


def test_readme_lists_every_warning_verbatim():
    for warning in (
        *IMPORTANT_FIELDS.values(),
        OXYGEN_WARNING,
        IV_ACCESS_WARNING,
        MOBILITY_WARNING,
        CODE_STATUS_WARNING,
        TELEMETRY_WARNING,
        FALL_RISK_WARNING,
    ):
        assert warning in README


def test_readme_lists_all_four_synthetic_patients():
    for patient_id, filename in (
        ("SYNTH-001", "simple_patient.json"),
        ("SYNTH-002", "chf_patient.json"),
        ("SYNTH-003", "incomplete_patient.json"),
        ("SYNTH-004", "complex_patient.json"),
    ):
        assert f"| `data/{filename}` | {patient_id} |" in README
