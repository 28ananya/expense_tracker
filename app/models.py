from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(80), nullable=False)  # hashed password

from datetime import datetime
from app import db

class Expense(db.Model):
    __tablename__ = 'expense'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    split_type = db.Column(db.String(50), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add date_created field with default value of the current date and time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships, if any
    # Add other columns as needed


class ExpenseParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=True)  # Only used for percentage split
