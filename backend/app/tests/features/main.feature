Feature: Root API Endpoint

  Scenario: Unauthenticated user visits root endpoint
    Given the API is running
    When an unauthenticated user sends a GET request to "/"
    Then the response status code is 200
    And the response contains "Welcome to FastAPI"
    And the response contains "/docs"
    And the response contains "/api/v1"

  Scenario: Normal user visits root endpoint
    Given the API is running
    And the user is authenticated as a normal user
    When a normal user sends a GET request to "/"
    Then the response status code is 200
    And the response contains "Welcome to FastAPI"
    And the response contains "/docs"
    And the response contains "/api/v1"

  Scenario: Superuser visits root endpoint
    Given the API is running
    And the user is authenticated as a superuser
    When a superuser sends a GET request to "/"
    Then the response status code is 200
    And the response contains "Welcome to FastAPI"
    And the response contains "/docs"
    And the response contains "/api/v1"

  Scenario: Unauthenticated user visits favicon endpoint
    Given the API is running
    When an unauthenticated user sends a GET request to "/favicon.ico"
    Then the response status code is 200
    And the response contains the favicon.ico file

  Scenario: Normal user visits favicon endpoint
    Given the API is running
    And the user is authenticated as a normal user
    When a normal user sends a GET request to "/favicon.ico"
    Then the response status code is 200
    And the response contains the favicon.ico file

  Scenario: Superuser visits favicon endpoint
    Given the API is running
    And the user is authenticated as a superuser
    When a superuser sends a GET request to "/favicon.ico"
    Then the response status code is 200
    And the response contains the favicon.ico file

  Scenario: Custom generate unique ID function returns route name
    Given the API is running
    When the custom generate unique ID function is called with an APIRoute object having no tags
    Then the function returns the route name

  Scenario: Custom generate unique ID function returns route name with tags
    Given the API is running
    When the custom generate unique ID function is called with an APIRoute object having tags
    Then the function returns the route name with tags

  Scenario: CORS is enabled for all origins
    Given the API is running
    When the CORS middleware is called with all origins enabled
    Then the middleware allows all origins

  Scenario: CORS is enabled for specific origins
    Given the API is running
    When the CORS middleware is called with specific origins enabled
    Then the middleware allows only the specified origins

  Scenario: API includes router with prefix
    Given the API is running
    When the API includes a router with a prefix
    Then the API has the router with the specified prefix

  Scenario: API includes router without prefix
    Given the API is running
    When the API includes a router without a prefix
    Then the API has the router without a prefix

  Scenario: API returns favicon.ico file
    Given the API is running
    When the API returns the favicon.ico file
    Then the response status code is 200
    And the response contains the favicon.ico file