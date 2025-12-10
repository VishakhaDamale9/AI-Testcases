from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("the API is running")
def step_impl(context):
    context.client = TestClient(app)

@given("the user is authenticated as a normal user")
def step_impl(context):
    access_token = create_access_token(subject="normal_user")
    context.headers = {"Authorization": f"Bearer {access_token}"}

@given("the user is authenticated as a superuser")
def step_impl(context):
    access_token = create_access_token(subject="superuser")
    context.headers = {"Authorization": f"Bearer {access_token}"}

@when("an unauthenticated user sends a GET request to \"/\"")
def step_impl(context):
    response = context.client.get("/")
    context.response = response

@when("a normal user sends a GET request to \"/\"")
def step_impl(context):
    response = context.client.get("/", headers=context.headers)
    context.response = response

@when("a superuser sends a GET request to \"/\"")
def step_impl(context):
    response = context.client.get("/", headers=context.headers)
    context.response = response

@when("an unauthenticated user sends a GET request to \"/favicon.ico\"")
def step_impl(context):
    response = context.client.get("/favicon.ico")
    context.response = response

@when("a normal user sends a GET request to \"/favicon.ico\"")
def step_impl(context):
    response = context.client.get("/favicon.ico", headers=context.headers)
    context.response = response

@when("a superuser sends a GET request to \"/favicon.ico\"")
def step_impl(context):
    response = context.client.get("/favicon.ico", headers=context.headers)
    context.response = response

@when("the custom generate unique ID function is called with an APIRoute object having no tags")
def step_impl(context):
    # Assuming the function is defined in app.api.deps
    from app.api.deps import get_unique_id
    context.unique_id = get_unique_id(models.APIRoute(tags=[]))

@when("the custom generate unique ID function is called with an APIRoute object having tags")
def step_impl(context):
    # Assuming the function is defined in app.api.deps
    from app.api.deps import get_unique_id
    context.unique_id = get_unique_id(models.APIRoute(tags=["tag1", "tag2"]))

@when("the CORS middleware is called with all origins enabled")
def step_impl(context):
    # Assuming the middleware is defined in app.main
    from app.main import CORS
    context.cors = CORS()

@when("the CORS middleware is called with specific origins enabled")
def step_impl(context):
    # Assuming the middleware is defined in app.main
    from app.main import CORS
    context.cors = CORS(allow_origins=["origin1", "origin2"])

@when("the API includes a router with a prefix")
def step_impl(context):
    # Assuming the router is defined in app.main
    from app.main import APIRouter
    context.router = APIRouter(prefix="/prefix")

@when("the API includes a router without a prefix")
def step_impl(context):
    # Assuming the router is defined in app.main
    from app.main import APIRouter
    context.router = APIRouter()

@when("the API returns the favicon.ico file")
def step_impl(context):
    response = context.client.get("/favicon.ico")
    context.response = response

@then("the response status code is 200")
def step_impl(context):
    assert context.response.status_code == 200

@then("the response contains \"Welcome to FastAPI\"")
def step_impl(context):
    assert "Welcome to FastAPI" in context.response.text

@then("the response contains \"/docs\"")
def step_impl(context):
    assert "/docs" in context.response.text

@then("the response contains \"/api/v1\"")
def step_impl(context):
    assert "/api/v1" in context.response.text

@then("the response contains the favicon.ico file")
def step_impl(context):
    assert "favicon.ico" in context.response.text

@then("the function returns the route name")
def step_impl(context):
    assert context.unique_id == "route_name"

@then("the function returns the route name with tags")
def step_impl(context):
    assert context.unique_id == "route_name_with_tags"

@then("the middleware allows all origins")
def step_impl(context):
    assert context.cors.allow_origins == ["*"]

@then("the middleware allows only the specified origins")
def step_impl(context):
    assert context.cors.allow_origins == ["origin1", "origin2"]

@then("the API has the router with the specified prefix")
def step_impl(context):
    assert context.router.prefix == "/prefix"

@then("the API has the router without a prefix")
def step_impl(context):
    assert context.router.prefix == ""