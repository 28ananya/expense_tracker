import pandas as pd
import os
from app.models import Expense, ExpenseParticipant, User

class BalanceService:
    @staticmethod
    def generate_balance_sheet():
        expenses = Expense.query.all()
        data = []
        for expense in expenses:
            participants = ExpenseParticipant.query.filter_by(expense_id=expense.id).all()
            payer = User.query.get(expense.payer_id)
            payer_name = payer.name if payer else "Unknown Payer"
            
            for participant in participants:
                user = User.query.get(participant.user_id)
                if user:
                    owed_by = user.name
                else:
                    owed_by = "Unknown User"  # Placeholder if user not found

                data.append({
                    "Expense": expense.description,
                    "Amount": expense.amount,
                    "Paid By": payer_name,
                    "Owed By": owed_by,
                    "Share": participant.amount,
                    "Percentage": participant.percentage or 0
                })

        # Ensure there is a file to return, even if data is empty
        if not data:
            data.append({"Expense": "None", "Amount": 0, "Paid By": "N/A", "Owed By": "N/A", "Share": 0, "Percentage": 0})
        
        # Convert data to a DataFrame and save it as CSV
        df = pd.DataFrame(data)
        file_path = os.path.join(os.getcwd(), 'balance_sheet.csv')
        df.to_csv(file_path, index=False)
        
        return file_path
