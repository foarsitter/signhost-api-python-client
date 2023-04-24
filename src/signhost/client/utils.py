import base64
import hashlib
import io
from struct import pack
from typing import AsyncIterator


# the same as httpx uses in IteratorByteStream
CHUNK_SIZE = 65_536


def b64_digest(file_content: io.IOBase) -> str:
    sha = hashlib.sha256(file_content.read())

    # rewind the file for further usage
    file_content.seek(0)

    digest = sha.digest()

    b64encode_digest = base64.b64encode(pack(f"{len(digest)}s", digest)).decode("utf-8")

    return b64encode_digest


async def bytes_as_stream(file_content: io.IOBase) -> AsyncIterator[bytes]:
    chunk = file_content.read(CHUNK_SIZE)
    while chunk:
        yield chunk
        chunk = file_content.read(CHUNK_SIZE)
