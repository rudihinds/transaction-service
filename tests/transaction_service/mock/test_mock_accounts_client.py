from transaction_service.mock.mock_accounts_client import MockAccountsClient
import pytest


@pytest.fixture(scope="function")
def accounts():
    accounts = MockAccountsClient()
    return accounts


def test_has_with_number_return_false_when_not_exists(accounts):
    accounts.add({
        'accountNumber': '2344235'
    })
    assert accounts.has_active_account('2344234') is False


def test_has_with_number_return_true_when_exists(accounts):
    account_number = '31245987'
    accounts.add({
        'accountNumber': account_number
    })
    assert accounts.has_active_account(account_number) is True
