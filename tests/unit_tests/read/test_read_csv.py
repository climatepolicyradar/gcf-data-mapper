import os
from typing import Any, Union

import pytest

from gcf_data_mapper.read import read_csv_pd

UNIT_TESTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_FOLDER = os.path.join(UNIT_TESTS_FOLDER, "test_fixtures")


@pytest.mark.parametrize(
    "filepath",
    (os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data.csv"),),
)
def test_valid_files_return_expected_output(
    filepath: str, expected_output: Union[dict, list[dict[str, Any]]]
):
    assert os.path.exists(filepath)
    data = read_csv_pd(filepath)
    assert data.empty is False

    expected_num_records = 3
    expected_num_cols = 5

    assert data.shape[0] == expected_num_records
    assert data.shape[1] == expected_num_cols


@pytest.mark.parametrize(
    "filepath",
    [
        os.path.join(FIXTURES_FOLDER, "invalid_climate_csv_data.csv"),
        os.path.join(FIXTURES_FOLDER, "empty_file.csv"),
        "non_existent_file.csv",
    ],
)
def test_returns_empty_df_when_exception(filepath):
    test_df = read_csv_pd(filepath)
    assert test_df.empty is True
