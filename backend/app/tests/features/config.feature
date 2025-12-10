Feature: Settings API Endpoints

  Scenario: Unauthenticated user tries to access settings
    Given the API is running
    When the user sends a GET request to "/api/v1/settings"
    Then the response status code is 401
    And the response contains "Not authenticated"

  Scenario: Normal user tries to access settings
    Given the API is running
    And the user is authenticated with normal user credentials
    When the user sends a GET request to "/api/v1/settings"
    Then the response status code is 200
    And the response contains the settings

  Scenario: Superuser tries to access settings
    Given the API is running
    And the user is authenticated with superuser credentials
    When the user sends a GET request to "/api/v1/settings"
    Then the response status code is 200
    And the response contains the settings

  Scenario: Unauthenticated user tries to update settings
    Given the API is running
    When the user sends a PATCH request to "/api/v1/settings" with invalid credentials
    Then the response status code is 401
    And the response contains "Not authenticated"

  Scenario: Normal user tries to update settings
    Given the API is running
    And the user is authenticated with normal user credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data
    Then the response status code is 200
    And the response contains the updated settings

  Scenario: Superuser tries to update settings
    Given the API is running
    And the user is authenticated with superuser credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data
    Then the response status code is 200
    And the response contains the updated settings

  Scenario: Unauthenticated user tries to update SECRET_KEY
    Given the API is running
    When the user sends a PATCH request to "/api/v1/settings" with invalid credentials and SECRET_KEY set to "changethis"
    Then the response status code is 401
    And the response contains "Not authenticated"

  Scenario: Normal user tries to update SECRET_KEY
    Given the API is running
    And the user is authenticated with normal user credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and SECRET_KEY set to "changethis"
    Then the response status code is 400
    And the response contains "The value of SECRET_KEY is 'changethis', for security, please change it, at least for deployments."

  Scenario: Superuser tries to update SECRET_KEY
    Given the API is running
    And the user is authenticated with superuser credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and SECRET_KEY set to "changethis"
    Then the response status code is 400
    And the response contains "The value of SECRET_KEY is 'changethis', for security, please change it, at least for deployments."

  Scenario: Unauthenticated user tries to update POSTGRES_PASSWORD
    Given the API is running
    When the user sends a PATCH request to "/api/v1/settings" with invalid credentials and POSTGRES_PASSWORD set to "changethis"
    Then the response status code is 401
    And the response contains "Not authenticated"

  Scenario: Normal user tries to update POSTGRES_PASSWORD
    Given the API is running
    And the user is authenticated with normal user credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and POSTGRES_PASSWORD set to "changethis"
    Then the response status code is 400
    And the response contains "The value of POSTGRES_PASSWORD is 'changethis', for security, please change it, at least for deployments."

  Scenario: Superuser tries to update POSTGRES_PASSWORD
    Given the API is running
    And the user is authenticated with superuser credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and POSTGRES_PASSWORD set to "changethis"
    Then the response status code is 400
    And the response contains "The value of POSTGRES_PASSWORD is 'changethis', for security, please change it, at least for deployments."

  Scenario: Unauthenticated user tries to update FIRST_SUPERUSER_PASSWORD
    Given the API is running
    When the user sends a PATCH request to "/api/v1/settings" with invalid credentials and FIRST_SUPERUSER_PASSWORD set to "changethis"
    Then the response status code is 401
    And the response contains "Not authenticated"

  Scenario: Normal user tries to update FIRST_SUPERUSER_PASSWORD
    Given the API is running
    And the user is authenticated with normal user credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and FIRST_SUPERUSER_PASSWORD set to "changethis"
    Then the response status code is 400
    And the response contains "The value of FIRST_SUPERUSER_PASSWORD is 'changethis', for security, please change it, at least for deployments."

  Scenario: Superuser tries to update FIRST_SUPERUSER_PASSWORD
    Given the API is running
    And the user is authenticated with superuser credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and FIRST_SUPERUSER_PASSWORD set to "changethis"
    Then the response status code is 400
    And the response contains "The value of FIRST_SUPERUSER_PASSWORD is 'changethis', for security, please change it, at least for deployments."

  Scenario: Unauthenticated user tries to update FRONTEND_HOST
    Given the API is running
    When the user sends a PATCH request to "/api/v1/settings" with invalid credentials and FRONTEND_HOST set to "http://example.com"
    Then the response status code is 401
    And the response contains "Not authenticated"

  Scenario: Normal user tries to update FRONTEND_HOST
    Given the API is running
    And the user is authenticated with normal user credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and FRONTEND_HOST set to "http://example.com"
    Then the response status code is 200
    And the response contains the updated settings

  Scenario: Superuser tries to update FRONTEND_HOST
    Given the API is running
    And the user is authenticated with superuser credentials
    When the user sends a PATCH request to "/api/v1/settings" with valid data and FRONTEND_HOST set to "http://example.com"
    Then the response status code is 200
    And the response contains the updated settings

  Scenario: parse_cors function handles empty input
    Given the input is an empty string
    When the function parse_cors is called with the input
    Then the output is an empty list

  Scenario: parse_cors function handles single origin
    Given the input is a string with a single origin
    When the function parse_cors is called with the input
    Then the output is a list with the single origin

  Scenario: parse_cors function handles multiple origins
    Given the input is a string with multiple origins
    When the function parse_cors is called with the input
    Then the output is a list with the multiple origins

  Scenario: parse_cors function handles invalid input
    Given the input is an invalid value
    When the function parse_cors is called with the input
    Then the output is an error message

  Scenario: parse_cors_origins function handles empty input
    Given the input is an empty string
    When the function parse_cors_origins is called with the input
    Then the output is an empty list

  Scenario: parse_cors_origins function handles single origin
    Given the input is a string with a single origin
    When the function parse_cors_origins is called with the input
    Then the output is a list with the single origin

  Scenario: parse_cors_origins function handles multiple origins
    Given the input is a string with multiple origins
    When the function parse_cors_origins is called with the input
    Then the output is a list with the multiple origins

  Scenario: parse_cors_origins function handles invalid input
    Given the input is an invalid value
    When the function parse_cors_origins is called with the input
    Then the output is an error message

  Scenario: _check_default_secret function handles default SECRET_KEY
    Given the SECRET_KEY is set to "changethis"
    When the function _check_default_secret is called with the SECRET_KEY
    Then the output is a warning message

  Scenario: _check_default_secret function handles non-default SECRET_KEY
    Given the SECRET_KEY is set to a non-default value
    When the function _check_default_secret is called with the SECRET_KEY
    Then the output is an empty message

  Scenario: _check_default_secret function handles default POSTGRES_PASSWORD
    Given the POSTGRES_PASSWORD is set to "changethis"
    When the function _check_default_secret is called with the POSTGRES_PASSWORD
    Then the output is a warning message

  Scenario: _check_default_secret function handles non-default POSTGRES_PASSWORD
    Given the POSTGRES_PASSWORD is set to a non-default value
    When the function _check_default_secret is called with the POSTGRES_PASSWORD
    Then the output is an empty message

  Scenario: _check_default_secret function handles default FIRST_SUPERUSER_PASSWORD
    Given the FIRST