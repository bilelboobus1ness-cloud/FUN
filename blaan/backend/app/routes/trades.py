from flask import Blueprint, request, jsonify
from app.models.trade_signal import TradeSignal
from app.services.risk_calculator import RiskCalculator

bp = Blueprint('trades', __name__, url_prefix='/api/trades')

@bp.route('/create', methods=['POST'])
def create_trade_signal():
    """Create a new trade signal"""
    try:
        data = request.get_json()
        db = request.app.config['db']
        trade_model = TradeSignal(db)
        
        signal_id = trade_model.create_signal(
            currency_pair=data.get('currency_pair'),
            entry_price=float(data.get('entry_price')),
            stop_loss=float(data.get('stop_loss')),
            take_profit=float(data.get('take_profit')),
            execution_time=data.get('execution_time'),
            signal_type=data.get('signal_type'),  # BUY or SELL
            news_source=data.get('news_source'),
            lot_size=float(data.get('lot_size')),
            risk_amount=float(data.get('risk_amount'))
        )
        
        return jsonify({
            'message': 'Trade signal created successfully',
            'signal_id': str(signal_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/all', methods=['GET'])
def get_all_signals():
    """Get all trade signals"""
    try:
        status = request.args.get('status')
        db = request.app.config['db']
        trade_model = TradeSignal(db)
        
        signals = trade_model.get_all_signals(status=status)
        signals_data = []
        for signal in signals:
            signal['_id'] = str(signal['_id'])
            signals_data.append(signal)
        
        return jsonify({'signals': signals_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pair/<currency_pair>', methods=['GET'])
def get_signals_by_pair(currency_pair):
    """Get signals for a specific currency pair"""
    try:
        db = request.app.config['db']
        trade_model = TradeSignal(db)
        
        signals = trade_model.get_signals_by_pair(currency_pair)
        signals_data = []
        for signal in signals:
            signal['_id'] = str(signal['_id'])
            signals_data.append(signal)
        
        return jsonify({
            'currency_pair': currency_pair,
            'signals': signals_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pending', methods=['GET'])
def get_pending_signals():
    """Get all pending trade signals"""
    try:
        db = request.app.config['db']
        trade_model = TradeSignal(db)
        
        signals = trade_model.get_pending_signals()
        signals_data = []
        for signal in signals:
            signal['_id'] = str(signal['_id'])
            signals_data.append(signal)
        
        return jsonify({'pending_signals': signals_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<signal_id>/update-status', methods=['PUT'])
def update_signal_status(signal_id):
    """Update trade signal status"""
    try:
        data = request.get_json()
        db = request.app.config['db']
        trade_model = TradeSignal(db)
        
        trade_model.update_signal_status(signal_id, data.get('status'))
        
        return jsonify({'message': 'Signal status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/calculate-lot-size', methods=['POST'])
def calculate_lot_size():
    """Calculate optimal lot size based on risk parameters"""
    try:
        data = request.get_json()
        
        lot_size = RiskCalculator.calculate_lot_size(
            account_balance=float(data.get('account_balance')),
            risk_percentage=float(data.get('risk_percentage', 2)),
            entry_price=float(data.get('entry_price')),
            stop_loss=float(data.get('stop_loss')),
            pip_value=int(data.get('pip_value', 10))
        )
        
        profit_loss = RiskCalculator.calculate_potential_profit_loss(
            entry_price=float(data.get('entry_price')),
            stop_loss=float(data.get('stop_loss')),
            take_profit=float(data.get('take_profit')),
            lot_size=lot_size
        )
        
        return jsonify({
            'lot_size': lot_size,
            'potential_loss': profit_loss['potential_loss'],
            'potential_profit': profit_loss['potential_profit'],
            'reward_risk_ratio': profit_loss['reward_risk_ratio']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
