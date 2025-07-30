Feature: Authentication

  Scenario: Access with invalid JWT token
    Given I have an invalid JWT token
    When I access a protected endpoint
    Then the response status code should be 403
    And the response should contain "Could not validate credentials"

  Scenario: Access with token for non-existent user
    Given I have a JWT token for a deleted user
    When I access a protected endpoint
    Then the response status code should be 404
    And the response should contain "User not found"

  Scenario: Access with inactive user
    Given I have a JWT token for an inactive user
    When I access a protected endpoint
    Then the response status code should be 400
    And the response should contain "Inactive user" 