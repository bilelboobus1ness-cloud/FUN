class RiskCalculator:
    """Service to calculate lot size and risk for trades"""
    
    @staticmethod
    def calculate_risk_amount(account_balance, risk_percentage):
        """Calculate risk amount in dollars"""
        return account_balance * (risk_percentage / 100)
    
    @staticmethod
    def calculate_lot_size(account_balance, risk_percentage, entry_price, stop_loss, 
                          pip_value=10, min_lot=0.01, max_lot=10):
        """
        Calculate optimal lot size based on risk management
        
        pip_value: Value of one pip (for most currency pairs = 10)
        For standard lot (100,000 units): 1 pip = $10
        """
        risk_amount = account_balance * (risk_percentage / 100)
        
        # Distance in pips
        pip_distance = abs(entry_price - stop_loss) * 10000
        
        if pip_distance == 0:
            return min_lot
        
        # Calculate lot size: Risk Amount / (Pip Distance * Pip Value)
        lot_size = risk_amount / (pip_distance * pip_value)
        
        # Ensure lot size is within acceptable range
        lot_size = max(min_lot, min(lot_size, max_lot))
        
        return round(lot_size, 2)
    
    @staticmethod
    def calculate_take_profit_from_reward_ratio(entry_price, stop_loss, reward_ratio=2):
        """
        Calculate take profit level based on reward/risk ratio
        Example: If R:R is 2:1, TP should be 2x the distance from SL
        """
        distance = abs(entry_price - stop_loss)
        if entry_price > stop_loss:  # BUY signal
            take_profit = entry_price + (distance * reward_ratio)
        else:  # SELL signal
            take_profit = entry_price - (distance * reward_ratio)
        
        return round(take_profit, 5)
    
    @staticmethod
    def calculate_pip_value(lot_size, currency_pair='EURUSD'):
        """Calculate pip value for the given lot size"""
        # For currency pairs, 1 pip = 0.0001
        # Pip value = (0.0001 * lot_size * 100000) = lot_size * 10
        pip_value = lot_size * 10
        return pip_value
    
    @staticmethod
    def calculate_potential_profit_loss(entry_price, stop_loss, take_profit, lot_size):
        """Calculate potential profit and loss for a trade"""
        pip_value = lot_size * 10
        
        # Risk (loss if SL is hit)
        risk_pips = abs(entry_price - stop_loss) * 10000
        potential_loss = risk_pips * pip_value
        
        # Reward (profit if TP is hit)
        reward_pips = abs(take_profit - entry_price) * 10000
        potential_profit = reward_pips * pip_value
        
        reward_risk_ratio = potential_profit / potential_loss if potential_loss > 0 else 0
        
        return {
            'potential_loss': round(potential_loss, 2),
            'potential_profit': round(potential_profit, 2),
            'reward_risk_ratio': round(reward_risk_ratio, 2)
        }
    
    @staticmethod
    def calculate_drawdown_percentage(starting_balance, current_balance):
        """Calculate percentage drawdown from starting balance"""
        if starting_balance == 0:
            return 0
        
        drawdown = (starting_balance - current_balance) / starting_balance * 100
        return round(drawdown, 2)
    
    @staticmethod
    def get_recommended_lot_size(account_balance, risk_percentage=2, entry_price=1.0850, 
                                 stop_loss=1.0800):
        """Get recommended lot size with sensible defaults"""
        return RiskCalculator.calculate_lot_size(
            account_balance=account_balance,
            risk_percentage=risk_percentage,
            entry_price=entry_price,
            stop_loss=stop_loss,
            pip_value=10,
            min_lot=0.01,
            max_lot=10
        )
