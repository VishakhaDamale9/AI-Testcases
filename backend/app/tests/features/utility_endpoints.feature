Feature: Utility Endpoints

  Scenario: Send test email
    When I send a test email to "test@example.com"
    Then the response should contain "Test email sent"

  Scenario: Health check endpoint
    When I check the health endpoint
    Then the response should be true 