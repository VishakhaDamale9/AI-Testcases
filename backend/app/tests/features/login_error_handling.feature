Feature: Login Error Handling

  Scenario: Login with incorrect password
    When I try to login with email "admin@example.com" and password "wrongpassword"
    Then the response status code should be 400
    And the response should contain "Incorrect email or password"

  Scenario: Login with inactive user
    Given a user exists with email "inactive@example.com" and is inactive
    When I try to login with email "inactive@example.com" and password "userpassword"
    Then the response status code should be 400
    And the response should contain "Inactive user" 