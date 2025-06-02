import pytest
from web-login-demo.main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_signup_success(client):
    response = client.post("/signup", json={"username": "alice", "password": "123"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created"

def test_signup_duplicate(client):
    client.post("/signup", json={"username": "bob", "password": "123"})
    response = client.post("/signup", json={"username": "bob", "password": "456"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_login_success(client):
    client.post("/signup", json={"username": "charlie", "password": "abc"})
    response = client.post("/login", json={"username": "charlie", "password": "abc"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"

def test_login_fail(client):
    response = client.post("/login", json={"username": "ghost", "password": "wrong"})
    assert response.status_code == 401
    assert "error" in response.get_json()
