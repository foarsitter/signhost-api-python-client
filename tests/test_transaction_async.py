from io import BytesIO
from pathlib import Path

import httpx
import pytest
from respx import MockRouter

from signhost.client import AsyncClient
from signhost.client import errors
from signhost.models import Transaction


pytestmark = pytest.mark.asyncio


async def test_get_transaction(
    asignhost: AsyncClient,
    mocked_api: None,
    transaction_id: str,
    respx_mock: MockRouter,
    test_file: Path,
) -> None:
    x = await asignhost.transaction_init(Transaction())

    y = await asignhost.transaction_get(x.Id)

    assert x.Id == y.Id

    with test_file.open("rb") as f:
        assert (
            await asignhost.transaction_file_put(transaction_id, "file.pdf", f) is True
        )
    submitted_file = await asignhost.transaction_file_get(transaction_id, "file.pdf")
    assert submitted_file
    assert await asignhost.transaction_start(transaction_id) is True
    assert (await asignhost.transaction_cancel(transaction_id)).Id == x.Id
    assert await asignhost.receipt_get(transaction_id)


async def test_401(asignhost: AsyncClient, respx_mock: MockRouter) -> None:
    respx_mock.get() % 401
    with pytest.raises(errors.SignhostAuthenticationError):
        await asignhost.transaction_get("")


async def test_invalid_json(asignhost: AsyncClient, respx_mock: MockRouter) -> None:
    respx_mock.get() % httpx.Response(200, content="this is not valid")
    with pytest.raises(errors.SignhostError):
        await asignhost.transaction_get("")


async def test_500(
    asignhost: AsyncClient, respx_mock: MockRouter, transaction_id: str
) -> None:
    respx_mock.get() % 500
    respx_mock.post() % 500
    respx_mock.put() % 500
    respx_mock.delete() % 500

    with pytest.raises(errors.SignhostServerError):
        await asignhost.transaction_get(transaction_id)

    with pytest.raises(errors.SignhostServerError):
        await asignhost.transaction_start(transaction_id)

    with pytest.raises(errors.SignhostServerError):
        await asignhost.transaction_init(Transaction())

    with pytest.raises(errors.SignhostServerError):
        await asignhost.transaction_file_put(transaction_id, "file.pdf", BytesIO(b""))

    with pytest.raises(errors.SignhostServerError):
        await asignhost.transaction_file_get(transaction_id, "file.pdf")

    with pytest.raises(errors.SignhostServerError):
        await asignhost.transaction_cancel(transaction_id)

    with pytest.raises(errors.SignhostServerError):
        await asignhost.receipt_get(transaction_id)


async def test_context_manager(
    respx_mock: MockRouter,
    mocked_api: None,
) -> None:
    async with AsyncClient("", "") as asignhost:
        await asignhost.transaction_init(Transaction())
