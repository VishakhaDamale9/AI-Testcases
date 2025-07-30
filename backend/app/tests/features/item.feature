Feature: Item management

    Scenario: Create a new item
      Given I am an authenticated superuser
      When I create an item with title "Foo" and description "Bar"
      Then the response status code should be 200
      And the response should contain "Foo" and "Bar" 