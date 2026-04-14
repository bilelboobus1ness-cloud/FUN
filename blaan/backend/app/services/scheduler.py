"""
Optional: Scheduled task runner for automated news fetching and signal generation
This can be run in the background to automatically check news and generate signals
"""

from apscheduler.schedulers.background import BackgroundScheduler
from app.services.news_service import NewsService
from app.models.trade_signal import TradeSignal
from app.models.account import TradingAccount
from app.services.notification_service import NotificationService
from app.services.risk_calculator import RiskCalculator
from pymongo import MongoClient
import os
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalScheduler:
    def __init__(self, db):
        self.db = db
        self.news_service = NewsService()
        self.notification_service = NotificationService()
        self.scheduler = BackgroundScheduler()
    
    def fetch_and_generate_signals(self):
        """Fetch news and generate signals every hour"""
        try:
            logger.info("Starting scheduled news fetch...")
            
            # Get categorized news
            news_data = self.news_service.get_forex_news()
            categorized = self.news_service.categorize_news_by_pair(news_data.get('articles', []))
            
            # Generate signals for each currency pair with high-impact news
            for pair, articles in categorized.items():
                for article in articles[:2]:  # Top 2 articles per pair
                    # Check if signal already exists for this article
                    if not self._signal_exists(article['url']):
                        self._generate_signal_from_article(pair, article)
            
            logger.info("Signal generation completed")
        except Exception as e:
            logger.error(f"Error in scheduled signal generation: {e}")
    
    def _signal_exists(self, source_url):
        """Check if signal already exists for this news source"""
        trade_signal_model = TradeSignal(self.db)
        signals = trade_signal_model.collection.find_one({'news_source': source_url})
        return signals is not None
    
    def _generate_signal_from_article(self, pair, article):
        """Generate a trade signal from news article"""
        try:
            trade_signal_model = TradeSignal(self.db)
            account_model = TradingAccount(self.db)
            
            # Parse pair (e.g., "EURUSD" from "EUR")
            currency_codes = {
                'EUR': 'EURUSD', 'GBP': 'GBPUSD', 'JPY': 'USDJPY',
                'AUD': 'AUDUSD', 'CAD': 'USDCAD', 'CHF': 'USDCHF'
            }
            
            full_pair = currency_codes.get(pair, f'{pair}USD')
            
            # Fetch current price (in production, use real-time data)
            entry_price = self._get_current_price(full_pair, 1.0850)
            
            # Determine signal direction based on article sentiment
            signal_type = self._analyze_sentiment(article['title'])
            
            # Set stop loss and take profit
            if signal_type == 'BUY':
                stop_loss = entry_price - 0.0050
                take_profit = entry_price + 0.0100
            else:
                stop_loss = entry_price + 0.0050
                take_profit = entry_price - 0.0100
            
            # Get account info for risk calculation
            system_account = account_model.collection.find_one()
            if system_account:
                lot_size = RiskCalculator.calculate_lot_size(
                    system_account['current_balance'],
                    system_account['risk_percentage'],
                    entry_price,
                    stop_loss
                )
                
                risk_amount = RiskCalculator.calculate_risk_amount(
                    system_account['current_balance'],
                    system_account['risk_percentage']
                )
            else:
                # Default values
                lot_size = 0.1
                risk_amount = 200
            
            # Create signal
            signal_id = trade_signal_model.create_signal(
                currency_pair=full_pair,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                execution_time=datetime.utcnow().isoformat(),
                signal_type=signal_type,
                news_source=article['source']['name'],
                lot_size=lot_size,
                risk_amount=risk_amount
            )
            
            logger.info(f"Generated signal: {full_pair} {signal_type} at {entry_price}")
            
            # Notify users (optional)
            # self._notify_users(signal)
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
    
    def _analyze_sentiment(self, title):
        """Simple sentiment analysis based on keywords"""
        positive_keywords = ['surge', 'rise', 'gain', 'strong', 'bullish', 'rally', 'up']
        negative_keywords = ['crash', 'fall', 'decline', 'weak', 'bearish', 'drop', 'down']
        
        title_lower = title.lower()
        
        positive_count = sum(1 for word in positive_keywords if word in title_lower)
        negative_count = sum(1 for word in negative_keywords if word in title_lower)
        
        return 'BUY' if positive_count > negative_count else 'SELL'
    
    def _get_current_price(self, pair, default_price):
        """Get current price for pair (placeholder)"""
        # In production, integrate with real price feed
        # This is a placeholder
        return default_price
    
    def start(self, interval_minutes=60):
        """Start the scheduler"""
        self.scheduler.add_job(
            self.fetch_and_generate_signals,
            'interval',
            minutes=interval_minutes,
            id='news_signal_generator',
            name='Generate trade signals from news'
        )
        
        self.scheduler.start()
        logger.info(f"Scheduler started - will fetch news every {interval_minutes} minutes")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")


# Usage in main.py:
# from app.scheduler import SignalScheduler
# scheduler = SignalScheduler(db)
# scheduler.start(interval_minutes=60)
