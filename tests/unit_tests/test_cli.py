import pytest
from click.testing import CliRunner

from gcf_data_mapper.cli import wrangle_json


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
