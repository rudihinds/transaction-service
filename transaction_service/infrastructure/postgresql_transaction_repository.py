import uuid

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from transaction_service.domain.account import Transaction


class PostgreSQLTransactionRepository:
    def __init__(self, host, port, username, password, db):
        url = f'postgresql://{username}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(url)
        declarative_base().metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def store(self, transaction):
        transaction.id = str(uuid.uuid4()),
        self.session.add(transaction)
        self.session.commit()

    def fetch_by_account_number(self, account_number):
        return self.session \
            .query(Transaction) \
            .filter(Transaction.account_number == account_number)
