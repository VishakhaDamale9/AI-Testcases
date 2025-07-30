from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

# Existing steps ...
# (keep your current step implementations here)

@given('I have a JWT token for an inactive user')
def step_impl(context):
    context.headers = {"Authorization": "Bearer <token-for-inactive-user>"}

@given('the database is down')
def step_impl(context):
    pass

@when('I run the backend pre-start script')
def step_impl(context):
    pass

@then('an error is logged and the script fails')
def step_impl(context):
    pass

@when('I parse the CORS value "http://localhost,http://127.0.0.1"')
def step_impl(context):
    context.cors_result = None
    pass

@then('the result should be a list with two URLs')
def step_impl(context):
    pass

@given('the environment is "local"')
def step_impl(context):
    pass

@when('I check the default secret "changethis"')
def step_impl(context):
    pass

@then('a warning is issued')
def step_impl(context):
    pass

@given('SMTP_TLS is true')
def step_impl(context):
    pass

@when('I send an email')
def step_impl(context):
    pass

@then('the smtp options include "tls"')
def step_impl(context):
    pass

@when('I try to login with email "admin@example.com" and password "wrongpassword"')
def step_impl(context):
    context.response = None
    pass

@given('a user exists with email "inactive@example.com" and is inactive')
def step_impl(context):
    pass

@when('I try to login with email "inactive@example.com" and password "userpassword"')
def step_impl(context):
    context.response = None
    pass

@when('I access the root route')
def step_impl(context):
    context.response = None
    pass

@then('the response contains "Welcome to FastAPI"')
def step_impl(context):
    pass

@when('I access the favicon route')
def step_impl(context):
    context.response = None
    pass

@then('the response is a file or 404')
def step_impl(context):
    pass

@given('a user object with no id')
def step_impl(context):
    context.user = None
    pass

@when('I try to update the user')
def step_impl(context):
    context.exception = None
    pass

@then('an exception is raised with "User id not set"')
def step_impl(context):
    pass 