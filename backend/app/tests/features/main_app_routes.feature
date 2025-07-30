Feature: Main App Routes

  Scenario: Access root route
    When I access the root route
    Then the response contains "Welcome to FastAPI"

  Scenario: Access favicon route
    When I access the favicon route
    Then the response is a file or 404 