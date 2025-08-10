Feature: User Management API

  Background:
    Given the application is running

  Scenario: Create a new user as superuser
    Given I am an authenticated superuser
    When I create a user with the following details:
      | email           | password   | is_superuser |
      | test@example.com | password123 | False        |
    Then the response status code should be 200
    And the response should contain a user with email "test@example.com"
    And the user should be stored in the database

  Scenario: Get user by ID
    Given I am an authenticated superuser
    And there is an existing user with ID "1"
    When I get the user with ID "1"
    Then the response status code should be 200
    And the response should contain a user with ID "1"

  Scenario: Get non-existent user
    Given I am an authenticated superuser
    When I get the user with ID "999"
    Then the response status code should be 404
    And the response should contain an error message

  Scenario: Update user
    Given I am an authenticated superuser
    And there is an existing user with ID "1"
    When I update the user with ID "1" with the following details:
      | email                | is_superuser |
      | updated@example.com | True         |
    Then the response status code should be 200
    And the response should contain a user with email "updated@example.com"
    And the user in the database should be updated

  Scenario: Delete user
    Given I am an authenticated superuser
    And there is an existing user with ID "1"
    When I delete the user with ID "1"
    Then the response status code should be 200
    And the user should be removed from the database

  Scenario: Access user endpoint without authentication
    Given I am not authenticated
    When I get the user with ID "1"
    Then the response status code should be 401
    And the response should contain an authentication error message

  Scenario: Access user endpoint as non-superuser
    Given I am an authenticated regular user
    When I get the user with ID "1"
    Then the response status code should be 403
    And the response should contain a permission error message

  Scenario: Create user with invalid email
    Given I am an authenticated superuser
    When I create a user with the following details:
      | email      | password   | is_superuser |
      | invalid-email | password123 | False        |
    Then the response status code should be 422
    And the response should contain validation errors for "email"

  Scenario: Create user with short password
    Given I am an authenticated superuser
    When I create a user with the following details:
      | email           | password | is_superuser |
      | test@example.com | short    | False        |
    Then the response status code should be 422
    And the response should contain validation errors for "password"

  Scenario: Update user with invalid email
    Given I am an authenticated superuser
    And there is an existing user with ID "1"
    When I update the user with ID "1" with the following details:
      | email      | is_superuser |
      | invalid-email | True         |
    Then the response status code should be 422
    And the response should contain validation errors for "email"

  Scenario: Update non-existent user
    Given I am an authenticated superuser
    When I update the user with ID "999" with the following details:
      | email                | is_superuser |
      | updated@example.com | True         |
    Then the response status code should be 404
    And the response should contain an error message

  Scenario: Delete non-existent user
    Given I am an authenticated superuser
    When I delete the user with ID "999"
    Then the response status code should be 404
    And the response should contain an error message