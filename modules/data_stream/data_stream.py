"""
DataStream - Huvudklass för realtidsdatainhämtning och trendanalys

Denna klass ansvarar för:
- WebSocket-anslutning till Finnhub API
- REST-polling för symbolbatchar
- Trendanalys (volym, momentum, volatilitet)
- Dynamisk prenumeration på toppsymboler
- Simulering av marknadsdata med realistisk prisrörelse
"""

import logging
import random
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class DataStream:
    """
    DataStream hanterar realtidsdata och trendanalys för marknadsdata.
    
    Attributes:
        api_key (str): API-nyckel för Finnhub
        symbols (List[str]): Lista över symboler att övervaka
        websocket_url (str): URL för WebSocket-anslutning
        rest_url (str): URL för REST API
        use_mock_data (bool): Om True används mockdata istället för riktig API-data
        market_simulation (Dict): Simulerad marknadsdata med prishistorik per symbol
    
    Not:
        use_mock_data-parametern styr om DataStream använder mockdata eller ansluter till riktiga API:er.
        När mock används, genereras realistisk simulerad marknadsdata med prisrörelse, volym och trender.
    """
    
    # Base prices för Nasdaq-100 symboler (simulerad marknadsdata)
    BASE_PRICES = {
        'AAPL': 180.0, 'GOOGL': 140.0, 'MSFT': 380.0, 'TSLA': 250.0,
        'AMZN': 150.0, 'META': 320.0, 'NVDA': 480.0, 'AMD': 130.0,
        'NFLX': 450.0, 'BA': 220.0, 'JPM': 150.0, 'V': 260.0
    }
    
    def __init__(self, api_key: str, symbols: Optional[List[str]] = None, use_mock_data: bool = False):
        """
        Initierar DataStream med API-nyckel och valfria symboler.
        
        Args:
            api_key: API-nyckel för Finnhub
            symbols: Lista över symboler att övervaka (valfritt)
            use_mock_data: Om True, använd mockdata istället för riktig API
        """
        self.api_key = api_key
        self.symbols = symbols or list(self.BASE_PRICES.keys())
        self.websocket_url = "wss://ws.finnhub.io"
        self.rest_url = "https://finnhub.io/api/v1"
        self.is_connected = False
        self.use_mock_data = use_mock_data
        self.market_data_cache: Dict[str, Dict[str, Any]] = {}
        
        # Simulerad marknadsdata - initialisera med baspris per symbol
        self.market_simulation: Dict[str, Dict[str, Any]] = {}
        if use_mock_data:
            self._initialize_market_simulation()
        
        logger.info(f"DataStream initialiserad med {len(self.symbols)} symboler (mock_data={use_mock_data})")
    
    def _initialize_market_simulation(self) -> None:
        """
        Initialiserar simulerad marknadsdata för alla symboler.
        Skapar realistiska startpriser och marknadsförhållanden.
        """
        logger.info("Initialiserar simulerad marknadsdata...")
        for symbol in self.symbols:
            base_price = self.BASE_PRICES.get(symbol, 100.0)
            # Lägg till lite initial varians
            current_price = base_price * random.uniform(0.98, 1.02)
            
            self.market_simulation[symbol] = {
                'base_price': base_price,
                'current_price': current_price,
                'prev_close': base_price,
                'open': current_price * random.uniform(0.995, 1.005),
                'high': current_price * random.uniform(1.0, 1.03),
                'low': current_price * random.uniform(0.97, 1.0),
                'volume': random.randint(10000000, 100000000),
                'trend': random.choice(['bullish', 'bearish', 'neutral']),
                'volatility': random.uniform(0.5, 3.0),  # % volatilitet
                'last_update': datetime.now()
            }
        logger.info(f"Marknadsdata initialiserad för {len(self.market_simulation)} symboler")
    
    def _simulate_price_movement(self, symbol: str) -> None:
        """
        Simulerar realistisk prisrörelse för en symbol.
        Använder random walk med trend och volatilitet.
        """
        if symbol not in self.market_simulation:
            return
        
        sim = self.market_simulation[symbol]
        current = sim['current_price']
        volatility = sim['volatility']
        trend = sim['trend']
        
        # Trend bias
        trend_bias = 0.0
        if trend == 'bullish':
            trend_bias = 0.001  # Svag uppåtgående trend
        elif trend == 'bearish':
            trend_bias = -0.001  # Svag nedåtgående trend
        
        # Random walk med trend och volatilitet
        price_change_pct = random.gauss(trend_bias, volatility / 100)
        new_price = current * (1 + price_change_pct)
        
        # Uppdatera simulerad data
        sim['current_price'] = new_price
        sim['high'] = max(sim['high'], new_price)
        sim['low'] = min(sim['low'], new_price)
        sim['volume'] += random.randint(100000, 5000000)
        sim['last_update'] = datetime.now()
        
        # Slumpmässig trendförändring (5% chans)
        if random.random() < 0.05:
            sim['trend'] = random.choice(['bullish', 'bearish', 'neutral'])
    
    def connect_websocket(self) -> bool:
        """
        Upprättar WebSocket-anslutning till Finnhub API.
        
        Returns:
            bool: True om anslutningen lyckades, annars False
        """
        logger.info("Försöker ansluta till WebSocket...")
        if self.use_mock_data:
            self.is_connected = True
            logger.info("Mock WebSocket-anslutning etablerad")
        else:
            # Real-time WebSocket not yet implemented
            self.is_connected = False
            logger.info("Real-time WebSocket not yet implemented - using REST polling mode")
        return self.is_connected
    
    def disconnect_websocket(self) -> None:
        """
        Stänger WebSocket-anslutningen.
        """
        logger.info("Stänger WebSocket-anslutning...")
        # TODO: Implementera WebSocket-nedkoppling
        self.is_connected = False
    
    def subscribe_symbol(self, symbol: str) -> bool:
        """
        Prenumererar på realtidsdata för en specifik symbol.
        
        Args:
            symbol: Tickersymbol att prenumerera på (t.ex. 'AAPL')
        
        Returns:
            bool: True om prenumerationen lyckades, annars False
        """
        logger.info(f"Prenumererar på symbol: {symbol}")
        # TODO: Implementera symbolprenumeration
        if symbol not in self.symbols:
            self.symbols.append(symbol)
        return True
    
    def unsubscribe_symbol(self, symbol: str) -> bool:
        """
        Avprenumererar från realtidsdata för en specifik symbol.
        
        Args:
            symbol: Tickersymbol att avprenumerera från
        
        Returns:
            bool: True om avprenumerationen lyckades, annars False
        """
        logger.info(f"Avprenumererar från symbol: {symbol}")
        # TODO: Implementera symbolavprenumeration
        if symbol in self.symbols:
            self.symbols.remove(symbol)
        return True
    
    def fetch_market_data(self, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Hämtar marknadsdata via REST API för angivna symboler.
        
        Args:
            symbols: Lista över symboler att hämta data för (använder self.symbols om None)
        
        Returns:
            Dict med marknadsdata per symbol (compatible with DataProvider format)
        """
        target_symbols = symbols or self.symbols
        logger.info(f"Hämtar marknadsdata för {len(target_symbols)} symboler via REST")
        
        if self.use_mock_data:
            # Simulera prisrörelse innan vi returnerar data
            for symbol in target_symbols:
                if symbol in self.market_simulation:
                    self._simulate_price_movement(symbol)
            
            # Generera data i DataProvider-kompatibelt format
            mock_data = {}
            for symbol in target_symbols:
                if symbol not in self.market_simulation:
                    # Om symbol saknas, lägg till den
                    base_price = self.BASE_PRICES.get(symbol, 100.0)
                    current_price = base_price * random.uniform(0.98, 1.02)
                    self.market_simulation[symbol] = {
                        'base_price': base_price,
                        'current_price': current_price,
                        'prev_close': base_price,
                        'open': current_price * random.uniform(0.995, 1.005),
                        'high': current_price * random.uniform(1.0, 1.03),
                        'low': current_price * random.uniform(0.97, 1.0),
                        'volume': random.randint(10000000, 100000000),
                        'trend': random.choice(['bullish', 'bearish', 'neutral']),
                        'volatility': random.uniform(0.5, 3.0),
                        'last_update': datetime.now()
                    }
                
                sim = self.market_simulation[symbol]
                current = sim['current_price']
                prev_close = sim['prev_close']
                change = current - prev_close
                change_percent = (change / prev_close) * 100 if prev_close > 0 else 0
                
                # Format kompatibelt med DataProvider (Finnhub API format)
                mock_data[symbol] = {
                    'c': round(current, 2),              # Current price
                    'h': round(sim['high'], 2),          # High
                    'l': round(sim['low'], 2),           # Low
                    'o': round(sim['open'], 2),          # Open
                    'pc': round(prev_close, 2),          # Previous close
                    'd': round(change, 2),               # Change
                    'dp': round(change_percent, 2),      # Change percent
                    'v': sim['volume'],                  # Volume
                    't': int(datetime.now().timestamp()),
                    'trend': sim['trend'],               # Extra: trend info
                    'volatility': round(sim['volatility'], 2)  # Extra: volatility
                }
                self.market_data_cache[symbol] = mock_data[symbol]
            
            logger.info(f"Genererade simulerad marknadsdata för {len(target_symbols)} symboler")
            return mock_data
        else:
            # Real API mode - fetch from Finnhub
            logger.info(f"Fetching real market data from Finnhub API for {len(target_symbols)} symbols")
            
            try:
                # Import FinnhubClient here to avoid circular imports
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(os.path.dirname(current_dir))
                dash_app_path = os.path.join(project_root, 'dash_app')
                if dash_app_path not in sys.path:
                    sys.path.insert(0, dash_app_path)
                
                from dash_app.utils.finnhub_client import FinnhubClient
                
                # Create Finnhub client
                client = FinnhubClient(self.api_key)
                
                # Fetch quotes for all symbols
                api_data = {}
                for symbol in target_symbols:
                    quote = client.get_quote(symbol)
                    if quote and quote.get('c', 0) > 0:  # Valid quote
                        api_data[symbol] = quote
                        self.market_data_cache[symbol] = quote
                        logger.debug(f"Fetched quote for {symbol}: ${quote.get('c', 0):.2f}")
                    else:
                        logger.warning(f"No valid quote data for {symbol}")
                    
                    # Small delay to avoid rate limiting
                    import time
                    time.sleep(0.1)
                
                if api_data:
                    logger.info(f"Successfully fetched real market data for {len(api_data)} symbols")
                else:
                    logger.warning("No market data received from API - check API key and symbol validity")
                
                return api_data
                
            except ImportError as e:
                logger.error(f"Failed to import FinnhubClient: {e}")
                logger.info("Falling back to mock data mode")
                # Fall back to mock data
                self.use_mock_data = True
                return self.fetch_market_data(symbols)
            except Exception as e:
                logger.error(f"Error fetching real market data: {e}")
                logger.info("Consider using mock data mode or check API configuration")
                return {}
    
    def analyze_trend(self, symbol: str) -> Dict[str, float]:
        """
        Analyserar trenddata för en symbol (volym, momentum, volatilitet).
        
        Args:
            symbol: Tickersymbol att analysera
        
        Returns:
            Dict med trendanalys (volume, momentum, volatility, score)
        """
        logger.info(f"Analyserar trend för symbol: {symbol}")
        
        if self.use_mock_data:
            if symbol in self.market_simulation:
                sim = self.market_simulation[symbol]
                # Använd simulerad data för trendanalys
                volume_score = min(100, (sim['volume'] / 1000000) * 2)  # Normalisera volym
                
                # Momentum baserat på prisrörelse
                change_pct = ((sim['current_price'] - sim['prev_close']) / sim['prev_close']) * 100
                momentum_score = change_pct * 10  # Skala momentum
                
                volatility_score = sim['volatility'] * 20  # Skala volatilitet
            else:
                # Fallback om symbol saknas
                volume_score = random.uniform(0, 100)
                momentum_score = random.uniform(-50, 50)
                volatility_score = random.uniform(0, 100)
            
            # Beräkna totalt score (viktad summa)
            total_score = (volume_score * 0.4 + 
                          abs(momentum_score) * 0.3 + 
                          volatility_score * 0.3)
            
            trend_data = {
                'volume': round(volume_score, 2),
                'momentum': round(momentum_score, 2),
                'volatility': round(volatility_score, 2),
                'score': round(total_score, 2)
            }
            logger.info(f"Trendanalys för {symbol}: score={trend_data['score']}")
            return trend_data
        else:
            # Real-time trend analysis not yet implemented
            logger.info("Real-time trend analysis not yet implemented - returning baseline values")
            return {
                'volume': 0.0,
                'momentum': 0.0,
                'volatility': 0.0,
                'score': 0.0
            }
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Hämtar realtidspris för en symbol (DataProvider-kompatibel metod).
        
        Returns:
            Dict med quote-data i Finnhub API format
        """
        data = self.fetch_market_data([symbol])
        return data.get(symbol, {})
    
    def get_batch_quotes(self, symbols: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Hämtar quotes för flera symboler (DataProvider-kompatibel metod).
        """
        return self.fetch_market_data(symbols)
    
    def get_market_summary(self) -> Dict[str, Any]:
        """
        Hämtar marknadssammanfattning (DataProvider-kompatibel metod).
        
        Returns:
            Dict med marknadsmetrics och quotes
        """
        quotes = self.get_batch_quotes()
        
        # Beräkna aggregerade metrics
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
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Hämtar företagsprofil (DataProvider-kompatibel metod).
        """
        # Statiska företagsprofiler
        profiles = {
            'AAPL': {'name': 'Apple Inc', 'ticker': 'AAPL', 'exchange': 'NASDAQ', 'ipo': '1980-12-12', 
                     'marketCapitalization': 2800000, 'shareOutstanding': 15500, 'finnhubIndustry': 'Technology'},
            'GOOGL': {'name': 'Alphabet Inc', 'ticker': 'GOOGL', 'exchange': 'NASDAQ', 'ipo': '2004-08-19',
                      'marketCapitalization': 1700000, 'shareOutstanding': 12200, 'finnhubIndustry': 'Technology'},
            'MSFT': {'name': 'Microsoft Corporation', 'ticker': 'MSFT', 'exchange': 'NASDAQ', 'ipo': '1986-03-13',
                     'marketCapitalization': 2900000, 'shareOutstanding': 7450, 'finnhubIndustry': 'Technology'},
            'TSLA': {'name': 'Tesla Inc', 'ticker': 'TSLA', 'exchange': 'NASDAQ', 'ipo': '2010-06-29',
                     'marketCapitalization': 800000, 'shareOutstanding': 3200, 'finnhubIndustry': 'Automobiles'}
        }
        return profiles.get(symbol, {
            'name': f'{symbol} Inc',
            'ticker': symbol,
            'exchange': 'NASDAQ',
            'marketCapitalization': random.randint(50000, 500000),
            'finnhubIndustry': 'Technology'
        })
    
    def get_historical_data(self, symbol: str, days: int = 30) -> Dict[str, List]:
        """
        Hämtar historisk prisdata (DataProvider-kompatibel metod).
        
        Returns:
            Dict med keys: t (timestamps), c (close), h (high), l (low), o (open), v (volume)
        """
        if not self.use_mock_data:
            logger.info("Historical data from API not yet implemented - using mock data fallback")
            return {'s': 'error'}
        
        # Generera historisk data baserat på simulerad marknad
        base_price = self.BASE_PRICES.get(symbol, 100.0)
        timestamps = []
        closes = []
        highs = []
        lows = []
        opens = []
        volumes = []
        
        current_price = base_price
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            timestamps.append(int(date.timestamp()))
            
            # Random walk
            change = random.uniform(-0.02, 0.02)
            current_price *= (1 + change)
            
            close = current_price
            open_price = current_price * random.uniform(0.98, 1.02)
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
    
    def get_top_symbols(self, limit: int = 10) -> List[str]:
        """
        Hämtar toppsymboler baserat på trendanalys.
        
        Args:
            limit: Antal symboler att returnera
        
        Returns:
            Lista över toppsymboler rankade efter score
        """
        logger.info(f"Hämtar topp {limit} symboler")
        
        if not self.symbols:
            logger.warning("Inga symboler att ranka")
            return []
        
        # Analysera alla symboler och ranka dem
        symbol_scores = []
        for symbol in self.symbols:
            trend_data = self.analyze_trend(symbol)
            symbol_scores.append((symbol, trend_data['score']))
        
        # Sortera efter score (högst först)
        symbol_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Returnera topp N symboler
        top_symbols = [symbol for symbol, score in symbol_scores[:limit]]
        logger.info(f"Toppsymboler: {top_symbols}")
        return top_symbols
    
    def start_stream(self) -> None:
        """
        Startar dataströmmen (ansluter WebSocket och börjar prenumerera).
        """
        logger.info("Startar dataström...")
        self.connect_websocket()
        for symbol in self.symbols:
            self.subscribe_symbol(symbol)
    
    def stop_stream(self) -> None:
        """
        Stoppar dataströmmen (avprenumererar och stänger WebSocket).
        """
        logger.info("Stoppar dataström...")
        for symbol in self.symbols:
            self.unsubscribe_symbol(symbol)
        self.disconnect_websocket()


# Factory function för DataStream (DataProvider-kompatibel)
def get_data_stream(use_mock: Optional[bool] = None, api_key: Optional[str] = None, 
                    symbols: Optional[List[str]] = None) -> DataStream:
    """
    Skapar en DataStream-instans med konfigurerbara parametrar.
    
    Args:
        use_mock: Om True, använd simulerad data. Om None, använd från config
        api_key: Finnhub API-nyckel. Om None, använd från config
        symbols: Lista av symboler att övervaka. Om None, använd från config
    
    Returns:
        DataStream instans konfigurerad för mock eller live data
    """
    # Import config här för att undvika cirkulärer imports
    try:
        import sys
        import os
        # Lägg till project root i path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from config import FINNHUB_API_KEY, USE_MOCK_DATA, DEFAULT_SYMBOLS
    except ImportError:
        # Fallback values
        FINNHUB_API_KEY = ""
        USE_MOCK_DATA = True
        DEFAULT_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 
                          'NVDA', 'AMD', 'NFLX', 'BA', 'JPM', 'V']
    
    # Använd parametrar eller config-värden
    final_use_mock = use_mock if use_mock is not None else USE_MOCK_DATA
    final_api_key = api_key or FINNHUB_API_KEY
    final_symbols = symbols or DEFAULT_SYMBOLS
    
    return DataStream(
        api_key=final_api_key,
        symbols=final_symbols,
        use_mock_data=final_use_mock
    )


# Alias för bakåtkompatibilitet med DataProvider
def get_data_provider(use_mock: Optional[bool] = None) -> DataStream:
    """
    Bakåtkompatibel factory function som returnerar DataStream.
    DataStream har nu alla DataProvider-metoder.
    """
    return get_data_stream(use_mock=use_mock)
