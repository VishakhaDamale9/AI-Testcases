from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.features.steps.common_steps import step_impl_auth_superuser, step_impl_auth_regular_user, step_impl_not_auth

client = TestClient(app)
response = None

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

@then('the response should contain "{title}" and "{desc}"'