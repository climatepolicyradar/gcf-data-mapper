import os
from typing import Any, Union

import pytest

from gcf_data_mapper.read import read_data_file

unit_tests_folder = os.path.dirname(os.path.abspath(__file__))
fixtures_folder = os.path.join(unit_tests_folder, "test_fixtures")


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

    json_data = {
        "climate_data": [
            {
                "country": "Brazil",
                "capital": "Brasilia",
                "climate_info": {
                    "avg_temp_celsius": 21.5,
                    "annual_rainfall_mm": 1500,
                    "climate_zone": "Tropical",
                },
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
                "natural_disasters": ["Blizzards", "Wildfires"],
            },
        ]
    }
    return json_data


@pytest.mark.parametrize(
    "filepath, expected_output",
    (
        (
            os.path.join(fixtures_folder, "valid_climate_json_data.json"),
            return_valid_json_data(),
        ),
        (
            os.path.join(fixtures_folder, "valid_climate_csv_data.csv"),
            return_valid_csv_data(),
        ),
    ),
)
def test_reads_files(filepath: str, expected_output: Union[dict, list[dict[str, Any]]]):
    assert os.path.exists(filepath)
    data = read_data_file(filepath)
    assert data is not None
    assert data == expected_output


def test_malformed_json_file_does_not_return_expected_output():
    filepath = os.path.join(fixtures_folder, "invalid_climate_json_data.json")
    data = read_data_file(filepath)
    assert data is not None
    assert data != return_valid_json_data()


def test_malformed_csv_file_does_not_return_expected_output():
    filepath = os.path.join(fixtures_folder, "invalid_climate_csv_data.csv")
    data = read_data_file(filepath)
    assert data is not None
    assert data != return_valid_csv_data()


def test_raises_error_on_invalid_file_extension():
    with pytest.raises(ValueError) as e:
        read_data_file(os.path.join(fixtures_folder, "test_text_file.txt"))
    assert str(e.value) == ("Error reading file: File must be a valid json or csv file")
