from flask import Blueprint, request, jsonify
from app.services.news_service import NewsService

bp = Blueprint('news', __name__, url_prefix='/api/news')

@bp.route('/forex', methods=['GET'])
def get_forex_news():
    """Get forex and currency trading news"""
    try:
        service = NewsService()
        news_data = service.get_forex_news()
        
        return jsonify(news_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/categorized', methods=['GET'])
def get_categorized_news():
    """Get news categorized by currency pair"""
    try:
        service = NewsService()
        news_data = service.get_forex_news()
        categorized = service.categorize_news_by_pair(news_data.get('articles', []))
        
        return jsonify({
            'categorized_news': categorized,
            'total_articles': sum(len(articles) for articles in categorized.values())
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/currency/<currency_code>', methods=['GET'])
def get_currency_news(currency_code):
    """Get news for specific currency"""
    try:
        service = NewsService()
        news_data = service.get_news_by_currency(currency_code)
        
        return jsonify({
            'currency': currency_code,
            'articles': news_data.get('articles', [])
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/high-impact', methods=['GET'])
def get_high_impact_news():
    """Get high impact news only"""
    try:
        service = NewsService()
        news_data = service.get_forex_news()
        high_impact = service.get_high_impact_news(news_data.get('articles', []))
        
        return jsonify({
            'high_impact_articles': high_impact,
            'count': len(high_impact)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
