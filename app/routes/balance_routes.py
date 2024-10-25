from flask import Blueprint, send_file
from app.services.balance_service import BalanceService
from flask_jwt_extended import jwt_required

balance_bp = Blueprint('balance_bp', __name__)  # Define the Blueprint instance

@balance_bp.route('/balance_sheet/download', methods=['GET'])
@jwt_required()
def download_balance_sheet():
    file_path = BalanceService.generate_balance_sheet()
    return send_file(file_path, as_attachment=True)
