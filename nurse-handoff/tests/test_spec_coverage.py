"""Every test listed in NURSE-HANDOFF-SPEC.md section 12 maps to a named test."""

import importlib

import pytest


# Spec section 12 bullet -> (test module, test function). Keep in spec order.
SPEC_SECTION_12_TESTS = {
    "Loader: valid JSON loads": (
        "test_loader",
        "test_loads_checked_in_synthetic_patients",
    ),
    "Loader: nonexistent file gives useful error": (
        "test_loader",
        "test_missing_file_has_useful_error",
    ),
    "Loader: invalid JSON gives useful error": (
        "test_loader",
        "test_invalid_json_has_path_and_parser_error",
    ),
    "Validator: missing patient ID fails": (
        "test_validator",
        "test_missing_patient_id_fails",
    ),
    "Validator: missing age fails": ("test_validator", "test_missing_age_fails"),
    "Validator: missing primary problem fails": (
        "test_validator",
        "test_missing_primary_problem_fails",
    ),
    "Generator: age appears": ("test_generator", "test_age_appears"),
    "Generator: diagnosis appears": ("test_generator", "test_diagnosis_appears"),
    "Generator: oxygen information appears correctly": (
        "test_generator",
        "test_oxygen_information_appears_correctly",
    ),
    "Generator: medications appear": ("test_generator", "test_medications_appear"),
    "Generator: pending tasks appear": (
        "test_generator",
        "test_pending_tasks_appear",
    ),
    "Missing data: missing optional field does not crash": (
        "test_generator",
        "test_missing_optional_field_does_not_crash",
    ),
    'Missing data: unknown data displays "Not documented"': (
        "test_generator",
        "test_unknown_data_displays_not_documented",
    ),
    'Missing data: unknown oxygen status does NOT become "Room air"': (
        "test_generator",
        "test_unknown_oxygen_status_does_not_become_room_air",
    ),
    "Rules: oxygen without device warns": (
        "test_rules",
        "test_oxygen_without_device_warns",
    ),
    "Rules: IV medication without access warns": (
        "test_rules",
        "test_iv_medication_without_access_warns",
    ),
    "Rules: missing mobility warns": ("test_rules", "test_missing_mobility_warns"),
}


def test_every_spec_section_12_bullet_is_mapped():
    assert len(SPEC_SECTION_12_TESTS) == 17


@pytest.mark.parametrize(
    ("bullet", "location"),
    list(SPEC_SECTION_12_TESTS.items()),
    ids=list(SPEC_SECTION_12_TESTS),
)
def test_spec_section_12_bullet_has_a_named_test(bullet, location):
    module_name, test_name = location
    module = importlib.import_module(f"tests.{module_name}")

    assert callable(getattr(module, test_name, None)), bullet
