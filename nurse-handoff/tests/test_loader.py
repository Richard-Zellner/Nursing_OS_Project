"""Loading preserves documented values and reports unusable input files."""

import json
from pathlib import Path

import pytest

from nurse_handoff.loader import PatientFileError, load_patient


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@pytest.mark.parametrize(
    "filename",
    (
        "simple_patient.json",
        "chf_patient.json",
        "incomplete_patient.json",
        "complex_patient.json",
    ),
)
def test_loads_checked_in_synthetic_patients(filename):
    path = DATA_DIR / filename

    assert load_patient(path) == json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path_type", (str, Path))
def test_load_preserves_missing_null_false_empty_and_unicode(tmp_path, path_type):
    path = tmp_path / "synthetic.json"
    path.write_text(
        '{"patient_id":"SYNTH-099","age":0,"primary_problem":"Synthetic test",'
        '"code_status":null,"respiratory":{"oxygen":false},'
        '"pending_tasks":[],"extension":"Synthetic \u2014 test"}',
        encoding="utf-8",
    )

    record = load_patient(path_type(path))

    assert record == {
        "patient_id": "SYNTH-099",
        "age": 0,
        "primary_problem": "Synthetic test",
        "code_status": None,
        "respiratory": {"oxygen": False},
        "pending_tasks": [],
        "extension": "Synthetic \u2014 test",
    }
    assert "mobility" not in record


def test_empty_object_is_left_for_field_validation(tmp_path):
    path = tmp_path / "empty_object.json"
    path.write_text("{}", encoding="utf-8")

    assert load_patient(path) == {}


def test_missing_file_has_useful_error(tmp_path):
    path = tmp_path / "missing.json"

    with pytest.raises(PatientFileError) as caught:
        load_patient(path)

    assert str(caught.value) == f"file not found: {path}"


@pytest.mark.parametrize("contents", ('{"age": 72,}', "", "{} trailing"))
def test_invalid_json_has_path_and_parser_error(tmp_path, contents):
    path = tmp_path / "invalid.json"
    path.write_text(contents, encoding="utf-8")

    with pytest.raises(PatientFileError) as caught:
        load_patient(path)

    assert isinstance(caught.value.__cause__, json.JSONDecodeError)
    assert str(caught.value) == f"invalid JSON in {path}: {caught.value.__cause__}"
    assert "line 1 column" in str(caught.value)


@pytest.mark.parametrize(
    "contents", ("[]", "[{}]", '"text"', "72", "1.5", "true", "false", "null")
)
def test_top_level_non_object_is_rejected(tmp_path, contents):
    path = tmp_path / "non_object.json"
    path.write_text(contents, encoding="utf-8")

    with pytest.raises(PatientFileError) as caught:
        load_patient(path)

    assert str(caught.value) == f"invalid JSON in {path}: expected a JSON object"


def test_invalid_utf8_is_reported_as_malformed_input(tmp_path):
    path = tmp_path / "invalid_encoding.json"
    path.write_bytes(b'{"extension":"\xff"}')

    with pytest.raises(PatientFileError) as caught:
        load_patient(path)

    assert isinstance(caught.value.__cause__, UnicodeDecodeError)
    assert str(caught.value).startswith(f"invalid JSON in {path}: ")


def test_directory_path_has_useful_read_error(tmp_path):
    with pytest.raises(PatientFileError) as caught:
        load_patient(tmp_path)

    assert isinstance(caught.value.__cause__, OSError)
    assert str(caught.value).startswith(f"could not read file: {tmp_path}: ")
