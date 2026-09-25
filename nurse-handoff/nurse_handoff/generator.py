"""Render deterministic sections of a synthetic nursing handoff."""


def render_overview(record: dict) -> str:
    """Render the handoff heading and patient overview from a validated record."""
    code_status = record.get("code_status")
    if code_status is None:
        status_text = "Code status: Not documented"
    else:
        status_text = code_status

    return (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        f"{record['age']}-year-old — {status_text}\n"
        f"Primary problem: {record['primary_problem']}"
    )
