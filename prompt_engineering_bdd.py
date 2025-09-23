import os # Interacts with the filesystem (list directories, run process commands, etc.)
import re # Regular expressions for pattern matching
import json # Read/write JSON data
import argparse # Parse command-line arguments for the script
import subprocess # Run shell commands (e.g., pytest, behave)
from pathlib import Path # Path manipulation
from typing import List, Dict, Any, Optional, Tuple # Type hints for better code clarity

# This script would use Groq's API in a real implementation
# For this example, we'll simulate the API calls

# Configuration
API_DIR = Path('backend/app/api') # Directory containing FastAPI API endpoints
MODELS_FILE = Path('backend/app/models.py') # File containing Pydantic models
CRUD_FILE = Path('backend/app/crud.py') # File containing CRUD operations
FEATURE_DIR = Path('backend/app/tests/features') # Directory to store generated feature files
STEPS_DIR = Path('backend/app/tests/features/steps') # Directory to store step definitions

# Ensure directories exist
FEATURE_DIR.mkdir(exist_ok=True, parents=True) # Create features directory if it doesn't exist
STEPS_DIR.mkdir(exist_ok=True, parents=True) # Create steps directory if it doesn't exist

# Templates for prompt engineering
ENDPOINT_ANALYSIS_PROMPT = """ 
You are an expert in BDD (Behavior-Driven Development) testing for FastAPI applications.

Analyze the following FastAPI endpoint and generate comprehensive BDD scenarios in Gherkin format:

```python
{code}
```

Consider the following aspects:
1. Authentication requirements (unauthenticated, normal user, superuser)
2. Input validation (required fields, data types, constraints)
3. Success scenarios (create, read, update, delete operations)
4. Error scenarios (validation errors, not found, unauthorized, etc.)
5. Edge cases (empty inputs, boundary values, etc.)
6. Business logic specific to this endpoint

Generate a complete .feature file with multiple scenarios that would achieve 100% code coverage.
Use the following format for the feature file:

Feature: [Feature Name]

  Scenario: [Scenario Name]
    Given [precondition]
    When [action]
    Then [expected result]
    And [additional expected result]

  Scenario: [Another Scenario Name]
    ...

Be specific about the inputs and expected outputs in each scenario.
"""

STEP_DEFINITION_PROMPT = """
You are an expert in BDD (Behavior-Driven Development) testing for FastAPI applications.

Create Python step definitions using behave for the following Gherkin feature file:

```gherkin
{feature_content}
```

Use the FastAPI TestClient for API testing. Include proper setup, test data creation, and assertions.
Make sure to handle authentication if needed, and include all necessary imports.

The step definitions should be comprehensive and cover all scenarios in the feature file.
Ensure that the step definitions will achieve 100% code coverage when executed.

Use the following format for the step definitions:

```python
from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
# Add other necessary imports

client = TestClient(app)

@given('...')
def step_impl(context):
    # Implementation

@when('...')
def step_impl(context):
    # Implementation

@then('...')
def step_impl(context):
    # Implementation
```

Be specific about how to set up test data, make API calls, and verify responses.
"""

COVERAGE_ANALYSIS_PROMPT = """
You are an expert in test coverage analysis for Python applications.

Analyze the following code coverage report and identify uncovered code paths:

```
{coverage_report}
```

For each uncovered code path, suggest specific BDD scenarios that would cover it.
Be detailed about the preconditions, actions, and expected results for each scenario.

Use the following format for your response:

1. Uncovered path: [file:line_number] [function_name]
   Suggested scenario:
   ```gherkin
   Scenario: [Scenario Name]
     Given [precondition]
     When [action]
     Then [expected result]
   ```

2. Uncovered path: ...

Focus on achieving 100% code coverage with the suggested scenarios.
"""

def simulate_groq_api_call(prompt, model="llama3-70b-8192"): 
    """Simulate a Groq API call for demonstration purposes"""
    # In a real implementation, this would call the Groq API
    # For this example, we'll return predefined responses based on prompt type
    
    if "generate comprehensive BDD scenarios" in prompt: # This is an endpoint analysis prompt
        # Check if the prompt is for user or item features
        if "users" in prompt.lower():
            return generate_user_feature()
        elif "items" in prompt.lower():
            return generate_item_feature()
        else:
            return generate_generic_feature()
    
    elif "Create Python step definitions" in prompt: # This is a step definition prompt
        # Check if the prompt is for user or item steps
        if "User" in prompt or "user" in prompt:
            return generate_user_steps()
        elif "Item" in prompt or "item" in prompt:
            return generate_item_steps()
        else:
            return generate_generic_steps()
    
    elif "Analyze the following code coverage report" in prompt: # This is a coverage analysis prompt
        # Generate coverage analysis response
        return generate_coverage_analysis()
    
    # Default response
    return "No response generated for this prompt type."

def generate_user_feature():
    """Generate a user management feature file"""
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
    Then the response status code should be 403
"""

def generate_item_feature():
    """Generate an item management feature file"""
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
    Then the response status code should be 401
"""

def generate_generic_feature():
    """Generate a generic feature file"""
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
    Then the response status code should be 404
"""

def generate_user_steps():
    """Generate step definitions for user management"""
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
    assert "detail" in data
"""

def generate_item_steps():
    """Generate step definitions for item management"""
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
    assert "detail" in data
"""

def generate_generic_steps():
    """Generate generic step definitions"""
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
    assert "detail" in data
"""

def generate_coverage_analysis():
    """Generate coverage analysis response"""
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
   ```
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

def generate_feature_files():
    """Generate feature files using prompt engineering"""
    print("Generating feature files using prompt engineering...")
    
    # Extract API endpoints
    endpoints = extract_api_endpoints()
    print(f"Found {len(endpoints)} API endpoint files")
    
    # Generate feature files for each endpoint
    for endpoint in endpoints:
        file_path = endpoint['file']
        file_name = os.path.basename(file_path).replace('.py', '')
        
        print(f"Analyzing endpoint: {file_name}")
        
        # Create prompt for this endpoint
        prompt = ENDPOINT_ANALYSIS_PROMPT.format(code=endpoint['content'])
        
        # Call Groq API (simulated)
        feature_content = simulate_groq_api_call(prompt)
        
        # Write feature file
        output_path = FEATURE_DIR / f"{file_name}.feature"
        with open(output_path, 'w') as f:
            f.write(feature_content)
        
        print(f"Generated feature file: {output_path}")
        
        # Generate step definitions
        generate_step_definitions(output_path, feature_content)

def generate_step_definitions(feature_path, feature_content): 
    """Generate step definitions for a feature file"""
    feature_name = os.path.basename(feature_path).replace('.feature', '') # Get the feature name from the file path
    print(f"Generating step definitions for: {feature_name}") 
    
    # Create prompt for step definitions
    prompt = STEP_DEFINITION_PROMPT.format(feature_content=feature_content) # Format the prompt with the feature content
    
    # Call Groq API (simulated)
    step_content = simulate_groq_api_call(prompt) # Simulate the API call to get step definitions
    
    # Write step file
    step_file = STEPS_DIR / f"{feature_name}_steps.py" # Create the step file path based on the feature name
    with open(step_file, 'w') as f:
        f.write(step_content)
    
    print(f"Generated step definition file: {step_file}")

def parse_coverage_xml(xml_path: str) -> List[Dict[str, Any]]: # Parse coverage XML report to identify uncovered code paths
    """Parse coverage XML report to identify uncovered code paths"""
    import xml.etree.ElementTree as ET
    
    if not os.path.exists(xml_path): # Check if the coverage XML file exists
        print(f"Coverage report not found at {xml_path}")
        return []
    
    try:
        tree = ET.parse(xml_path) # Parse the XML file 
        root = tree.getroot() # Get the root element of the XML tree
        
        uncovered_paths = [] # List to store uncovered paths
        
        # Find all classes with uncovered lines
        for class_elem in root.findall('.//class'): # Iterate through each class element in the XML
            filename = class_elem.get('filename')  # Get the filename from the class element
            
            # Skip test files and migrations
            if 'test' in filename or 'migration' in filename:
                continue
                
            # Find all uncovered lines
            for line in class_elem.findall('.//line'): 
                if line.get('hits') == '0':  # Uncovered line
                    line_num = int(line.get('number')) 
                    
                    # Try to find the function name for this line
                    function_name = "unknown" 
                    for method in class_elem.findall('.//method'): 
                        start_line = int(method.get('line', '0'))  
                        if start_line <= line_num and start_line > 0: # Check if the method starts before the uncovered line
                            function_name = method.get('name', 'unknown')
                    
                    uncovered_paths.append({
                        'file': filename,
                        'line': line_num,
                        'function': function_name
                    })
        
        return uncovered_paths
    except Exception as e: 
        print(f"Error parsing coverage XML: {e}")
        return []

def analyze_coverage(coverage_report: str) -> None:
    """Analyze coverage report and generate additional scenarios"""
    print("Analyzing coverage report...")
    
    # Parse coverage XML to identify uncovered code paths
    uncovered_paths = []
    if coverage_report.endswith('.xml'):
        uncovered_paths = parse_coverage_xml(coverage_report)
    else:
        # If it's not an XML file, assume it's the report text
        # Create prompt for coverage analysis
        prompt = COVERAGE_ANALYSIS_PROMPT.format(coverage_report=coverage_report)
        
        # Call Groq API (simulated)
        analysis = simulate_groq_api_call(prompt)
        
        # Extract uncovered paths from the analysis
        path_pattern = r'Uncovered path: \[([^:]+):([0-9]+)\] ([^\n]+)'
        for match in re.finditer(path_pattern, analysis):
            uncovered_paths.append({
                'file': match.group(1),
                'line': int(match.group(2)),
                'function': match.group(3)
            })
    
    print(f"Found {len(uncovered_paths)} uncovered code paths")
    
    if not uncovered_paths:
        print("No uncovered code paths found. Coverage might be complete!")
        return
    
    # Group uncovered paths by file and function
    grouped_paths = {}
    for path in uncovered_paths: 
        key = f"{path['file']}:{path['function']}"
        if key not in grouped_paths:
            grouped_paths[key] = []
        grouped_paths[key].append(path)
    
    print(f"Found {len(grouped_paths)} unique functions with uncovered code")
    
    # Generate scenarios for each uncovered function
    all_scenarios = []
    
    for key, paths in grouped_paths.items():
        file, function = key.split(':')  
        
        # Read the function code if possible
        function_code = ""
        try:
            with open(file, 'r') as f:
                content = f.read()
                # Try to extract the function definition
                func_pattern = rf'def\s+{function}\s*\([^)]*\):\s*([^\n]*\n(?:\s+[^\n]*\n)*)'
                match = re.search(func_pattern, content)
                if match:
                    function_code = match.group(0)
        except Exception as e:
            print(f"Error reading function code: {e}")
        
        # Create prompt for this uncovered function
        prompt = f"{COVERAGE_ANALYSIS_PROMPT}\n\nUncovered function:\n```python\n{function_code}\n```\n"
        
        # Call Groq API (simulated)
        analysis = simulate_groq_api_call(prompt)
        
        # Extract scenarios from analysis
        scenario_pattern = r'Scenario: ([^\n]+)\s+Given ([^\n]+)\s+When ([^\n]+)\s+Then ([^\n]+)(?:\s+And ([^\n]+))?'
        for match in re.finditer(scenario_pattern, analysis, re.MULTILINE):
            scenario = {
                'name': match.group(1).strip(),
                'given': match.group(2).strip(),
                'when': match.group(3).strip(),
                'then': match.group(4).strip(),
                'and': match.group(5).strip() if match.group(5) else None,
                'file': file,
                'function': function
            }
            all_scenarios.append(scenario)
    
    # Generate additional feature file
    additional_feature = "Feature: Additional Scenarios for Coverage\n\n"
    
    for scenario in all_scenarios:
        additional_feature += f"  # For {scenario['file']} - {scenario['function']}\n"
        additional_feature += f"  Scenario: {scenario['name']}\n"
        additional_feature += f"    Given {scenario['given']}\n"
        additional_feature += f"    When {scenario['when']}\n"
        additional_feature += f"    Then {scenario['then']}\n"
        if scenario['and']:
            additional_feature += f"    And {scenario['and']}\n"
        additional_feature += "\n"
    
    # Write additional feature file
    output_path = FEATURE_DIR / "additional_coverage.feature"
    with open(output_path, 'w') as f:
        f.write(additional_feature)
    
    print(f"Generated additional feature file: {output_path}")
    
    # Generate step definitions for additional scenarios
    generate_step_definitions(output_path, additional_feature)

def run_tests_with_coverage() -> Tuple[str, float]:
    """Run tests with coverage and return the report and coverage percentage"""
    print("Running tests with coverage...")
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir('backend')
    
    try:
        # Run tests with coverage
        result = subprocess.run(
            ['python', '-m', 'pytest', '--cov=app', '--cov-report=xml', '--cov-report=term'],
            capture_output=True,
            text=True
        )
        
        coverage_report = result.stdout
        
        # Extract coverage percentage
        coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', coverage_report)
        coverage_percentage = float(coverage_match.group(1)) if coverage_match else 0.0
        
        print(f"Current test coverage: {coverage_percentage:.2f}%")
        
        return coverage_report, coverage_percentage
    except Exception as e:
        print(f"Error running tests: {e}")
        return "", 0.0
    finally:
        # Return to original directory
        os.chdir(original_dir)

def run_behave_tests() -> bool:
    """Run behave tests and return success status"""
    print("Running behave tests...")
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir('backend')
    
    try:
        # Run behave tests
        result = subprocess.run(
            ['python', '-m', 'behave', 'app/tests/features'],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running behave tests: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

def main():
    parser = argparse.ArgumentParser(description='Generate BDD tests using prompt engineering')
    parser.add_argument('--coverage-report', type=str, help='Path to coverage report')
    parser.add_argument('--target-coverage', type=float, default=100.0, help='Target coverage percentage')
    parser.add_argument('--max-iterations', type=int, default=3, help='Maximum number of iterations for test generation')
    args = parser.parse_args()
    
    print("Starting BDD test generation with prompt engineering...")
    
    # Initial coverage check
    initial_report, initial_coverage = run_tests_with_coverage()
    
    # Generate feature files
    generate_feature_files()
    
    # Run behave tests
    run_behave_tests()
    
    # Check coverage again
    current_report, current_coverage = run_tests_with_coverage()
    
    # Iterative improvement to reach target coverage
    iteration = 1
    while current_coverage < args.target_coverage and iteration <= args.max_iterations:
        print(f"\nIteration {iteration}: Current coverage {current_coverage:.2f}% < Target {args.target_coverage:.2f}%")
        print("Analyzing coverage to generate additional tests...")
        
        # Use provided coverage report or the one we just generated
        coverage_report_path = args.coverage_report if args.coverage_report else 'backend/coverage.xml'
        analyze_coverage(coverage_report_path)
        
        # Run behave tests again
        run_behave_tests()
        
        # Check coverage again
        previous_coverage = current_coverage
        current_report, current_coverage = run_tests_with_coverage()
        
        # If coverage isn't improving, break the loop
        if current_coverage <= previous_coverage:
            print(f"Coverage not improving (was {previous_coverage:.2f}%, now {current_coverage:.2f}%). Stopping iterations.")
            break
        
        iteration += 1
    
    # Final coverage check
    final_report, final_coverage = run_tests_with_coverage()
    
    print(f"\nBDD test generation complete!")
    print(f"Initial coverage: {initial_coverage:.2f}%")  
    print(f"Final coverage: {final_coverage:.2f}%") 
    
    if final_coverage >= args.target_coverage: 
        print(f"✅ Target coverage of {args.target_coverage:.2f}% achieved!")
    else:
        print(f"⚠️ Target coverage of {args.target_coverage:.2f}% not reached. Current coverage: {final_coverage:.2f}%")
        print("Consider running the script again or manually adding tests for uncovered code paths.")
    
    print("\nRun the tests with: cd backend && python -m behave app/tests/features")
    print("Check coverage with: cd backend && python -m pytest --cov=app --cov-report=term")

if __name__ == "__main__":
    main()