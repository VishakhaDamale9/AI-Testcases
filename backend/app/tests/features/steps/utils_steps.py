from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the email service is configured")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/email/configure")
    assert response.status_code == 200

@given("the email service is not configured")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/email/configure")
    assert response.status_code != 200

@when("I send an email to {email} with subject {subject} and HTML content {html_content}")
def step_impl(context, email, subject, html_content):
    client = TestClient(app)
    response = client.post("/email/send", json={"email": email, "subject": subject, "html_content": html_content})
    context.email_response = response

@then("the email is sent successfully")
def step_impl(context):
    assert context.email_response.status_code == 200

@then("the email is not sent")
def step_impl(context):
    assert context.email_response.status_code != 200

@then("the email is not sent with error {error}")
def step_impl(context, error):
    assert context.email_response.status_code != 200
    assert error in context.email_response.text

@when("I generate a test email for {email}")
def step_impl(context, email):
    client = TestClient(app)
    response = client.post("/email/test", json={"email": email})
    context.test_email_response = response

@then("the email has subject {subject} and HTML content {html_content}")
def step_impl(context, subject, html_content):
    assert context.test_email_response.status_code == 200
    assert subject in context.test_email_response.text
    assert html_content in context.test_email_response.text

@when("I generate a reset password email for {email} with email {email} and token {token}")
def step_impl(context, email, email2, token):
    client = TestClient(app)
    response = client.post("/email/reset_password", json={"email": email, "email2": email2, "token": token})
    context.reset_password_email_response = response

@then("the email has subject {subject} and HTML content {html_content}")
def step_impl(context, subject, html_content):
    assert context.reset_password_email_response.status_code == 200
    assert subject in context.reset_password_email_response.text
    assert html_content in context.reset_password_email_response.text

@when("I generate a new account email for {email} with username {username} and password {password}")
def step_impl(context, email, username, password):
    client = TestClient(app)
    response = client.post("/email/new_account", json={"email": email, "username": username, "password": password})
    context.new_account_email_response = response

@then("the email has subject {subject} and HTML content {html_content}")
def step_impl(context, subject, html_content):
    assert context.new_account_email_response.status_code == 200
    assert subject in context.new_account_email_response.text
    assert html_content in context.new_account_email_response.text

@when("I generate a password reset token for {email}")
def step_impl(context, email):
    client = TestClient(app)
    response = client.post("/email/reset_password_token", json={"email": email})
    context.password_reset_token_response = response

@then("the token is valid for 2 hours")
def step_impl(context):
    token = context.password_reset_token_response.json()["token"]
    db = next(get_db())
    token_data = crud.token.get(db, token)
    assert token_data is not None
    assert token_data.expiration_time > token_data.creation_time

@when("I verify a password reset token {token}")
def step_impl(context, token):
    client = TestClient(app)
    response = client.post("/email/verify_password_reset_token", json={"token": token})
    context.verify_password_reset_token_response = response

@then("the email is {email}")
def step_impl(context, email):
    assert context.verify_password_reset_token_response.status_code == 200
    assert email in context.verify_password_reset_token_response.text

@when("I wait for {time} and {unit}")
def step_impl(context, time, unit):
    if unit == "hours":
        time = int(time)
        import time
        time.sleep(time * 3600)
    elif unit == "minutes":
        time = int(time)
        import time
        time.sleep(time * 60)
    else:
        raise ValueError("Invalid unit")

@when("I generate a password reset token for {email} with expiration time in the past")
def step_impl(context, email):
    client = TestClient(app)
    response = client.post("/email/reset_password_token", json={"email": email, "expiration_time": int(time.time()) - 3600})
    context.password_reset_token_response = response

@when("I generate a password reset token for {email}")
def step_impl(context, email):
    client = TestClient(app)
    response = client.post("/email/reset_password_token", json={"email": email})
    context.password_reset_token_response = response