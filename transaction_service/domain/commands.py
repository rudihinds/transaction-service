from transaction_service.domain.account_repository import AccountNotFound


class CreditAccount:
    def __init__(self, account_repository, logger):
        self.account_repository = account_repository
        self.logger = logger

    def execute(self, account_number, amount):
        try:
            account = self._load_account(account_number)
            account.credit(amount)
            self.logger.info('Successful credit transaction',
                             account_number=account_number,
                             amount=amount,
                             balance=account.balance)
        except AccountNotFound:
            self.logger.warning(
                'Attempted transaction against inactive account',
                account_number=account_number,
                amount=amount)

    def _load_account(self, account_number):
        return self.account_repository.fetch_by_account_number(account_number)


class DebitAccount:
    def __init__(self, account_repository, logger):
        self.account_repository = account_repository
        self.logger = logger

    def execute(self, account_number, amount):
        try:
            account = self._load_account(account_number)
            account.debit(amount)
            self.logger.info('Successful debit transaction',
                             account_number=account_number,
                             amount=amount,
                             balance=account.balance)
        except AccountNotFound:
            self.logger.warning(
                'Attempted transaction against inactive account',
                account_number=account_number,
                amount=amount)

    def _load_account(self, account_number):
        return self.account_repository.fetch_by_account_number(account_number)
