## Daily Expenses Sharing Application

## Features
User Management: Register users with email, name, and mobile number.
Expense Management: Add expenses and split them among participants using three methods:
Equal: Split equally among participants.
Exact: Specify exact amounts for each participant.
Percentage: Specify the percentage each participant owes.
Balance Sheet: View individual or overall expenses and download the balance sheet as a CSV file.
Authentication: Secure endpoints with JWT-based authentication.

## Setup and Installation

1. Clone the Repository
    ## git clone  https://github.com/28ananya/expense_tracker.git
2. Install Dependencies
    ## pip install -r requirements.txt

3. Run the Application
    ## python run.py
    It runs on local host http://127.0.0.1:5000/

## API END POINTS

User Endpoints
1. Register User

        URL: POST /user/register
        Body:
        json
        {
        "email": "user@example.com",
        "name": "User Name",
        "mobile": "1234567890",
        "password": "password123"
        }
2. Login User

        URL: POST /user/login

        json
        {
        "email": "user@example.com",
        "password": "password123"
        }
3. Expense Endpoints
Add Expense

    URL: POST /expense
    Authorization: Bearer token required
    Body (example for equal split):
    json

    {
    "description": "Dinner",
    "amount": 300,
    "split_type": "Equal",
    "payer_id": 1,
    "participants": [
        {"user_id": 1},
        {"user_id": 2},
        {"user_id": 3}
    ]
    }
4. Retrieve User Expenses

            URL: GET /expense/<user_id>
            Authorization: Bearer token required
            Retrieve Overall Expenses

5. URL: GET /expense/overall
        Authorization: Bearer token required
        Download Balance Sheet

6. URL: GET /balance/balance_sheet/download
        Authorization: Bearer token required

## Unit and Integrated testing
      pytest --disable-warnings