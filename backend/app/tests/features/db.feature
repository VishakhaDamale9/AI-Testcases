Feature: User Management API

  Scenario: Unauthenticated user tries to create a new user
    Given the API endpoint "/users" is not authenticated
    When the user sends a POST request with invalid credentials
    Then the API returns a 401 Unauthorized status code
    And the response contains the error message "Not authenticated"

  Scenario: Normal user tries to create a new user
    Given the API endpoint "/users" is authenticated with a normal user
    When the user sends a POST request with valid credentials
    Then the API returns a 201 Created status code
    And the response contains the user's details

  Scenario: Superuser tries to create a new user
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a POST request with valid credentials
    Then the API returns a 201 Created status code
    And the response contains the user's details

  Scenario: Validating required fields for user creation
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a POST request with missing required fields
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Missing required fields"

  Scenario: Validating email format for user creation
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a POST request with an invalid email format
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Invalid email format"

  Scenario: Validating password strength for user creation
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a POST request with a weak password
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Password must be at least 8 characters long"

  Scenario: Validating existing email for user creation
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a POST request with an existing email
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Email already exists"

  Scenario: Validating existing username for user creation
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a POST request with an existing username
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Username already exists"

  Scenario: Superuser tries to read a non-existent user
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a GET request for a non-existent user
    Then the API returns a 404 Not Found status code
    And the response contains the error message "User not found"

  Scenario: Normal user tries to read a user they don't own
    Given the API endpoint "/users" is authenticated with a normal user
    When the user sends a GET request for a user they don't own
    Then the API returns a 403 Forbidden status code
    And the response contains the error message "Forbidden"

  Scenario: Superuser tries to update a non-existent user
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a PATCH request for a non-existent user
    Then the API returns a 404 Not Found status code
    And the response contains the error message "User not found"

  Scenario: Normal user tries to update a user they don't own
    Given the API endpoint "/users" is authenticated with a normal user
    When the user sends a PATCH request for a user they don't own
    Then the API returns a 403 Forbidden status code
    And the response contains the error message "Forbidden"

  Scenario: Validating required fields for user update
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a PATCH request with missing required fields
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Missing required fields"

  Scenario: Validating email format for user update
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a PATCH request with an invalid email format
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Invalid email format"

  Scenario: Validating password strength for user update
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a PATCH request with a weak password
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Password must be at least 8 characters long"

  Scenario: Validating existing email for user update
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a PATCH request with an existing email
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Email already exists"

  Scenario: Validating existing username for user update
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a PATCH request with an existing username
    Then the API returns a 422 Unprocessable Entity status code
    And the response contains the error message "Username already exists"

  Scenario: Superuser tries to delete a non-existent user
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a DELETE request for a non-existent user
    Then the API returns a 404 Not Found status code
    And the response contains the error message "User not found"

  Scenario: Normal user tries to delete a user they don't own
    Given the API endpoint "/users" is authenticated with a normal user
    When the user sends a DELETE request for a user they don't own
    Then the API returns a 403 Forbidden status code
    And the response contains the error message "Forbidden"

  Scenario: Superuser tries to delete a user with active sessions
    Given the API endpoint "/users" is authenticated with a superuser
    When the user sends a DELETE request for a user with active sessions
    Then the API returns a 409 Conflict status code
    And the response contains the error message "User has active sessions"