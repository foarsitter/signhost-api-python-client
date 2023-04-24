from json import JSONDecodeError
from typing import Dict
from typing import Mapping
from typing import Type
from typing import TypeVar

import httpx

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

    def create_content_headers(self, data: str) -> Mapping[str, str]:
        content_length: str = str(len(data))
        content_type: str = "application/json"
        headers: Mapping[str, str] = {
            "Content-Length": content_length,
            "Content-Type": content_type,
        }
        return headers

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
