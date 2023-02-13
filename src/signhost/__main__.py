"""Command-line interface."""
import io
import json
import os
from pathlib import Path

import click
import httpx

from signhost.client import RequestFixtures
from signhost.client.client import DefaultClient
from signhost.models import Signer
from signhost.models import Transaction
from signhost.models import verifications
from signhost.models.enums import Language


@click.group()
@click.version_option()
def main() -> None:
    """Signhost Api Python Client."""
    pass


@main.command()
@click.argument("filename", type=click.Path())
@click.argument("email")
@click.option("--yes", is_flag=True, help="Skip confirmation")
def transaction(
    filename: Path,
    email: str,
    yes: bool,
) -> None:
    api_key = os.getenv("SIGNHOST_API_KEY")
    app_key = os.getenv("SIGNHOST_APP_KEY")

    if not api_key or not app_key:  # pragma: no cover
        click.echo("Please set SIGNHOST_API_KEY and SIGNHOST_APP_KEY")
        return

    log_response = ResponseStorage()

    client = DefaultClient(
        api_key,
        app_key,
        event_hooks={"response": [log_response]},
    )

    response_path = Path(filename)

    signers = [
        Signer(
            SendSignRequest=False,
            Email=email,
            SignRequestMessage="Please sign this document",
            Verifications=[
                verifications.Scribble(
                    RequireHandsignature=True,
                    ScribbleNameFixed=True,
                    ScribbleName="Jelmer Draaijer",
                )
            ],
        )
    ]
    t = Transaction(
        Language=Language.NL,
        Signers=signers,
        PostbackUrl=os.getenv("TEST_POSTBACK_TUNNEL"),
    )

    transaction_created = client.transaction_init(t)

    client.transaction_file_put(
        transaction_created.Id,
        "file.pdf",
        io.BytesIO(b"test"),
    )
    client.transaction_start(transaction_created.Id)

    click.echo(transaction_created.Signers[0].SignUrl)

    if not yes:
        click.confirm("Are you done with signing?")  # pragma: no cover

    client.transaction_get(transaction_created.Id)
    client.transaction_file_get(transaction_created.Id, "file.pdf")
    client.transaction_cancel(transaction_created.Id)
    client.receipt_get(transaction_created.Id)

    click.echo(json.dumps(log_response.responses, indent=4))

    with response_path.open("w+") as f:
        json.dump(log_response.responses, f, indent=2)


if __name__ == "__main__":
    main(prog_name="signhost")  # pragma: no cover


class ResponseStorage:
    def __init__(self) -> None:
        self.responses: RequestFixtures = {}

    def __call__(self, response: httpx.Response) -> None:

        response.read()

        if response.headers.get("content-type", "") == "application/json":
            data = response.json()
        else:
            data = {"binary": True}

        key = str(response.url)

        if key not in self.responses:
            self.responses[key] = {}
        if response.request.method not in self.responses[key]:  # pragma: no cover
            self.responses[key][response.request.method] = {}

        self.responses[key][response.request.method][
            str(response.status_code)
        ] = data  # pragma: no cover
