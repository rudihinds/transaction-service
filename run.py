import os

import structlog

from transaction_service.app import Application
from transaction_service.infrastructure.postgresql_transaction_repository import PostgreSQLTransactionRepository  # noqa
from transaction_service.infrastructure.rabbit_events import RabbitConsumer, \
    RabbitProducer
from transaction_service.infrastructure.rest_accounts_client import \
    RestAccountsClient

if __name__ == "__main__":
    consumer_properties = dict(exchange='transactions',
                               queue='transactions',
                               host=os.getenv('RABBITMQ_HOST', 'localhost'))

    producer_properties = dict(exchange='balance_updates',
                               host=os.getenv('RABBITMQ_HOST', 'localhost'))

    consumer = RabbitConsumer(consumer_properties)
    publisher = RabbitProducer(producer_properties)
    accounts = RestAccountsClient(os.getenv('ACCOUNT_SERVICE_URL'))

    app = Application(transaction_events=consumer, balance_updates=publisher,
                      accounts_client=accounts,
                      transaction_repository=PostgreSQLTransactionRepository(
                          username=os.getenv('DB_USERNAME'),
                          password=os.getenv('DB_PASSWORD'),
                          host=os.getenv('DB_HOST'),
                          port=os.getenv('DB_PORT'),
                          db='transaction-service'),
                      logger=structlog.get_logger())

    app.start()
