from fastapi.testclient import TestClient
from app.main import app

def before_all(context):
    context.client = TestClient(app)