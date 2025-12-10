from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the API endpoint '/users' is not authenticated")
def step_impl(context):
    client = TestClient(app)
    response = client.post("/users", json={"username": "test", "email": "test@example.com", "password": "password"})
    assert response.status_code == 401

@given("the API endpoint '/users' is authenticated with a normal user")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    assert response.status_code == 201

@given("the API endpoint '/users' is authenticated with a superuser")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    assert response.status_code == 201

@when("the user sends a POST request with invalid credentials")
def step_impl(context):
    client = TestClient(app)
    response = client.post("/users", json={"username": "test", "email": "test@example.com", "password": ""})
    assert response.status_code == 422

@when("the user sends a POST request with valid credentials")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    assert response.status_code == 201

@then("the API returns a 401 Unauthorized status code")
def step_impl(context):
    assert context.response.status_code == 401

@then("the API returns a 201 Created status code")
def step_impl(context):
    assert context.response.status_code == 201

@then("the response contains the user's details")
def step_impl(context):
    assert "username" in context.response.json()
    assert "email" in context.response.json()

@then("the API returns a 422 Unprocessable Entity status code")
def step_impl(context):
    assert context.response.status_code == 422

@then("the response contains the error message '{error_message}'")
def step_impl(context, error_message):
    assert error_message in context.response.json()["detail"][0]["msg"]

@when("the user sends a POST request with missing required fields")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", headers=headers, json={"username": "test", "password": "password"})
    assert response.status_code == 422

@when("the user sends a POST request with an invalid email format")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", headers=headers, json={"username": "test", "email": "invalid_email", "password": "password"})
    assert response.status_code == 422

@when("the user sends a POST request with a weak password")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "weak"})
    assert response.status_code == 422

@when("the user sends a POST request with an existing email")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    response = client.post("/users", headers=headers, json={"username": "test2", "email": "test@example.com", "password": "password"})
    assert response.status_code == 422

@when("the user sends a POST request with an existing username")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    response = client.post("/users", headers=headers, json={"username": "test", "email": "test2@example.com", "password": "password"})
    assert response.status_code == 422

@when("the user sends a GET request for a non-existent user")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/999")
    assert response.status_code == 404

@when("the user sends a GET request for a user they don't own")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/999")
    assert response.status_code == 403

@when("the user sends a PATCH request for a non-existent user")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/users/999", headers=headers, json={"username": "test", "email": "test@example.com"})
    assert response.status_code == 404

@when("the user sends a PATCH request for a user they don't own")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/users/999", headers=headers, json={"username": "test", "email": "test@example.com"})
    assert response.status_code == 403

@when("the user sends a PATCH request with missing required fields")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/users/999", headers=headers, json={"email": "test@example.com"})
    assert response.status_code == 422

@when("the user sends a PATCH request with an invalid email format")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/users/999", headers=headers, json={"username": "test", "email": "invalid_email"})
    assert response.status_code == 422

@when("the user sends a PATCH request with a weak password")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/users/999", headers=headers, json={"username": "test", "password": "weak"})
    assert response.status_code == 422

@when("the user sends a PATCH request with an existing email")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    response = client.patch("/users/999", headers=headers, json={"username": "test", "email": "test@example.com"})
    assert response.status_code == 422

@when("the user sends a PATCH request with an existing username")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {access_token}"}
    client.post("/users", headers=headers, json={"username": "test", "email": "test@example.com", "password": "password"})
    response = client.patch("/users/999", headers=headers, json={"username": "test", "email": "test2@example.com"})
    assert response.status_code == 422

@when("the user sends a DELETE request for a non-existent user")
def step_impl(context):
    client = TestClient(app)
    access_token = create_access_token(subject="super