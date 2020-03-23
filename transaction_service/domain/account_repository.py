from transaction_service.domain.account import Account


class AccountRepository:
    def __init__(self,
                 accounts_client,
                 transaction_repository,
                 balance_updates):
        self.accounts_client = accounts_client
        self.transaction_repository = transaction_repository
        self.balance_updates = balance_updates

    def fetch_by_account_number(self, account_number):
        if not self._account_exists(account_number):
            raise AccountNotFound()

        transactions = self._fetch_transactions(account_number)

        account = Account(account_number=account_number,
                          transaction_repository=self.transaction_repository,
                          balance_updates=self.balance_updates,
                          transactions=transactions)

        return account

    def _account_exists(self, account_number):
        return self.accounts_client.has_active_account(account_number)

    def _fetch_transactions(self, account_number):
        return self.transaction_repository \
            .fetch_by_account_number(account_number)


class AccountNotFound(RuntimeError):
    pass
