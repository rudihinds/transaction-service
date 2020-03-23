Feature: Debiting account
  As a service I want to debit an account

  Scenario: Debit account
    Given an account 87654321 has balance 50
    When an account 87654321 is debited with 30
    Then a account 87654321 should have a balance of 20

  Scenario: Account does not exist
    Given there is not account with the number 87654321
    When an account 87654321 is debited with 10
    Then a bad transaction should be reported

    # Scenario: Amount debited is greater than the current balance
