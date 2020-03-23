import pytest

from transaction_service.domain.account import Transaction
from transaction_service.mock.mock_transaction_repository import \
    MockTransactionRepository


@pytest.fixture
def transactions():
    return MockTransactionRepository()


def test_fetch_by_account_number_when_no_transactions(transactions):
    assert transactions.fetch_by_account_number('1234') == []


def test_fetch_by_account_number_returns_the_transactions(transactions):
    account_a = '1234'
    account_b = '4567'
    tx1 = Transaction(account_number=account_a, amount=10)
    tx2 = Transaction(account_number=account_b, amount=20)
    tx3 = Transaction(account_number=account_a, amount=30)
    transactions.store(tx1)
    transactions.store(tx2)
    transactions.store(tx3)

    assert transactions.fetch_by_account_number(account_a) == [tx1, tx3]
