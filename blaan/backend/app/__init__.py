from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
    jwt = JWTManager(app)
    
    # MongoDB Connection
    mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ismaster')
        db = client[os.getenv('DATABASE_NAME', 'blaan_db')]
        logger.info("✓ MongoDB connected")
    except Exception as e:
        logger.error(f"✗ MongoDB connection failed: {e}")
        db = None
    
    app.config['db'] = db
    
    # Register blueprints
    try:
        from app.routes import auth, trades, account, news
        app.register_blueprint(auth.bp)
        app.register_blueprint(trades.bp)
        app.register_blueprint(account.bp)
        app.register_blueprint(news.bp)
        logger.info("✓ All blueprints registered")
    except Exception as e:
        logger.error(f"✗ Blueprint registration error: {e}")
    
    return app
