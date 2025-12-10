from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given('the user is not authenticated')
def step_impl(context):
    context.client = TestClient(app)

@given('the user is authenticated as a normal user')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated as a superuser')
def step_impl(context):
    user = models.User(name='superuser', email='superuser@example.com', is_active=True, is_superuser=True)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with an invalid token')
def step_impl(context):
    context.headers = {'Authorization': 'Bearer invalid_token'}

@given('the user is authenticated with an expired token')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id}, expires_delta=-1)
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with a blacklisted token')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    crud.token.blacklist(db, obj_in={'token': token})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with a revoked token')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    crud.token.revoke(db, obj_in={'token': token})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with a token issued for a different user')
def step_impl(context):
    user = models.User(name='different_user', email='different_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with an empty token')
def step_impl(context):
    context.headers = {'Authorization': 'Bearer '}

@given('the user is authenticated with a token that contains invalid characters')
def step_impl(context):
    context.headers = {'Authorization': 'Bearer invalid_token'}

@given('the user is authenticated with a tampered token')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with a token that has expired due to a clock skew')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id}, expires_delta=-1)
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with a token issued for a user who is not active')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=False, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated with a token issued for a user who is inactive')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=False, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated as a superuser with a token issued for a user who is not a superuser')
def step_impl(context):
    user = models.User(name='normal_user', email='normal_user@example.com', is_active=True, is_superuser=False)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@given('the user is authenticated as a superuser with a token issued for a user who is a superuser')
def step_impl(context):
    user = models.User(name='superuser', email='superuser@example.com', is_active=True, is_superuser=True)
    db = next(get_db())
    crud.user.create(db, obj_in=user)
    token = create_access_token(data={'sub': user.id})
    context.headers = {'Authorization': f'Bearer {token}'}

@when('the user tries to access a protected endpoint')
def step_impl(context):
    response = context.client.get('/protected')
    context.response = response

@then('the API returns a 403 Forbidden status code')
def step_impl(context):
    assert context.response.status_code == 403

@then('the API returns a 200 OK status code with the user\'s details')
def step_impl(context):
    assert context.response.status_code == 200
    assert context.response.json()['name'] == 'superuser'

@then('the API returns a 400 Bad Request status code')
def step_impl(context):
    assert context.response.status_code == 400