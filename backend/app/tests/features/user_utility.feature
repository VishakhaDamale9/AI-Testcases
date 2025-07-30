Feature: User Utility

  Scenario: Update user with no id
    Given a user object with no id
    When I try to update the user
    Then an exception is raised with "User id not set" 