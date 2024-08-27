import json

import pytest
from click.testing import CliRunner

from gcf_data_mapper.cli import read_data_file, wrangle_json


def test_version():
    runner = CliRunner()
    result = runner.invoke(wrangle_json, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.strip()


@pytest.mark.skip()
def test_wrangle_json_fail():
    runner = CliRunner()
    result = runner.invoke(wrangle_json)
    assert result.exit_code == 1
    assert "Failed to map GCF data to expected JSON" in result.output.strip()


def test_wrangle_json_success():
    runner = CliRunner()
    result = runner.invoke(wrangle_json)
    assert result.exit_code == 0
    assert "Finished mapping GCF data." in result.output.strip()


def get_json_test_data():
    with open("tests/unit_tests/test_fixtures/test.json", "r") as file:
        data = file.read()
        return json.loads(data)


def test_reads_json_files():
    runner = CliRunner()
    result = runner.invoke(read_data_file, ["tests/unit_tests/test_fixtures/test.json"])
    data = get_json_test_data()
    assert result.exit_code == 0
    output_data = json.loads(result.output)
    assert data == output_data


def test_reads_csv_files():
    runner = CliRunner()
    result = runner.invoke(read_data_file, ["tests/unit_tests/test_fixtures/test.csv"])
    assert result.exit_code == 0
    assert "['Brazil', 'Canada', 'Egypt']" in result.output.strip()


def test_errors_on_invalid_file():
    runner = CliRunner()
    result = runner.invoke(read_data_file, ["tests/unit_tests/test_fixtures/test.py"])
    assert (
        "Error reading file: File must be a valid json or csv file"
        in result.output.strip()
    )
