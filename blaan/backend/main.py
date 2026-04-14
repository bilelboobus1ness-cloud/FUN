from app import create_app
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = create_app()

@app.route('/')
def index():
    return {
        'message': '✓ BLAAN Trading API is LIVE',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/register, /api/auth/login',
            'account': '/api/account/create, /api/account/<user_id>',
            'trades': '/api/trades/all, /api/trades/create',
            'news': '/api/news/categorized, /api/news/forex'
        }
    }

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        db = app.config.get('db')
        if db:
            db.admin.command('ismaster')
            db_status = "✓ Connected"
        else:
            db_status = "✗ Not connected"
        
        return {
            'status': 'healthy',
            'service': 'BLAAN Trading API',
            'database': db_status,
            'version': '1.0.0'
        }, 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {'status': 'unhealthy', 'error': str(e)}, 500

@app.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad request'}, 400

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"🚀 Starting BLAAN Trading API...")
    logger.info(f"📍 Environment: {'Development' if debug else 'Production'}")
    logger.info(f"🔗 Server: http://localhost:{port}")
    logger.info(f"📚 API Docs: http://localhost:{port}/")
    logger.info(f"❤️  Status check: http://localhost:{port}/health")
    logger.info("")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
