"""Exact overview formatting, including undocumented code status."""

from nurse_handoff.generator import render_overview


def test_render_overview_with_code_status_is_byte_exact():
    record = {
        "age": 72,
        "code_status": "Full Code",
        "primary_problem": "CHF exacerbation",
    }

    assert render_overview(record) == (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        "72-year-old — Full Code\n"
        "Primary problem: CHF exacerbation"
    )


def test_render_overview_with_missing_code_status_is_byte_exact():
    record = {
        "age": 48,
        "primary_problem": "Synthetic test condition",
    }

    assert render_overview(record) == (
        "NURSING HANDOFF\n"
        "---------------\n"
        "\n"
        "48-year-old — Code status: Not documented\n"
        "Primary problem: Synthetic test condition"
    )


def test_null_code_status_is_not_documented():
    record = {
        "age": 48,
        "code_status": None,
        "primary_problem": "Synthetic test condition",
    }

    assert render_overview(record).splitlines()[3] == (
        "48-year-old — Code status: Not documented"
    )
