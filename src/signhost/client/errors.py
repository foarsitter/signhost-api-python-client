from typing import Any
from typing import Dict
from typing import Optional

from attr import define


@define
class SignhostError(Exception):
    message: str
    status_code: int
    json: Optional[Dict[str, Any]] = None


class SignhostValidationError(SignhostError):
    pass


class SignhostAuthenticationError(SignhostError):
    pass


class SignhostNotFoundError(SignhostError):
    pass
