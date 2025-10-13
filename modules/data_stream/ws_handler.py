"""
WebSocket Handler - Hanterar WebSocket-subscriptions för top-symboler

Denna modul:
- Initierar WebSocket endast för top-symboler från trending_pool
- Begränsar till max 50 aktiva subscriptions samtidigt
- Roterar sub-listan baserat på trend_score var 10-15 sekunder
- Avsubscriberar inaktiva symboler, subscribar nya top-symboler
- Streamar tickdata till trending_pool
"""

import asyncio
import logging
import json
import websockets
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class WebSocketHandler:
    """
    Hanterar WebSocket-anslutningar och subscriptions för realtidsdata.
    
    Attributes:
        api_key: Finnhub API-nyckel
        ws_url: WebSocket URL
        max_subscriptions: Max antal samtidiga subscriptions (default 50)
        rotation_interval: Sekunder mellan subscription-rotationer (default 12)
    """
    
    def __init__(
        self,
        api_key: str,
        ws_url: str = "wss://ws.finnhub.io",
        max_subscriptions: int = 50,
        rotation_interval: float = 12.0
    ):
        """
        Initierar WebSocket Handler.
        
        Args:
            api_key: Finnhub API-nyckel
            ws_url: WebSocket URL
            max_subscriptions: Max antal samtidiga subscriptions
            rotation_interval: Sekunder mellan rotationer
        """
        self.api_key = api_key
        self.ws_url = ws_url
        self.max_subscriptions = max_subscriptions
        self.rotation_interval = rotation_interval
        
        # WebSocket connection
        self.websocket = None
        self.is_connected = False
        
        # Aktiva subscriptions
        self.active_subscriptions: Set[str] = set()
        
        # Tick-data cache (senaste 30 sekunder per symbol)
        self.tick_cache: Dict[str, deque] = {}
        self.tick_cache_duration = 30  # sekunder
        
        # Statistik
        self.stats = {
            'total_ticks': 0,
            'ticks_per_symbol': {},
            'subscriptions_added': 0,
            'subscriptions_removed': 0,
            'connection_errors': 0,
            'last_tick_time': None,
            'last_rotation_time': None
        }
        
        logger.info(f"WebSocketHandler initialiserad: max {max_subscriptions} subs, "
                   f"{rotation_interval}s rotation")
    
    async def connect(self):
        """Upprättar WebSocket-anslutning till Finnhub."""
        try:
            url = f"{self.ws_url}?token={self.api_key}"
            self.websocket = await websockets.connect(url)
            self.is_connected = True
            logger.info("WebSocket-anslutning etablerad")
        except Exception as e:
            logger.error(f"Fel vid WebSocket-anslutning: {e}")
            self.is_connected = False
            self.stats['connection_errors'] += 1
            raise
    
    async def disconnect(self):
        """Stänger WebSocket-anslutningen."""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            logger.info("WebSocket-anslutning stängd")
    
    async def subscribe(self, symbol: str):
        """
        Subscribar på en symbol.
        
        Args:
            symbol: Symbol att subscriba på
        """
        if not self.is_connected or not self.websocket:
            logger.warning(f"Kan inte subscriba på {symbol}, inte ansluten")
            return
        
        if symbol in self.active_subscriptions:
            logger.debug(f"Redan subscriberad på {symbol}")
            return
        
        if len(self.active_subscriptions) >= self.max_subscriptions:
            logger.warning(f"Max subscriptions ({self.max_subscriptions}) nått, kan inte subscriba {symbol}")
            return
        
        try:
            # Skicka subscribe-meddelande
            subscribe_msg = {"type": "subscribe", "symbol": symbol}
            await self.websocket.send(json.dumps(subscribe_msg))
            
            self.active_subscriptions.add(symbol)
            self.stats['subscriptions_added'] += 1
            
            # Initiera tick cache för symbolen
            if symbol not in self.tick_cache:
                self.tick_cache[symbol] = deque(maxlen=100)  # Max 100 senaste ticks
            
            logger.debug(f"Subscriberade på {symbol} ({len(self.active_subscriptions)}/{self.max_subscriptions})")
            
        except Exception as e:
            logger.error(f"Fel vid subscription på {symbol}: {e}")
    
    async def unsubscribe(self, symbol: str):
        """
        Avsubscriberar från en symbol.
        
        Args:
            symbol: Symbol att avsubscribera från
        """
        if not self.is_connected or not self.websocket:
            return
        
        if symbol not in self.active_subscriptions:
            return
        
        try:
            # Skicka unsubscribe-meddelande
            unsubscribe_msg = {"type": "unsubscribe", "symbol": symbol}
            await self.websocket.send(json.dumps(unsubscribe_msg))
            
            self.active_subscriptions.discard(symbol)
            self.stats['subscriptions_removed'] += 1
            
            logger.debug(f"Avsubscriberade från {symbol} ({len(self.active_subscriptions)}/{self.max_subscriptions})")
            
        except Exception as e:
            logger.error(f"Fel vid unsubscribe från {symbol}: {e}")
    
    async def rotate_subscriptions(self, top_symbols: List[str]):
        """
        Roterar subscriptions baserat på nya top-symboler.
        
        Args:
            top_symbols: Lista av top-symboler från trending_pool
        """
        if not self.is_connected:
            logger.debug("Inte ansluten, skippar rotation")
            return
        
        # Begränsa till max antal subscriptions
        target_symbols = set(top_symbols[:self.max_subscriptions])
        current_symbols = self.active_subscriptions.copy()
        
        # Symboler att ta bort (finns i current men inte i target)
        symbols_to_remove = current_symbols - target_symbols
        
        # Symboler att lägga till (finns i target men inte i current)
        symbols_to_add = target_symbols - current_symbols
        
        # Avsubscribera från gamla
        for symbol in symbols_to_remove:
            await self.unsubscribe(symbol)
        
        # Subscriba på nya
        for symbol in symbols_to_add:
            await self.subscribe(symbol)
        
        self.stats['last_rotation_time'] = datetime.now()
        
        logger.info(f"Subscription rotation: +{len(symbols_to_add)} -{len(symbols_to_remove)} "
                   f"(Total: {len(self.active_subscriptions)})")
    
    def _clean_old_ticks(self):
        """Tar bort gamla ticks från cache (äldre än tick_cache_duration)."""
        cutoff_time = datetime.now() - timedelta(seconds=self.tick_cache_duration)
        
        for symbol in list(self.tick_cache.keys()):
            # Filtrera bort gamla ticks
            self.tick_cache[symbol] = deque(
                [tick for tick in self.tick_cache[symbol] 
                 if tick.get('timestamp', datetime.min) > cutoff_time],
                maxlen=100
            )
    
    async def listen_for_ticks(self, trending_pool=None):
        """
        Lyssnar på tick-meddelanden från WebSocket.
        
        Args:
            trending_pool: TrendingPool-instans att uppdatera (optional)
        """
        if not self.is_connected or not self.websocket:
            logger.warning("Kan inte lyssna på ticks, inte ansluten")
            return
        
        logger.info("Börjar lyssna på WebSocket-ticks...")
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    
                    # Hantera olika meddelande-typer
                    if data.get('type') == 'trade':
                        # Trade tick
                        for trade in data.get('data', []):
                            symbol = trade.get('s')
                            price = trade.get('p')
                            volume = trade.get('v')
                            timestamp = datetime.fromtimestamp(trade.get('t', 0) / 1000)
                            
                            if symbol and price:
                                # Lägg till i cache
                                tick_data = {
                                    'symbol': symbol,
                                    'price': price,
                                    'volume': volume,
                                    'timestamp': timestamp
                                }
                                
                                if symbol not in self.tick_cache:
                                    self.tick_cache[symbol] = deque(maxlen=100)
                                
                                self.tick_cache[symbol].append(tick_data)
                                
                                # Uppdatera statistik
                                self.stats['total_ticks'] += 1
                                self.stats['ticks_per_symbol'][symbol] = \
                                    self.stats['ticks_per_symbol'].get(symbol, 0) + 1
                                self.stats['last_tick_time'] = datetime.now()
                                
                                # Uppdatera trending_pool om tillgänglig
                                if trending_pool:
                                    # Beräkna kort-term metrics från tick-data
                                    recent_ticks = list(self.tick_cache[symbol])[-10:]  # Senaste 10 ticks
                                    if len(recent_ticks) >= 2:
                                        price_change = (recent_ticks[-1]['price'] - recent_ticks[0]['price']) / recent_ticks[0]['price'] * 100
                                        avg_volume = sum(t['volume'] for t in recent_ticks) / len(recent_ticks)
                                        
                                        tick_trend = {
                                            'volume': avg_volume / 1000,  # Normalisera
                                            'momentum': price_change,
                                            'volatility': abs(price_change),
                                            'score': 0  # Kommer beräknas av trending_pool
                                        }
                                        trending_pool.update_symbol_tick(symbol, tick_trend)
                    
                    # Städa upp gamla ticks periodiskt
                    if self.stats['total_ticks'] % 100 == 0:
                        self._clean_old_ticks()
                    
                except json.JSONDecodeError:
                    logger.debug(f"Kunde inte parsa meddelande: {message}")
                except Exception as e:
                    logger.error(f"Fel vid hantering av tick: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket-anslutning stängd")
            self.is_connected = False
        except Exception as e:
            logger.error(f"Fel i tick-lyssnare: {e}")
            self.is_connected = False
    
    def get_recent_ticks(self, symbol: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Hämtar senaste ticks för en symbol.
        
        Args:
            symbol: Symbol att hämta ticks för
            count: Antal ticks att hämta
        
        Returns:
            Lista av tick-data
        """
        if symbol not in self.tick_cache:
            return []
        
        ticks = list(self.tick_cache[symbol])
        return ticks[-count:] if len(ticks) > count else ticks
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik om WebSocket-aktivitet.
        
        Returns:
            Dict med statistik
        """
        return {
            **self.stats,
            'is_connected': self.is_connected,
            'active_subscriptions': len(self.active_subscriptions),
            'active_symbols': list(self.active_subscriptions),
            'cache_symbols': len(self.tick_cache),
            'max_subscriptions': self.max_subscriptions
        }
