import click.testing

from fetchbin.console import main


def test_cli_help_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
