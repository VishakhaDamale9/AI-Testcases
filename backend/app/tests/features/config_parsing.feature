Feature: Config Parsing

  Scenario: Parse CORS string
    When I parse the CORS value "http://localhost,http://127.0.0.1"
    Then the result should be a list with two URLs

  Scenario: Default secret warning in local
    Given the environment is "local"
    When I check the default secret "changethis"
    Then a warning is issued 