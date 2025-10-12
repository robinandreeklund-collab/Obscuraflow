"""
DataStream - Huvudklass för realtidsdatainhämtning och trendanalys

Denna klass ansvarar för:
- WebSocket-anslutning till Finnhub API
- REST-polling för symbolbatchar
- Trendanalys (volym, momentum, volatilitet)
- Dynamisk prenumeration på toppsymboler
"""

import logging
import random
from typing import List, Dict, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class DataStream:
    """
    DataStream hanterar realtidsdata och trendanalys för marknadsdata.
    
    Attributes:
        api_key (str): API-nyckel för Finnhub
        symbols (List[str]): Lista över symboler att övervaka
        websocket_url (str): URL för WebSocket-anslutning
        rest_url (str): URL för REST API
    """
    
    def __init__(self, api_key: str, symbols: Optional[List[str]] = None, use_mock_data: bool = False):
        """
        Initierar DataStream med API-nyckel och valfria symboler.
        
        Args:
            api_key: API-nyckel för Finnhub
            symbols: Lista över symboler att övervaka (valfritt)
            use_mock_data: Om True, använd mockdata istället för riktig API
        """
        self.api_key = api_key
        self.symbols = symbols or []
        self.websocket_url = "wss://ws.finnhub.io"
        self.rest_url = "https://finnhub.io/api/v1"
        self.is_connected = False
        self.use_mock_data = use_mock_data
        self.market_data_cache: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"DataStream initialiserad med {len(self.symbols)} symboler (mock_data={use_mock_data})")
    
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
            # TODO: Implementera riktig WebSocket-anslutning
            self.is_connected = False
            logger.warning("Riktig WebSocket-anslutning ej implementerad")
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
            Dict med marknadsdata per symbol
        """
        target_symbols = symbols or self.symbols
        logger.info(f"Hämtar marknadsdata för {len(target_symbols)} symboler via REST")
        
        if self.use_mock_data:
            # Generera mockdata för varje symbol
            mock_data = {}
            for symbol in target_symbols:
                mock_data[symbol] = {
                    'price': round(random.uniform(50, 500), 2),
                    'volume': random.randint(1000000, 50000000),
                    'change': round(random.uniform(-5, 5), 2),
                    'change_percent': round(random.uniform(-5, 5), 2),
                    'timestamp': datetime.now().isoformat()
                }
                self.market_data_cache[symbol] = mock_data[symbol]
            logger.info(f"Genererade mockdata för {len(target_symbols)} symboler")
            return mock_data
        else:
            # TODO: Implementera REST-hämtning
            logger.warning("Riktig REST-hämtning ej implementerad")
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
            # Generera mockdata för trendanalys
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
            # TODO: Implementera riktig trendanalys
            logger.warning("Riktig trendanalys ej implementerad")
            return {
                'volume': 0.0,
                'momentum': 0.0,
                'volatility': 0.0,
                'score': 0.0
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
