import json
import pytest

@pytest.fixture
def auth_token(client):
    # Register and log in a user to get the token
    client.post('/user/register', data=json.dumps({
        "email": "expenseuser@example.com",
        "name": "Expense User",
        "mobile": "1234567890",
        "password": "password123"
    }), content_type='application/json')

    response = client.post('/user/login', data=json.dumps({
        "email": "expenseuser@example.com",
        "password": "password123"
    }), content_type='application/json')
    
    return response.json['access_token']

def test_add_expense(client, auth_token):
    auth_token = auth_token[0].get('access_token')
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/expense', data=json.dumps({
        "description": "Dinner",
        "amount": 300,
        "split_type": "Equal",
        "payer_id": 1,
        "participants": [
            {"user_id": 1},
            {"user_id": 2},
            {"user_id": 3}
        ]
    }), headers=headers, content_type='application/json')
    
    assert response.status_code == 201
    assert response.json['message'] == "Expense added successfully"


def test_get_user_expenses(client, auth_token):
    auth_token = auth_token[0].get('access_token')
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/expense/1', headers=headers)
    assert response.status_code == 200
    assert "expenses" in response.json

def test_get_overall_expenses(client, auth_token):
    auth_token = auth_token[0].get('access_token')
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/expense/overall', headers=headers)
    assert response.status_code == 200
    assert "expenses" in response.json
