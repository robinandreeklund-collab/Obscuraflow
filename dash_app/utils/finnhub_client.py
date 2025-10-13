"""
Finnhub API Client
Handles real-time and historical data from Finnhub API
"""

import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)


class FinnhubClient:
    """
    Client for fetching real market data from Finnhub API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Finnhub client
        
        Args:
            api_key: Finnhub API key
        """
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
        self.session = requests.Session()
        self.session.headers.update({'X-Finnhub-Token': api_key})
        self._cache = {}
        self._cache_time = {}
        self._cache_ttl = 60  # Cache for 60 seconds
        
    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get real-time quote for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Dict with quote data or None if error
            Returns {'error': 'rate_limit', 'status_code': 429} if rate limited
        """
        cache_key = f"quote_{symbol}"
        
        # Check cache
        if cache_key in self._cache:
            if time.time() - self._cache_time[cache_key] < self._cache_ttl:
                return self._cache[cache_key]
        
        try:
            url = f"{self.base_url}/quote"
            params = {'symbol': symbol}
            response = self.session.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # Cache the result
                self._cache[cache_key] = data
                self._cache_time[cache_key] = time.time()
                return data
            elif response.status_code == 429:
                logger.warning(f"Rate limit exceeded for {symbol}")
                return {'error': 'rate_limit', 'status_code': 429}
            else:
                logger.error(f"Error fetching quote for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Exception fetching quote for {symbol}: {e}")
            return None
    
    def get_company_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get company profile information
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dict with company data or None if error
        """
        cache_key = f"profile_{symbol}"
        
        # Check cache (longer TTL for profile data)
        if cache_key in self._cache:
            if time.time() - self._cache_time[cache_key] < 3600:  # 1 hour cache
                return self._cache[cache_key]
        
        try:
            url = f"{self.base_url}/stock/profile2"
            params = {'symbol': symbol}
            response = self.session.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self._cache[cache_key] = data
                self._cache_time[cache_key] = time.time()
                return data
            else:
                logger.error(f"Error fetching profile for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Exception fetching profile for {symbol}: {e}")
            return None
    
    def get_candles(self, symbol: str, resolution: str = 'D', 
                    from_date: Optional[datetime] = None,
                    to_date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
        """
        Get historical candle data
        
        Args:
            symbol: Stock symbol
            resolution: Candle resolution (1, 5, 15, 30, 60, D, W, M)
            from_date: Start date
            to_date: End date
            
        Returns:
            Dict with OHLCV data or None if error
        """
        if to_date is None:
            to_date = datetime.now()
        if from_date is None:
            from_date = to_date - timedelta(days=30)
        
        try:
            url = f"{self.base_url}/stock/candle"
            params = {
                'symbol': symbol,
                'resolution': resolution,
                'from': int(from_date.timestamp()),
                'to': int(to_date.timestamp())
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('s') == 'ok':
                    return data
                else:
                    logger.warning(f"No data for {symbol}: {data.get('s')}")
                    return None
            else:
                logger.error(f"Error fetching candles for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Exception fetching candles for {symbol}: {e}")
            return None
    
    def get_batch_quotes(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get quotes for multiple symbols
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dict mapping symbol to quote data
        """
        results = {}
        for symbol in symbols:
            quote = self.get_quote(symbol)
            if quote:
                results[symbol] = quote
            # Add small delay to avoid rate limiting
            time.sleep(0.1)
        return results
    
    def get_market_status(self) -> Optional[Dict[str, Any]]:
        """
        Get current market status
        
        Returns:
            Dict with market status or None if error
        """
        cache_key = "market_status"
        
        # Check cache
        if cache_key in self._cache:
            if time.time() - self._cache_time[cache_key] < 300:  # 5 min cache
                return self._cache[cache_key]
        
        try:
            url = f"{self.base_url}/stock/market-status"
            params = {'exchange': 'US'}
            response = self.session.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self._cache[cache_key] = data
                self._cache_time[cache_key] = time.time()
                return data
            else:
                return None
                
        except Exception as e:
            logger.error(f"Exception fetching market status: {e}")
            return None
