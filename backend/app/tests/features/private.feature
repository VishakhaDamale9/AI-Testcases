Feature: Create User Endpoint
  As a user
  I want to create a new user
  So that I can access the application

  Scenario: Create user with valid credentials
    Given a valid email address
    And a valid full name
    And a valid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 201
    And the response should contain the following JSON:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "is_verified": false
      }
      """
    And the response should contain the user ID

  Scenario: Create user with missing required fields
    Given a valid email address
    And a valid full name
    And an empty password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "password is required"

  Scenario: Create user with invalid email address
    Given an invalid email address
    And a valid full name
    And a valid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "email must be a valid email address"

  Scenario: Create user with invalid full name
    Given a valid email address
    And an invalid full name
    And a valid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "full_name must be a string"

  Scenario: Create user with invalid password
    Given a valid email address
    And a valid full name
    And an invalid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "password must be a string"

  Scenario: Create user with empty email address
    Given an empty email address
    And a valid full name
    And a valid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "email is required"

  Scenario: Create user with empty full name
    Given a valid email address
    And an empty full name
    And a valid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "full_name is required"

  Scenario: Create user with empty password
    Given a valid email address
    And a valid full name
    And an empty password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "",
        "is_verified": false
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "password is required"

  Scenario: Create user with invalid is_verified value
    Given a valid email address
    And a valid full name
    And a valid password
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": "true"
      }
      """
    Then the response status code should be 422
    And the response should contain the error message "is_verified must be a boolean"

  Scenario: Create user without authentication
    When I send a POST request to "/private/users/"
    Then the response status code should be 401
    And the response should contain the error message "Not authenticated"

  Scenario: Create user with invalid authentication
    Given an invalid token
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 401
    And the response should contain the error message "Invalid token"

  Scenario: Create user with superuser authentication
    Given a valid token for a superuser
    When I send a POST request to "/private/users/" with the following JSON body:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "password": "<password>",
        "is_verified": false
      }
      """
    Then the response status code should be 201
    And the response should contain the following JSON:
      """
      {
        "email": "<email>",
        "full_name": "<full_name>",
        "is_verified": false
      }
      """
    And the response should contain the user ID