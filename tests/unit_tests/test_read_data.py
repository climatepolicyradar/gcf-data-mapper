import os

import pytest

from gcf_data_mapper.read import read_data_file

print()
unit_tests_folder = os.path.dirname(os.path.abspath(__file__))
fixtures_folder = os.path.join(unit_tests_folder, "test_fixtures")


def good_test_json():
    """Fixture to yield expected data structure based on file type.

    what would you expected the output of read_data_file() to be with
    the JSON data in your file read in?

    return that data type with the above data in as the function would
    be expected to output
    """
    pass


def good_test_csv():
    """Fixture to yield expected data structure based on file type.

    what would you expected the output of read_data_file() to be with
    the following data read in?

    country,capital,avg_temp_celsius,annual_rainfall_mm,climate_zone
    Brazil,Brasilia,21.5,1500,Tropical
    Canada,Ottawa,6.3,940,Continental
    Egypt,Cairo,22.1,25,Desert

    return that data type with the above data in as the function would
    be expected to output
    """
    pass


@pytest.mark.parametrize(
    "filepath, expected_output",
    (
        (os.path.join(fixtures_folder, "test.json"), good_test_json()),
        (os.path.join(fixtures_folder, "test.csv"), good_test_csv()),
    ),
)
def test_reads_files(filepath):
    assert os.path.exists(filepath)
    data = read_data_file(filepath)
    assert data is not None
    # if isinstance(get_test_data, list):
    #     data = read_data_file("tests/unit_tests/test_fixtures/test.csv")
    #     assert get_test_data == data
    # elif isinstance(get_test_data, dict):
    #     data = read_data_file("tests/unit_tests/test_fixtures/test.json")
    #     assert get_test_data == data


def test_errors_on_invalid_file():
    with pytest.raises(ValueError) as e:
        read_data_file("tests/unit_tests/test_fixtures/test.py")
    assert str(e.value) == ("Error reading file: File must be a valid json or csv file")
