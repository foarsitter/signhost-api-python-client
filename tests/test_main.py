"""Test cases for the __main__ module."""
import tempfile

import pytest
from click.testing import CliRunner

from signhost import __main__
from signhost.__main__ import transaction


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner, mocked_api: None) -> None:
    """It exits with a status code of zero."""

    with tempfile.NamedTemporaryFile() as temp:
        result = runner.invoke(
            __main__.main,
            ["transaction", str(temp.name), "test@pytest.io", "--yes"],
            env={"SIGNHOST_API_KEY": "test1234", "SIGNHOST_APP_KEY": "test1234"},
        )
        assert result.exit_code == 0, result
