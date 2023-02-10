import os

import pytest

from signhost.client.client import DefaultClient


@pytest.fixture
def signhost() -> DefaultClient:
    client = DefaultClient(os.getenv("SIGNHOST_API_KEY"), os.getenv("SIGNHOST_APP_KEY"))
    return client
