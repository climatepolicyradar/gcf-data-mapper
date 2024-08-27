import pytest
from click.testing import CliRunner

from gcf_data_mapper.cli import entrypoint


def test_version():
    runner = CliRunner()
    result = runner.invoke(entrypoint, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.strip()


@pytest.mark.skip()
def test_entrypoint_fail():
    runner = CliRunner()
    result = runner.invoke(entrypoint)
    assert result.exit_code == 1
    assert "Failed to map GCF data to expected JSON" in result.output.strip()


def test_entrypoint_success():
    runner = CliRunner()
    result = runner.invoke(entrypoint)
    assert result.exit_code == 0
    assert all(
        item in result.output.strip()
        for item in ["Finished mapping GCF data", "Finished dumping mapped GCF data"]
    )
