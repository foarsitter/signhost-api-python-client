import json
import logging
import os
from pathlib import Path
from typing import Any
from typing import Dict

import pytest
import respx
from httpx import Response

from signhost.client.client import DefaultClient


RequestFixtures = Dict[str, Dict[str, Dict[str, Any]]]


@pytest.fixture(scope="session")
def test_path() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="session")
def test_file(test_path: Path) -> Path:
    return test_path / "invoice.pdf"


@pytest.fixture(scope="session")
def test_fixtures_path(test_path: Path) -> Path:
    return test_path / "responses.json"


@pytest.fixture(scope="session")
def signhost() -> DefaultClient:
    api_key = os.getenv("SIGNHOST_API_KEY")
    app_key = os.getenv("SIGNHOST_APP_KEY")

    if not api_key or not app_key:
        raise Exception("Please set SIGNHOST_API_KEY and SIGNHOST_APP_KEY")

    client = DefaultClient(api_key, app_key)
    return client


@pytest.fixture(scope="session")
def safe_response(signhost: DefaultClient, test_fixtures_path: Path) -> None:
    signhost.safe_response = test_fixtures_path


@pytest.fixture(scope="session")
def request_fixtures(test_fixtures_path: Path) -> RequestFixtures:
    logging.getLogger().info("Loading test fixtures from %s", str(test_fixtures_path))
    data: RequestFixtures = json.load(test_fixtures_path.open())

    return data


@pytest.fixture(scope="session")
def mocked_api(request_fixtures: RequestFixtures, test_file: Path) -> None:
    for url, methods in request_fixtures.items():
        for method, status_codes in methods.items():
            for status_code, response in status_codes.items():

                if response == {"binary": True}:
                    respx.request(method=method, url=url) % Response(
                        status_code=int(status_code), content=test_file.read_bytes()
                    )
                else:
                    respx.request(method=method, url=url) % Response(
                        status_code=int(status_code), json=response
                    )


@pytest.fixture(scope="session")
def transaction_id(request_fixtures: RequestFixtures) -> str:
    return str(
        request_fixtures["https://api.signhost.com/api/transaction"]["POST"]["200"][
            "Id"
        ]
    )
