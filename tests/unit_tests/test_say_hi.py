
from click.testing import CliRunner
from gcf_data_mapper.cli import greet

def test_greet():
    runner = CliRunner()
    result = runner.invoke(greet, ['--name', 'World'])
    assert result.exit_code == 0
    assert result.output.strip() == 'Hello World!'
