import io
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar

import httpx
from httpx import Request
from httpx import Response

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
        self.safe_response: Optional[Path] = None

    def process_response(
        self, response: Response, model: Type[_T], status_code_success: int = 200
    ) -> _T:

        try:
            response_json = response.json()

            if self.safe_response:
                self.write_response_to_path(response, response_json)

            if response.status_code == status_code_success:
                return model(**response_json)
        except JSONDecodeError:
            pass

        raise self.create_error(response)

    def write_response_to_path(
        self, response: httpx.Response, response_json: Any
    ) -> None:
        """
        Function for saving responses to a file, so we can use it for testing
        """

        if self.safe_response:

            with self.safe_response.open("rb") as outfile:
                saved_responses = json.load(outfile)
                if saved_responses is None:
                    saved_responses = {}

                key = str(response.url)
                if key not in saved_responses:
                    saved_responses[key] = {}
                if response.request.method not in saved_responses[key]:
                    saved_responses[key][response.request.method] = {}
                saved_responses[key][response.request.method][
                    str(response.status_code)
                ] = response_json
            with self.safe_response.open("w") as outfile:
                json.dump(saved_responses, outfile, indent=4)

    def create_error(self, response: Response) -> errors.SignhostError:

        try:
            response_json = response.json()
        except JSONDecodeError:
            response_json = {"message": response.text}

        if self.safe_response:
            self.write_response_to_path(response, response_json)

        response_json["status_code"] = response.status_code

        exception_type = self.map_exception(response)
        return exception_type(
            status_code=response.status_code,
            json=response_json,
            message="Error from server",
        )

    def map_exception(self, response: Response) -> Type[errors.SignhostError]:
        exception_type = self.ERROR_RESPONSE_MAPPING.get(
            response.status_code, errors.SignhostError
        )
        return exception_type

    def authenticate_request(self, request: Request) -> Request:

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
    ):
        super().__init__(api_key, app_key, base_url)
        self.client = httpx.Client(base_url=base_url, auth=self.authenticate_request)

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
            if self.safe_response:
                self.write_response_to_path(response, {"binary": True})
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
            if self.safe_response:
                self.write_response_to_path(response, {})
            return True

        self.create_error(response)
        return False

    def transaction_start(self, transaction_id: str) -> bool:
        """PUT /api/transaction/{transactionId}/start"""
        response = self.client.put(f"transaction/{transaction_id}/start")

        if response.status_code != httpx.codes.NO_CONTENT:
            self.create_error(response)

        if self.safe_response:
            self.write_response_to_path(response, None)

        return True


class AsyncClient(BaseClient):
    """Asynchronous client."""

    client: httpx.AsyncClient
