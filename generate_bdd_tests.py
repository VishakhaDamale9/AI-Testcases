import os
import re
import json
import subprocess
from pathlib import Path

# Configuration
API_DIR = Path('backend/app/api')
MODELS_FILE = Path('backend/app/models.py')
CRUD_FILE = Path('backend/app/crud.py')
FEATURE_DIR = Path('backend/app/tests/features')
STEPS_DIR = Path('backend/app/tests/features/steps')

# Ensure directories exist
FEATURE_DIR.mkdir(exist_ok=True, parents=True)
STEPS_DIR.mkdir(exist_ok=True, parents=True)

# Templates for prompt engineering
ENDPOINT_ANALYSIS_PROMPT = """
Analyze the following FastAPI endpoint and generate BDD scenarios in Gherkin format:

```python
{code}
```

Consider the following aspects:
1. Authentication requirements
2. Input validation
3. Success scenarios
4. Error scenarios (validation errors, not found, etc.)
5. Edge cases

Generate a complete .feature file with multiple scenarios.
"""

STEP_DEFINITION_PROMPT = """
Create Python step definitions using behave for the following Gherkin feature file:

```gherkin
{feature_content}
```

Use the FastAPI TestClient for API testing. Include proper setup and assertions.
Make sure to handle authentication if needed.
"""

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

def analyze_models():
    """Extract model definitions from models.py"""
    if not MODELS_FILE.exists():
        return {}
    
    with open(MODELS_FILE, 'r') as f:
        content = f.read()
    
    # Extract model classes using regex
    model_pattern = r'class\s+([A-Za-z0-9_]+)\s*\([A-Za-z0-9_,\s]+\):\s*([^\n]*\n(?:\s+[^\n]*\n)*)'  
    models = {}
    for match in re.finditer(model_pattern, content):
        model_name = match.group(1)
        model_def = match.group(0)
        models[model_name] = model_def
    
    return models

def analyze_crud_operations():
    """Extract CRUD operations from crud.py"""
    if not CRUD_FILE.exists():
        return {}
    
    with open(CRUD_FILE, 'r') as f:
        content = f.read()
    
    # Extract CRUD functions using regex
    crud_pattern = r'def\s+([a-z_]+)\s*\([^)]*\):\s*([^\n]*\n(?:\s+[^\n]*\n)*)'  
    crud_ops = {}
    for match in re.finditer(crud_pattern, content):
        func_name = match.group(1)
        func_def = match.group(0)
        crud_ops[func_name] = func_def
    
    return crud_ops

def generate_feature_file(endpoint_info, models, crud_ops):
    """Generate a Gherkin feature file based on endpoint analysis"""
    # In a real implementation, this would call an LLM API with the prompt
    # For this example, we'll create a simplified version
    
    file_path = endpoint_info['file']
    file_name = os.path.basename(file_path).replace('.py', '')
    
    # Extract endpoint paths and methods using regex
    router_pattern = r'@router\.([a-z]+)\("([^"]+)"'  
    endpoints = []
    for match in re.finditer(router_pattern, endpoint_info['content']):
        method = match.group(1)  # get, post, put, delete
        path = match.group(2)    # /users/, /items/{item_id}, etc.
        endpoints.append((method, path))
    
    # Generate feature content based on endpoints
    feature_name = file_name.replace('_', ' ').title()
    feature_content = f"Feature: {feature_name}\n\n"
    
    for method, path in endpoints:
        # Generate scenarios based on HTTP method
        if method == 'get':
            if '{' in path:  # Path parameter - get by ID
                feature_content += generate_get_by_id_scenario(path)
            else:  # List endpoint
                feature_content += generate_list_scenario(path)
        elif method == 'post':
            feature_content += generate_create_scenario(path, models)
        elif method == 'put':
            feature_content += generate_update_scenario(path, models)
        elif method == 'delete':
            feature_content += generate_delete_scenario(path)
    
    # Write feature file
    output_path = FEATURE_DIR / f"{file_name}.feature"
    with open(output_path, 'w') as f:
        f.write(feature_content)
    
    print(f"Generated feature file: {output_path}")
    return output_path, feature_content

def generate_get_by_id_scenario(path):
    """Generate scenario for GET by ID endpoint"""
    entity = path.split('/')[-2] if path.endswith('/') else path.split('/')[-1]
    entity = entity.replace('{', '').replace('}', '').replace('_id', '')
    
    return f"""  Scenario: Get {entity} by ID
    Given I am an authenticated user
    When I request the {entity} with ID "1"
    Then the response status code should be 200
    And the response should contain the {entity} details

  Scenario: Get non-existent {entity}
    Given I am an authenticated user
    When I request the {entity} with ID "999"
    Then the response status code should be 404

"""

def generate_list_scenario(path):
    """Generate scenario for GET list endpoint"""
    entity = path.split('/')[-2] if path.endswith('/') else path.split('/')[-1]
    
    return f"""  Scenario: List all {entity}
    Given I am an authenticated user
    When I request all {entity}
    Then the response status code should be 200
    And the response should contain a list of {entity}

  Scenario: Filter {entity} by query parameter
    Given I am an authenticated user
    When I request all {entity} with filter parameter
    Then the response status code should be 200
    And the response should contain filtered {entity}

"""

def generate_create_scenario(path, models):
    """Generate scenario for POST endpoint"""
    entity = path.split('/')[-2] if path.endswith('/') else path.split('/')[-1]
    
    return f"""  Scenario: Create a new {entity}
    Given I am an authenticated user
    When I create a new {entity} with valid data
    Then the response status code should be 200
    And the response should contain the created {entity}

  Scenario: Create {entity} with invalid data
    Given I am an authenticated user
    When I create a new {entity} with invalid data
    Then the response status code should be 422

"""

def generate_update_scenario(path, models):
    """Generate scenario for PUT endpoint"""
    entity = path.split('/')[-2] if path.endswith('/') else path.split('/')[-1]
    entity = entity.replace('{', '').replace('}', '').replace('_id', '')
    
    return f"""  Scenario: Update {entity}
    Given I am an authenticated user
    When I update the {entity} with ID "1" with valid data
    Then the response status code should be 200
    And the response should contain the updated {entity}

  Scenario: Update {entity} with invalid data
    Given I am an authenticated user
    When I update the {entity} with ID "1" with invalid data
    Then the response status code should be 422

  Scenario: Update non-existent {entity}
    Given I am an authenticated user
    When I update the {entity} with ID "999" with valid data
    Then the response status code should be 404

"""

def generate_delete_scenario(path):
    """Generate scenario for DELETE endpoint"""
    entity = path.split('/')[-2] if path.endswith('/') else path.split('/')[-1]
    entity = entity.replace('{', '').replace('}', '').replace('_id', '')
    
    return f"""  Scenario: Delete {entity}
    Given I am an authenticated user
    When I delete the {entity} with ID "1"
    Then the response status code should be 200

  Scenario: Delete non-existent {entity}
    Given I am an authenticated user
    When I delete the {entity} with ID "999"
    Then the response status code should be 404

"""

def generate_step_definitions(feature_path, feature_content):
    """Generate step definitions for a feature file"""
    # In a real implementation, this would call an LLM API with the prompt
    # For this example, we'll create a simplified version
    
    feature_name = os.path.basename(feature_path).replace('.feature', '')
    step_file = STEPS_DIR / f"{feature_name}_steps.py"
    
    # Extract entity name from feature content
    entity_match = re.search(r'Feature: ([\w\s]+)', feature_content)
    entity = entity_match.group(1).strip() if entity_match else "Item"
    entity_lower = entity.lower().replace(' ', '_')
    
    # Generate step definitions
    step_content = f"""from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings

client = TestClient(app)

@given('I am an authenticated user')
def step_impl(context):
    context.headers = {{
        "Authorization": f"Bearer {{authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=None)}}"
    }}

@given('I am an authenticated superuser')
def step_impl(context):
    # This would use a superuser token in a real implementation
    context.headers = {{
        "Authorization": f"Bearer {{authentication_token_from_email(client=client, email=settings.FIRST_SUPERUSER, db=None)}}"
    }}

@when('I request the {entity_lower} with ID "{{id}}"')
def step_impl(context, id):
    context.response = client.get(
        f"/api/v1/{entity_lower}s/{{id}}",
        headers=context.headers
    )

@when('I request all {entity_lower}')
def step_impl(context):
    context.response = client.get(
        f"/api/v1/{entity_lower}s/",
        headers=context.headers
    )

@when('I request all {entity_lower} with filter parameter')
def step_impl(context):
    context.response = client.get(
        f"/api/v1/{entity_lower}s/?skip=0&limit=10",
        headers=context.headers
    )

@when('I create a new {entity_lower} with valid data')
def step_impl(context):
    context.response = client.post(
        f"/api/v1/{entity_lower}s/",
        headers=context.headers,
        json={{
            "title": "Test {entity}",
            "description": "Test description"
        }}
    )

@when('I create a new {entity_lower} with invalid data')
def step_impl(context):
    context.response = client.post(
        f"/api/v1/{entity_lower}s/",
        headers=context.headers,
        json={{}}
    )

@when('I update the {entity_lower} with ID "{{id}}" with valid data')
def step_impl(context, id):
    context.response = client.put(
        f"/api/v1/{entity_lower}s/{{id}}",
        headers=context.headers,
        json={{
            "title": "Updated {entity}",
            "description": "Updated description"
        }}
    )

@when('I update the {entity_lower} with ID "{{id}}" with invalid data')
def step_impl(context, id):
    context.response = client.put(
        f"/api/v1/{entity_lower}s/{{id}}",
        headers=context.headers,
        json={{}}
    )

@when('I delete the {entity_lower} with ID "{{id}}"')
def step_impl(context, id):
    context.response = client.delete(
        f"/api/v1/{entity_lower}s/{{id}}",
        headers=context.headers
    )

@then('the response status code should be {{code:d}}')
def step_impl(context, code):
    assert context.response.status_code == code

@then('the response should contain the {entity_lower} details')
def step_impl(context):
    data = context.response.json()
    assert "id" in data
    assert "title" in data

@then('the response should contain a list of {entity_lower}')
def step_impl(context):
    data = context.response.json()
    assert isinstance(data, list)

@then('the response should contain filtered {entity_lower}')
def step_impl(context):
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Limit parameter

@then('the response should contain the created {entity_lower}')
def step_impl(context):
    data = context.response.json()
    assert "id" in data
    assert data["title"] == "Test {entity}"

@then('the response should contain the updated {entity_lower}')
def step_impl(context):
    data = context.response.json()
    assert "id" in data
    assert data["title"] == "Updated {entity}"
"""
    
    with open(step_file, 'w') as f:
        f.write(step_content)
    
    print(f"Generated step definition file: {step_file}")
    return step_file

def run_coverage_analysis():
    """Run tests with coverage and analyze results"""
    # Change to backend directory
    os.chdir('backend')
    
    # Run tests with coverage
    result = subprocess.run(
        ['python', '-m', 'pytest', '--cov=app', '--cov-report=xml', '--cov-report=term'],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    # Parse coverage report to identify uncovered lines
    if os.path.exists('coverage.xml'):
        # In a real implementation, parse the XML to identify uncovered lines
        # For this example, we'll just print a message
        print("Coverage report generated. Analyzing uncovered code...")
    
    # Return to original directory
    os.chdir('..')

def identify_uncovered_code():
    """Identify uncovered code paths from coverage report"""
    # In a real implementation, this would parse the coverage report
    # and return a list of uncovered functions/lines
    
    # For this example, we'll return a dummy list
    return [
        {'file': 'app/api/routes/users.py', 'line': 45, 'function': 'update_user'},
        {'file': 'app/api/routes/items.py', 'line': 30, 'function': 'delete_item'},
        {'file': 'app/utils.py', 'line': 20, 'function': 'send_email'}
    ]

def generate_edge_case_features(uncovered_code):
    """Generate additional feature files for edge cases"""
    # In a real implementation, this would call an LLM API with specific prompts
    # For this example, we'll create a simplified version
    
    edge_case_file = FEATURE_DIR / "edge_cases.feature"
    
    feature_content = """Feature: Edge Cases and Error Handling

  Scenario: Invalid authentication token
    Given I have an invalid authentication token
    When I request all items
    Then the response status code should be 401

  Scenario: Expired authentication token
    Given I have an expired authentication token
    When I request all items
    Then the response status code should be 401

  Scenario: Missing required fields
    Given I am an authenticated user
    When I create a new item with missing required fields
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Invalid data types
    Given I am an authenticated user
    When I create a new item with invalid data types
    Then the response status code should be 422
    And the response should contain validation errors

  Scenario: Concurrent updates
    Given I am an authenticated user
    When I update the same item concurrently
    Then the response status code should be 409

  Scenario: Database connection error
    Given the database is unavailable
    When I request all items
    Then the response status code should be 500
"""
    
    with open(edge_case_file, 'w') as f:
        f.write(feature_content)
    
    print(f"Generated edge case feature file: {edge_case_file}")
    
    # Generate step definitions for edge cases
    step_file = STEPS_DIR / "edge_case_steps.py"
    
    step_content = """from behave import given, when, then
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@given('I have an invalid authentication token')
def step_impl(context):
    context.headers = {"Authorization": "Bearer invalid_token"}

@given('I have an expired authentication token')
def step_impl(context):
    # This would use an expired token in a real implementation
    context.headers = {"Authorization": "Bearer expired_token"}

@when('I create a new item with missing required fields')
def step_impl(context):
    context.response = client.post(
        "/api/v1/items/",
        headers=context.headers,
        json={}
    )

@when('I create a new item with invalid data types')
def step_impl(context):
    context.response = client.post(
        "/api/v1/items/",
        headers=context.headers,
        json={
            "title": 123,  # Should be string
            "description": True  # Should be string
        }
    )

@when('I update the same item concurrently')
def step_impl(context):
    # Simulate concurrent update with a mock
    with patch('app.crud.update_item') as mock_update:
        mock_update.side_effect = Exception("Concurrent update error")
        context.response = client.put(
            "/api/v1/items/1",
            headers=context.headers,
            json={"title": "Updated Item"}
        )

@given('the database is unavailable')
def step_impl(context):
    # Setup for database unavailable scenario
    context.headers = {"Authorization": "Bearer valid_token"}
    # This would patch the database session in a real implementation

@then('the response should contain validation errors')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data
"""
    
    with open(step_file, 'w') as f:
        f.write(step_content)
    
    print(f"Generated edge case step definition file: {step_file}")

def main():
    print("Starting BDD test generation process...")
    
    # Step 1: Extract API endpoints
    print("\nExtracting API endpoints...")
    endpoints = extract_api_endpoints()
    print(f"Found {len(endpoints)} API endpoint files")
    
    # Step 2: Analyze models and CRUD operations
    print("\nAnalyzing models and CRUD operations...")
    models = analyze_models()
    crud_ops = analyze_crud_operations()
    print(f"Found {len(models)} models and {len(crud_ops)} CRUD operations")
    
    # Step 3: Generate feature files
    print("\nGenerating feature files...")
    feature_files = []
    for endpoint in endpoints:
        feature_path, feature_content = generate_feature_file(endpoint, models, crud_ops)
        feature_files.append((feature_path, feature_content))
    
    # Step 4: Generate step definitions
    print("\nGenerating step definitions...")
    for feature_path, feature_content in feature_files:
        generate_step_definitions(feature_path, feature_content)
    
    # Step 5: Run initial coverage analysis
    print("\nRunning initial coverage analysis...")
    run_coverage_analysis()
    
    # Step 6: Identify uncovered code
    print("\nIdentifying uncovered code...")
    uncovered_code = identify_uncovered_code()
    print(f"Found {len(uncovered_code)} uncovered code paths")
    
    # Step 7: Generate edge case features
    print("\nGenerating edge case features...")
    generate_edge_case_features(uncovered_code)
    
    # Step 8: Run final coverage analysis
    print("\nRunning final coverage analysis...")
    run_coverage_analysis()
    
    print("\nBDD test generation complete!")
    print("Run the tests with: cd backend && python -m behave app/tests/features")
    print("Check coverage with: cd backend && python -m pytest --cov=app --cov-report=term")

if __name__ == "__main__":
    main()