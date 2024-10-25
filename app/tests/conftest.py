import pytest
from app import create_app, db
import json
@pytest.fixture
def app():
    # Set up the application for testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    
    with app.app_context():
        db.create_all()  # Create tables before tests run
        yield app  # This provides the `app` fixture
        db.session.remove()
        db.drop_all()  # Clean up tables after tests

@pytest.fixture
def client(app):
    return app.test_client()  # This will be the `test_client` fixture for tests

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
@pytest.fixture
def auth_token(client):
    # Register a user to generate a token
    client.post('/user/register', data=json.dumps({
        "email": "expenseuser@example.com",
        "name": "Expense User",
        "mobile": "1234567890",
        "password": "password123"
    }), content_type='application/json')

    # Login to get the access token
    response = client.post('/user/login', data=json.dumps({
        "email": "expenseuser@example.com",
        "password": "password123"
    }), content_type='application/json')
    
    # Return only the access_tosken string
    return response.json['access_token']

