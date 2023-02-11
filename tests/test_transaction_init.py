from signhost.models import Transaction


def test_get_transaction(signhost, mocked_api, transaction_id, respx_mock, test_file):
    x = signhost.transaction_init(Transaction())

    y = signhost.transaction_get(x.Id)

    assert x.Id == y.Id

    with test_file.open("rb") as f:
        assert signhost.transaction_file_put(transaction_id, "file.pdf", f) is True
    submitted_file = signhost.transaction_file_get(transaction_id, "file.pdf")
    assert submitted_file
    assert signhost.transaction_start(transaction_id) is True
    assert signhost.transaction_cancel(transaction_id).Id == x.Id
    assert signhost.receipt_get(transaction_id)
