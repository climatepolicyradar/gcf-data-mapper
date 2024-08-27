import os

import pytest

from gcf_data_mapper.read import read_data_file


@pytest.fixture(
    params=[
        "tests/unit_tests/test_fixtures/test.json",
        "tests/unit_tests/test_fixtures/test.csv",
    ]
)
def get_test_data(request):
    """Fixture to yield expected data structure based on file type."""
    file_path = request.param
    assert os.path.exists(file_path)
    yield read_data_file(file_path)


def test_reads_files(get_test_data):
    if isinstance(get_test_data, list):
        data = read_data_file("tests/unit_tests/test_fixtures/test.csv")
        assert get_test_data == data
    elif isinstance(get_test_data, dict):
        data = read_data_file("tests/unit_tests/test_fixtures/test.json")
        assert get_test_data == data


def test_errors_on_invalid_file():
    with pytest.raises(ValueError) as e:
        read_data_file("tests/unit_tests/test_fixtures/test.py")
    assert str(e.value) == ("Error reading file: File must be a valid json or csv file")
