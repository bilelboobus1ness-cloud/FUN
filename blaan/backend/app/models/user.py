from datetime import datetime
from bson.objectid import ObjectId
import bcrypt
import logging

logger = logging.getLogger(__name__)

class User:
    """User model with REAL password hashing using bcrypt"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db['users']
        try:
            self.collection.create_index('email', unique=True)
        except:
            pass
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt - REAL implementation"""
        try:
            salt = bcrypt.gensalt(rounds=12)
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        except Exception as e:
            logger.error(f"Password hashing error: {e}")
            raise
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    def create_user(self, email, password, full_name, whatsapp=None, telegram_id=None):
        """Create a new user with REAL hashed password"""
        email = email.lower().strip()
        full_name = full_name.strip()
        
        if not email or not password or not full_name:
            raise ValueError("Email, password, and full name required")
        
        if len(password) < 8:
            raise ValueError("Password must be 8+ characters")
        
        if self.find_by_email(email):
            raise ValueError(f"Email {email} already exists")
        
        user = {
            'email': email,
            'password_hash': self.hash_password(password),
            'full_name': full_name,
            'whatsapp': whatsapp,
            'telegram_id': telegram_id,
            'notification_preferences': {
                'email': True,
                'whatsapp': False,
                'telegram': False
            },
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(user)
        logger.info(f"✓ User registered: {email}")
        return result.inserted_id
    
    def find_by_email(self, email):
        """Find user by email"""
        if not email:
            return None
        return self.collection.find_one({'email': email.lower().strip()})
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    def verify_credentials(self, email, password):
        """Verify user credentials with REAL password check"""
        if not email or not password:
            return None
        
        user = self.find_by_email(email)
        if not user or not user.get('is_active'):
            return None
        
        if self.verify_password(password, user.get('password_hash', '')):
            logger.info(f"✓ Login: {email}")
            return user
        
        logger.warning(f"✗ Failed login: {email}")
        return None
    
    def update_notification_preferences(self, user_id, preferences):
        """Update user notification preferences"""
        try:
            self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'notification_preferences': preferences, 'updated_at': datetime.utcnow()}}
            )
            logger.info(f"✓ Preferences updated: {user_id}")
        except Exception as e:
            logger.error(f"Error: {e}")
            raise
    
    def update_contact_info(self, user_id, whatsapp=None, telegram_id=None):
        """Update user contact information"""
        update_data = {}
        if whatsapp:
            update_data['whatsapp'] = whatsapp
        if telegram_id:
            update_data['telegram_id'] = telegram_id
        
        if update_data:
            try:
                update_data['updated_at'] = datetime.utcnow()
                self.collection.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$set': update_data}
                )
                logger.info(f"✓ Contact updated: {user_id}")
            except Exception as e:
                logger.error(f"Error: {e}")
                raise
