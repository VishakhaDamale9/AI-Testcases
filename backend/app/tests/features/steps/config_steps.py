from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the API is running")
def step_impl(context):
    context.client = TestClient(app)

@given("the user is authenticated with normal user credentials")
def step_impl(context):
    user = crud.user.get(db=get_db(), id=1)
    access_token = create_access_token(user)
    context.headers = {"Authorization": f"Bearer {access_token}"}

@given("the user is authenticated with superuser credentials")
def step_impl(context):
    user = crud.user.get(db=get_db(), id=1)
    access_token = create_access_token(user)
    context.headers = {"Authorization": f"Bearer {access_token}"}

@when("the user sends a GET request to \"/api/v1/settings\"")
def step_impl(context):
    response = context.client.get("/api/v1/settings", headers=context.headers)
    context.response = response

@then("the response status code is {status_code}")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then("the response contains {message}")
def step_impl(context, message):
    assert message in context.response.text

@when("the user sends a PATCH request to \"/api/v1/settings\" with valid data")
def step_impl(context):
    response = context.client.patch("/api/v1/settings", {"key": "value"}, headers=context.headers)
    context.response = response

@when("the user sends a PATCH request to \"/api/v1/settings\" with valid data and SECRET_KEY set to \"changethis\"")
def step_impl(context):
    response = context.client.patch("/api/v1/settings", {"key": "value", "SECRET_KEY": "changethis"}, headers=context.headers)
    context.response = response

@when("the user sends a PATCH request to \"/api/v1/settings\" with valid data and POSTGRES_PASSWORD set to \"changethis\"")
def step_impl(context):
    response = context.client.patch("/api/v1/settings", {"key": "value", "POSTGRES_PASSWORD": "changethis"}, headers=context.headers)
    context.response = response

@when("the user sends a PATCH request to \"/api/v1/settings\" with valid data and FIRST_SUPERUSER_PASSWORD set to \"changethis\"")
def step_impl(context):
    response = context.client.patch("/api/v1/settings", {"key": "value", "FIRST_SUPERUSER_PASSWORD": "changethis"}, headers=context.headers)
    context.response = response

@when("the user sends a PATCH request to \"/api/v1/settings\" with valid data and FRONTEND_HOST set to \"http://example.com\"")
def step_impl(context):
    response = context.client.patch("/api/v1/settings", {"key": "value", "FRONTEND_HOST": "http://example.com"}, headers=context.headers)
    context.response = response

@when("the function parse_cors is called with the input")
def step_impl(context):
    context.output = crud.settings.parse_cors(context.input)

@when("the function parse_cors_origins is called with the input")
def step_impl(context):
    context.output = crud.settings.parse_cors_origins(context.input)

@when("the function _check_default_secret is called with the SECRET_KEY")
def step_impl(context):
    context.output = crud.settings._check_default_secret(context.SECRET_KEY)

@when("the function _check_default_secret is called with the POSTGRES_PASSWORD")
def step_impl(context):
    context.output = crud.settings._check_default_secret(context.POSTGRES_PASSWORD)

@when("the function _check_default_secret is called with the FIRST_SUPERUSER_PASSWORD")
def step_impl(context):
    context.output = crud.settings._check_default_secret(context.FIRST_SUPERUSER_PASSWORD)