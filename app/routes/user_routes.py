# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.schemas import UserSchema
from app.services.user_service import UserService  # Import UserService

user_bp = Blueprint('user_bp', __name__)  # Define the Blueprint instance

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_data = UserSchema().load(data)
    user = UserService.register_user(user_data)
    return jsonify(message="User registered successfully"), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token = UserService.login_user(data['email'], data['password'])
    if token:
        return jsonify(access_token=token), 200
    return jsonify(message="Invalid credentials"), 401

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

