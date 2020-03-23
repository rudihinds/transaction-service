import json

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


class Account:
    def __init__(self,
                 account_number,
                 transaction_repository,
                 balance_updates,
                 transactions):
        self.account_number = account_number
        self.balance = sum([tx.amount for tx in transactions])
        self.balance_updates = balance_updates
        self.transaction_repository = transaction_repository

    def credit(self, amount):
        transaction = Transaction(account_number=self.account_number,
                                  amount=amount)
        self.transaction_repository.store(transaction)
        self.balance = self.balance + amount
        self._produce_update()

    def debit(self, amount):
        transaction = Transaction(account_number=self.account_number,
                                  amount=-amount)
        self.transaction_repository.store(transaction)
        self.balance = self.balance - amount
        self._produce_update()

    def _produce_update(self):
        balance_update = json.dumps(dict(accountNumber=self.account_number,
                                         balance=self.balance))
        self.balance_updates.produce(balance_update)


Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String(50), primary_key=True)
    account_number = Column(String(50))
    amount = Column(Integer)
