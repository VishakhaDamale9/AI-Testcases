from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("a valid email address")
def step_impl(context):
    context.email = "test@example.com"

@given("a valid full name")
def step_impl(context):
    context.full_name = "Test User"

@given("a valid password")
def step_impl(context):
    context.password = "password123"

@given("an invalid email address")
def step_impl(context):
    context.email = "invalid_email"

@given("an invalid full name")
def step_impl(context):
    context.full_name = 123

@given("an invalid password")
def step_impl(context):
    context.password = 123

@given("an empty email address")
def step_impl(context):
    context.email = ""

@given("an empty full name")
def step_impl(context):
    context.full_name = ""

@given("an empty password")
def step_impl(context):
    context.password = ""

@given("an invalid token")
def step_impl(context):
    context.token = "invalid_token"

@given("a valid token for a superuser")
def step_impl(context):
    context.token = create_access_token({"sub": "superuser"})

@when("I send a POST request to \"/private/users/\" with the following JSON body:")
def step_impl(context):
    client = TestClient(app)
    response = client.post("/private/users/", json={
        "email": context.email,
        "full_name": context.full_name,
        "password": context.password,
        "is_verified": False
    }, headers={"Authorization": f"Bearer {context.token}"})
    context.response = response

@then("the response status code should be {status_code}")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then("the response should contain the following JSON:")
def step_impl(context):
    assert context.response.json() == {
        "email": context.email,
        "full_name": context.full_name,
        "is_verified": False
    }

@then("the response should contain the user ID")
def step_impl(context):
    assert "user_id" in context.response.json()

@then("the response should contain the error message {error_message}")
def step_impl(context, error_message):
    assert error_message in context.response.json()["detail"][0]["msg"]

@when("I send a POST request to \"/private/users/\"")
def step_impl(context):
    client = TestClient(app)
    response = client.post("/private/users/")
    context.response = response

@then("the response status code should be 401")
def step_impl(context):
    assert context.response.status_code == 401

@then("the response should contain the error message {error_message}")
def step_impl(context, error_message):
    assert error_message in context.response.json()["detail"][0]["msg"]