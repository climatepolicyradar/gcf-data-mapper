import os

import pytest

from gcf_data_mapper.read import read_data_file


@pytest.fixture()
def get_test_data(request):
    """Fixture to yield expected data structure based on file type."""
    file_path = request.param
    assert os.path.exists(file_path)
    yield read_data_file(file_path)


@pytest.mark.parametrize(
    "get_test_data",
    [
        "tests/unit_tests/test_fixtures/test.json",
    ],
)
def test_reads_json_files(get_test_data):
    data = read_data_file("tests/unit_tests/test_fixtures/test.json")
    assert data == get_test_data


@pytest.mark.parametrize(
    "get_test_data",
    [
        "tests/unit_tests/test_fixtures/test.csv",
    ],
)
def test_reads_csv_files(get_test_data):
    data = read_data_file("tests/unit_tests/test_fixtures/test.csv")
    assert data == get_test_data


def test_errors_on_invalid_file():
    with pytest.raises(ValueError) as e:
        read_data_file("tests/unit_tests/test_fixtures/test.py")
    assert str(e.value) == ("Error reading file: File must be a valid json or csv file")
