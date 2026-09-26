"""The command-line interface prints exact reports, errors, and exit codes."""

import subprocess
import sys
from pathlib import Path

import pytest


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"
NO_WARNINGS_BLOCK = "\nWARNINGS\n--------\nNone\n"

INCOMPLETE_PATIENT_OUTPUT = (
    "NURSING HANDOFF\n"
    "---------------\n"
    "\n"
    "68-year-old — Code status: Not documented\n"
    "Primary problem: Fluid volume excess\n"
    "\n"
    "ASSESSMENT\n"
    "Neuro: Awake and responsive\n"
    "Cardiac: Regular rhythm\n"
    "Respiratory: Not documented\n"
    "Mobility: Not documented\n"
    "Diet: Low-sodium diet\n"
    "\n"
    "ACCESS\n"
    "- Peripheral IV, right forearm\n"
    "\n"
    "MEDICATIONS OF NOTE\n"
    "None\n"
    "\n"
    "THIS SHIFT\n"
    "- Intake and output recorded this shift\n"
    "\n"
    "PENDING\n"
    "- Review morning laboratory results\n"
    "\n"
    "WARNINGS\n"
    "--------\n"
    "⚠ Code status not documented\n"
    "⚠ Respiratory assessment not documented\n"
    "WARNING: Mobility status not documented.\n"
)

COMPLEX_PATIENT_OUTPUT = (
    "NURSING HANDOFF\n"
    "---------------\n"
    "\n"
    "61-year-old — Full Code\n"
    "Primary problem: Synthetic respiratory assessment scenario\n"
    "\n"
    "ASSESSMENT\n"
    "Neuro: Alert and oriented\n"
    "Cardiac: Regular rhythm\n"
    "Respiratory: Supplemental oxygen (device not documented)\n"
    "Mobility: Independent\n"
    "Diet: Regular diet\n"
    "\n"
    "ACCESS\n"
    "None\n"
    "\n"
    "MEDICATIONS OF NOTE\n"
    "- Synthetic medication 20 mg IV once\n"
    "\n"
    "THIS SHIFT\n"
    "None\n"
    "\n"
    "PENDING\n"
    "None\n"
    "\n"
    "WARNINGS\n"
    "--------\n"
    "WARNING: Supplemental oxygen documented but device/flow information is incomplete.\n"
    "WARNING: IV medication listed but no vascular access documented.\n"
)


def run_cli(*args):
    """Run ``python -m nurse_handoff`` from the package root and decode UTF-8."""
    completed = subprocess.run(
        [sys.executable, "-m", "nurse_handoff", *args],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        timeout=60,
    )
    return (
        completed.returncode,
        completed.stdout.decode("utf-8"),
        completed.stderr.decode("utf-8"),
    )


def _snapshot(name):
    return (SNAPSHOT_DIR / name).read_bytes().decode("utf-8")


def test_patient_a_prints_handoff_and_no_warnings():
    code, stdout, stderr = run_cli("data/simple_patient.json")

    assert (code, stderr) == (0, "")
    assert stdout == _snapshot("simple_patient.txt") + NO_WARNINGS_BLOCK


def test_patient_b_prints_handoff_and_warnings_none():
    code, stdout, stderr = run_cli("data/chf_patient.json")

    assert (code, stderr) == (0, "")
    assert stdout == _snapshot("chf_patient.txt") + NO_WARNINGS_BLOCK
    assert stdout.endswith("\n\nWARNINGS\n--------\nNone\n")


def test_patient_c_prints_handoff_with_missing_field_warnings():
    code, stdout, stderr = run_cli("data/incomplete_patient.json")

    assert (code, stderr) == (0, "")
    assert stdout == INCOMPLETE_PATIENT_OUTPUT


def test_patient_d_prints_both_rule_warnings():
    code, stdout, stderr = run_cli("data/complex_patient.json")

    assert (code, stderr) == (0, "")
    assert stdout == COMPLEX_PATIENT_OUTPUT


@pytest.mark.parametrize(
    "filename",
    [
        "simple_patient.json",
        "chf_patient.json",
        "incomplete_patient.json",
        "complex_patient.json",
    ],
)
def test_cli_output_is_lf_only_and_never_assumes_room_air(filename):
    completed = subprocess.run(
        [sys.executable, "-m", "nurse_handoff", f"data/{filename}"],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        timeout=60,
    )

    assert completed.returncode == 0
    assert b"\r" not in completed.stdout
    assert completed.stdout.endswith(b"\n")
    assert not completed.stdout.endswith(b"\n\n")
    assert b"Room air" not in completed.stdout


def test_missing_file_exits_2_with_error_and_no_handoff():
    assert not (PACKAGE_ROOT / "data" / "missing_patient.json").exists()

    code, stdout, stderr = run_cli("data/missing_patient.json")

    assert code == 2
    assert stdout == ""
    assert stderr == "ERROR: file not found: data/missing_patient.json\n"


def test_invalid_json_exits_2_with_error_and_no_handoff(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"patient_id": "SYNTH-900",}', encoding="utf-8")

    code, stdout, stderr = run_cli(str(path))

    assert code == 2
    assert stdout == ""
    assert stderr.startswith(f"ERROR: invalid JSON in {path}: ")
    assert stderr.endswith("\n")
    assert stderr.count("\n") == 1


def test_missing_required_fields_exit_1_with_ordered_errors(tmp_path):
    path = tmp_path / "missing_required.json"
    path.write_text('{"age": 72, "code_status": "Full Code"}', encoding="utf-8")

    code, stdout, stderr = run_cli(str(path))

    assert code == 1
    assert stdout == ""
    assert stderr == (
        "ERROR: patient_id is required\n"
        "ERROR: primary_problem is required\n"
    )


def test_type_error_exits_1_without_coercion(tmp_path):
    path = tmp_path / "wrong_type.json"
    path.write_text(
        '{"patient_id": "SYNTH-900", "age": "seventy", '
        '"primary_problem": "Synthetic test condition"}',
        encoding="utf-8",
    )

    code, stdout, stderr = run_cli(str(path))

    assert code == 1
    assert stdout == ""
    assert stderr == "ERROR: age must be an integer\n"


@pytest.mark.parametrize(
    ("fields", "error"),
    [
        ('"age": -1', "ERROR: age must be a non-negative integer\n"),
        ('"age": 35, "medications_of_note": [17]',
         "ERROR: medications_of_note must be a list of strings\n"),
    ],
)
def test_out_of_schema_values_exit_1_without_a_handoff(tmp_path, fields, error):
    path = tmp_path / "out_of_schema.json"
    path.write_text(
        '{"patient_id": "SYNTH-900", "primary_problem": "Synthetic test condition", '
        + fields + "}",
        encoding="utf-8",
    )

    code, stdout, stderr = run_cli(str(path))

    assert code == 1
    assert stdout == ""
    assert stderr == error


@pytest.mark.parametrize(
    "args",
    [(), ("data/simple_patient.json", "data/chf_patient.json")],
    ids=["no-path", "two-paths"],
)
def test_wrong_argument_count_prints_usage_and_exits_2(args):
    code, stdout, stderr = run_cli(*args)

    assert code == 2
    assert stdout == ""
    assert stderr == "Usage: python -m nurse_handoff <patient.json>\n"
