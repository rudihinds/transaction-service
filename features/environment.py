import logging

from structlog import wrap_logger

from transaction_service.app import Application
from transaction_service.mock.mock_accounts_client import MockAccountsClient
from transaction_service.mock.mock_events import MockEvents
from transaction_service.mock.mock_transaction_repository import \
    MockTransactionRepository


def before_scenario(context, scenario):
    context.events_in = MockEvents()
    context.events_out = MockEvents()

    context.accounts_client = MockAccountsClient()

    logger = logging.getLogger()
    logger.addHandler(logging.NullHandler())

    context.app = Application(
        transaction_events=context.events_in,
        balance_updates=context.events_out,
        accounts_client=context.accounts_client,
        transaction_repository=MockTransactionRepository(),
        logger=wrap_logger(logger))

    context.app.start()
