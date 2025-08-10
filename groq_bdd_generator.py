import os
import json
import argparse
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# In a real implementation, you would use the Groq API
# For this example, we'll import it but provide a fallback simulation
try:
    import groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Groq package not found. Using simulation mode.")

# Configuration
API_DIR = Path('backend/app/api')
MODELS_FILE = Path('backend/app/models.py')
CRUD_FILE = Path('backend/app/crud.py')
FEATURE_DIR = Path('backend/app/tests/features')
STEPS_DIR = Path('backend/app/tests/features/steps')
TEMPLATES_FILE = Path('prompt_templates.json')

# Ensure directories exist
FEATURE_DIR.mkdir(exist_ok=True, parents=True)
STEPS_DIR.mkdir(exist_ok=True, parents=True)

def load_templates() -> Dict[str, Dict[str, str]]:
    """Load prompt templates from JSON file"""
    if not TEMPLATES_FILE.exists():
        raise FileNotFoundError(f"Templates file not found: {TEMPLATES_FILE}")
    
    with open(TEMPLATES_FILE, 'r') as f:
        return json.load(f)

def call_groq_api(prompt_type: str, content: str, model: str = "llama3-70b-8192") -> str:
    """Call Groq API with the specified prompt template and content"""
    templates = load_templates()
    
    if prompt_type not in templates:
        raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    template = templates[prompt_type]
    user_prompt = template["user"].format(code=content) if "{code}" in template["user"] else \
                 template["user"].format(feature_content=content) if "{feature_content}" in template["user"] else \
                 template["user"].format(coverage_report=content) if "{coverage_report}" in template["user"] else \
                 template["user"].format(function_code=content) if "{function_code}" in template["user"] else \
                 template["user"].format(model_code=content)
    
    if GROQ_AVAILABLE and "GROQ_API_KEY" in os.environ:
        try:
            client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": template["system"]},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,  # Lower temperature for more deterministic outputs
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            print("Falling back to simulation mode.")
    
    # Simulation mode - return predefined responses based on prompt type
    print("Using simulation mode for Groq API call.")
    return simulate_groq_response(prompt_type, content)

def simulate_groq_response(prompt_type: str, content: str) -> str:
    """Simulate Groq API response for demonstration purposes"""
    # In a real implementation, this would be replaced by actual API calls
    # For this example, we'll return predefined responses
    
    if prompt_type == "endpoint_analysis":
        if "users" in content.lower():
            return generate_user_feature()
        elif "items" in content.lower():
            return generate_item_feature()
        else:
            return generate_generic_feature()
    
    elif prompt_type == "step_definition":
        if "User" in content or "user" in content:
            return generate_user_steps()
        elif "Item" in content or "item" in content:
            return generate_item_steps()
        else:
            return generate_generic_steps()
    
    elif prompt_type == "coverage_analysis":
        return generate_coverage_analysis()
    
    elif prompt_type == "function_analysis":
        return generate_function_analysis(content)
    
    elif prompt_type == "model_analysis":
        return generate_model_analysis(content)
    
    elif prompt_type == "negative_testing":
        return generate_negative_testing()
    
    elif prompt_type == "performance_testing":
        return generate_performance_testing()
    
    return "No response generated for this prompt type."

# Simulation response generators
def generate_user_feature():
    return """Feature: User Management

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

  Scenario: Get non-existent user
    Given I am an authenticated superuser
    When I get a user by ID "999"
    Then the response status code should be 404

  Scenario: Update user
    Given I am an authenticated superuser
    When I update a user with ID "1" with new email "updated@example.com"
    Then the response status code should be 200
    And the response should contain the email "updated@example.com"

  Scenario: Update user with invalid email
    Given I am an authenticated superuser
    When I update a user with ID "1" with new email "invalid-email"
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Delete user
    Given I am an authenticated superuser
    When I delete a user with ID "1"
    Then the response status code should be 200
    And the user should no longer exist

  Scenario: Delete non-existent user
    Given I am an authenticated superuser
    When I delete a user with ID "999"
    Then the response status code should be 404

  Scenario: Access user endpoint without authentication
    Given I am not authenticated
    When I get a user by ID "1"
    Then the response status code should be 401

  Scenario: Access user endpoint as non-superuser
    Given I am an authenticated regular user
    When I get a user by ID "1"
    Then the response status code should be 403"""

def generate_item_feature():
    return """Feature: Item Management

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
    Then the response status code should be 401"""

def generate_generic_feature():
    return """Feature: API Endpoint

  Scenario: Successful request
    Given I am an authenticated user
    When I make a request to the endpoint
    Then the response status code should be 200
    And the response should contain expected data

  Scenario: Unauthorized request
    Given I am not authenticated
    When I make a request to the endpoint
    Then the response status code should be 401

  Scenario: Validation error
    Given I am an authenticated user
    When I make a request with invalid data
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Not found error
    Given I am an authenticated user
    When I make a request for a non-existent resource
    Then the response status code should be 404"""

def generate_user_steps():
    return """from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings

client = TestClient(app)

@given('I am an authenticated superuser')
def step_impl(context):
    context.headers = {
        "Authorization": f"Bearer {authentication_token_from_email(client=client, email=settings.FIRST_SUPERUSER, db=None)}"
    }

@given('I am an authenticated regular user')
def step_impl(context):
    context.headers = {
        "Authorization": f"Bearer {authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=None)}"
    }

@given('I am not authenticated')
def step_impl(context):
    context.headers = {}

@when('I create a user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.response = client.post(
        "/api/v1/users/",
        headers=context.headers,
        json={
            "email": email,
            "password": password,
            "is_superuser": False,
        }
    )

@when('I get a user by ID "{id}"')
def step_impl(context, id):
    context.response = client.get(
        f"/api/v1/users/{id}",
        headers=context.headers
    )

@when('I update a user with ID "{id}" with new email "{email}"')
def step_impl(context, id, email):
    context.response = client.put(
        f"/api/v1/users/{id}",
        headers=context.headers,
        json={
            "email": email,
            "is_superuser": False,
        }
    )

@when('I delete a user with ID "{id}"')
def step_impl(context, id):
    context.response = client.delete(
        f"/api/v1/users/{id}",
        headers=context.headers
    )

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@then('the response should contain the email "{email}"')
def step_impl(context, email):
    data = context.response.json()
    assert data["email"] == email

@then('the response should contain user details')
def step_impl(context):
    data = context.response.json()
    assert "id" in data
    assert "email" in data
    assert "is_active" in data
    assert "is_superuser" in data

@then('the user should no longer exist')
def step_impl(context):
    # Try to get the user, should return 404
    response = client.get(
        f"/api/v1/users/{context.user_id}",
        headers=context.headers
    )
    assert response.status_code == 404

@then('the response should contain validation errors')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data"""

def generate_item_steps():
    return """from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings
from app.tests.utils.item import create_random_item

client = TestClient(app)

@given('I am an authenticated user')
def step_impl(context):
    context.headers = {
        "Authorization": f"Bearer {authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=None)}"
    }

@given('I am not authenticated')
def step_impl(context):
    context.headers = {}

@given('there is an existing item with ID "{id}"')
def step_impl(context, id):
    # Create an item if it doesn't exist
    # This is a simplified version - in a real implementation, you would check if the item exists first
    item = create_random_item()
    context.item_id = item.id

@given('there are multiple items in the database')
def step_impl(context):
    # Create multiple items
    for _ in range(5):
        create_random_item()

@given('there are more than 10 items in the database')
def step_impl(context):
    # Create more than 10 items
    for _ in range(15):
        create_random_item()

@when('I create an item with title "{title}" and description "{desc}"')
def step_impl(context, title, desc):
    context.response = client.post(
        "/api/v1/items/",
        headers=context.headers,
        json={
            "title": title,
            "description": desc
        }
    )

@when('I create an item with missing title')
def step_impl(context):
    context.response = client.post(
        "/api/v1/items/",
        headers=context.headers,
        json={
            "description": "Test Description"
        }
    )

@when('I get the item with ID "{id}"')
def step_impl(context, id):
    context.response = client.get(
        f"/api/v1/items/{id}",
        headers=context.headers
    )

@when('I request all items')
def step_impl(context):
    context.response = client.get(
        "/api/v1/items/",
        headers=context.headers
    )

@when('I request items with skip {skip:d} and limit {limit:d}')
def step_impl(context, skip, limit):
    context.response = client.get(
        f"/api/v1/items/?skip={skip}&limit={limit}",
        headers=context.headers
    )

@when('I update the item with ID "{id}" with new title "{title}"')
def step_impl(context, id, title):
    context.response = client.put(
        f"/api/v1/items/{id}",
        headers=context.headers,
        json={
            "title": title,
            "description": "Updated Description"
        }
    )

@when('I delete the item with ID "{id}"')
def step_impl(context, id):
    context.response = client.delete(
        f"/api/v1/items/{id}",
        headers=context.headers
    )

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@then('the response should contain "{title}" and "{desc}"')
def step_impl(context, title, desc):
    data = context.response.json()
    assert data["title"] == title
    assert data["description"] == desc

@then('the response should contain "{title}"')
def step_impl(context, title):
    data = context.response.json()
    assert data["title"] == title

@then('the response should contain the item details')
def step_impl(context):
    data = context.response.json()
    assert "id" in data
    assert "title" in data
    assert "description" in data

@then('the response should contain a list of items')
def step_impl(context):
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@then('the response should contain exactly {count:d} items')
def step_impl(context, count):
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) == count

@then('the item should no longer exist')
def step_impl(context):
    # Try to get the item, should return 404
    response = client.get(
        f"/api/v1/items/{context.item_id}",
        headers=context.headers
    )
    assert response.status_code == 404

@then('the response should contain validation errors')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data"""

def generate_generic_steps():
    return """from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings

client = TestClient(app)

@given('I am an authenticated user')
def step_impl(context):
    context.headers = {
        "Authorization": f"Bearer {authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=None)}"
    }

@given('I am not authenticated')
def step_impl(context):
    context.headers = {}

@when('I make a request to the endpoint')
def step_impl(context):
    context.response = client.get(
        "/api/v1/endpoint/",
        headers=context.headers
    )

@when('I make a request with invalid data')
def step_impl(context):
    context.response = client.post(
        "/api/v1/endpoint/",
        headers=context.headers,
        json={"invalid": "data"}
    )

@when('I make a request for a non-existent resource')
def step_impl(context):
    context.response = client.get(
        "/api/v1/endpoint/999",
        headers=context.headers
    )

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@then('the response should contain expected data')
def step_impl(context):
    data = context.response.json()
    assert data is not None

@then('the response should contain validation errors')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data"""

def generate_coverage_analysis():
    return """1. Uncovered path: [app/api/routes/users.py:45] update_user_me
   Suggested scenario:
   ```gherkin
   Scenario: Update current user
     Given I am an authenticated regular user
     When I update my own user information
     Then the response status code should be 200
     And the response should contain the updated information
   ```

2. Uncovered path: [app/api/routes/users.py:60] update_user_password
   Suggested scenario:
   ```gherkin
   Scenario: Update user password
     Given I am an authenticated user
     When I update my password from "oldpassword" to "newpassword"
     Then the response status code should be 200
     And I can login with the new password
   ```

3. Uncovered path: [app/utils.py:30] send_email
   Suggested scenario:
   ```gherkin
   Scenario: Send password reset email
     Given I am an unauthenticated user
     When I request a password reset for "user@example.com"
     Then the response status code should be 200
     And a password reset email should be sent
   ```

4. Uncovered path: [app/api/routes/login.py:25] recover_password
   Suggested scenario:
   ```gherkin
   Scenario: Recover password
     Given I am an unauthenticated user
     When I request password recovery for "user@example.com"
     Then the response status code should be 200
     And a recovery email should be sent
   ```

5. Uncovered path: [app/api/routes/login.py:40] reset_password
   Suggested scenario:
   ```gherkin
   Scenario: Reset password with token
     Given I am an unauthenticated user
     And I have a valid password reset token
     When I reset my password using the token
     Then the response status code should be 200
     And I can login with the new password
   ```"""

def generate_function_analysis(content):
    # This would analyze the function code and generate scenarios
    # For this example, we'll return a generic response
    return """Scenario: Function executes successfully with valid input
  Given the function is called with valid parameters
  When the function executes
  Then it should return the expected result
  And no exceptions should be raised

Scenario: Function handles invalid input
  Given the function is called with invalid parameters
  When the function executes
  Then it should raise an appropriate exception
  And the error message should be descriptive

Scenario: Function handles edge cases
  Given the function is called with edge case values
  When the function executes
  Then it should handle the edge case correctly
  And return the appropriate result"""

def generate_model_analysis(content):
    # This would analyze the model code and generate scenarios
    # For this example, we'll return a generic response
    return """Feature: Model Management

  Scenario: Create model with valid data
    Given I have valid model data
    When I create a new model instance
    Then the model should be saved to the database
    And the model should have the correct attributes

  Scenario: Create model with invalid data
    Given I have invalid model data
    When I try to create a new model instance
    Then validation errors should be raised
    And the model should not be saved to the database

  Scenario: Retrieve model by ID
    Given a model exists in the database
    When I retrieve the model by its ID
    Then I should get the correct model instance
    And all attributes should be correctly loaded

  Scenario: Update model with valid data
    Given a model exists in the database
    When I update the model with valid data
    Then the model should be updated in the database
    And the model should have the updated attributes

  Scenario: Delete model
    Given a model exists in the database
    When I delete the model
    Then the model should be removed from the database
    And retrieving the model by ID should return not found"""

def generate_negative_testing():
    return """Feature: Negative Testing for API Endpoint

  Scenario: Request with invalid authentication token
    Given I have an invalid authentication token
    When I make a request to the endpoint
    Then the response status code should be 401
    And the response should contain an error message about authentication

  Scenario: Request with expired authentication token
    Given I have an expired authentication token
    When I make a request to the endpoint
    Then the response status code should be 401
    And the response should contain an error message about token expiration

  Scenario: Request with insufficient permissions
    Given I am authenticated as a regular user
    When I make a request to an admin-only endpoint
    Then the response status code should be 403
    And the response should contain an error message about insufficient permissions

  Scenario: Request with malformed JSON
    Given I am an authenticated user
    When I make a request with malformed JSON
    Then the response status code should be 422
    And the response should contain an error message about invalid JSON

  Scenario: Request with SQL injection attempt
    Given I am an authenticated user
    When I make a request with a SQL injection payload
    Then the response status code should be 422
    And the database should not be compromised

  Scenario: Request with XSS attempt
    Given I am an authenticated user
    When I make a request with an XSS payload
    Then the response status code should be 422
    And the payload should be sanitized

  Scenario: Request during database unavailability
    Given the database is unavailable
    When I make a request to the endpoint
    Then the response status code should be 500
    And the response should contain an error message about database connectivity"""

def generate_performance_testing():
    return """Feature: Performance Testing for API Endpoint

  Scenario: Response time under normal load
    Given the system is under normal load
    When I make 10 sequential requests to the endpoint
    Then the average response time should be less than 200ms
    And no request should take longer than 500ms

  Scenario: Response time under heavy load
    Given the system is under heavy load
    When I make 100 concurrent requests to the endpoint
    Then the average response time should be less than 1000ms
    And 95% of requests should complete within 2000ms

  Scenario: Database query performance
    Given the database contains 10000 records
    When I make a request that requires filtering these records
    Then the response time should be less than 500ms
    And the database query should use appropriate indexes

  Scenario: Caching effectiveness
    Given the system has caching enabled
    When I make the same request multiple times
    Then the first request should take normal time
    And subsequent requests should be significantly faster
    And the cache hit ratio should be above 90%

  Scenario: Connection pooling efficiency
    Given the system uses connection pooling
    When I make 50 concurrent requests that require database access
    Then all requests should complete successfully
    And no database connection errors should occur
    And the number of database connections should not exceed the pool size"""

def extract_api_endpoints():
    """Extract API endpoints from the codebase"""
    endpoints = []
    
    # Walk through the API directory
    for root, _, files in os.walk(API_DIR):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Extract router definitions and endpoint handlers
                    endpoints.append({
                        'file': file_path,
                        'content': content
                    })
    
    return endpoints

def generate_feature_file(endpoint_info: Dict[str, str], output_path: Optional[Path] = None) -> Tuple[Path, str]:
    """Generate a Gherkin feature file for an API endpoint"""
    print(f"Generating feature file for: {endpoint_info['file']}")
    
    # Call Groq API to generate feature content
    feature_content = call_groq_api("endpoint_analysis", endpoint_info['content'])
    
    # Write feature file if output path is provided
    if output_path:
        with open(output_path, 'w') as f:
            f.write(feature_content)
        print(f"Generated feature file: {output_path}")
    else:
        # Generate output path based on file name
        file_name = os.path.basename(endpoint_info['file']).replace('.py', '')
        output_path = FEATURE_DIR / f"{file_name}.feature"
        with open(output_path, 'w') as f:
            f.write(feature_content)
        print(f"Generated feature file: {output_path}")
    
    return output_path, feature_content

def generate_step_definitions(feature_path: Path, feature_content: str) -> Path:
    """Generate step definitions for a feature file"""
    feature_name = os.path.basename(feature_path).replace('.feature', '')
    print(f"Generating step definitions for: {feature_name}")
    
    # Call Groq API to generate step definitions
    step_content = call_groq_api("step_definition", feature_content)
    
    # Write step file
    step_file = STEPS_DIR / f"{feature_name}_steps.py"
    with open(step_file, 'w') as f:
        f.write(step_content)
    
    print(f"Generated step definition file: {step_file}")
    return step_file

def main():
    parser = argparse.ArgumentParser(description='Generate BDD tests using Groq API')
    parser.add_argument('--api-key', type=str, help='Groq API key')
    parser.add_argument('--model', type=str, default='llama3-70b-8192', help='Groq model to use')
    parser.add_argument('--endpoint', type=str, help='Specific API endpoint file to analyze')
    args = parser.parse_args()
    
    # Set Groq API key if provided
    if args.api_key:
        os.environ["GROQ_API_KEY"] = args.api_key
    # Otherwise use the one from .env file (already loaded into environment)
    
    print("Starting BDD test generation with Groq...")
    
    # Extract API endpoints
    if args.endpoint and os.path.exists(args.endpoint):
        print(f"Analyzing specific endpoint: {args.endpoint}")
        with open(args.endpoint, 'r') as f:
            content = f.read()
        endpoints = [{'file': args.endpoint, 'content': content}]
    else:
        print("Extracting API endpoints...")
        endpoints = extract_api_endpoints()
    
    print(f"Found {len(endpoints)} API endpoint files")
    
    # Generate feature files and step definitions
    for endpoint in endpoints:
        # Generate feature file
        feature_path, feature_content = generate_feature_file(endpoint)
        
        # Generate step definitions
        generate_step_definitions(feature_path, feature_content)
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
    
    print("\nBDD test generation complete!")
    print("Run the tests with: cd backend && python -m behave app/tests/features")

if __name__ == "__main__":
    main()