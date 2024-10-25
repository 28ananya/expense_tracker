from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Import and register blueprints
    from .routes import user_bp, expense_bp, balance_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(expense_bp, url_prefix='/expense')  # Ensure correct registration
    app.register_blueprint(balance_bp, url_prefix='/balance')

    with app.app_context():
        db.create_all()  # Create tables
    
    return app
