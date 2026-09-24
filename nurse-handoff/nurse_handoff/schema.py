"""Field metadata for the v0.1 synthetic patient record."""

# Keep these in the order used by PATIENT-SCHEMA.md and the handoff output.
REQUIRED_FIELDS = ["patient_id", "age", "primary_problem"]

# Values are the exact important-field warning lines, including the glyph.
# Dict insertion order preserves the warning order from the schema document.
IMPORTANT_FIELDS = {
    "code_status": "⚠ Code status not documented",
    "neuro": "⚠ Neuro assessment not documented",
    "respiratory": "⚠ Respiratory assessment not documented",
    "mobility": "⚠ Mobility status not documented",
    "access": "⚠ Vascular access not documented",
    "pending_tasks": "⚠ Pending tasks not documented",
}

OPTIONAL_FIELDS = ["cardiac", "diet", "medications_of_note", "recent_events"]

# Each JSON field path maps to its expected Python type. All fields may be
# absent or null; callers should skip type checks for those values. A tuple
# represents one of multiple accepted types, as for numeric flow_lpm values.
FIELD_TYPES = {
    "patient_id": str,
    "age": int,
    "primary_problem": str,
    "code_status": str,
    "neuro": str,
    "cardiac": str,
    "respiratory": dict,
    "respiratory.oxygen": bool,
    "respiratory.device": str,
    "respiratory.flow_lpm": (int, float),
    "mobility": str,
    "diet": str,
    "access": list,
    "medications_of_note": list,
    "recent_events": list,
    "pending_tasks": list,
}
