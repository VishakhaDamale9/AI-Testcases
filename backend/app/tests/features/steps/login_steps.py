from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given('an existing user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email, password=password))

@given('an existing inactive user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email, password=password))
    crud.user.update(db=get_db(), db_obj=context.user, obj_in=models.UserUpdate(is_active=False))

@given('a non-existent user with email "{email}"')
def step_impl(context, email):
    context.user = None

@given('an existing user with email "{email}" and password "{password}" as a superuser')
def step_impl(context, email, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email, password=password))

@given('a non-existent user with email "{email}" as a superuser')
def step_impl(context, email):
    context.user = None

@when('I send a POST request to "/login/access-token" with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    if email is None or password is None:
        context.response = TestClient(app).post('/login/access-token', json={'email': email, 'password': password})
    else:
        context.response = TestClient(app).post('/login/access-token', json={'email': email, 'password': password})

@when('I send a POST request to "/login/access-token" as a superuser')
def step_impl(context):
    context.response = TestClient(app).post('/login/access-token', headers={'Authorization': 'Bearer superuser'})

@when('I send a POST request to "/login/test-token" with access token "{access_token}"')
def step_impl(context, access_token):
    if access_token is None or access_token == '':
        context.response = TestClient(app).post('/login/test-token', headers={'Authorization': 'Bearer ' + access_token})
    else:
        context.response = TestClient(app).post('/login/test-token', headers={'Authorization': 'Bearer ' + access_token})

@when('I send a POST request to "/login/test-token" with access token "{access_token}" as a superuser')
def step_impl(context, access_token):
    if access_token is None or access_token == '':
        context.response = TestClient(app).post('/login/test-token', headers={'Authorization': 'Bearer ' + access_token})
    else:
        context.response = TestClient(app).post('/login/test-token', headers={'Authorization': 'Bearer ' + access_token})

@when('I send a POST request to "/password-recovery/{email}"')
def step_impl(context, email):
    context.response = TestClient(app).post('/password-recovery/' + email)

@when('I send a POST request to "/password-recovery/{email}" as a superuser')
def step_impl(context, email):
    context.response = TestClient(app).post('/password-recovery/' + email, headers={'Authorization': 'Bearer superuser'})

@when('I send a POST request to "/password-recovery-html-content/{email}" as a superuser')
def step_impl(context, email):
    context.response = TestClient(app).post('/password-recovery-html-content/' + email, headers={'Authorization': 'Bearer superuser'})

@when('I send a POST request to "/reset-password/" with new password "{new_password}" and access token "{access_token}"')
def step_impl(context, new_password, access_token):
    if access_token is None or access_token == '':
        context.response = TestClient(app).post('/reset-password/', json={'new_password': new_password})
    else:
        context.response = TestClient(app).post('/reset-password/', json={'new_password': new_password, 'access_token': access_token})

@then('the response status code is {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then('the response contains an access token')
def step_impl(context):
    assert 'access_token' in context.response.json()

@then('the response contains the error message "{error_message}"')
def step_impl(context, error_message):
    assert context.response.json()['error'] == error_message

@then('the response contains a message indicating that the password recovery email was sent')
def step_impl(context):
    assert 'Password recovery email sent' in context.response.json()['message']

@then('the response contains the user\'s public information')
def step_impl(context):
    assert 'email' in context.response.json()
    assert 'id' in context.response.json()
    assert 'is_active' in context.response.json()

@then('the response contains the HTML content for password recovery')
def step_impl(context):
    assert 'password_recovery_html' in context.response.json()