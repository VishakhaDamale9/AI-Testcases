# BDD Test Generation with Prompt Engineering

This document explains how to use prompt engineering to automatically generate Behavior-Driven Development (BDD) test cases and achieve 100% test coverage for the backend API.

## Overview

The test generation process consists of two main parts:

1. **BDD Test Case Generation Using Prompt Engineering**
   - Analyze API endpoints from the FastAPI codebase
   - Use templates to generate Gherkin `.feature` files
   - Create Python step definitions using behave
   - Organize tests in appropriate folder structure

2. **Achieving 100% Coverage**
   - Run initial test suite with coverage tool
   - Identify uncovered code paths
   - Generate additional tests to cover edge cases, validation errors, and negative scenarios
   - Refactor/extend step definitions accordingly
   - Re-run tests to validate 100% backend code coverage

## Prerequisites

- Python 3.8 or higher
- Virtual environment with required packages installed
- Backend API running or available for testing

## Quick Start

To automatically generate BDD tests and achieve 100% coverage, run:

```bash
generate_bdd_tests.bat
```

This script will:
1. Set up the virtual environment if needed
2. Install required packages
3. Run initial tests to establish baseline coverage
4. Generate BDD tests using prompt engineering
5. Run the tests and verify coverage

## How It Works

### 1. API Endpoint Analysis

The script analyzes your FastAPI codebase to identify:
- API endpoints and their HTTP methods
- Request/response models
- Authentication requirements
- Validation rules

### 2. Feature File Generation

For each API endpoint, the script generates Gherkin `.feature` files with scenarios for:
- Success cases (200 OK responses)
- Validation errors (422 Unprocessable Entity)
- Not found errors (404 Not Found)
- Authentication errors (401 Unauthorized, 403 Forbidden)
- Edge cases specific to the endpoint

Example feature file:

```gherkin
Feature: User Management

  Scenario: Create a new user
    Given I am an authenticated superuser
    When I create a user with email "test@example.com" and password "password123"
    Then the response status code should be 200
    And the response should contain the email "test@example.com"

  Scenario: Get non-existent user
    Given I am an authenticated superuser
    When I get a user by ID "999"
    Then the response status code should be 404
```

### 3. Step Definition Generation

The script generates Python step definitions that implement the Gherkin scenarios using FastAPI's TestClient:

```python
from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@given('I am an authenticated superuser')
def step_impl(context):
    # Authentication implementation
    pass

@when('I create a user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    # API call implementation
    pass

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code
```

### 4. Coverage Analysis

After running the initial tests, the script:
1. Analyzes the coverage report to identify uncovered code paths
2. Generates additional test scenarios targeting those specific paths
3. Creates step definitions for the new scenarios
4. Runs the tests again to verify improved coverage

This process repeats until 100% coverage is achieved or the maximum number of iterations is reached.

## Manual Usage

### Running the Script with Custom Parameters

```bash
python prompt_engineering_bdd.py --target-coverage=95.0 --max-iterations=5
```

Parameters:
- `--target-coverage`: Target coverage percentage (default: 100.0)
- `--max-iterations`: Maximum number of iterations for test generation (default: 3)
- `--coverage-report`: Path to an existing coverage report (optional)

### Running Tests Manually

To run the BDD tests:

```bash
cd backend
python -m behave app/tests/features
```

To check coverage:

```bash
cd backend
python -m pytest --cov=app --cov-report=term --cov-report=html
```

## Customizing the Process

### Modifying Prompt Templates

You can customize the prompt templates in `prompt_engineering_bdd.py` to generate different types of tests or to focus on specific aspects of your API.

### Adding Custom Test Scenarios

You can manually add custom test scenarios to the generated `.feature` files to cover specific business logic or edge cases that might not be automatically detected.

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Ensure all required packages are installed: `pip install pytest pytest-cov behave fastapi httpx`

2. **Coverage Not Reaching 100%**
   - Check the coverage report to identify which lines are not covered
   - Add specific test scenarios for those lines
   - Some code paths might be difficult to test (error handlers, edge cases) and might require manual test writing

3. **Test Failures**
   - Ensure your API is correctly implemented and matches the expected behavior in the tests
   - Check that the database is properly set up with test data
   - Verify authentication mechanisms are working correctly

## Conclusion

This prompt engineering approach to BDD test generation provides a powerful way to achieve comprehensive test coverage with minimal manual effort. By automatically analyzing your API and generating appropriate test scenarios, you can ensure your application is thoroughly tested against a wide range of inputs and conditions.