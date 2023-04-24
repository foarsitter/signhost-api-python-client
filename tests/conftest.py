import json
import logging
import os
from pathlib import Path
from typing import Generator

import pytest
import respx
from httpx import Response

from signhost.client import AsyncClient
from signhost.client import DefaultClient
from signhost.client import RequestFixtures


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
    api_key = os.getenv("SIGNHOST_API_KEY", "empty")
    app_key = os.getenv("SIGNHOST_APP_KEY", "empty")

    client = DefaultClient(api_key, app_key)
    return client


@pytest.fixture(scope="session")
def asignhost() -> AsyncClient:
    api_key = os.getenv("SIGNHOST_API_KEY", "empty")
    app_key = os.getenv("SIGNHOST_APP_KEY", "empty")

    client = AsyncClient(api_key, app_key)
    return client


@pytest.fixture(scope="session")
def request_fixtures(test_fixtures_path: Path) -> RequestFixtures:
    logging.getLogger().info("Loading test fixtures from %s", str(test_fixtures_path))
    data: RequestFixtures = json.load(test_fixtures_path.open())

    return data


@pytest.fixture(scope="function")
def mocked_api(
    request_fixtures: RequestFixtures, test_file: Path
) -> Generator[None, None, None]:
    # using a context manager here so the mock is reset after each test
    with respx.mock:
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
        yield


@pytest.fixture(scope="session")
def transaction_id(request_fixtures: RequestFixtures) -> str:
    return str(
        request_fixtures["https://api.signhost.com/api/transaction"]["POST"]["200"][
            "Id"
        ]
    )
