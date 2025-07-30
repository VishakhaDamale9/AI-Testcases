from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

@given('I have a JWT token for a deleted user')
def step_impl(context):
    # Implement logic to create a token for a user that does not exist
    pass

@when('I access a protected endpoint')
def step_impl(context):
    # Use TestClient to access a protected endpoint
    pass

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@given('I am an authenticated superuser')
def step_impl(context):
    # Replace with your actual superuser credentials
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    context.headers = {"Authorization": f"Bearer {token}"}

@when('I create an item with title "{title}" and description "{desc}"')
def step_impl(context, title, desc):
    context.response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=context.headers,
        json={"title": title, "description": desc}
    )

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@then('the response should contain "{title}" and "{desc}"')
def step_impl(context, title, desc):
    data = context.response.json()
    assert data["title"] == title
    assert data["description"] == desc


# User Authentication Steps
@given('I have an invalid JWT token')
def step_impl(context):
    context.headers = {"Authorization": "Bearer invalidtoken"}

@given('I have a valid JWT token for a non-existent user')
def step_impl(context):
    # Generate a token with a user id that does not exist
    context.headers = {"Authorization": "Bearer <token-for-nonexistent-user>"}

@given('I have a valid JWT token for an inactive user')
def step_impl(context):
    # Create an inactive user, get token
    context.headers = {"Authorization": "Bearer <token-for-inactive-user>"}

@when('I try to access a protected endpoint')
def step_impl(context):
    response = context.client.get("/api/v1/items/", headers=context.headers)
    context.response = response

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@then('the response should contain "{msg}"')
def step_impl(context, msg):
    assert msg in context.response.text


@given('I am an authenticated normal user')
def step_impl(context):
    # Login as normal user, set context.headers
    pass

@when('I list items')
def step_impl(context):
    response = context.client.get("/api/v1/items/", headers=context.headers)
    context.response = response

@then('the response contains all items')
def step_impl(context):
    # Check that all items are present
    data = context.response.json()
    assert len(data["data"]) >= 2  # or whatever logic fits

@then('the response contains only my items')
def step_impl(context):
    # Check that only items owned by the user are present
    data = context.response.json()
    for item in data["data"]:
        assert item["owner_id"] == context.user_id


# Utility Endpoints Steps
@when('I send a test email to "{email}"')
def step_impl(context, email):
    response = context.client.post("/api/v1/utils/test-email/", json={"email_to": email})
    context.response = response



@when('I check the health endpoint')
def step_impl(context):
    response = context.client.get("/api/v1/utils/health-check/")
    context.response = response

@then('the response should be true')
def step_impl(context):
    assert context.response.json() is True 

