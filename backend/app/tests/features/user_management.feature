Feature: User management

    Scenario: Create a new user
      Given I am an authenticated superuser
      When I create a user with email "test@example.com" and password "password123"
      Then the response status code should be 200
      And the response should contain the email "test@example.com"

    Scenario: Get user by ID
      Given I am an authenticated superuser
      When I get a user by ID
      Then the response status code should be 200
      And the response should contain user details

    Scenario: Update user
      Given I am an authenticated superuser
      When I update a user with new email "updated@example.com"
      Then the response status code should be 200
      And the response should contain the email "updated@example.com"

    Scenario: Delete user
      Given I am an authenticated superuser
      When I delete a user
      Then the response status code should be 200
      And the user should no longer exist