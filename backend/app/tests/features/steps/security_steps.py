from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the user is not authenticated")
def step_impl(context):
    context.client = TestClient(app)

@given("the user is authenticated as a normal user")
def step_impl(context):
    context.user = models.User(username="normal_user", email="normal_user@example.com", is_superuser=False)
    context.db = get_db()
    crud.user.create(db=context.db, obj_in=context.user)
    context.token = create_access_token(subject=context.user.username, expires_delta=3600)

@given("the user is authenticated as a superuser")
def step_impl(context):
    context.user = models.User(username="superuser", email="superuser@example.com", is_superuser=True)
    context.db = get_db()
    crud.user.create(db=context.db, obj_in=context.user)
    context.token = create_access_token(subject=context.user.username, expires_delta=3600)

@when("the user tries to create an access token")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"})

@when("the user tries to create an access token with an invalid subject")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer invalid_token"}, json={"subject": "invalid_subject"})

@when("the user tries to create an access token with an empty subject")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": ""})

@when("the user tries to create an access token with an expired subject")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": "expired_subject", "expires_delta": -3600})

@when("the user tries to create an access token with an invalid expires delta")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": "invalid_subject", "expires_delta": "invalid_delta"})

@when("the user tries to create an access token with an empty expires delta")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": "empty_subject", "expires_delta": ""})

@when("the user tries to verify a password with an invalid password")
def step_impl(context):
    context.response = context.client.post("/password/verify", json={"password": "invalid_password", "username": "normal_user"})

@when("the user tries to verify a password with an empty password")
def step_impl(context):
    context.response = context.client.post("/password/verify", json={"password": "", "username": "normal_user"})

@when("the user tries to get a password hash with an empty password")
def step_impl(context):
    context.response = context.client.post("/password/hash", json={"password": ""})

@when("the user tries to verify a password with a valid password")
def step_impl(context):
    context.response = context.client.post("/password/verify", json={"password": "valid_password", "username": "normal_user"})

@when("the user tries to get a password hash with a valid password")
def step_impl(context):
    context.response = context.client.post("/password/hash", json={"password": "valid_password"})

@when("the user tries to create an access token with a valid subject and expires delta")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": "valid_subject", "expires_delta": 3600})

@when("the user tries to create an access token with a valid subject and empty expires delta")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": "valid_subject", "expires_delta": ""})

@when("the user tries to create an access token with a valid subject and expired expires delta")
def step_impl(context):
    context.response = context.client.post("/token", headers={"Authorization": f"Bearer {context.token}"}, json={"subject": "valid_subject", "expires_delta": -3600})

@then("the API returns a 401 Unauthorized response")
def step_impl(context):
    assert context.response.status_code == 401

@then("the API returns a 200 OK response with a valid access token")
def step_impl(context):
    assert context.response.status_code == 200
    assert "access_token" in context.response.json()

@then("the API returns a 400 Bad Request response with a validation error")
def step_impl(context):
    assert context.response.status_code == 400
    assert "detail" in context.response.json()

@then("the API returns a 200 OK response with a verification result")
def step_impl(context):
    assert context.response.status_code == 200
    assert "verified" in context.response.json()

@then("the API returns a 200 OK response with a password hash")
def step_impl(context):
    assert context.response.status_code == 200
    assert "password_hash" in context.response.json()