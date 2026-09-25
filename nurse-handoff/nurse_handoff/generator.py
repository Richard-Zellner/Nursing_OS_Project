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


def render_assessment(record: dict) -> str:
    """Render the assessment section without filling in undocumented data."""
    respiratory = record.get("respiratory")
    if not isinstance(respiratory, dict):
        respiratory_text = "Not documented"
    else:
        oxygen = respiratory.get("oxygen")
        if oxygen is True:
            device = respiratory.get("device")
            flow_lpm = respiratory.get("flow_lpm")
            if device is None:
                respiratory_text = "Supplemental oxygen (device not documented)"
            elif flow_lpm is None:
                respiratory_text = f"{device} (flow not documented)"
            else:
                respiratory_text = f"{flow_lpm:g} L/min {device}"
        elif oxygen is False:
            respiratory_text = "No supplemental oxygen documented"
        else:
            respiratory_text = "Not documented"

    lines = ["ASSESSMENT"]
    for field, label in (
        ("neuro", "Neuro"),
        ("cardiac", "Cardiac"),
    ):
        value = record.get(field)
        lines.append(f"{label}: {value if value is not None else 'Not documented'}")

    lines.append(f"Respiratory: {respiratory_text}")
    for field, label in (("mobility", "Mobility"), ("diet", "Diet")):
        value = record.get(field)
        lines.append(f"{label}: {value if value is not None else 'Not documented'}")

    return "\n".join(lines)


def render_list_section(title: str, items: list[str] | None) -> str:
    """Render a titled list while preserving the distinction between unknown and empty."""
    if items is None:
        body = "Not documented"
    elif not items:
        body = "None"
    else:
        body = "\n".join(f"- {item}" for item in items)

    return f"{title}\n{body}"


def render_handoff(record: dict) -> str:
    """Render the handoff sections in their fixed output order."""
    sections = [
        render_overview(record),
        render_assessment(record),
        render_list_section("ACCESS", record.get("access")),
        render_list_section(
            "MEDICATIONS OF NOTE", record.get("medications_of_note")
        ),
        render_list_section("THIS SHIFT", record.get("recent_events")),
        render_list_section("PENDING", record.get("pending_tasks")),
    ]
    return "\n\n".join(sections) + "\n"
