Feature: Items API Endpoints

  Scenario: Unauthenticated user tries to retrieve items
    Given the API endpoint "/items" is accessed without authentication
    When the GET request is made
    Then a 401 Unauthorized response is returned

  Scenario: Normal user tries to retrieve items
    Given the API endpoint "/items" is accessed with normal user authentication
    When the GET request is made
    Then a list of items is returned

  Scenario: Superuser tries to retrieve items
    Given the API endpoint "/items" is accessed with superuser authentication
    When the GET request is made
    Then a list of all items is returned

  Scenario: Normal user tries to retrieve an item
    Given the API endpoint "/items/{id}" is accessed with normal user authentication
    When the GET request is made with a valid item ID
    Then the item is returned

  Scenario: Superuser tries to retrieve an item
    Given the API endpoint "/items/{id}" is accessed with superuser authentication
    When the GET request is made with a valid item ID
    Then the item is returned

  Scenario: Normal user tries to retrieve an item with invalid ID
    Given the API endpoint "/items/{id}" is accessed with normal user authentication
    When the GET request is made with an invalid item ID
    Then a 404 Not Found response is returned

  Scenario: Superuser tries to retrieve an item with invalid ID
    Given the API endpoint "/items/{id}" is accessed with superuser authentication
    When the GET request is made with an invalid item ID
    Then a 404 Not Found response is returned

  Scenario: Normal user tries to create an item
    Given the API endpoint "/items" is accessed with normal user authentication
    When the POST request is made with valid item data
    Then the item is created and returned

  Scenario: Superuser tries to create an item
    Given the API endpoint "/items" is accessed with superuser authentication
    When the POST request is made with valid item data
    Then the item is created and returned

  Scenario: Normal user tries to create an item with missing required field
    Given the API endpoint "/items" is accessed with normal user authentication
    When the POST request is made with item data missing a required field
    Then a 422 Unprocessable Entity response is returned

  Scenario: Normal user tries to update an item
    Given the API endpoint "/items/{id}" is accessed with normal user authentication
    When the PUT request is made with valid item data
    Then the item is updated and returned

  Scenario: Superuser tries to update an item
    Given the API endpoint "/items/{id}" is accessed with superuser authentication
    When the PUT request is made with valid item data
    Then the item is updated and returned

  Scenario: Normal user tries to update an item with invalid ID
    Given the API endpoint "/items/{id}" is accessed with normal user authentication
    When the PUT request is made with an invalid item ID
    Then a 404 Not Found response is returned

  Scenario: Superuser tries to update an item with invalid ID
    Given the API endpoint "/items/{id}" is accessed with superuser authentication
    When the PUT request is made with an invalid item ID
    Then a 404 Not Found response is returned

  Scenario: Normal user tries to delete an item
    Given the API endpoint "/items/{id}" is accessed with normal user authentication
    When the DELETE request is made with a valid item ID
    Then the item is deleted and a success message is returned

  Scenario: Superuser tries to delete an item
    Given the API endpoint "/items/{id}" is accessed with superuser authentication
    When the DELETE request is made with a valid item ID
    Then the item is deleted and a success message is returned

  Scenario: Normal user tries to delete an item with invalid ID
    Given the API endpoint "/items/{id}" is accessed with normal user authentication
    When the DELETE request is made with an invalid item ID
    Then a 404 Not Found response is returned

  Scenario: Superuser tries to delete an item with invalid ID
    Given the API endpoint "/items/{id}" is accessed with superuser authentication
    When the DELETE request is made with an invalid item ID
    Then a 404 Not Found response is returned