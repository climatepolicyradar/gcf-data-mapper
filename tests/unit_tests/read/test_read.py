import os

import pandas as pd
import pytest

from gcf_data_mapper.read import read
from tests.unit_tests.read.conftest import FIXTURES_FOLDER


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
        {
            "country": "Egypt",
            "capital": "Cairo",
            "climate_info": {
                "avg_temp_celsius": 26,
                "annual_rainfall_mm": 80,
                "climate_zone": "Desert",
            },
            "rivers": {"names": [{"egypt": "Nile"}, {"london": "Thames"}]},
            "natural_disasters": ["Droughts"],
        },
    ]
    return json_data


def test_valid_files_return_expected_output():
    fam_data, doc_data = read(
        os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data.csv"),
        os.path.join(FIXTURES_FOLDER, "valid_climate_json_data.json"),
        os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data_2_records.csv"),
    )

    assert fam_data is not None
    assert (
        pd.testing.assert_frame_equal(
            fam_data,
            pd.DataFrame(
                {
                    "country": ["Brazil", "Canada", "Egypt"],
                    "capital": ["Brasilia", "Ottawa", "Cairo"],
                    "climate_info.avg_temp_celsius": [21.5, 6.3, 22.1],
                    "climate_info.annual_rainfall_mm": [1500, 940, 25],
                    "climate_info.climate_zone": ["Tropical", "Continental", "Desert"],
                    "rivers.names": [
                        [{"egypt": "Nile"}, {"london": "Thames"}],
                        [{"egypt": "Nile"}, {"london": "Thames"}],
                        [{"egypt": "Nile"}, {"london": "Thames"}],
                    ],
                    "natural_disasters": [
                        ["Floods", "Landslides"],
                        ["Blizzards", "Wildfires"],
                        ["Droughts"],
                    ],
                }
            ),
            check_like=True,  # Ignore the order of columns and records.
        )
        is None
    )

    assert doc_data is not None
    assert (
        pd.testing.assert_frame_equal(
            doc_data,
            pd.DataFrame(
                {"country": ["Brazil", "Canada"], "capital": ["Brasilia", "Ottawa"]}
            ),
        )
        is None
    )


@pytest.mark.parametrize(
    "filepath,error,error_msg",
    [
        (
            os.path.join(FIXTURES_FOLDER, "empty_file.csv"),
            ValueError,
            "One or more of the expected dataframes are empty",
        ),
        (
            os.path.join(FIXTURES_FOLDER, "malformed_data.json"),
            ValueError,
            "One or more of the expected dataframes are empty",
        ),
        (
            os.path.join(FIXTURES_FOLDER, "invalid_climate_csv_data.csv"),
            ValueError,
            "One or more of the expected dataframes are empty",
        ),
        (
            os.path.join(FIXTURES_FOLDER, "test_text_file.txt"),
            ValueError,
            "Error reading file: File must be a valid json or csv file",
        ),
        (
            os.path.join(FIXTURES_FOLDER, "non_existent_file.csv"),
            FileNotFoundError,
            "No such file or directory",
        ),
        (
            os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data_2_records.csv"),
            ValueError,
            "Record number mismatch",
        ),
    ],
)
def test_raises(filepath, error, error_msg):
    with pytest.raises(error) as e:
        read(
            os.path.join(FIXTURES_FOLDER, "valid_climate_json_data.json"),
            filepath,
            os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data.csv"),
        )
    assert error_msg in str(e.value)