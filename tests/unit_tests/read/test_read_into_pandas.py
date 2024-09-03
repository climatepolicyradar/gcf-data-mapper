import os

import pytest

from gcf_data_mapper.read import read_into_pandas
from tests.unit_tests.read.conftest import FIXTURES_FOLDER


@pytest.mark.parametrize(
    ("filepath", "expected_cols", "expected_records"),
    (
        (os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data.csv"), 2, 3),
        (
            os.path.join(FIXTURES_FOLDER, "valid_climate_json_data.json"),
            7,
            3,
        ),
    ),
)
def test_valid_files_return_expected_output(
    filepath: str, expected_cols: int, expected_records: int
):
    assert os.path.exists(filepath)
    data = read_into_pandas(filepath)
    assert data.empty is False

    assert data.shape[0] == expected_records
    assert data.shape[1] == expected_cols


@pytest.mark.parametrize(
    "filepath",
    [
        os.path.join(FIXTURES_FOLDER, "invalid_climate_csv_data.csv"),
        os.path.join(FIXTURES_FOLDER, "malformed_data.json"),
    ],
)
def test_returns_empty_df_when_exception(filepath):
    test_df = read_into_pandas(filepath)
    assert test_df.empty is True


@pytest.mark.parametrize(
    "filepath",
    [
        "non_existent_file.csv",
        "non_existent_file.json",
    ],
)
def test_raises_when_file_not_exist(filepath):
    with pytest.raises(FileNotFoundError):
        read_into_pandas(filepath)


@pytest.mark.parametrize(
    "filepath",
    [
        os.path.join(FIXTURES_FOLDER, "empty_file.csv"),
    ],
)
def test_raises_when_file_is_empty(filepath):
    test_df = read_into_pandas(filepath)
    assert test_df.empty is True
