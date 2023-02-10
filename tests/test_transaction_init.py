import os
import secrets
import time
from pathlib import Path

from signhost.models import Language
from signhost.models import Signer
from signhost.models import Status
from signhost.models import Transaction


def test_transaction_init_200(signhost):
    """Test the transaction init."""

    signers = [
        Signer(
            SendSignRequest=True,
            Email=os.getenv("TEST_EMAIL"),
            SignRequestMessage="Please sign this document",
        )
    ]
    transaction = Transaction(
        Language=Language.nl_NL,
        Signers=signers,
        PostbackUrl=os.getenv("TEST_POSTBACK_TUNNEL"),
    )

    created = signhost.transaction_init(transaction)

    cwd = Path(__file__).parent

    assert created.Id

    time.sleep(1)

    assert signhost.transaction_get(created.Id).Status == Status.WAITING_FOR_DOCUMENT

    upload_response = signhost.transaction_file_put(
        created.Id,
        secrets.token_urlsafe(16),
        (cwd / "invoice.pdf").open("rb"),
    )

    assert upload_response.status_code == 201

    assert signhost.transaction_start(created.Id)


def test_get_transaction(signhost):
    x = signhost.transaction_get("d73340de-3cf9-4707-b18f-bf64ed58e058")

    assert x

    signhost.transaction_start("d73340de-3cf9-4707-b18f-bf64ed58e058")


def test_receipt_get(signhost):
    signhost.receipt_get("d73340de-3cf9-4707-b18f-bf64ed58e058")
