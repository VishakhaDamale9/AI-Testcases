from behave import given, when, then, step
from fastapi.testclient import TestClient
import json
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string
from app.crud import crud_user
from app.db.session import SessionLocal
from app.tests.features.steps.common_steps import step_impl_auth_superuser, step_impl_auth_regular_user, step_impl_not_auth

# Initialize the TestClient
client = TestClient(app)

# Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@given('the application is running')
def step_impl(context):
    # This is a placeholder step to ensure the application is running
    response = client.get("/api/v1/")
    assert response.status_code in [200, 404], f"Application is not running, status code: {response.status_code}"
    
    # Initialize context attributes
    context.client = client
    context.headers = {}
    context.response = None
    context.db = next(get_db())

"}

"}

@given('there is an existing user with ID "{user_id}"')
def step_impl(context, user_id):
    # Check if user exists, if not create one
    user = crud_user.get(context.db, id=int(user_id))
    if not user:
        user_in = {
            "email": random_email(),
            "password": random_lower_string(),
            "is_superuser": False
        }
        user = crud_user.create(context.db, obj_in=user_in)
    
    context.user_id = user.id
    context.user_email = user.email

@when('I create a user with the following details:')
def step_impl(context):
    # Extract user details from the table
    user_data = context.table[0].as_dict()
    
    # Convert string values to appropriate types
    if 'is_superuser' in user_data:
        user_data['is_superuser'] = user_data['is_superuser'].lower() == 'true'
    
    context.response = context.client.post(
        "/api/v1/users/",
        headers=context.headers,
        json=user_data
    )
    
    # Store the response data for later steps
    if context.response.status_code == 200:
        context.user_data = context.response.json()

@when('I get the user with ID "{user_id}"')
def step_impl(context, user_id):
    context.response = context.client.get(
        f"/api/v1/users/{user_id}",
        headers=context.headers
    )

@when('I update the user with ID "{user_id}" with the following details:')
def step_impl(context, user_id):
    # Extract user details from the table
    user_data = context.table[0].as_dict()
    
    # Convert string values to appropriate types
    if 'is_superuser' in user_data:
        user_data['is_superuser'] = user_data['is_superuser'].lower() == 'true'
    
    context.response = context.client.put(
        f"/api/v1/users/{user_id}",
        headers=context.headers,
        json=user_data
    )

@when('I delete the user with ID "{user_id}"')
def step_impl(context, user_id):
    context.response = context.client.delete(
        f"/api/v1/users/{user_id}",
        headers=context.headers
    )

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected status code {status_code}, got {context.response.status_code}\nResponse: {context.response.text}"

@then('the response should contain a user with email "{email}"')
def step_impl(context, email):
    data = context.response.json()
    assert "email" in data, f"Response does not contain 'email' field: {data}"
    assert data["email"] == email, f"Expected email {email}, got {data['email']}"

@then('the response should contain a user with ID "{user_id}"')
def step_impl(context, user_id):
    data = context.response.json()
    assert "id" in data, f"Response does not contain 'id' field: {data}"
    assert str(data["id"]) == user_id, f"Expected user ID {user_id}, got {data['id']}"

@then('the user should be stored in the database')
def step_impl(context):
    data = context.response.json()
    user = crud_user.get(context.db, id=data["id"])
    assert user is not None, f"User with ID {data['id']} not found in database"
    assert user.email == data["email"], f"Expected email {data['email']}, got {user.email}"

@then('the user in the database should be updated')
def step_impl(context):
    data = context.response.json()
    user = crud_user.get(context.db, id=data["id"])
    assert user is not None, f"User with ID {data['id']} not found in database"
    assert user.email == data["email"], f"Expected email {data['email']}, got {user.email}"
    assert user.is_superuser == data["is_superuser"], \
        f"Expected is_superuser {data['is_superuser']}, got {user.is_superuser}"

@then('the user should be removed from the database')
def step_impl(context):
    user = crud_user.get(context.db, id=context.user_id)
    assert user is None, f"User with ID {context.user_id} still exists in database"

@then('the response should contain an error message')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data, f"Response does not contain 'detail' field: {data}"

@then('the response should contain an authentication error message')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data, f"Response does not contain 'detail' field: {data}"
    assert "authentication" in data["detail"].lower() or "not authenticated" in data["detail"].lower(), \
        f"Expected authentication error, got: {data['detail']}"

@then('the response should contain a permission error message')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data, f"Response does not contain 'detail' field: {data}"
    assert "permission" in data["detail"].lower() or "not enough privileges" in data["detail"].lower(), \
        f"Expected permission error, got: {data['detail']}"

@then('the response should contain validation errors for "{field}"')
def step_impl(context, field):
    data = context.response.json()
    assert "detail" in data, f"Response does not contain 'detail' field: {data}"
    
    # Check if the validation error is for the specified field
    found = False
    for error in data["detail"]:
        if field in error.get("loc", []):
            found = True
            break
    
    assert found, f"Validation error for field '{field}'