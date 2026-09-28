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
CODE_STATUS_WARNING = (
    "WARNING: Code status not documented; confirm before handoff."
)
TELEMETRY_WARNING = (
    "WARNING: Telemetry documented but no cardiac rhythm documented."
)
DIURETIC_WARNING = (
    "WARNING: Diuretic listed but no urine output documented this shift."
)
NPO_CONFLICT_WARNING = (
    "WARNING: NPO diet documented but a meal-related task is pending."
)
FALL_RISK_WARNING = (
    "WARNING: Fall risk documented but mobility status not documented."
)

# Case-sensitive, word-bounded: "IV" and "IV/PO" match; "IVF", "IVIG",
# "PIV", and "Ivabradine" do not.
_IV_TOKEN = re.compile(r"\bIV\b")
_TELEMETRY_TOKEN = re.compile(r"\btelemetry\b", re.IGNORECASE)
_DIURETIC_NAMES = ("furosemide", "bumetanide", "torsemide")
_URINE_OUTPUT_PHRASE = "urine output"
_UO_ABBREVIATION = "UO"


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


def check_code_status(record: dict) -> list[str]:
    """Rule 5: missing code status gets an additional, intentional warning."""
    if record.get("code_status") is None:
        return [CODE_STATUS_WARNING]
    return []


def check_telemetry(record: dict) -> list[str]:
    """Rule 6: telemetry without a documented cardiac rhythm gets a warning."""
    monitoring = record.get("monitoring")
    if not isinstance(monitoring, str) or not _TELEMETRY_TOKEN.search(monitoring):
        return []
    if record.get("cardiac") is None:
        return [TELEMETRY_WARNING]
    return []


def check_diuretic_output(record: dict) -> list[str]:
    """Rule 7: a listed loop diuretic needs documented urine output this shift."""
    medications = record.get("medications_of_note")
    if not isinstance(medications, list):
        return []

    has_diuretic = any(
        isinstance(medication, str)
        and any(name in medication.casefold() for name in _DIURETIC_NAMES)
        for medication in medications
    )
    if not has_diuretic:
        return []

    recent_events = record.get("recent_events")
    has_urine_output = isinstance(recent_events, list) and any(
        isinstance(event, str)
        and (
            _URINE_OUTPUT_PHRASE in event or _UO_ABBREVIATION in event
        )
        for event in recent_events
    )
    if not has_urine_output:
        return [DIURETIC_WARNING]
    return []


def check_npo_conflict(record: dict) -> list[str]:
    """Rule 8: flag meal-related pending tasks when the diet documents NPO."""
    diet = record.get("diet")
    if not isinstance(diet, str) or "npo" not in diet.casefold():
        return []

    pending_tasks = record.get("pending_tasks")
    if not isinstance(pending_tasks, list):
        return []
    has_meal_related_task = any(
        isinstance(task, str)
        and ("meal" in task.casefold() or "tray" in task.casefold())
        for task in pending_tasks
    )
    return [NPO_CONFLICT_WARNING] if has_meal_related_task else []


def check_fall_risk(record: dict) -> list[str]:
    """Rule 9: documented fall risk needs a documented mobility status."""
    if record.get("fall_risk") is not True or record.get("mobility") is not None:
        return []
    return [FALL_RISK_WARNING]


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
        check_oxygen(record)
        + check_iv_access(record)
        + check_mobility(record)
        + check_code_status(record)
        + check_telemetry(record)
        + check_diuretic_output(record)
        + check_npo_conflict(record)
        + check_fall_risk(record)
    )
    field_warnings = check_important_fields(record)
    if MOBILITY_WARNING in rule_warnings:
        field_warnings = [
            warning
            for warning in field_warnings
            if warning != IMPORTANT_FIELDS["mobility"]
        ]
    return field_warnings + rule_warnings
