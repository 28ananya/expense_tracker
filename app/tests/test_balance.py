import pytest
import json

@pytest.fixture
def auth_token(client):
    # Register and log in a user to get the token
    client.post('/user/register', data=json.dumps({
        "email": "balanceuser@example.com",
        "name": "Balance User",
        "mobile": "1234567890",
        "password": "password123"
    }), content_type='application/json')

    response = client.post('/user/login', data=json.dumps({
        "email": "balanceuser@example.com",
        "password": "password123"
    }), content_type='application/json')
    
    return response.json['access_token']

def test_download_balance_sheet(client, auth_token):
    auth_token = auth_token[0].get('access_token')
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/balance/balance_sheet/download', headers=headers)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'].startswith("attachment")
