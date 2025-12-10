from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the API endpoint {endpoint} is accessed without authentication")
def step_impl(context, endpoint):
    client = TestClient(app)
    context.response = client.get(endpoint)

@given("the API endpoint {endpoint} is accessed with normal user authentication")
def step_impl(context, endpoint):
    client = TestClient(app)
    user = crud.user.get(db=get_db(), id=1)
    access_token = create_access_token(subject=user.id)
    context.headers = {"Authorization": f"Bearer {access_token}"}
    context.response = client.get(endpoint, headers=context.headers)

@given("the API endpoint {endpoint} is accessed with superuser authentication")
def step_impl(context, endpoint):
    client = TestClient(app)
    user = crud.user.get(db=get_db(), id=1)
    access_token = create_access_token(subject=user.id, scopes=["superuser"])
    context.headers = {"Authorization": f"Bearer {access_token}"}
    context.response = client.get(endpoint, headers=context.headers)

@when("the GET request is made")
def step_impl(context):
    client = TestClient(app)
    context.response = client.get(context.endpoint)

@when("the GET request is made with a valid item ID")
def step_impl(context):
    client = TestClient(app)
    item = crud.item.get(db=get_db(), id=1)
    context.response = client.get(f"/items/{item.id}", headers=context.headers)

@when("the GET request is made with an invalid item ID")
def step_impl(context):
    client = TestClient(app)
    context.response = client.get(f"/items/999", headers=context.headers)

@when("the POST request is made with valid item data")
def step_impl(context):
    client = TestClient(app)
    item_data = {"name": "Test Item", "description": "Test item description"}
    context.response = client.post("/items", headers=context.headers, json=item_data)

@when("the POST request is made with item data missing a required field")
def step_impl(context):
    client = TestClient(app)
    item_data = {"name": "Test Item"}
    context.response = client.post("/items", headers=context.headers, json=item_data)

@when("the PUT request is made with valid item data")
def step_impl(context):
    client = TestClient(app)
    item = crud.item.get(db=get_db(), id=1)
    item_data = {"name": "Updated Test Item", "description": "Updated test item description"}
    context.response = client.put(f"/items/{item.id}", headers=context.headers, json=item_data)

@when("the PUT request is made with an invalid item ID")
def step_impl(context):
    client = TestClient(app)
    context.response = client.put("/items/999", headers=context.headers, json={"name": "Test Item"})

@when("the DELETE request is made with a valid item ID")
def step_impl(context):
    client = TestClient(app)
    item = crud.item.get(db=get_db(), id=1)
    context.response = client.delete(f"/items/{item.id}", headers=context.headers)

@when("the DELETE request is made with an invalid item ID")
def step_impl(context):
    client = TestClient(app)
    context.response = client.delete("/items/999", headers=context.headers)

@then("a 401 Unauthorized response is returned")
def step_impl(context):
    assert context.response.status_code == 401

@then("a list of items is returned")
def step_impl(context):
    assert context.response.status_code == 200
    assert len(context.response.json()) > 0

@then("a list of all items is returned")
def step_impl(context):
    assert context.response.status_code == 200
    assert len(context.response.json()) > 0

@then("the item is returned")
def step_impl(context):
    assert context.response.status_code == 200
    assert context.response.json()["id"] == 1

@then("a 404 Not Found response is returned")
def step_impl(context):
    assert context.response.status_code == 404

@then("the item is created and returned")
def step_impl(context):
    assert context.response.status_code == 201
    assert context.response.json()["id"] == 2

@then("a 422 Unprocessable Entity response is returned")
def step_impl(context):
    assert context.response.status_code == 422

@then("the item is updated and returned")
def step_impl(context):
    assert context.response.status_code == 200
    assert context.response.json()["id"] == 1

@then("the item is deleted and a success message is returned")
def step_impl(context):
    assert context.response.status_code == 200
    assert context.response.json()["message"] == "Item deleted successfully"