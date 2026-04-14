from datetime import datetime
from bson.objectid import ObjectId

class TradingAccount:
    """Trading account model"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db['trading_accounts']
    
    def create_account(self, user_id, broker_name, account_number, api_key, 
                      balance, currency='USD', leverage=1, risk_percentage=2):
        """Create a new trading account"""
        account = {
            'user_id': ObjectId(user_id),
            'broker_name': broker_name,
            'account_number': account_number,
            'api_key': api_key,
            'initial_balance': balance,
            'current_balance': balance,
            'currency': currency,
            'leverage': leverage,
            'risk_percentage': risk_percentage,  # Risk per trade
            'status': 'active',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(account)
        return result.inserted_id
    
    def find_by_user_id(self, user_id):
        """Find all accounts for a user"""
        return list(self.collection.find({'user_id': ObjectId(user_id)}))
    
    def find_by_id(self, account_id):
        """Find account by ID"""
        return self.collection.find_one({'_id': ObjectId(account_id)})
    
    def update_balance(self, account_id, new_balance):
        """Update account balance"""
        self.collection.update_one(
            {'_id': ObjectId(account_id)},
            {'$set': {'current_balance': new_balance, 'updated_at': datetime.utcnow()}}
        )
    
    def update_risk_percentage(self, account_id, risk_percentage):
        """Update risk percentage for account"""
        self.collection.update_one(
            {'_id': ObjectId(account_id)},
            {'$set': {'risk_percentage': risk_percentage, 'updated_at': datetime.utcnow()}}
        )
    
    def deactivate_account(self, account_id):
        """Deactivate an account"""
        self.collection.update_one(
            {'_id': ObjectId(account_id)},
            {'$set': {'status': 'inactive', 'updated_at': datetime.utcnow()}}
        )
