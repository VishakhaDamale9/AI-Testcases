Feature: User Management

  Scenario: Create a new user
    Given I am an authenticated superuser
    When I create a user with email "test@example.com" and password "password123"
    Then the response status code should be 200
    And the response should contain the email "test@example.com"

  Scenario: Get user by ID
    Given I am an authenticated superuser
    When I get a user by ID "1"
    Then the response status code should be 200
    And the response should contain user details

  Scenario: Get non-existent user
    Given I am an authenticated superuser
    When I get a user by ID "999"
    Then the response status code should be 404

  Scenario: Update user
    Given I am an authenticated superuser
    When I update a user with ID "1" with new email "updated@example.com"
    Then the response status code should be 200
    And the response should contain the email "updated@example.com"

  Scenario: Update user with invalid email
    Given I am an authenticated superuser
    When I update a user with ID "1" with new email "invalid-email"
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Delete user
    Given I am an authenticated superuser
    When I delete a user with ID "1"
    Then the response status code should be 200
    And the user should no longer exist

  Scenario: Delete non-existent user
    Given I am an authenticated superuser
    When I delete a user with ID "999"
    Then the response status code should be 404

  Scenario: Access user endpoint without authentication
    Given I am not authenticated
    When I get a user by ID "1"
    Then the response status code should be 401

  Scenario: Access user endpoint as non-superuser
    Given I am an authenticated regular user
    When I get a user by ID "1"
    Then the response status code should be 403