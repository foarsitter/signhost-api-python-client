import io
from json import JSONDecodeError
from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

import httpx

from .. import models
from . import errors


_T = TypeVar("_T")


class BaseClient:
    """Class with method shared between async and default client"""

    ERROR_RESPONSE_MAPPING: Dict[int, Type[errors.SignhostError]] = {
        422: errors.SignhostValidationError,
        401: errors.SignhostAuthenticationError,
        403: errors.SignhostAuthenticationError,
        404: errors.SignhostNotFoundError,
        400: errors.SignhostValidationError,
        500: errors.SignhostServerError,
    }

    def __init__(
        self,
        api_key: str,
        app_key: str,
        base_url: str = "https://api.signhost.com/api/",
    ):
        self.api_key = api_key
        self.app_key = app_key
        self.base_url = base_url

    def process_response(
        self, response: httpx.Response, model: Type[_T], status_code_success: int = 200
    ) -> _T:

        try:
            if response.status_code == status_code_success:
                response_json = response.json()
                return model(**response_json)
            else:
                raise self.create_error(response)
        except JSONDecodeError as e:
            raise errors.SignhostServerError(
                "Invalid json from server", status_code=400
            ) from e

    def create_error(self, response: httpx.Response) -> errors.SignhostError:

        try:
            response_json = response.json()
        except JSONDecodeError:
            response_json = {"message": response.text}

        response_json["status_code"] = response.status_code

        exception_type = self.map_exception(response)
        return exception_type(
            status_code=response.status_code,
            json=response_json,
            message="Error from server",
        )

    def map_exception(self, response: httpx.Response) -> Type[errors.SignhostError]:
        exception_type = self.ERROR_RESPONSE_MAPPING.get(
            response.status_code, errors.SignhostError
        )
        return exception_type

    def authenticate_request(self, request: httpx.Request) -> httpx.Request:

        request.headers["Authorization"] = f"APIKey {self.api_key}"
        request.headers["Application"] = f"APPKey {self.app_key}"

        return request


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
        response = self.client.get(f"/api/file/receipt/{transaction_id}")

        if response.status_code == httpx.codes.OK:
            return response.content

        raise self.create_error(response)

    def transaction_init(self, transaction: models.Transaction) -> models.Transaction:
        """POST /api/transaction"""

        data = transaction.json()
        content_length = str(len(data))
        content_type = "application/json"
        headers = {"Content-Length": content_length, "Content-Type": content_type}

        response = self.client.post("transaction", content=data, headers=headers)

        return self.process_response(response, models.Transaction)

    def transaction_file_put(
        self, transaction_id: str, file_id: str, file_content: io.IOBase
    ) -> bool:
        """PUT /api/transaction/{transactionId}/file/{fileId}"""
        # sha = hashlib.sha256(file_content.read())
        # file_digest = base64.urlsafe_b64encode(sha.digest()).decode("utf-8")

        file_content.seek(0)

        response = self.client.put(
            f"transaction/{transaction_id}/file/{file_id}",
            content=file_content,
            headers={
                "Content-Type": "application/pdf",
                # "Digest": f"SHA256={file_digest}",
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


class AsyncClient(BaseClient):
    """Asynchronous client."""

    client: httpx.AsyncClient
