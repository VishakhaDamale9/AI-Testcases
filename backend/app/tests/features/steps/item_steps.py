from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = None

@given('I am an authenticated superuser')
def step_impl(context):
    context.headers = {"Authorization": "Bearer <your_token>"}

@when('I create an item with title "{title}" and description "{desc}"')
def step_impl(context, title, desc):
    context.response = client.post(
        "/api/v1/items/",
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