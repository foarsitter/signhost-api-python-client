"""Test cases for the __main__ module."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from signhost import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner, mocked_api: None, tmp_path: str) -> None:
    """It exits with a status code of zero."""

    with runner.isolated_filesystem():
        document = Path(__file__).parent / "invoice.pdf"

        result = runner.invoke(
            __main__.main,
            [
                "transaction",
                "transaction.json",
                "test@pytest.io",
                str(document),
                "--yes",
            ],
            env={"SIGNHOST_API_KEY": "test1234", "SIGNHOST_APP_KEY": "test1234"},
        )
        assert result.exit_code == 0, result

        assert result.output
        print(result.output)

        with open("transaction.json") as temp:
            p = json.load(temp)
            assert len(p.keys()) == 5
