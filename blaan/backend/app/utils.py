"""
Trading Utilities and Helpers
"""

from datetime import datetime, timedelta

class TradingUtils:
    """Utility functions for trading operations"""
    
    @staticmethod
    def get_market_session():
        """Determine current forex market session"""
        now = datetime.utcnow()
        hour = now.hour
        
        if 8 <= hour < 16:
            return "Asian Session"
        elif 15 <= hour < 23:
            return "European/London Session"
        elif 22 <= hour or hour < 7:
            return "US Session"
        else:
            return "Market Closed"
    
    @staticmethod
    def is_high_volatility_pair(pair):
        """Check if pair is high volatility"""
        high_volatility_pairs = [
            'GBPUSD', 'GBPJPY', 'EURUSD', 'USDCHF', 'USDJPY'
        ]
        return pair in high_volatility_pairs
    
    @staticmethod
    def get_pip_size(pair):
        """Get pip size for currency pair"""
        # JPY pairs have different pip sizes
        if 'JPY' in pair:
            return 0.01
        return 0.0001
    
    @staticmethod
    def calculate_margin_required(lot_size, leverage=1):
        """Calculate margin requirement"""
        # Standard lot = 100,000 units
        pip_value = lot_size * 100000 * 0.0001
        return (pip_value * 100) / leverage
    
    @staticmethod
    def get_average_spread(pair):
        """Get average spread for pair (placeholder)"""
        spreads = {
            'EURUSD': 0.0002,
            'GBPUSD': 0.0003,
            'USDJPY': 0.0003,
            'USDCAD': 0.0003,
            'AUDUSD': 0.0003,
            'NZDUSD': 0.0005,
        }
        return spreads.get(pair, 0.0005)
    
    @staticmethod
    def days_until_next_session(session_name):
        """Calculate days until next session"""
        now = datetime.utcnow()
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        
        if session_name == "Asian Session" and current_day < 4:
            return 0
        
        return (7 - current_day) % 7


class ValidationUtils:
    """Validation helpers"""
    
    @staticmethod
    def validate_price(price, min_price=0.00001, max_price=999999.99999):
        """Validate price format"""
        try:
            p = float(price)
            return min_price <= p <= max_price
        except:
            return False
    
    @staticmethod
    def validate_lot_size(lot_size, min_lot=0.01, max_lot=50):
        """Validate lot size"""
        try:
            l = float(lot_size)
            return min_lot <= l <= max_lot
        except:
            return False
    
    @staticmethod
    def validate_currency_pair(pair):
        """Validate currency pair format"""
        valid_pairs = [
            'EURUSD', 'GBPUSD', 'USDJPY', 'USDCAD', 'AUDUSD', 'NZDUSD',
            'EURJPY', 'GBPJPY', 'GBPCHF', 'EURCHF', 'AUDCHF', 'AUDNZD'
        ]
        return pair in valid_pairs or (len(pair) == 6 and pair[:3] != pair[3:])


class FormatUtils:
    """Output formatting utilities"""
    
    @staticmethod
    def format_price(price, pair='EURUSD'):
        """Format price based on pair type"""
        if 'JPY' in pair:
            return f"{price:.2f}"
        return f"{price:.5f}"
    
    @staticmethod
    def format_currency(amount, currency='USD'):
        """Format currency amount"""
        if currency == 'JPY':
            return f"¥{amount:,.0f}"
        elif currency == 'EUR':
            return f"€{amount:,.2f}"
        elif currency == 'GBP':
            return f"£{amount:,.2f}"
        else:
            return f"${amount:,.2f}"
    
    @staticmethod
    def format_percentage(value):
        """Format percentage"""
        return f"{value:.2f}%"
    
    @staticmethod
    def format_datetime(dt):
        """Format datetime for display"""
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
