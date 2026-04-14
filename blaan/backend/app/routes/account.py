from flask import Blueprint, request, jsonify
from app.models.account import TradingAccount
from app.services.risk_calculator import RiskCalculator

bp = Blueprint('account', __name__, url_prefix='/api/account')

@bp.route('/create', methods=['POST'])
def create_account():
    """Create a new trading account"""
    try:
        data = request.get_json()
        db = request.app.config['db']
        account_model = TradingAccount(db)
        
        account_id = account_model.create_account(
            user_id=data.get('user_id'),
            broker_name=data.get('broker_name'),
            account_number=data.get('account_number'),
            api_key=data.get('api_key'),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', 'USD'),
            leverage=int(data.get('leverage', 1)),
            risk_percentage=float(data.get('risk_percentage', 2))
        )
        
        return jsonify({
            'message': 'Account created successfully',
            'account_id': str(account_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<user_id>', methods=['GET'])
def get_user_accounts(user_id):
    """Get all trading accounts for a user"""
    try:
        db = request.app.config['db']
        account_model = TradingAccount(db)
        
        accounts = account_model.find_by_user_id(user_id)
        accounts_data = []
        for acc in accounts:
            acc['_id'] = str(acc['_id'])
            acc['user_id'] = str(acc['user_id'])
            accounts_data.append(acc)
        
        return jsonify({'accounts': accounts_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<account_id>/risk-info', methods=['GET'])
def get_risk_info(account_id):
    """Get risk information for an account"""
    try:
        db = request.app.config['db']
        account_model = TradingAccount(db)
        
        account = account_model.find_by_id(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        risk_amount = RiskCalculator.calculate_risk_amount(
            account['current_balance'],
            account['risk_percentage']
        )
        
        recommended_lot = RiskCalculator.get_recommended_lot_size(
            account['current_balance'],
            account['risk_percentage']
        )
        
        return jsonify({
            'account_id': str(account['_id']),
            'balance': account['current_balance'],
            'risk_percentage': account['risk_percentage'],
            'risk_amount': round(risk_amount, 2),
            'recommended_lot_size': recommended_lot,
            'currency': account['currency'],
            'leverage': account['leverage']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<account_id>/update-balance', methods=['PUT'])
def update_balance(account_id):
    """Update account balance"""
    try:
        data = request.get_json()
        db = request.app.config['db']
        account_model = TradingAccount(db)
        
        account_model.update_balance(account_id, float(data.get('new_balance')))
        
        return jsonify({'message': 'Balance updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<account_id>/update-risk', methods=['PUT'])
def update_risk(account_id):
    """Update risk percentage for account"""
    try:
        data = request.get_json()
        db = request.app.config['db']
        account_model = TradingAccount(db)
        
        account_model.update_risk_percentage(account_id, float(data.get('risk_percentage')))
        
        return jsonify({'message': 'Risk percentage updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
