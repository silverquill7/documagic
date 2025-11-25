Feature: User Login

  Scenario: Successful login
    Given a user exists with email "user@example.com" and password "Password123"
    When the user logs in with correct credentials
    Then the system should log the user in successfully
