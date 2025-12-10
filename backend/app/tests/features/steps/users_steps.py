from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the API endpoint \"/users\" is accessible")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

@when("an unauthenticated user sends a GET request to \"/users\"")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 401

@then("the API returns a 401 Unauthorized status code")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 401

@when("an unauthenticated user sends a POST request to \"/users\" with a valid user")
def step_impl(context):
    client = TestClient(app)
    user = {"email": "user@example.com", "password": "password"}
    response = client.post("/users", json=user)
    assert response.status_code == 401

@then("the API returns a 401 Unauthorized status code")
def step_impl(context):
    client = TestClient(app)
    response = client.post("/users", json={"email": "user@example.com", "password": "password"})
    assert response.status_code == 401

@when("a normal user sends a GET request to \"/users\"")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 403

@then("the API returns a 403 Forbidden status code")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 403

@when("a normal user sends a POST request to \"/users\" with a valid user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"email": "user@example.com", "password": "password"}
    response = client.post("/users", headers=headers, json=user)
    assert response.status_code == 403

@then("the API returns a 403 Forbidden status code")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/users", headers=headers, json={"email": "user@example.com", "password": "password"})
    assert response.status_code == 403

@when("a superuser sends a GET request to \"/users\"")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200

@then("the API returns a list of users")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200

@when("a superuser sends a POST request to \"/users\" with a valid user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"email": "user@example.com", "password": "password"}
    response = client.post("/users", headers=headers, json=user)
    assert response.status_code == 201

@then("the API returns the created user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"email": "user@example.com", "password": "password"}
    response = client.post("/users", headers=headers, json=user)
    assert response.status_code == 201

@when("a superuser sends a PATCH request to \"/users/{user_id}\" with a valid user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    user = {"email": "user@example.com", "password": "password"}
    response = client.patch(f"/users/{user_id}", headers=headers, json=user)
    assert response.status_code == 200

@then("the API returns the updated user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    user = {"email": "user@example.com", "password": "password"}
    response = client.patch(f"/users/{user_id}", headers=headers, json=user)
    assert response.status_code == 200

@when("a superuser sends a DELETE request to \"/users/{user_id}\"")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    response = client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200

@then("the API returns a success message")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    response = client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200

@when("a superuser sends a DELETE request to \"/users/me\"")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 403

@then("the API returns a 403 Forbidden status code")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="superuser")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 403

@when("a normal user sends a PATCH request to \"/users/me\" with a valid user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"email": "user@example.com", "password": "password"}
    response = client.patch("/users/me", headers=headers, json=user)
    assert response.status_code == 200

@then("the API returns the updated user")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"email": "user@example.com", "password": "password"}
    response = client.patch("/users/me", headers=headers, json=user)
    assert response.status_code == 200

@when("a normal user sends a PATCH request to \"/users/me/password\" with a valid password")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"password": "password"}
    response = client.patch("/users/me/password", headers=headers, json=user)
    assert response.status_code == 200

@then("the API returns a success message")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    user = {"password": "password"}
    response = client.patch("/users/me/password", headers=headers, json=user)
    assert response.status_code == 200

@when("a normal user sends a DELETE request to \"/users/me\"")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 200

@then("the API returns a success message")
def step_impl(context):
    client = TestClient(app)
    token = create_access_token(subject="normal_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 200

@when("a superuser sends a PATCH request to \"/users/{user_id}\" with a non-existent user")
def step_impl(context):
    client = TestClient(app)