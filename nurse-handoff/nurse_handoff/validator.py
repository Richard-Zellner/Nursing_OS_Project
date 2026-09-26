"""Validate the documented field requirements of a synthetic patient record."""

from .schema import FIELD_TYPES, REQUIRED_FIELDS


def _is_expected_type(value, expected_type):
    """Check JSON value types without treating booleans as integers."""
    accepted_types = expected_type if isinstance(expected_type, tuple) else (expected_type,)
    return any(
        type(value) is accepted_type_item
        for accepted_type_item in accepted_types
    )


def _type_label(expected_type):
    """Return the human-readable type names used by validation errors."""
    if expected_type is str:
        return "a string"
    if expected_type is int:
        return "an integer"
    if expected_type is float:
        return "a number"
    if expected_type is bool:
        return "a boolean"
    if expected_type is dict:
        return "an object"
    if expected_type is list:
        return "a list"
    if isinstance(expected_type, tuple) and expected_type == (int, float):
        return "a number"
    return "the expected type"


def _field_value(record, field_path):
    """Get a schema field, returning None when any path component is absent."""
    value = record
    for component in field_path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(component)
    return value


def validate(record: dict) -> list[str]:
    """Return required-field and type errors in schema order.

    Missing and null values are accepted for optional fields. Empty strings
    are missing for required fields. This function reports errors only; it
    never coerces or fills in values.
    """
    errors = []

    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if value is None or value == "":
            errors.append(f"{field} is required")

    for field_path, expected_type in FIELD_TYPES.items():
        value = _field_value(record, field_path)
        if value is None:
            continue

        # A malformed parent object gets one error of its own; its nested
        # fields cannot be meaningfully inspected until it is an object.
        parent_path = field_path.rpartition(".")[0]
        if parent_path:
            parent_value = _field_value(record, parent_path)
            if not isinstance(parent_value, dict):
                continue

        if field_path in REQUIRED_FIELDS and value == "":
            continue
        if not _is_expected_type(value, expected_type):
            errors.append(f"{field_path} must be {_type_label(expected_type)}")
            continue

        # PATIENT-SCHEMA.md: age is an integer >= 0 and every list holds strings.
        if field_path == "age" and value < 0:
            errors.append("age must be a non-negative integer")
        if expected_type is list and not all(type(item) is str for item in value):
            errors.append(f"{field_path} must be a list of strings")

    return errors
