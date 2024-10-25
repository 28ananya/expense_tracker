import json
import pytest

def test_register_user(client):
    response = client.post('/user/register', data=json.dumps({
        "email": "testuser@example.com",
        "name": "Test User",
        "mobile": "1234567890",
        "password": "password123"
    }), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully"

def test_login_user(client):
    # Ensure the user is registered
    client.post('/user/register', data=json.dumps({
        "email": "testuser@example.com",
        "name": "Test User",
        "mobile": "1234567890",
        "password": "password123"
    }), content_type='application/json')
    
    # Attempt login
    response = client.post('/user/login', data=json.dumps({
        "email": "testuser@example.com",
        "password": "password123"
    }), content_type='application/json')
    
    assert response.status_code == 200
    assert "access_token" in response.json
