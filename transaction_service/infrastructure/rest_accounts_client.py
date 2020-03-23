import requests


class RestAccountsClient:
    def __init__(self, url):
        self.url = url

    def has_active_account(self, account_number):
        url = f'{self.url}/accounts/{account_number}'

        response = requests.get(url)

        if response.status_code is not 200:
            return False

        body = response.json()

        if body['accountStatus'] == 'closed':
            return False

        return True
