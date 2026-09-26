"""Deterministic clinical consistency rules that return warning lines."""

import re

from .schema import IMPORTANT_FIELDS

OXYGEN_WARNING = (
    "WARNING: Supplemental oxygen documented but device/flow information "
    "is incomplete."
)
IV_ACCESS_WARNING = (
    "WARNING: IV medication listed but no vascular access documented."
)
MOBILITY_WARNING = "WARNING: Mobility status not documented."

# Case-sensitive, word-bounded: "IV" and "IV/PO" match; "IVF", "IVIG",
# "PIV", and "Ivabradine" do not.
_IV_TOKEN = re.compile(r"\bIV\b")


def check_oxygen(record: dict) -> list[str]:
    """Rule 1: documented supplemental oxygen needs a device and a flow rate.

    Only ``oxygen: true`` triggers the rule. An absent, null, or false
    ``oxygen`` value, or an absent respiratory object, emits nothing.
    """
    respiratory = record.get("respiratory")
    if not isinstance(respiratory, dict) or respiratory.get("oxygen") is not True:
        return []
    if respiratory.get("device") is None or respiratory.get("flow_lpm") is None:
        return [OXYGEN_WARNING]
    return []


def check_iv_access(record: dict) -> list[str]:
    """Rule 2: an IV medication needs documented vascular access.

    A medication matches only on the case-sensitive, word-bounded token
    ``IV``. Access that is absent, null, or an empty list counts as no
    documented access.
    """
    medications = record.get("medications_of_note")
    if medications is None:
        return []

    has_iv_medication = any(
        isinstance(medication, str) and _IV_TOKEN.search(medication)
        for medication in medications
    )
    if not has_iv_medication:
        return []

    access = record.get("access")
    if access is None or len(access) == 0:
        return [IV_ACCESS_WARNING]
    return []


def check_mobility(record: dict) -> list[str]:
    """Rule 3: an absent or null mobility status is reported, never assumed."""
    if record.get("mobility") is None:
        return [MOBILITY_WARNING]
    return []


def check_important_fields(record: dict) -> list[str]:
    """Return the glyph warning for each absent or null important field.

    Warnings follow schema order. An explicitly empty list, such as
    ``pending_tasks: []``, is documented as nothing and does not warn.
    """
    return [
        warning
        for field, warning in IMPORTANT_FIELDS.items()
        if record.get(field) is None
    ]


def collect_warnings(record: dict) -> list[str]:
    """Return important-field warnings, then rule warnings in rule order.

    Rule 3 and the mobility important-field warning describe the same fact,
    so only the rule wording is kept when mobility is not documented.
    """
    rule_warnings = (
        check_oxygen(record) + check_iv_access(record) + check_mobility(record)
    )
    field_warnings = check_important_fields(record)
    if MOBILITY_WARNING in rule_warnings:
        field_warnings = [
            warning
            for warning in field_warnings
            if warning != IMPORTANT_FIELDS["mobility"]
        ]
    return field_warnings + rule_warnings
