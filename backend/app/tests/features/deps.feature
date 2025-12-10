Feature: Authentication and Authorization

  Scenario: Unauthenticated user tries to access a protected endpoint
    Given the user is not authenticated
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: Normal user tries to access a protected endpoint
    Given the user is authenticated as a normal user
    When the user tries to access a protected endpoint
    Then the API returns a 200 OK status code with the user's details

  Scenario: Superuser tries to access a protected endpoint
    Given the user is authenticated as a superuser
    When the user tries to access a protected endpoint
    Then the API returns a 200 OK status code with the user's details

  Scenario: User tries to access a protected endpoint with an invalid token
    Given the user is authenticated with an invalid token
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with an expired token
    Given the user is authenticated with an expired token
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that has been blacklisted
    Given the user is authenticated with a blacklisted token
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that has been revoked
    Given the user is authenticated with a revoked token
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that has been issued for a different user
    Given the user is authenticated with a token issued for a different user
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with an empty token
    Given the user is authenticated with an empty token
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that contains invalid characters
    Given the user is authenticated with a token that contains invalid characters
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that has been tampered with
    Given the user is authenticated with a tampered token
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that has expired due to a clock skew
    Given the user is authenticated with a token that has expired due to a clock skew
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: User tries to access a protected endpoint with a token that has been issued for a user who is not active
    Given the user is authenticated with a token issued for a user who is not active
    When the user tries to access a protected endpoint
    Then the API returns a 400 Bad Request status code

  Scenario: User tries to access a protected endpoint with a token that has been issued for a user who is inactive
    Given the user is authenticated with a token issued for a user who is inactive
    When the user tries to access a protected endpoint
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to access a protected endpoint with a token that has been issued for a user who is not a superuser
    Given the user is authenticated as a superuser with a token issued for a user who is not a superuser
    When the user tries to access a protected endpoint
    Then the API returns a 403 Forbidden status code

  Scenario: Superuser tries to access a protected endpoint with a token that has been issued for a user who is a superuser
    Given the user is authenticated as a superuser with a token issued for a user who is a superuser
    When the user tries to access a protected endpoint
    Then the API returns a 200 OK status code with the user's details