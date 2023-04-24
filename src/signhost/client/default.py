import io
from typing import Any

import httpx

from .. import models
from . import utils
from .base import BaseClient


class DefaultClient(BaseClient):
    """Synchronous client"""

    client: httpx.Client

    def __init__(
        self,
        api_key: str,
        app_key: str,
        base_url: str = "https://api.signhost.com/api/",
        **httpx_kwargs: Any,
    ):
        super().__init__(api_key, app_key, base_url)
        self.client = self.create_client(base_url, **httpx_kwargs)

    def create_client(self, base_url: str, **httpx_kwargs: Any) -> httpx.Client:
        httpx_kwargs.setdefault("base_url", base_url)
        httpx_kwargs.setdefault("auth", self.authenticate_request)
        return httpx.Client(**httpx_kwargs)

    def transaction_get(self, transaction_id: str) -> models.Transaction:
        """GET /api/transaction/{transactionId}"""
        response = self.client.get(f"transaction/{transaction_id}")

        return self.process_response(response, models.Transaction)

    def transaction_cancel(
        self, transaction_id: str, send_notifications: bool = False, reason: str = ""
    ) -> models.Transaction:
        """DELETE /api/transaction/{transactionId}"""
        response = self.client.request(
            "DELETE",
            f"transaction/{transaction_id}",
            json={"SendNotifications": send_notifications, "Reason": reason},
        )
        return self.process_response(response, models.Transaction)

    def transaction_file_get(self, transaction_id: str, file_id: str) -> bytes:
        """
        GET /api/transaction/{transactionId}/file/{fileId}

        Returns the contents of the (signed) document(s).
        """
        response = self.client.get(f"transaction/{transaction_id}/file/{file_id}")

        if response.status_code == httpx.codes.OK:
            return response.content

        raise self.create_error(response)

    def receipt_get(self, transaction_id: str) -> bytes:
        """
        GET /api/file/receipt/{transactionId}

        Returns the contents of the receipt when the transaction is successfully signed (Status=30)
        """
        response = self.client.get(f"file/receipt/{transaction_id}")

        if response.status_code == httpx.codes.OK:
            return response.content

        raise self.create_error(response)

    def transaction_init(self, transaction: models.Transaction) -> models.Transaction:
        """POST /api/transaction"""

        data = transaction.json()
        headers = self.create_content_headers(data)

        response = self.client.post("transaction", content=data, headers=headers)

        return self.process_response(response, models.Transaction)

    def transaction_file_put(
        self, transaction_id: str, file_id: str, file_content: io.IOBase
    ) -> bool:
        """PUT /api/transaction/{transactionId}/file/{fileId}"""
        digest: str = utils.b64_digest(file_content)

        response = self.client.put(
            f"transaction/{transaction_id}/file/{file_id}",
            content=file_content,
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

    def transaction_start(self, transaction_id: str) -> bool:
        """PUT /api/transaction/{transactionId}/start"""
        response = self.client.put(f"transaction/{transaction_id}/start")

        if response.status_code != httpx.codes.NO_CONTENT:
            raise self.create_error(response)

        return True
