Feature: Email Sending

  Scenario: Send email with TLS
    Given SMTP_TLS is true
    When I send an email
    Then the smtp options include "tls" 