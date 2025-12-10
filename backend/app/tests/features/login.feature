Feature: Login and Password Recovery Endpoints

  Scenario: Successful login with valid credentials
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/access-token" with email "user@example.com" and password "password123"
    Then the response status code is 200
    And the response contains an access token

  Scenario: Unsuccessful login with invalid credentials
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/access-token" with email "wrong@example.com" and password "wrongpassword"
    Then the response status code is 400
    And the response contains the error message "Incorrect email or password"

  Scenario: Successful test token
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/test-token" with access token obtained from previous login
    Then the response status code is 200
    And the response contains the user's public information

  Scenario: Successful password recovery
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/password-recovery/user@example.com"
    Then the response status code is 200
    And the response contains a message indicating that the password recovery email was sent

  Scenario: Unsuccessful password recovery with non-existent user
    Given a non-existent user with email "wrong@example.com"
    When I send a POST request to "/password-recovery/wrong@example.com"
    Then the response status code is 404
    And the response contains the error message "The user with this email does not exist in the system."

  Scenario: Successful password recovery HTML content
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/password-recovery-html-content/user@example.com" as a superuser
    Then the response status code is 200
    And the response contains the HTML content for password recovery

  Scenario: Unsuccessful password recovery HTML content with non-existent user
    Given a non-existent user with email "wrong@example.com"
    When I send a POST request to "/password-recovery-html-content/wrong@example.com" as a superuser
    Then the response status code is 404
    And the response contains the error message "The user with this username does not exist in the system."

  Scenario: Successful password reset
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/reset-password/" with new password "newpassword" and access token obtained from previous login
    Then the response status code is 200
    And the response contains a message indicating that the password was updated successfully

  Scenario: Unsuccessful password reset with invalid token
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/reset-password/" with new password "newpassword" and invalid token
    Then the response status code is 400
    And the response contains the error message "Invalid token"

  Scenario: Unsuccessful password reset with non-existent user
    Given a non-existent user with email "wrong@example.com"
    When I send a POST request to "/reset-password/" with new password "newpassword" and access token obtained from previous login
    Then the response status code is 404
    And the response contains the error message "The user with this email does not exist in the system."

  Scenario: Unsuccessful password reset with inactive user
    Given an existing inactive user with email "user@example.com" and password "password123"
    When I send a POST request to "/reset-password/" with new password "newpassword" and access token obtained from previous login
    Then the response status code is 400
    And the response contains the error message "Inactive user"

  Scenario: Successful login with empty email
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/access-token" with email "" and password "password123"
    Then the response status code is 400
    And the response contains the error message "Incorrect email or password"

  Scenario: Successful login with empty password
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/access-token" with email "user@example.com" and password ""
    Then the response status code is 400
    And the response contains the error message "Incorrect email or password"

  Scenario: Successful login with null email
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/access-token" with email null and password "password123"
    Then the response status code is 400
    And the response contains the error message "Incorrect email or password"

  Scenario: Successful login with null password
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/access-token" with email "user@example.com" and password null
    Then the response status code is 400
    And the response contains the error message "Incorrect email or password"

  Scenario: Successful test token with null access token
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/test-token" with access token null
    Then the response status code is 401
    And the response contains the error message "Not authenticated"

  Scenario: Successful test token with empty access token
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/test-token" with access token ""
    Then the response status code is 401
    And the response contains the error message "Not authenticated"

  Scenario: Successful test token with null access token as superuser
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/test-token" with access token null as a superuser
    Then the response status code is 200
    And the response contains the user's public information

  Scenario: Successful test token with empty access token as superuser
    Given an existing user with email "user@example.com" and password "password123"
    When I send a POST request to "/login/test-token" with access token "" as a superuser
    Then the response status code is 200
    And the response contains the user's public information