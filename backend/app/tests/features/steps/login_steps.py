from behave import given, when, then
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