from datetime import datetime
from bson.objectid import ObjectId

class TradeSignal:
    """Trade signal model"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db['trade_signals']
    
    def create_signal(self, currency_pair, entry_price, stop_loss, take_profit, 
                     execution_time, signal_type, news_source, lot_size, risk_amount):
        """Create a new trade signal"""
        signal = {
            'currency_pair': currency_pair,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'execution_time': execution_time,
            'signal_type': signal_type,  # 'BUY' or 'SELL'
            'news_source': news_source,
            'lot_size': lot_size,
            'risk_amount': risk_amount,
            'status': 'pending',  # pending, executed, closed, cancelled
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(signal)
        return result.inserted_id
    
    def get_all_signals(self, status=None):
        """Get all signals, optionally filtered by status"""
        query = {}
        if status:
            query['status'] = status
        return list(self.collection.find(query).sort('created_at', -1))
    
    def get_signals_by_pair(self, currency_pair):
        """Get signals for a specific currency pair"""
        return list(self.collection.find({'currency_pair': currency_pair}).sort('created_at', -1))
    
    def update_signal_status(self, signal_id, status):
        """Update signal status"""
        self.collection.update_one(
            {'_id': ObjectId(signal_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )
    
    def get_pending_signals(self):
        """Get all pending signals"""
        return list(self.collection.find({'status': 'pending'}).sort('execution_time', 1))
