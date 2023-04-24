import io
from types import TracebackType
from typing import Any
from typing import Optional
from typing import Type

import httpx

from signhost import models
from signhost.client import utils
from signhost.client.base import BaseClient


class AsyncClient(BaseClient):
    """Asynchronous client."""

    client: httpx.AsyncClient

    def __init__(
        self,
        api_key: str,
        app_key: str,
        base_url: str = "https://api.signhost.com/api/",
        **httpx_kwargs: Any,
    ):
        super().__init__(api_key, app_key, base_url)
        self.client = self.create_client(base_url, **httpx_kwargs)

    async def __aenter__(self) -> "AsyncClient":
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self.client.__aexit__(exc_type, exc_value, traceback)

    def create_client(self, base_url: str, **httpx_kwargs: Any) -> httpx.AsyncClient:
        httpx_kwargs.setdefault("base_url", base_url)
        httpx_kwargs.setdefault("auth", self.authenticate_request)
        return httpx.AsyncClient(**httpx_kwargs)

    async def transaction_get(self, transaction_id: str) -> models.Transaction:
        """GET /api/transaction/{transactionId}"""
        response = await self.client.get(f"transaction/{transaction_id}")

        return self.process_response(response, models.Transaction)

    async def transaction_cancel(
        self, transaction_id: str, send_notifications: bool = False, reason: str = ""
    ) -> models.Transaction:
        """DELETE /api/transaction/{transactionId}"""
        response = await self.client.request(
            "DELETE",
            f"transaction/{transaction_id}",
            json={"SendNotifications": send_notifications, "Reason": reason},
        )
        return self.process_response(response, models.Transaction)

    async def transaction_file_get(self, transaction_id: str, file_id: str) -> bytes:
        """
        GET /api/transaction/{transactionId}/file/{fileId}

        Returns the contents of the (signed) document(s).
        """
        response = await self.client.get(f"transaction/{transaction_id}/file/{file_id}")

        if response.status_code == httpx.codes.OK:
            return response.content

        raise self.create_error(response)

    async def receipt_get(self, transaction_id: str) -> bytes:
        """
        GET /api/file/receipt/{transactionId}

        Returns the contents of the receipt when the transaction is successfully signed (Status=30)
        """
        response = await self.client.get(f"file/receipt/{transaction_id}")

        if response.status_code == httpx.codes.OK:
            return response.content

        raise self.create_error(response)

    async def transaction_init(
        self, transaction: models.Transaction
    ) -> models.Transaction:
        """POST /api/transaction"""
        data: str = transaction.json()

        headers = self.create_content_headers(data)

        response = await self.client.post("transaction", content=data, headers=headers)

        return self.process_response(response, models.Transaction)

    async def transaction_file_put(
        self, transaction_id: str, file_id: str, file_content: io.IOBase
    ) -> bool:
        """PUT /api/transaction/{transactionId}/file/{fileId}"""
        digest: str = utils.b64_digest(file_content)

        response = await self.client.put(
            f"transaction/{transaction_id}/file/{file_id}",
            content=utils.bytes_as_stream(file_content),
            headers={
                "Content-Type": "application/pdf",
                "Digest": f"SHA256={digest}",
            },
        )

        if response.status_code in [
            httpx.codes.CREATED,
            httpx.codes.ACCEPTED,
            httpx.codes.NO_CONTENT,
        ]:
            return True

        raise self.create_error(response)

    async def transaction_start(self, transaction_id: str) -> bool:
        """PUT /api/transaction/{transactionId}/start"""
        response = await self.client.put(f"transaction/{transaction_id}/start")

        if response.status_code != httpx.codes.NO_CONTENT:
            raise self.create_error(response)

        return True
