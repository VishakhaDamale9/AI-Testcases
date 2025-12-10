Feature: Authentication and Authorization

  Scenario: Unauthenticated user tries to create access token
    Given the user is not authenticated
    When the user tries to create an access token
    Then the API returns a 401 Unauthorized response

  Scenario: Normal user tries to create access token
    Given the user is authenticated as a normal user
    When the user tries to create an access token
    Then the API returns a 200 OK response with a valid access token

  Scenario: Superuser tries to create access token
    Given the user is authenticated as a superuser
    When the user tries to create an access token
    Then the API returns a 200 OK response with a valid access token

  Scenario: User tries to create access token with invalid subject
    Given the user is authenticated as a normal user
    When the user tries to create an access token with an invalid subject
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to create access token with empty subject
    Given the user is authenticated as a normal user
    When the user tries to create an access token with an empty subject
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to create access token with expired subject
    Given the user is authenticated as a normal user
    When the user tries to create an access token with an expired subject
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to create access token with invalid expires delta
    Given the user is authenticated as a normal user
    When the user tries to create an access token with an invalid expires delta
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to create access token with empty expires delta
    Given the user is authenticated as a normal user
    When the user tries to create an access token with an empty expires delta
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to verify a password with an invalid password
    Given the user is authenticated as a normal user
    When the user tries to verify a password with an invalid password
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to verify a password with an empty password
    Given the user is authenticated as a normal user
    When the user tries to verify a password with an empty password
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to get a password hash with an empty password
    Given the user is authenticated as a normal user
    When the user tries to get a password hash with an empty password
    Then the API returns a 400 Bad Request response with a validation error

  Scenario: User tries to verify a password with a valid password
    Given the user is authenticated as a normal user
    When the user tries to verify a password with a valid password
    Then the API returns a 200 OK response with a verification result

  Scenario: User tries to get a password hash with a valid password
    Given the user is authenticated as a normal user
    When the user tries to get a password hash with a valid password
    Then the API returns a 200 OK response with a password hash

  Scenario: User tries to create access token with a valid subject and expires delta
    Given the user is authenticated as a normal user
    When the user tries to create an access token with a valid subject and expires delta
    Then the API returns a 200 OK response with a valid access token

  Scenario: User tries to create access token with a valid subject and empty expires delta
    Given the user is authenticated as a normal user
    When the user tries to create an access token with a valid subject and empty expires delta
    Then the API returns a 200 OK response with a valid access token

  Scenario: User tries to create access token with a valid subject and expired expires delta
    Given the user is authenticated as a normal user
    When the user tries to create an access token with a valid subject and expired expires delta
    Then the API returns a 400 Bad Request response with a validation error