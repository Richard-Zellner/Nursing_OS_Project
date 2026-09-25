"""Read synthetic patient JSON without filling in undocumented values."""

import json
from os import PathLike


class PatientFileError(Exception):
    """A patient file could not be read as a JSON object."""


def load_patient(path: str | PathLike[str]) -> dict:
    """Load one UTF-8 JSON object; field validation is a separate step."""
    try:
        with open(path, encoding="utf-8") as patient_file:
            record = json.load(patient_file)
    except FileNotFoundError as error:
        raise PatientFileError(f"file not found: {path}") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise PatientFileError(f"invalid JSON in {path}: {error}") from error
    except OSError as error:
        raise PatientFileError(f"could not read file: {path}: {error}") from error

    if not isinstance(record, dict):
        raise PatientFileError(f"invalid JSON in {path}: expected a JSON object")
    return record
