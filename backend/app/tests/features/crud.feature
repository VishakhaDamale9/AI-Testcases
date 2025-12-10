Feature: User Management API
  As a user
  I want to be able to create, read, update and delete users
  So that I can manage user data

  Scenario: Create a new user
    Given a new user with email "user@example.com" and password "password123"
    When I create the user
    Then the user should be created with the correct email and hashed password
    And the user should have a unique ID

  Scenario: Create a new user with missing required fields
    Given a new user with missing email and password
    When I create the user
    Then a validation error should be raised for missing email
    And a validation error should be raised for missing password

  Scenario: Create a new user with invalid email
    Given a new user with email "invalid_email"
    When I create the user
    Then a validation error should be raised for invalid email

  Scenario: Create a new user with invalid password
    Given a new user with password "invalid_password"
    When I create the user
    Then a validation error should be raised for invalid password

  Scenario: Update an existing user
    Given an existing user with email "user@example.com" and password "password123"
    When I update the user with new email "new_user@example.com" and password "new_password123"
    Then the user should be updated with the new email and hashed password
    And the user should have the same ID

  Scenario: Update an existing user with missing required fields
    Given an existing user with email "user@example.com" and password "password123"
    When I update the user with missing email and password
    Then a validation error should be raised for missing email
    And a validation error should be raised for missing password

  Scenario: Update an existing user with invalid email
    Given an existing user with email "user@example.com" and password "password123"
    When I update the user with email "invalid_email"
    Then a validation error should be raised for invalid email

  Scenario: Update an existing user with invalid password
    Given an existing user with email "user@example.com" and password "password123"
    When I update the user with password "invalid_password"
    Then a validation error should be raised for invalid password

  Scenario: Authenticate a user with correct credentials
    Given an existing user with email "user@example.com" and password "password123"
    When I authenticate the user with email "user@example.com" and password "password123"
    Then the user should be authenticated successfully

  Scenario: Authenticate a user with incorrect password
    Given an existing user with email "user@example.com" and password "password123"
    When I authenticate the user with email "user@example.com" and password "wrong_password"
    Then the user should not be authenticated

  Scenario: Authenticate a user with non-existent email
    Given a non-existent user with email "non_existent@example.com"
    When I authenticate the user with email "non_existent@example.com" and password "password123"
    Then the user should not be authenticated

  Scenario: Get a user by email
    Given an existing user with email "user@example.com"
    When I get the user by email "user@example.com"
    Then the user should be retrieved successfully

  Scenario: Get a user by non-existent email
    Given a non-existent user with email "non_existent@example.com"
    When I get the user by email "non_existent@example.com"
    Then the user should not be retrieved

  Scenario: Create an item for a user
    Given an existing user with email "user@example.com"
    When I create an item for the user with name "item_name"
    Then the item should be created successfully
    And the item should be owned by the user

  Scenario: Create an item for a user with missing required fields
    Given an existing user with email "user@example.com"
    When I create an item for the user with missing name
    Then a validation error should be raised for missing name

  Scenario: Create an item for a user with invalid name
    Given an existing user with email "user@example.com"
    When I create an item for the user with name "invalid_name"
    Then a validation error should be raised for invalid name