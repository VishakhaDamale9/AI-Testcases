Feature: Backend Pre-Start

  Scenario: Database is unreachable during pre-start
    Given the database is down
    When I run the backend pre-start script
    Then an error is logged and the script fails 