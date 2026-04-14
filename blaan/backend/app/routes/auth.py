from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from email_validator import validate_email, EmailNotValidError
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user with REAL validation"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        full_name = data.get('full_name', '').strip()
        
        if not all([email, password, full_name]):
            return jsonify({'error': 'Email, password, and name required'}), 400
        
        # Validate email format
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Password must be 8+ characters'}), 400
        
        db = request.app.config['db']
        user_model = User(db)
        
        try:
            user_id = user_model.create_user(
                email=email,
                password=password,
                full_name=full_name,
                whatsapp=data.get('whatsapp'),
                telegram_id=data.get('telegram_id')
            )
            
            return jsonify({
                'message': '✓ Registration successful',
                'user_id': str(user_id),
                'email': email
            }), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login with REAL password verification and JWT token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        db = request.app.config['db']
        user_model = User(db)
        
        # REAL credential verification
        user = user_model.verify_credentials(email, password)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'message': '✓ Login successful',
            'access_token': access_token,
            'user_id': str(user['_id']),
            'email': user['email'],
            'full_name': user['full_name']
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user from JWT token"""
    try:
        user_id = get_jwt_identity()
        db = request.app.config['db']
        user_model = User(db)
        
        user = user_model.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user_id': str(user['_id']),
            'email': user['email'],
            'full_name': user['full_name'],
            'notification_preferences': user.get('notification_preferences')
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch user'}), 500
