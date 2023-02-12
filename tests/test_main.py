"""Test cases for the __main__ module."""
import json
from tempfile import NamedTemporaryFile

import pytest
from click.testing import CliRunner

from signhost import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner, mocked_api) -> None:
    """It exits with a status code of zero."""

    with NamedTemporaryFile() as temp:

        result = runner.invoke(
            __main__.main, ["transaction", str(temp.name), "test@pytest.io", "--yes"]
        )
        assert result.exit_code == 0, result

        result_json = json.load(temp)

        assert len(result_json.keys()) == 5
