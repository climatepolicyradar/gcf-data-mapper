import os

import pytest

from gcf_data_mapper.read import read_into_pandas

UNIT_TESTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_FOLDER = os.path.join(UNIT_TESTS_FOLDER, "test_fixtures")


@pytest.mark.parametrize(
    ("filepath", "expected_cols", "expected_records"),
    (
        (os.path.join(FIXTURES_FOLDER, "valid_climate_csv_data.csv"), 5, 3),
        (
            os.path.join(FIXTURES_FOLDER, "valid_climate_json_data.csv"),
            4,
            2,
        ),  # TODO: Fix
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
def test_returns_empty_df_when_exception(filepath, monkeypatch):
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
        test_df = read_into_pandas(filepath)
        assert test_df.empty is True


@pytest.mark.parametrize(
    "filepath",
    [
        os.path.join(FIXTURES_FOLDER, "empty_file.csv"),
    ],
)
def test_raises_when_file_is_empty(filepath):
    with pytest.raises(ValueError) as e:
        test_df = read_into_pandas(filepath)
        assert test_df.empty is True
    assert ("File is empty") in str(e.value)
