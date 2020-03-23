import json
from datetime import datetime

from behave import given, when, then


@given('an account {account_number} has balance {amount:d}')
def create_account(context, account_number, amount):
    context.accounts_client.add(dict(accountNumber=account_number,
                                     accountState='active'))

    if amount > 0:
        credit_account(context, account_number, amount)


@given('there is not account with the number {account_number}')
def do_not_create_account(context, account_number):
    pass  # Intentional no-op


@when('an account {account_number} is credited with {amount:d}')
def credit_account(context, account_number, amount):
    context.events_in.produce(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber=account_number,
        amount=amount,
        operation='credit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))


@when("an account {account_number} is debited with {amount:d}")
def step_impl(context, account_number, amount):
    context.events_in.produce(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber=account_number,
        amount=amount,
        operation='debit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))


@then('a account {account_number} should have a balance of {balance:d}')
def assert_account_balance(context, account_number, balance):
    published_event = json.loads(context.events_out.last_event)

    expected_event = dict(accountNumber=account_number, balance=balance)

    assert published_event == expected_event, \
        f'{repr(published_event)} != {repr(expected_event)}'


@then('a bad transaction should be reported')
def assert_bad_transaction(context):
    published_event = context.events_out.last_event
    assert published_event is None
