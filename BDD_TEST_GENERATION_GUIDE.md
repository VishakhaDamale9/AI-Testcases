# BDD Test Generation with Prompt Engineering

This guide explains how to use prompt engineering with Groq's API to automatically generate Behavior-Driven Development (BDD) test cases and achieve 100% test coverage for your FastAPI backend.

## Overview

The process consists of two main parts:

1. **BDD Test Case Generation**
   - Analyze API endpoints from the FastAPI codebase
   - Use predefined prompt templates for LLM interaction
   - Generate Gherkin `.feature` files
   - Create Python step definitions using behave
   - Organize tests in appropriate folder structure

2. **Achieving 100% Coverage**
   - Run initial test suite with coverage tool
   - Identify uncovered code paths
   - Generate additional prompts to cover edge cases, validation errors, and negative scenarios
   - Refactor/extend step definitions accordingly
   - Re-run tests to validate 100% backend code coverage

## Prerequisites

- Python 3.8+
- FastAPI backend application
- Groq API key (for production use)
- Required Python packages:
  - behave
  - pytest
  - pytest-cov
  - fastapi
  - httpx

## Quick Start

1. Run the provided batch script to generate and execute BDD tests:

```bash
run_groq_bdd_generator.bat
```

This script will:
- Set up the virtual environment if needed
- Install required packages
- Run the Groq BDD generator
- Execute the generated BDD tests
- Run pytest with coverage reporting

## How It Works

### 1. API Analysis

The system extracts API endpoints from your FastAPI codebase and analyzes them to understand:

- HTTP methods (GET, POST, PUT, DELETE)
- Path parameters
- Query parameters
- Request body schemas
- Response schemas
- Authentication requirements
- Validation rules

### 2. Feature File Generation

For each API endpoint, the system generates a Gherkin `.feature` file with scenarios that test:

- Happy paths (successful operations)
- Validation errors
- Authentication/authorization
- Edge cases
- Error responses

Example feature file:

```gherkin
Feature: User Management

  Scenario: Create a new user
    Given I am an authenticated superuser
    When I create a user with email "test@example.com" and password "password123"
    Then the response status code should be 200
    And the response should contain the email "test@example.com"

  Scenario: Get user by ID
    Given I am an authenticated superuser
    When I get a user by ID "1"
    Then the response status code should be 200
    And the response should contain user details
```

### 3. Step Definition Generation

For each feature file, the system generates corresponding Python step definitions that implement the steps using FastAPI's TestClient:

```python
from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@given('I am an authenticated superuser')
def step_impl(context):
    # Implementation

@when('I create a user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    # Implementation

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code
```

### 4. Coverage Analysis

After running the initial tests, the system analyzes the coverage report to identify uncovered code paths. For each uncovered path, it generates additional test scenarios to improve coverage.

## Manual Usage

You can also use the components individually:

### Generate BDD Tests

```bash
python groq_bdd_generator.py [--api-key YOUR_API_KEY] [--model llama3-70b-8192] [--endpoint path/to/specific/endpoint.py]
```

### Run BDD Tests

```bash
cd backend
python -m behave app/tests/features
```

### Run Coverage Analysis

```bash
cd backend
python -m pytest --cov=app --cov-report=term --cov-report=xml
```

## Customization

### Prompt Templates

You can customize the prompt templates in `prompt_templates.json` to adjust the style and focus of the generated tests.

### Coverage Thresholds

You can adjust the coverage threshold in the batch script or when running pytest manually:

```bash
python -m pytest --cov=app --cov-report=term --cov-fail-under=90  # For 90% coverage
```

## Troubleshooting

### API Key Issues

If you're using the real Groq API, make sure your API key is set correctly:

```bash
set GROQ_API_KEY=your_api_key_here
```

### Test Failures

If tests are failing, check:

1. Database setup and test data
2. Authentication configuration
3. Step definition implementations

### Coverage Issues

If you're not reaching 100% coverage:

1. Check for exception handling code that's hard to trigger
2. Look for conditional branches that depend on configuration
3. Consider adding more negative test scenarios

## Conclusion

By using prompt engineering with LLMs, you can automate the generation of comprehensive BDD tests and achieve high test coverage with minimal manual effort. This approach combines the best of both worlds: the natural language readability of BDD and the power of AI to generate comprehensive test cases.