from app.utils.auth import generate_access_token  # Import the correct function
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def register_user(data):
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {"message": "User already exists with this email."}, 409

        # Create new user if no duplicate found
        new_user = User(
            email=data['email'],
            name=data['name'],
            mobile=data['mobile'],
            password=generate_password_hash(data['password'])
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            return {"message": "Failed to register user due to duplicate email."}, 409
    def login_user(email, password):
        # Retrieve user by email
        user = User.query.filter_by(email=email).first()
        
        # Verify user exists and password is correct
        if user and check_password_hash(user.password, password):
            # Generate and return a token
            token = generate_access_token(identity=user.id)
            return {"access_token": token}, 200
        else:
            # Return error if credentials are invalid
            return {"message": "Invalid email or password"}, 401
