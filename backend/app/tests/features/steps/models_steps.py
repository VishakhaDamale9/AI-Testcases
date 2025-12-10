from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the API endpoint {endpoint} is not authenticated")
def step_impl(context, endpoint):
    client = TestClient(app)
    response = client.post(endpoint)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@given("the API endpoint {endpoint} is authenticated with a normal user")
def step_impl(context, endpoint):
    client = TestClient(app)
    user = crud.user.get(db=get_db(), id=1)
    access_token = create_access_token(subject=user.id)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(endpoint, headers=headers)
    assert response.status_code == 200

@given("the API endpoint {endpoint} is authenticated with a superuser")
def step_impl(context, endpoint):
    client = TestClient(app)
    user = crud.user.get(db=get_db(), id=1)
    access_token = create_access_token(subject=user.id, scopes=["superuser"])
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(endpoint, headers=headers)
    assert response.status_code == 200

@when("I send a POST request with a valid UserCreate object")
def step_impl(context):
    client = TestClient(app)
    user_create = models.UserCreate(email="test@example.com", password="password")
    response = client.post("/users", json=user_create.dict())
    assert response.status_code == 201

@when("I send a POST request with a UserCreate object having an invalid email")
def step_impl(context):
    client = TestClient(app)
    user_create = models.UserCreate(email="invalid_email", password="password")
    response = client.post("/users", json=user_create.dict())
    assert response.status_code == 422

@when("I send a POST request with a UserCreate object having an empty password")
def step_impl(context):
    client = TestClient(app)
    user_create = models.UserCreate(email="test@example.com", password="")
    response = client.post("/users", json=user_create.dict())
    assert response.status_code == 422

@when("I send a POST request with a valid ItemCreate object")
def step_impl(context):
    client = TestClient(app)
    item_create = models.ItemCreate(name="Test Item", description="Test Description")
    response = client.post("/items", json=item_create.dict())
    assert response.status_code == 201

@when("I send a GET request with a valid user ID")
def step_impl(context):
    client = TestClient(app)
    user = crud.user.get(db=get_db(), id=1)
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200

@when("I send a GET request with a non-existent user ID")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/users/999")
    assert response.status_code == 404

@when("I send a GET request with a valid item ID")
def step_impl(context):
    client = TestClient(app)
    item = crud.item.get(db=get_db(), id=1)
    response = client.get(f"/items/{item.id}")
    assert response.status_code == 200

@when("I send a GET request with a non-existent item ID")
def step_impl(context):
    client = TestClient(app)
    response = client.get("/items/999")
    assert response.status_code == 404

@when("I send a PATCH request with a valid UserUpdate object")
def step_impl(context):
    client = TestClient(app)
    user_update = models.UserUpdate(email="updated_email@example.com")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch(f"/users/{user.id}", json=user_update.dict())
    assert response.status_code == 200

@when("I send a PATCH request with a UserUpdate object having an invalid email")
def step_impl(context):
    client = TestClient(app)
    user_update = models.UserUpdate(email="invalid_email")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch(f"/users/{user.id}", json=user_update.dict())
    assert response.status_code == 422

@when("I send a PATCH request with a valid ItemUpdate object")
def step_impl(context):
    client = TestClient(app)
    item_update = models.ItemUpdate(name="Updated Item")
    item = crud.item.get(db=get_db(), id=1)
    response = client.patch(f"/items/{item.id}", json=item_update.dict())
    assert response.status_code == 200

@when("I send a PATCH request with a valid UpdatePassword object")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="password", new_password="new_password")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 200

@when("I send a PATCH request with an UpdatePassword object having an invalid current password")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="invalid_password", new_password="new_password")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 422

@when("I send a PATCH request with an UpdatePassword object having an empty new password")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="password", new_password="")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 422

@when("I send a PATCH request with an UpdatePassword object having an invalid new password")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="password", new_password="invalid_password")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 422

@when("I send a PATCH request with an UpdatePassword object having an empty current password")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="", new_password="new_password")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 422

@when("I send a PATCH request with an UpdatePassword object having an empty new password and an empty current password")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="", new_password="")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 422

@when("I send a PATCH request with an UpdatePassword object having an empty new password and a valid current password")
def step_impl(context):
    client = TestClient(app)
    update_password = models.UpdatePassword(current_password="password", new_password="")
    user = crud.user.get(db=get_db(), id=1)
    response = client.patch("/users/me", json=update_password.dict())
    assert response.status_code == 422

@when("I send a DELETE request with a valid user ID")
def step_impl(context):
    client = TestClient(app)
    user = crud.user.get(db=get_db(), id=1)
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 200

@when("I send a DELETE request with a non-existent user ID")
def step_impl(context):
    client = TestClient(app)
    response = client.delete("/users/999")
    assert response.status_code == 404

@when("I send a DELETE request with a valid item ID")
def step_impl(context):
    client = TestClient(app)
    item = crud.item.get(db=get_db(), id=1)
    response = client.delete(f"/items/{item.id}")
    assert response.status_code == 200

@when("I send a DELETE request with a non-existent item ID")
def step_impl(context):
    client = TestClient(app)
    response = client.delete("/items/999")
    assert response.status_code == 404

@then("the response status code should be {status_code}")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then("the response should contain {message}")
def step_impl(context, message):
    assert message in context.response.text