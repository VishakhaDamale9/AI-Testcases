from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings

client = TestClient(app)

@given('I am an authenticated superuser')
def step_impl_auth_superuser(context):
    context.headers = {
        "Authorization": f"Bearer {authentication_token_from_email(client=client, email=settings.FIRST_SUPERUSER, db=None)}"
    }

@given('I am an authenticated regular user')
def step_impl_auth_regular_user(context):
    context.headers = {
        "Authorization": f"Bearer {authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=None)}"
    }

@given('I am not authenticated')
def step_impl_not_auth(context):
    context.headers = {}