"""Command-line interface."""
import os
from pathlib import Path

import click

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
def transaction(
    filename: Path,
    email: str,
) -> None:
    api_key = os.getenv("SIGNHOST_API_KEY")
    app_key = os.getenv("SIGNHOST_APP_KEY")

    if not api_key or not app_key:
        click.echo("Please set SIGNHOST_API_KEY and SIGNHOST_APP_KEY")
        return

    client = DefaultClient(api_key, app_key)
    test_dir = Path(__file__).parent.parent.parent / "tests"
    response_path = Path(filename)

    response_path.write_text("{}")

    client.safe_response = response_path

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

    if (
        transaction_created.Id
        and transaction_created.Signers
        and len(transaction_created.Signers) > 0
    ):
        client.transaction_file_put(
            transaction_created.Id,
            "file.pdf",
            (test_dir / "invoice.pdf").open("rb"),
        )
        client.transaction_start(transaction_created.Id)

        click.echo(transaction_created.Signers[0].SignUrl)
        click.confirm("Are you done with signing?")

        client.transaction_get(transaction_created.Id)
        client.transaction_file_get(transaction_created.Id, "file.pdf")
        client.transaction_cancel(transaction_created.Id)
        client.receipt_get(transaction_created.Id)


if __name__ == "__main__":
    main(prog_name="signhost")  # pragma: no cover
