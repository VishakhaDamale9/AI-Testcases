Feature: Item Listing

  Scenario: Superuser lists all items
    Given I am an authenticated superuser
    When I list items
    Then the response contains all items

  Scenario: Normal user lists their items
    Given I am an authenticated normal user
    When I list items
    Then the response contains only my items 