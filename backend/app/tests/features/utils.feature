Feature: API Endpoint

  Scenario: Successful request
    Given I am an authenticated user
    When I make a request to the endpoint
    Then the response status code should be 200
    And the response should contain expected data

  Scenario: Unauthorized request
    Given I am not authenticated
    When I make a request to the endpoint
    Then the response status code should be 401

  Scenario: Validation error
    Given I am an authenticated user
    When I make a request with invalid data
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Not found error
    Given I am an authenticated user
    When I make a request for a non-existent resource
    Then the response status code should be 404