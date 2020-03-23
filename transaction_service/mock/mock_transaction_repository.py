class MockTransactionRepository:
    def __init__(self):
        self.transactions = []

    def store(self, transaction):
        self.transactions.append(transaction)

    def fetch_by_account_number(self, account_number):
        return [tx for tx in self.transactions if
                tx.account_number == account_number]
