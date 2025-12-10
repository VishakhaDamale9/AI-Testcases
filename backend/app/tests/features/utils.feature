Feature: Email Service

  Scenario: Send email with valid data
    Given the email service is configured
    When I send an email to "test@example.com" with subject "Test email" and HTML content "<p>Hello World!</p>"
    Then the email is sent successfully

  Scenario: Send email with invalid SMTP configuration
    Given the email service is not configured
    When I send an email to "test@example.com" with subject "Test email" and HTML content "<p>Hello World!</p>"
    Then the email is not sent

  Scenario: Send email with invalid email address
    Given the email service is configured
    When I send an email to "invalid_email" with subject "Test email" and HTML content "<p>Hello World!</p>"
    Then the email is not sent with error "Invalid email address"

  Scenario: Send email with missing subject
    Given the email service is configured
    When I send an email to "test@example.com" with subject "" and HTML content "<p>Hello World!</p>"
    Then the email is not sent with error "Subject is required"

  Scenario: Send email with missing HTML content
    Given the email service is configured
    When I send an email to "test@example.com" with subject "Test email" and HTML content ""
    Then the email is not sent with error "HTML content is required"

  Scenario: Generate test email
    Given the email service is configured
    When I generate a test email for "test@example.com"
    Then the email has subject "Test email" and HTML content "<p>Hello World!</p>"

  Scenario: Generate reset password email
    Given the email service is configured
    When I generate a reset password email for "test@example.com" with email "test@example.com" and token "abc123"
    Then the email has subject "Test email - Password recovery for user test@example.com" and HTML content "<p>Hello World!</p>"

  Scenario: Generate new account email
    Given the email service is configured
    When I generate a new account email for "test@example.com" with username "test_user" and password "password123"
    Then the email has subject "Test email - New account for user test_user" and HTML content "<p>Hello World!</p>"

  Scenario: Generate password reset token
    Given the email service is configured
    When I generate a password reset token for "test@example.com"
    Then the token is valid for 2 hours

  Scenario: Verify password reset token
    Given the email service is configured
    When I verify a password reset token "abc123"
    Then the email is "test@example.com"

  Scenario: Verify password reset token with invalid token
    Given the email service is configured
    When I verify a password reset token "invalid_token"
    Then the email is None

  Scenario: Verify password reset token with expired token
    Given the email service is configured
    When I generate a password reset token for "test@example.com"
    And I wait for 2 hours and 1 minute
    When I verify a password reset token "abc123"
    Then the email is None

  Scenario: Verify password reset token with token created in the past
    Given the email service is configured
    When I generate a password reset token for "test@example.com" with expiration time in the past
    When I verify a password reset token "abc123"
    Then the email is None