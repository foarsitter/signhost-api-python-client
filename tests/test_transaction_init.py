from io import BytesIO
from pathlib import Path

import pytest
from respx import MockRouter

from signhost.client import errors
from signhost.client.client import DefaultClient
from signhost.models import Transaction


def test_get_transaction(
    signhost: DefaultClient,
    mocked_api: None,
    transaction_id: str,
    respx_mock: MockRouter,
    test_file: Path,
) -> None:
    x = signhost.transaction_init(Transaction())

    if x.Id:
        y = signhost.transaction_get(x.Id)

        assert x.Id == y.Id

        with test_file.open("rb") as f:
            assert signhost.transaction_file_put(transaction_id, "file.pdf", f) is True
        submitted_file = signhost.transaction_file_get(transaction_id, "file.pdf")
        assert submitted_file
        assert signhost.transaction_start(transaction_id) is True
        assert signhost.transaction_cancel(transaction_id).Id == x.Id
        assert signhost.receipt_get(transaction_id)


def test_401(signhost: DefaultClient, respx_mock: MockRouter) -> None:
    respx_mock.get() % 401
    with pytest.raises(errors.SignhostAuthenticationError):
        signhost.transaction_get("")


def test_500(
    signhost: DefaultClient, respx_mock: MockRouter, transaction_id: str
) -> None:
    respx_mock.get() % 500
    respx_mock.post() % 500
    respx_mock.put() % 500
    respx_mock.delete() % 500

    with pytest.raises(errors.SignhostServerError):
        signhost.transaction_get(transaction_id)

    with pytest.raises(errors.SignhostServerError):
        signhost.transaction_start(transaction_id)

    with pytest.raises(errors.SignhostServerError):
        signhost.transaction_init(Transaction())

    with pytest.raises(errors.SignhostServerError):
        signhost.transaction_file_put(transaction_id, "file.pdf", BytesIO(b""))

    with pytest.raises(errors.SignhostServerError):
        signhost.transaction_file_get(transaction_id, "file.pdf")

    with pytest.raises(errors.SignhostServerError):
        signhost.transaction_cancel(transaction_id)

    with pytest.raises(errors.SignhostServerError):
        signhost.receipt_get(transaction_id)
