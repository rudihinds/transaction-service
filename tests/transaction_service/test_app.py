import json
from datetime import datetime
from unittest import mock
from unittest.mock import Mock

import pytest

from transaction_service.app import Application
from transaction_service.domain.account import Transaction
from transaction_service.mock.mock_events import MockEvents
from transaction_service.mock.mock_transaction_repository import \
    MockTransactionRepository


@pytest.fixture(scope='function')
def app(logger):
    app = Application(
        transaction_events=MockEvents(),
        balance_updates=MockEvents(),
        accounts_client=Mock(),
        transaction_repository=MockTransactionRepository(),
        logger=logger)

    app.start()

    return app


@pytest.fixture(scope='function')
def logger():
    return Mock()


def test_a_message_is_logged_on_event(app, logger):
    event = dict(accountNumber='1234', amount='99')
    app.transaction_events.produce(event)
    logger.debug.assert_called_with('Received transaction event',
                                    received_event=event)


GOOD_PAYLOAD = dict(id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
                    accountNumber='12345678',
                    amount=99,
                    operation='credit',
                    status='accepted',
                    created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))


@pytest.mark.parametrize(
    'payload',
    [dict(),
     {**GOOD_PAYLOAD, 'extra': '?'},
     {**GOOD_PAYLOAD, 'id': ''},
     {**GOOD_PAYLOAD, 'accountNumber': '1234567'},
     {**GOOD_PAYLOAD, 'accountNumber': '123456789'},
     {**GOOD_PAYLOAD, 'amount': '10'},
     {**GOOD_PAYLOAD, 'amount': 0},
     {**GOOD_PAYLOAD, 'operation': 'bad'},
     {**GOOD_PAYLOAD, 'status': 'unknown'},
     {**GOOD_PAYLOAD, 'created': ''}])
def test_invalid_payloads_log_and_abort(payload, app, logger):
    app.transaction_events.produce(payload)

    assert app.balance_updates.last_event is None
    logger.warning.assert_called_with('Invalid transaction event',
                                      error=mock.ANY,
                                      received_event=payload)


def test_the_app_checks_if_the_account_exists(app):
    app.transaction_events.produce(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber='12345678',
        amount=99,
        operation='credit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))

    app.accounts_client.has_active_account.assert_called()


def test_successful_credit_transaction(app, logger):
    account_number = '12345678'
    app.transaction_repository.store(Transaction(account_number=account_number,
                                                 amount=100))

    app.transaction_events.produce(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber=account_number,
        amount=99,
        operation='credit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))

    expected_event = dict(accountNumber="12345678", balance=199)
    assert json.loads(app.balance_updates.last_event) == expected_event
    logger.info.assert_called_with('Successful credit transaction',
                                   account_number=account_number,
                                   amount=99,
                                   balance=199)


def test_successful_debit_transaction(app, logger):
    account_number = '12345678'
    app.transaction_repository.store(Transaction(account_number=account_number,
                                                 amount=187))

    app.transaction_events.produce(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber=account_number,
        amount=87,
        operation='debit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))

    expected_event = dict(accountNumber="12345678", balance=100)
    assert json.loads(app.balance_updates.last_event) == expected_event
    logger.info.assert_called_with('Successful debit transaction',
                                   account_number=account_number,
                                   amount=87,
                                   balance=100)


def test_transaction_when_account_is_not_active(app, logger):
    app.accounts_client.has_active_account.return_value = False

    account_number = '12345678'
    app.transaction_events.produce(
        dict(
            id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
            accountNumber=account_number,
            amount=99,
            operation='credit',
            status='accepted',
            created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))

    assert app.balance_updates.last_event is None
    logger.warning.assert_called_with('Attempted transaction against inactive '
                                      'account',
                                      account_number=account_number,
                                      amount=99)
