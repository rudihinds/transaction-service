class MockAccountsClient:
    def __init__(self):
        self._accounts = dict()

    def add(self, account):
        self._accounts[account['accountNumber']] = account

    def has_active_account(self, account):
        return account in self._accounts
