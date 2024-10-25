from app import db
from app.models import Expense, ExpenseParticipant

class ExpenseService:

    @staticmethod
    def get_user_expenses(user_id):
        expenses = Expense.query.filter_by(payer_id=user_id).all()
        expense_list = []
        for expense in expenses:
            expense_list.append({
                "description": expense.description,
                "amount": expense.amount,
                "split_type": expense.split_type,
                "date": expense.date_created
            })
        return expense_list
    @staticmethod
    def get_all_expenses():
        # Query all expenses
        expenses = Expense.query.all()
        expense_list = []
        for expense in expenses:
            expense_list.append({
                "description": expense.description,
                "amount": expense.amount,
                "split_type": expense.split_type,
                "payer_id": expense.payer_id,
                "date_created": expense.date_created  # Ensure this field exists in the Expense model
            })
        return expense_list

    @staticmethod
    def add_expense(expense_data):
        # Create a new expense record
        new_expense = Expense(
            description=expense_data['description'],
            amount=expense_data['amount'],
            split_type=expense_data['split_type'],
            payer_id=expense_data['payer_id']
        )
        db.session.add(new_expense)
        db.session.commit()

        # Process participants based on split type
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
        return new_expense

    @staticmethod
    def add_participant(expense_id, user_id, amount, percentage=None):
        participant_entry = ExpenseParticipant(
            expense_id=expense_id,
            user_id=user_id,
            amount=amount,
            percentage=percentage
        )
        db.session.add(participant_entry)
