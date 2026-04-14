import requests
import os
from datetime import datetime, timedelta

class NewsService:
    """Service to fetch trading-related news from NewsAPI"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY', 'demo_key')
        self.base_url = 'https://newsapi.org/v2'
    
    def get_forex_news(self, language='en', sort_by='publishedAt'):
        """Fetch forex and currency trading news"""
        try:
            url = f'{self.base_url}/everything'
            params = {
                'q': '(forex OR currency OR "forex trading" OR "currency pair")',
                'language': language,
                'sortBy': sort_by,
                'pageSize': 50,
                'apiKey': self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching news: {e}")
            return {'articles': []}
    
    def get_news_by_currency(self, currency_code):
        """Fetch news for specific currency pair"""
        try:
            url = f'{self.base_url}/everything'
            currency_name = self._get_currency_name(currency_code)
            params = {
                'q': currency_name,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 30,
                'apiKey': self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching currency news: {e}")
            return {'articles': []}
    
    def categorize_news_by_pair(self, articles):
        """Categorize news articles by currency pair"""
        pairs = {}
        currency_keywords = {
            'EUR': ['euro', 'european central bank', 'ECB'],
            'USD': ['dollar', 'fed', 'federal reserve', 'US economy'],
            'GBP': ['pound', 'BOE', 'bank of england', 'UK'],
            'JPY': ['yen', 'BOJ', 'bank of japan', 'japan'],
            'CHF': ['swiss franc', 'SNB', 'switzerland'],
            'AUD': ['australian dollar', 'RBA', 'australia'],
            'CAD': ['canadian dollar', 'BoC', 'canada'],
        }
        
        for article in articles:
            title_lower = article.get('title', '').lower()
            description_lower = article.get('description', '').lower()
            text = title_lower + ' ' + description_lower
            
            for pair, keywords in currency_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        if pair not in pairs:
                            pairs[pair] = []
                        pairs[pair].append(article)
                        break
        
        return pairs
    
    @staticmethod
    def _get_currency_name(currency_code):
        """Map currency code to currency name"""
        currency_map = {
            'EUR': 'Euro',
            'USD': 'Dollar',
            'GBP': 'Pound',
            'JPY': 'Yen',
            'CHF': 'Swiss Franc',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'NZD': 'New Zealand Dollar',
        }
        return currency_map.get(currency_code, currency_code)
    
    def get_high_impact_news(self, articles):
        """Filter high impact news (based on keywords)"""
        high_impact_keywords = [
            'fed', 'interest rate', 'inflation', 'gdp', 'employment',
            'central bank', 'monetary policy', 'economic data', 'crisis',
            'surge', 'crash', 'record', 'unprecedented'
        ]
        
        high_impact_articles = []
        for article in articles:
            title_lower = article.get('title', '').lower()
            for keyword in high_impact_keywords:
                if keyword in title_lower:
                    high_impact_articles.append(article)
                    break
        
        return high_impact_articles
