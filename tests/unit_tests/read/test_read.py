import json
import os
from typing import Any, Union

import pytest

from gcf_data_mapper.read import read

UNIT_TESTS_FOLDER = os.path.dirname(os.path.abspath(__file__))
FIXTURES_FOLDER = os.path.join(UNIT_TESTS_FOLDER, "fixtures")


def return_valid_csv_data():
    """
    Function which returns expected data structure of csv file.
    """

    csv_data = [
        {
            "country": "Brazil",
            "capital": "Brasilia",
            "avg_temp_celsius": "21.5",
            "annual_rainfall_mm": "1500",
            "climate_zone": "Tropical",
        },
        {
            "country": "Canada",
            "capital": "Ottawa",
            "avg_temp_celsius": "6.3",
            "annual_rainfall_mm": "940",
            "climate_zone": "Continental",
        },
        {
            "country": "Egypt",
            "capital": "Cairo",
            "avg_temp_celsius": "22.1",
            "annual_rainfall_mm": "25",
            "climate_zone": "Desert",
        },
    ]
    return csv_data


def return_valid_json_data():
    """
    Function which returns expected data structure of json file.
    """

    json_data = [
        {
            "country": "Brazil",
            "capital": "Brasilia",
            "climate_info": {
                "avg_temp_celsius": 21.5,
                "annual_rainfall_mm": 1500,
                "climate_zone": "Tropical",
            },
            "rivers": {"names": [{"egypt": "Nile"}, {"london": "Thames"}]},
            "natural_disasters": ["Floods", "Landslides"],
        },
        {
            "country": "Canada",
            "capital": "Ottawa",
            "climate_info": {
                "avg_temp_celsius": 6.3,
                "annual_rainfall_mm": 940,
                "climate_zone": "Continental",
            },
            "rivers": {"names": [{"egypt": "Nile"}, {"london": "Thames"}]},
            "natural_disasters": ["Blizzards", "Wildfires"],
        },
    ]
    return json_data


@pytest.mark.parametrize(
    "filepath, expected_output",
    (
        (
            os.path.join(FIXTURES_FOLDER, "valid_climate_json_data.json"),
            return_valid_json_data(),
        ),
        (
            os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data.csv"),
            return_valid_csv_data(),
        ),
    ),
)
def test_valid_files_return_expected_output(
    filepath: str, expected_output: Union[dict, list[dict[str, Any]]]
):
    assert os.path.exists(filepath)
    data = read(filepath)
    assert data is not None
    assert data == expected_output


@pytest.mark.parametrize(
    "filepath, expected_output",
    (
        (
            os.path.join(FIXTURES_FOLDER, "invalid_climate_json_data.json"),
            return_valid_json_data(),
        ),
        (
            os.path.join(FIXTURES_FOLDER, "invalid_climate_csv_data.csv"),
            return_valid_csv_data(),
        ),
    ),
)
def test_invalid_files_do_not_return_expected_output(
    filepath: str, expected_output: Union[dict, list[dict[str, Any]]]
):
    assert os.path.exists(filepath)
    data = read(filepath)
    assert data != expected_output


def test_raises_error_on_invalid_file_extension():
    with pytest.raises(ValueError) as e:
        read(os.path.join(FIXTURES_FOLDER, "test_text_file.txt"))
    assert str(e.value) == ("Error reading file: File must be a valid json or csv file")


def test_raises_error_with_non_existent_file():
    non_existent_file_path = os.path.join(FIXTURES_FOLDER, "non_existent_file.csv")
    with pytest.raises(FileNotFoundError) as e:
        read(non_existent_file_path)
    assert str(e.value) == f"No such file or directory: '{non_existent_file_path}'"


def test_raises_error_with_empty_file():
    empty_file_path = os.path.join(FIXTURES_FOLDER, "empty_file.csv")
    with pytest.raises(ValueError) as e:
        read(empty_file_path)
    assert str(e.value) == "Error reading file: File is empty"


def test_raises_error_on_malformed_json():
    with pytest.raises(json.JSONDecodeError):
        read(os.path.join(FIXTURES_FOLDER, "malformed_data.json"))
