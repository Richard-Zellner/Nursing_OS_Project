"""Checked-in data is synthetic: no identifying keys and no birth dates."""

import json
import re
from pathlib import Path

import pytest


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILES = sorted(path for path in DATA_DIR.rglob("*") if path.is_file())
JSON_FILES = [path for path in DATA_FILES if path.suffix == ".json"]

FORBIDDEN_KEYS = {
    "name",
    "first_name",
    "last_name",
    "dob",
    "date_of_birth",
    "birth_date",
    "birthdate",
    "mrn",
    "ssn",
    "facility",
}

_MONTH = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?"
    r"|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)
DATE_OF_BIRTH_PATTERNS = (
    re.compile(r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b"),
    re.compile(r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b"),
    re.compile(rf"\b{_MONTH}\.? \d{{1,2}}(?:st|nd|rd|th)?,? \d{{4}}\b", re.IGNORECASE),
    re.compile(rf"\b\d{{1,2}}(?:st|nd|rd|th)? {_MONTH}\.?,? \d{{4}}\b", re.IGNORECASE),
    re.compile(r"\b(?:dob|d\.o\.b\.|date of birth|born)\b", re.IGNORECASE),
)


def _all_keys(value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield key
            yield from _all_keys(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from _all_keys(nested_value)


def _looks_like_date_of_birth(text):
    return any(pattern.search(text) for pattern in DATE_OF_BIRTH_PATTERNS)


def test_data_directory_holds_the_synthetic_patients():
    assert len(JSON_FILES) >= 4


@pytest.mark.parametrize("path", JSON_FILES, ids=lambda path: path.name)
def test_data_files_contain_no_forbidden_keys(path):
    record = json.loads(path.read_text(encoding="utf-8"))
    keys = {key.casefold() for key in _all_keys(record)}

    assert keys.isdisjoint(FORBIDDEN_KEYS)
    assert not any("birth" in key for key in keys)


@pytest.mark.parametrize("path", DATA_FILES, ids=lambda path: path.name)
def test_data_files_contain_nothing_matching_a_date_of_birth(path):
    text = path.read_text(encoding="utf-8")

    assert not _looks_like_date_of_birth(text)


@pytest.mark.parametrize("path", JSON_FILES, ids=lambda path: path.name)
def test_patient_ids_are_synthetic(path):
    record = json.loads(path.read_text(encoding="utf-8"))

    assert re.fullmatch(r"SYNTH-\d{3}", record["patient_id"])


@pytest.mark.parametrize(
    "text",
    [
        '"dob": "1950-03-14"',
        "1950/03/14",
        "03/14/1950",
        "3-14-50",
        "14.03.1950",
        "March 14, 1950",
        "Mar 14 1950",
        "14th March 1950",
        "Date of birth unknown",
        "born in the spring",
    ],
)
def test_date_of_birth_detector_catches_birth_dates(text):
    assert _looks_like_date_of_birth(text)


@pytest.mark.parametrize(
    "text",
    [
        "Furosemide given at 1800",
        "Intake 700 mL; urine output 900 mL this shift",
        "Synthetic medication 20 mg IV once",
        "20G peripheral IV, left forearm",
        "Respiratory: 2.5 L/min nasal cannula",
        "SYNTH-004",
        "Alert and oriented x4",
    ],
)
def test_date_of_birth_detector_ignores_clinical_text(text):
    assert not _looks_like_date_of_birth(text)
