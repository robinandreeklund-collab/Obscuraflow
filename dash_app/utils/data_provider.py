"""
Data Provider
Unified interface for both mock and real Finnhub data
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from dash_app.utils.finnhub_client import FinnhubClient
    from dash_app.config import FINNHUB_API_KEY, USE_MOCK_DATA, DEFAULT_SYMBOLS
except ImportError:
    # Fallback for testing
    FINNHUB_API_KEY = ""
    USE_MOCK_DATA = True
    DEFAULT_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']


class DataProvider:
    """
    Provides market data from either mock or real Finnhub API
    """
    
    def __init__(self, use_mock: Optional[bool] = None, api_key: Optional[str] = None):
        """
        Initialize data provider
        
        Args:
            use_mock: If True, use mock data. If None, use config setting
            api_key: Finnhub API key. If None, use config setting
        """
        self.use_mock = use_mock if use_mock is not None else USE_MOCK_DATA
        self.api_key = api_key or FINNHUB_API_KEY
        self.finnhub_client = None if self.use_mock else FinnhubClient(self.api_key)
        self.symbols = DEFAULT_SYMBOLS
        
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a symbol
        
        Returns:
            Dict with keys: c (current), h (high), l (low), o (open), pc (previous close), d (change), dp (change percent)
        """
        if self.use_mock:
            return self._generate_mock_quote(symbol)
        else:
            quote = self.finnhub_client.get_quote(symbol)
            if quote:
                return quote
            else:
                # Fallback to mock data if API fails
                return self._generate_mock_quote(symbol)
    
    def get_batch_quotes(self, symbols: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Get quotes for multiple symbols
        """
        if symbols is None:
            symbols = self.symbols
        
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_quote(symbol)
        return results
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile
        
        Returns:
            Dict with company information
        """
        if self.use_mock:
            return self._generate_mock_profile(symbol)
        else:
            profile = self.finnhub_client.get_company_profile(symbol)
            if profile:
                return profile
            else:
                return self._generate_mock_profile(symbol)
    
    def get_historical_data(self, symbol: str, days: int = 30) -> Dict[str, List]:
        """
        Get historical price data
        
        Returns:
            Dict with keys: t (timestamps), c (close), h (high), l (low), o (open), v (volume)
        """
        if self.use_mock:
            return self._generate_mock_historical(symbol, days)
        else:
            from_date = datetime.now() - timedelta(days=days)
            candles = self.finnhub_client.get_candles(symbol, 'D', from_date)
            if candles and candles.get('s') == 'ok':
                return candles
            else:
                return self._generate_mock_historical(symbol, days)
    
    def get_market_summary(self) -> Dict[str, Any]:
        """
        Get market summary with multiple symbols
        """
        quotes = self.get_batch_quotes()
        
        # Calculate aggregate metrics
        total_symbols = len(quotes)
        gainers = sum(1 for q in quotes.values() if q.get('dp', 0) > 0)
        losers = sum(1 for q in quotes.values() if q.get('dp', 0) < 0)
        avg_change = sum(q.get('dp', 0) for q in quotes.values()) / total_symbols if total_symbols > 0 else 0
        
        return {
            'total_symbols': total_symbols,
            'gainers': gainers,
            'losers': losers,
            'unchanged': total_symbols - gainers - losers,
            'avg_change_percent': avg_change,
            'quotes': quotes,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_mock_quote(self, symbol: str) -> Dict[str, Any]:
        """Generate realistic mock quote data"""
        # Base price depends on symbol
        base_prices = {
            'AAPL': 180.0, 'GOOGL': 140.0, 'MSFT': 380.0, 'TSLA': 250.0,
            'AMZN': 150.0, 'META': 320.0, 'NVDA': 480.0, 'AMD': 130.0,
            'NFLX': 450.0, 'BA': 220.0, 'JPM': 150.0, 'V': 260.0
        }
        base_price = base_prices.get(symbol, 100.0)
        
        # Add random variation
        variation = random.uniform(-0.03, 0.03)
        current = base_price * (1 + variation)
        prev_close = base_price
        change = current - prev_close
        change_percent = (change / prev_close) * 100
        
        # Daily high/low
        high = current * random.uniform(1.0, 1.02)
        low = current * random.uniform(0.98, 1.0)
        open_price = prev_close * random.uniform(0.99, 1.01)
        
        return {
            'c': round(current, 2),      # Current price
            'h': round(high, 2),          # High
            'l': round(low, 2),           # Low
            'o': round(open_price, 2),    # Open
            'pc': round(prev_close, 2),   # Previous close
            'd': round(change, 2),        # Change
            'dp': round(change_percent, 2), # Change percent
            't': int(datetime.now().timestamp())
        }
    
    def _generate_mock_profile(self, symbol: str) -> Dict[str, Any]:
        """Generate mock company profile"""
        profiles = {
            'AAPL': {'name': 'Apple Inc', 'ticker': 'AAPL', 'exchange': 'NASDAQ', 'ipo': '1980-12-12', 'marketCapitalization': 2800000, 'shareOutstanding': 15500, 'logo': '', 'phone': '14089961010', 'weburl': 'https://www.apple.com/', 'finnhubIndustry': 'Technology'},
            'GOOGL': {'name': 'Alphabet Inc', 'ticker': 'GOOGL', 'exchange': 'NASDAQ', 'ipo': '2004-08-19', 'marketCapitalization': 1700000, 'shareOutstanding': 12200, 'logo': '', 'phone': '', 'weburl': 'https://www.google.com/', 'finnhubIndustry': 'Technology'},
            'MSFT': {'name': 'Microsoft Corporation', 'ticker': 'MSFT', 'exchange': 'NASDAQ', 'ipo': '1986-03-13', 'marketCapitalization': 2900000, 'shareOutstanding': 7450, 'logo': '', 'phone': '14258828080', 'weburl': 'https://www.microsoft.com/', 'finnhubIndustry': 'Technology'},
            'TSLA': {'name': 'Tesla Inc', 'ticker': 'TSLA', 'exchange': 'NASDAQ', 'ipo': '2010-06-29', 'marketCapitalization': 800000, 'shareOutstanding': 3200, 'logo': '', 'phone': '', 'weburl': 'https://www.tesla.com/', 'finnhubIndustry': 'Automobiles'}
        }
        return profiles.get(symbol, {
            'name': f'{symbol} Inc',
            'ticker': symbol,
            'exchange': 'NASDAQ',
            'marketCapitalization': random.randint(50000, 500000),
            'finnhubIndustry': 'Technology'
        })
    
    def _generate_mock_historical(self, symbol: str, days: int) -> Dict[str, List]:
        """Generate mock historical data"""
        base_price = 100.0
        timestamps = []
        closes = []
        highs = []
        lows = []
        opens = []
        volumes = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            timestamps.append(int(date.timestamp()))
            
            # Random walk
            change = random.uniform(-0.02, 0.02)
            base_price *= (1 + change)
            
            close = base_price
            open_price = base_price * random.uniform(0.98, 1.02)
            high = max(close, open_price) * random.uniform(1.0, 1.03)
            low = min(close, open_price) * random.uniform(0.97, 1.0)
            volume = random.randint(50000000, 150000000)
            
            closes.append(round(close, 2))
            opens.append(round(open_price, 2))
            highs.append(round(high, 2))
            lows.append(round(low, 2))
            volumes.append(volume)
        
        return {
            't': timestamps,
            'c': closes,
            'h': highs,
            'l': lows,
            'o': opens,
            'v': volumes,
            's': 'ok'
        }


# Global instance
_data_provider = None

def get_data_provider(use_mock: Optional[bool] = None) -> DataProvider:
    """Get or create the global data provider instance"""
    global _data_provider
    # Always recreate if use_mock is specified, or if provider doesn't exist
    if use_mock is not None or _data_provider is None:
        _data_provider = DataProvider(use_mock=use_mock)
    return _data_provider
