from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.features.steps.common_steps import step_impl_auth_superuser, step_impl_auth_regular_user, step_impl_not_auth

client = TestClient(app)

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
    if context.response.status_code == 200:
        context.user_id = context.response.json()["id"]

@when('I get a user by ID')
def step_impl(context):
    # Create a user first if we don't have one
    if not context.user_id:
        user = create_random_user()
        context.user_id = user.id
    
    context.response = client.get(
        f"/api/v1/users/{context.user_id}",
        headers=context.headers
    )

@when('I update a user with new email "{email}"')
def step_impl(context, email):
    # Create a user first if we don't have one
    if not context.user_id:
        user = create_random_user()
        context.user_id = user.id
    
    context.response = client.put(
        f"/api/v1/users/{context.user_id}",
        headers=context.headers,
        json={
            "email": email,
            "is_superuser": False,
        }
    )

@when('I delete a user')
def step_impl(context):
    # Create a user first if we don't have one
    if not context.user_id:
        user = create_random_user()
        context.user_id = user.id
    
    context.response = client.delete(
        f"/api/v1/users/{context.user_id}",
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

@then('the user should no longer exist'