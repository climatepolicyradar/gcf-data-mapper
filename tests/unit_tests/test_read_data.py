import os

import pytest

from gcf_data_mapper.read import read_data_file


@pytest.fixture()
def get__test_data():
    """Yield data based on"""
    assert os.path.exists("tests/unit_tests/test_fixtures/test.json")
    yield read_data_file("tests/unit_tests/test_fixtures/test.json")


@pytest.fixture()
def get_csv_test_data():
    assert os.path.exists("tests/unit_tests/test_fixtures/test.csv")
    yield read_data_file("tests/unit_tests/test_fixtures/test.csv")


def test_reads_json_files(get_json_test_data):
    data = read_data_file("tests/unit_tests/test_fixtures/test.json")
    assert data == get_json_test_data


def test_reads_csv_files(get_csv_test_data):
    data = read_data_file("tests/unit_tests/test_fixtures/test.csv")
    assert get_csv_test_data == data


def test_errors_on_invalid_file():
    with pytest.raises(ValueError) as e:
        read_data_file("tests/unit_tests/test_fixtures/test.py")
    assert str(e.value) == ("Error reading file: File must be a valid json or csv file")
