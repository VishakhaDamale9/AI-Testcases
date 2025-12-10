Feature: Users API Endpoints

  Scenario: Unauthenticated user tries to read users
    Given the API endpoint "/users" is accessible
    When an unauthenticated user sends a GET request to "/users"
    Then the API returns a 401 Unauthorized status code

  Scenario: Unauthenticated user tries to create a user
    Given the API endpoint "/users" is accessible
    When an unauthenticated user sends a POST request to "/users" with a valid user
    Then the API returns a 401 Unauthorized status code

  Scenario: Normal user tries to read users
    Given the API endpoint "/users" is accessible
    When a normal user sends a GET request to "/users"
    Then the API returns a 403 Forbidden status code

  Scenario: Normal user tries to create a user
    Given the API endpoint "/users" is accessible
    When a normal user sends a POST request to "/users" with a valid user
    Then the API returns a 403 Forbidden status code

  Scenario: Superuser tries to read users
    Given the API endpoint "/users" is accessible
    When a superuser sends a GET request to "/users"
    Then the API returns a list of users

  Scenario: Superuser tries to create a user
    Given the API endpoint "/users" is accessible
    When a superuser sends a POST request to "/users" with a valid user
    Then the API returns the created user

  Scenario: Superuser tries to update a user
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with a valid user
    Then the API returns the updated user

  Scenario: Superuser tries to delete a user
    Given the API endpoint "/users" is accessible
    When a superuser sends a DELETE request to "/users/{user_id}"
    Then the API returns a success message

  Scenario: Superuser tries to delete themselves
    Given the API endpoint "/users" is accessible
    When a superuser sends a DELETE request to "/users/me"
    Then the API returns a 403 Forbidden status code

  Scenario: Normal user tries to update their own user
    Given the API endpoint "/users" is accessible
    When a normal user sends a PATCH request to "/users/me" with a valid user
    Then the API returns the updated user

  Scenario: Normal user tries to update their own password
    Given the API endpoint "/users" is accessible
    When a normal user sends a PATCH request to "/users/me/password" with a valid password
    Then the API returns a success message

  Scenario: Normal user tries to delete their own user
    Given the API endpoint "/users" is accessible
    When a normal user sends a DELETE request to "/users/me"
    Then the API returns a success message

  Scenario: Superuser tries to update a non-existent user
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with a non-existent user
    Then the API returns a 404 Not Found status code

  Scenario: Superuser tries to delete a non-existent user
    Given the API endpoint "/users" is accessible
    When a superuser sends a DELETE request to "/users/{user_id}"
    Then the API returns a 404 Not Found status code

  Scenario: Normal user tries to update a non-existent user
    Given the API endpoint "/users" is accessible
    When a normal user sends a PATCH request to "/users/{user_id}" with a non-existent user
    Then the API returns a 403 Forbidden status code

  Scenario: Normal user tries to delete a non-existent user
    Given the API endpoint "/users" is accessible
    When a normal user sends a DELETE request to "/users/{user_id}"
    Then the API returns a 403 Forbidden status code

  Scenario: Superuser tries to update a user with an existing email
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with a user having an existing email
    Then the API returns a 409 Conflict status code

  Scenario: Superuser tries to create a user with an existing email
    Given the API endpoint "/users" is accessible
    When a superuser sends a POST request to "/users" with a user having an existing email
    Then the API returns a 400 Bad Request status code

  Scenario: Normal user tries to update their own user with an existing email
    Given the API endpoint "/users" is accessible
    When a normal user sends a PATCH request to "/users/me" with a user having an existing email
    Then the API returns a 409 Conflict status code

  Scenario: Normal user tries to create a user with an existing email
    Given the API endpoint "/users" is accessible
    When a normal user sends a POST request to "/users" with a user having an existing email
    Then the API returns a 403 Forbidden status code

  Scenario: Superuser tries to read a user by ID
    Given the API endpoint "/users" is accessible
    When a superuser sends a GET request to "/users/{user_id}"
    Then the API returns the user with the given ID

  Scenario: Superuser tries to read a non-existent user by ID
    Given the API endpoint "/users" is accessible
    When a superuser sends a GET request to "/users/{user_id}"
    Then the API returns a 404 Not Found status code

  Scenario: Normal user tries to read a user by ID
    Given the API endpoint "/users" is accessible
    When a normal user sends a GET request to "/users/{user_id}"
    Then the API returns a 403 Forbidden status code

  Scenario: Superuser tries to update a user with invalid data
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with invalid data
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to create a user with invalid data
    Given the API endpoint "/users" is accessible
    When a superuser sends a POST request to "/users" with invalid data
    Then the API returns a 400 Bad Request status code

  Scenario: Normal user tries to update their own user with invalid data
    Given the API endpoint "/users" is accessible
    When a normal user sends a PATCH request to "/users/me" with invalid data
    Then the API returns a 400 Bad Request status code

  Scenario: Normal user tries to create a user with invalid data
    Given the API endpoint "/users" is accessible
    When a normal user sends a POST request to "/users" with invalid data
    Then the API returns a 403 Forbidden status code

  Scenario: Superuser tries to delete a user with invalid data
    Given the API endpoint "/users" is accessible
    When a superuser sends a DELETE request to "/users/{user_id}" with invalid data
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to read users with invalid pagination
    Given the API endpoint "/users" is accessible
    When a superuser sends a GET request to "/users" with invalid pagination
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to create a user with empty email
    Given the API endpoint "/users" is accessible
    When a superuser sends a POST request to "/users" with an empty email
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to create a user with empty password
    Given the API endpoint "/users" is accessible
    When a superuser sends a POST request to "/users" with an empty password
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to update a user with empty email
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with an empty email
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to update a user with empty password
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with an empty password
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to update a user with empty name
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with an empty name
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to update a user with empty surname
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with an empty surname
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to update a user with empty email and password
    Given the API endpoint "/users" is accessible
    When a superuser sends a PATCH request to "/users/{user_id}" with an empty email and password
    Then the API returns a 400 Bad Request status code

  Scenario: Superuser tries to update a user with empty name and surname
    Given the API endpoint "/users" is accessible
    When a