from app import db
from app.models import Expense, ExpenseParticipant
from flask import jsonify

class ExpenseService:

    @staticmethod
    def get_user_expenses(user_id):
        expenses = Expense.query.filter_by(payer_id=user_id).all()
        return [
            {
                "description": expense.description,
                "amount": expense.amount,
                "split_type": expense.split_type,
                "date": expense.date_created
            }
            for expense in expenses
        ]

    @staticmethod
    def get_all_expenses():
        expenses = Expense.query.all()
        return [
            {
                "description": expense.description,
                "amount": expense.amount,
                "split_type": expense.split_type,
                "payer_id": expense.payer_id,
                "date_created": expense.date_created
            }
            for expense in expenses
        ]

    @staticmethod
    def validate_expense_data(expense_data):
        # Basic validation for description, amount, and participants
        if not expense_data.get("description"):
            return jsonify({"error": "Description is required"}), 400
        if not expense_data.get("amount") or expense_data["amount"] <= 0:
            return jsonify({"error": "Amount must be a positive number"}), 400
        if not expense_data.get("participants") or not isinstance(expense_data["participants"], list):
            return jsonify({"error": "Participants must be a list"}), 400
        
        # Validate split type-specific requirements
        if expense_data["split_type"] == "Percentage":
            total_percentage = sum(participant.get("percentage", 0) for participant in expense_data["participants"])
            if total_percentage != 100:
                return jsonify({"error": "Percentages must add up to 100%"}), 400
        
        return None

    @staticmethod
    def add_expense(expense_data):
        # Validate data before adding the expense
        validation_error = ExpenseService.validate_expense_data(expense_data)
        if validation_error:
            return validation_error
        
        # Create the expense record
        new_expense = Expense(
            description=expense_data['description'],
            amount=expense_data['amount'],
            split_type=expense_data['split_type'],
            payer_id=expense_data['payer_id']
        )
        db.session.add(new_expense)
        db.session.commit()

        # Process participants according to split type
        participants = expense_data['participants']
        if expense_data['split_type'] == 'Equal':
            equal_share = new_expense.amount / len(participants)
            for participant in participants:
                ExpenseService.add_participant(new_expense.id, participant['user_id'], equal_share)
        elif expense_data['split_type'] == 'Exact':
            for participant in participants:
                ExpenseService.add_participant(new_expense.id, participant['user_id'], participant['amount'])
        elif expense_data['split_type'] == 'Percentage':
            for participant in participants:
                share = new_expense.amount * (participant['percentage'] / 100)
                ExpenseService.add_participant(new_expense.id, participant['user_id'], share, participant['percentage'])

        db.session.commit()
        return jsonify({"message": "Expense added successfully", "expense_id": new_expense.id}), 201

    @staticmethod
    def add_participant(expense_id, user_id, amount, percentage=None):
        participant_entry = ExpenseParticipant(
            expense_id=expense_id,
            user_id=user_id,
            amount=amount,
            percentage=percentage
        )
        db.session.add(participant_entry)
