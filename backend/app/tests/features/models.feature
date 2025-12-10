Feature: User Management API

  Scenario: Unauthenticated user tries to create a new user
    Given the API endpoint "/users" is not authenticated
    When I send a POST request with a valid UserCreate object
    Then the response status code should be 401
    And the response should contain "Not authenticated"

  Scenario: Unauthenticated user tries to read a user
    Given the API endpoint "/users/{user_id}" is not authenticated
    When I send a GET request with a valid user ID
    Then the response status code should be 401
    And the response should contain "Not authenticated"

  Scenario: Unauthenticated user tries to update a user
    Given the API endpoint "/users/{user_id}" is not authenticated
    When I send a PATCH request with a valid UserUpdate object
    Then the response status code should be 401
    And the response should contain "Not authenticated"

  Scenario: Unauthenticated user tries to delete a user
    Given the API endpoint "/users/{user_id}" is not authenticated
    When I send a DELETE request with a valid user ID
    Then the response status code should be 401
    And the response should contain "Not authenticated"

  Scenario: Normal user tries to create a new user with invalid email
    Given the API endpoint "/users" is authenticated with a normal user
    When I send a POST request with a UserCreate object having an invalid email
    Then the response status code should be 422
    And the response should contain "Invalid email"

  Scenario: Normal user tries to create a new user with empty password
    Given the API endpoint "/users" is authenticated with a normal user
    When I send a POST request with a UserCreate object having an empty password
    Then the response status code should be 422
    And the response should contain "Password is required"

  Scenario: Normal user tries to read a user that does not exist
    Given the API endpoint "/users/{user_id}" is authenticated with a normal user
    When I send a GET request with a non-existent user ID
    Then the response status code should be 404
    And the response should contain "User not found"

  Scenario: Normal user tries to update a user with invalid email
    Given the API endpoint "/users/{user_id}" is authenticated with a normal user
    When I send a PATCH request with a UserUpdate object having an invalid email
    Then the response status code should be 422
    And the response should contain "Invalid email"

  Scenario: Normal user tries to delete a user that does not exist
    Given the API endpoint "/users/{user_id}" is authenticated with a normal user
    When I send a DELETE request with a non-existent user ID
    Then the response status code should be 404
    And the response should contain "User not found"

  Scenario: Superuser tries to create a new user with invalid email
    Given the API endpoint "/users" is authenticated with a superuser
    When I send a POST request with a UserCreate object having an invalid email
    Then the response status code should be 422
    And the response should contain "Invalid email"

  Scenario: Superuser tries to create a new user with empty password
    Given the API endpoint "/users" is authenticated with a superuser
    When I send a POST request with a UserCreate object having an empty password
    Then the response status code should be 422
    And the response should contain "Password is required"

  Scenario: Superuser tries to read a user that does not exist
    Given the API endpoint "/users/{user_id}" is authenticated with a superuser
    When I send a GET request with a non-existent user ID
    Then the response status code should be 404
    And the response should contain "User not found"

  Scenario: Superuser tries to update a user with invalid email
    Given the API endpoint "/users/{user_id}" is authenticated with a superuser
    When I send a PATCH request with a UserUpdate object having an invalid email
    Then the response status code should be 422
    And the response should contain "Invalid email"

  Scenario: Superuser tries to delete a user that does not exist
    Given the API endpoint "/users/{user_id}" is authenticated with a superuser
    When I send a DELETE request with a non-existent user ID
    Then the response status code should be 404
    And the response should contain "User not found"

  Scenario: Normal user tries to create a new item
    Given the API endpoint "/items" is authenticated with a normal user
    When I send a POST request with a valid ItemCreate object
    Then the response status code should be 201
    And the response should contain the created item

  Scenario: Normal user tries to read an item that does not exist
    Given the API endpoint "/items/{item_id}" is authenticated with a normal user
    When I send a GET request with a non-existent item ID
    Then the response status code should be 404
    And the response should contain "Item not found"

  Scenario: Normal user tries to update an item that does not exist
    Given the API endpoint "/items/{item_id}" is authenticated with a normal user
    When I send a PATCH request with a valid ItemUpdate object
    Then the response status code should be 404
    And the response should contain "Item not found"

  Scenario: Normal user tries to delete an item that does not exist
    Given the API endpoint "/items/{item_id}" is authenticated with a normal user
    When I send a DELETE request with a non-existent item ID
    Then the response status code should be 404
    And the response should contain "Item not found"

  Scenario: Superuser tries to create a new item
    Given the API endpoint "/items" is authenticated with a superuser
    When I send a POST request with a valid ItemCreate object
    Then the response status code should be 201
    And the response should contain the created item

  Scenario: Superuser tries to read an item that does not exist
    Given the API endpoint "/items/{item_id}" is authenticated with a superuser
    When I send a GET request with a non-existent item ID
    Then the response status code should be 404
    And the response should contain "Item not found"

  Scenario: Superuser tries to update an item that does not exist
    Given the API endpoint "/items/{item_id}" is authenticated with a superuser
    When I send a PATCH request with a valid ItemUpdate object
    Then the response status code should be 404
    And the response should contain "Item not found"

  Scenario: Superuser tries to delete an item that does not exist
    Given the API endpoint "/items/{item_id}" is authenticated with a superuser
    When I send a DELETE request with a non-existent item ID
    Then the response status code should be 404
    And the response should contain "Item not found"

  Scenario: User tries to update their own password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with a valid UpdatePassword object
    Then the response status code should be 200
    And the response should contain the updated user

  Scenario: User tries to update their own password with invalid current password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with an UpdatePassword object having an invalid current password
    Then the response status code should be 422
    And the response should contain "Invalid password"

  Scenario: User tries to update their own password with empty new password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with an UpdatePassword object having an empty new password
    Then the response status code should be 422
    And the response should contain "Password is required"

  Scenario: User tries to update their own password with invalid new password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with an UpdatePassword object having an invalid new password
    Then the response status code should be 422
    And the response should contain "Invalid password"

  Scenario: User tries to update their own password with empty current password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with an UpdatePassword object having an empty current password
    Then the response status code should be 422
    And the response should contain "Current password is required"

  Scenario: User tries to update their own password with empty new password and empty current password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with an UpdatePassword object having an empty new password and an empty current password
    Then the response status code should be 422
    And the response should contain "Password is required"

  Scenario: User tries to update their own password with empty new password and valid current password
    Given the API endpoint "/users/me" is authenticated with a normal user
    When I send a PATCH request with an UpdatePassword object having an empty new password and a valid current password
    Then the response status code should be 422
    And the response should contain "Password is required"

  Scenario: User tries to update their own password with empty