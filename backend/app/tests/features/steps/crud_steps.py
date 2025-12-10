from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.api.deps import get_db
from app import crud, models

@given("a new user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email, password=password))

@given("a new user with missing email and password")
def step_impl(context):
    context.user = None

@given("a new user with email {email}")
def step_impl(context, email):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email))

@given("a new user with password {password}")
def step_impl(context, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(password=password))

@given("a new user with email {email} and password {password} with invalid email")
def step_impl(context, email, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email, password=password))

@given("a new user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.create(db=get_db(), obj_in=models.UserCreate(email=email, password=password))

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid email")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("a non-existent user with email {email}")
def step_impl(context, email):
    context.user = None

@given("a non-existent user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = None

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} with invalid email")
def step_impl(context, email):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password}")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email} and password {password} with invalid password")
def step_impl(context, email, password):
    context.user = crud.user.get(db=get_db(), email=email)

@given("an existing user with email {email}")
def step_impl(context, email):
    context