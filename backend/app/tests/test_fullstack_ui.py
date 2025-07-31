import requests
from bs4 import BeautifulSoup
import time
import pytest

def test_frontend_dashboard():
    """Test that the frontend dashboard loads and displays correctly"""
    
    # 1. Test that frontend is accessible
    frontend_url = "http://localhost:5173/"
    try:
        response = requests.get(frontend_url, timeout=5)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Frontend not running on http://localhost:5173/")
    

    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 3. Check for basic page structure
    assert soup.find("html") is not None
    assert soup.find("body") is not None
    
    # 4. Check for React app mounting point (usually div with id="root")
    root_div = soup.find("div", id="root")
    assert root_div is not None

def test_backend_api_accessible():
    """Test that backend API is accessible"""
    
    # Test root endpoint
    backend_url = "http://localhost:8000/"
    response = requests.get(backend_url)
    assert response.status_code == 200
    
    # Test API docs
    docs_url = "http://localhost:8000/docs"
    response = requests.get(docs_url)
    assert response.status_code == 200

def test_full_stack_integration():
    """Test that frontend can communicate with backend"""
    
    # 1. Create an item via backend API
    login_data = {
        "username": "admin@example.com",  # Update with your credentials
        "password": "yourpassword",       # Update with your credentials
    }
    
    # Login to get token
    login_response = requests.post(
        "http://localhost:8000/api/v1/login/access-token",
        data=login_data
    )
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create test item
        item_data = {"title": "Test Item", "description": "Test Description"}
        create_response = requests.post(
            "http://localhost:8000/api/v1/items/",
            json=item_data,
            headers=headers
        )
        assert create_response.status_code == 200
        
        # 2. Check that frontend can load (basic connectivity test)
        frontend_response = requests.get("http://localhost:5173/")
        assert frontend_response.status_code == 200