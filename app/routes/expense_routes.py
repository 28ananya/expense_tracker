from flask import Blueprint, request, jsonify
from app.services.expense_service import ExpenseService
from flask_jwt_extended import jwt_required

expense_bp = Blueprint('expense_bp', __name__)  # Define the Blueprint instance

@expense_bp.route('', methods=['POST'])  # Use an empty string here to map '/expense' correctly
@jwt_required()
def add_expense():
    data = request.get_json()
    expense = ExpenseService.add_expense(data)
    return jsonify(message="Expense added successfully"), 201

@expense_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_expenses(user_id):
    expenses = ExpenseService.get_user_expenses(user_id)
    return jsonify(expenses=expenses), 200

@expense_bp.route('/overall', methods=['GET'])
@jwt_required()
def get_overall_expenses():
    expenses = ExpenseService.get_all_expenses()
    return jsonify(expenses=expenses), 200


