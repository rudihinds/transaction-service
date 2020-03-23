Feature: Crediting account
  As a service I want to credit an account

  Scenario: Crediting account
    Given an account 12345678 has balance 0
    When an account 12345678 is credited with 10
    Then a account 12345678 should have a balance of 10

  Scenario: Account does not exist
    Given there is not account with the number 12345678
    When an account 12345678 is credited with 10
    Then a bad transaction should be reported
