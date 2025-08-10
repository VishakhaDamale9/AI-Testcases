Feature: Item Management

  Scenario: Create a new item
    Given I am an authenticated user
    When I create an item with title "Test Item" and description "Test Description"
    Then the response status code should be 200
    And the response should contain "Test Item" and "Test Description"

  Scenario: Create an item with missing title
    Given I am an authenticated user
    When I create an item with missing title
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Get item by ID
    Given I am an authenticated user
    And there is an existing item with ID "1"
    When I get the item with ID "1"
    Then the response status code should be 200
    And the response should contain the item details

  Scenario: Get non-existent item
    Given I am an authenticated user
    When I get the item with ID "999"
    Then the response status code should be 404

  Scenario: List all items
    Given I am an authenticated user
    And there are multiple items in the database
    When I request all items
    Then the response status code should be 200
    And the response should contain a list of items

  Scenario: List items with pagination
    Given I am an authenticated user
    And there are more than 10 items in the database
    When I request items with skip 5 and limit 5
    Then the response status code should be 200
    And the response should contain exactly 5 items

  Scenario: Update item
    Given I am an authenticated user
    And there is an existing item with ID "1"
    When I update the item with ID "1" with new title "Updated Item"
    Then the response status code should be 200
    And the response should contain "Updated Item"

  Scenario: Update non-existent item
    Given I am an authenticated user
    When I update the item with ID "999" with new title "Updated Item"
    Then the response status code should be 404

  Scenario: Delete item
    Given I am an authenticated user
    And there is an existing item with ID "1"
    When I delete the item with ID "1"
    Then the response status code should be 200
    And the item should no longer exist

  Scenario: Delete non-existent item
    Given I am an authenticated user
    When I delete the item with ID "999"
    Then the response status code should be 404

  Scenario: Access item endpoint without authentication
    Given I am not authenticated
    When I request all items
    Then the response status code should be 401