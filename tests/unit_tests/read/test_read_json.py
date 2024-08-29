import os

import pytest

from gcf_data_mapper.read import read_json_pd

UNIT_TESTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_FOLDER = os.path.join(UNIT_TESTS_FOLDER, "test_fixtures")


@pytest.mark.parametrize(
    "filepath",
    (os.path.join(FIXTURES_FOLDER, "valid_climate_json_data.json"),),
)
def test_valid_files_return_expected_output(filepath: str):
    assert os.path.exists(filepath)
    data = read_json_pd(filepath)
    assert data.empty is False

    expected_num_records = 2
    expected_num_cols = 6

    assert data.shape[0] == expected_num_records
    assert data.shape[1] == expected_num_cols


@pytest.mark.parametrize(
    "filepath",
    [
        os.path.join(FIXTURES_FOLDER, "invalid_climate_json_data.csv"),
        os.path.join(FIXTURES_FOLDER, "malformed_json.json"),
        "non_existent_file.json",
    ],
)
def test_returns_empty_df_when_exception(filepath):
    test_df = read_json_pd(filepath)
    assert test_df.empty is True
