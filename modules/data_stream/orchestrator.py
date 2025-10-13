"""
Data Orchestrator - Koordinerar REST-batching och WebSocket-subscriptions

Denna modul:
- Startar och hanterar REST batcher för snapshot-data
- Startar och hanterar WebSocket för tick-data
- Koordinerar rotation av WebSocket-subscriptions baserat på top-symboler
- Uppdaterar trending_pool med kombinerad data
- Tillhandahåller unified interface för att hämta marknadsdata
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from modules.data_stream.rest_batcher import RestBatcher
from modules.data_stream.ws_handler import WebSocketHandler
from modules.trending_pool.trending_pool import TrendingPool

logger = logging.getLogger(__name__)


class DataOrchestrator:
    """
    Koordinerar data-hämtning från REST och WebSocket.
    
    Attributes:
        api_key: Finnhub API-nyckel
        symbols: Lista över symboler att övervaka
        use_mock_data: Om True, använd mock data istället för API
        trending_pool: TrendingPool-instans
        rest_batcher: RestBatcher-instans
        ws_handler: WebSocketHandler-instans
    """
    
    def __init__(
        self,
        api_key: str,
        symbols: List[str],
        use_mock_data: bool = False,
        batch_size: int = 10,
        batch_interval: float = 10.0,
        max_ws_subscriptions: int = 50,
        ws_rotation_interval: float = 12.0
    ):
        """
        Initierar Data Orchestrator.
        
        Args:
            api_key: Finnhub API-nyckel
            symbols: Lista över symboler att övervaka
            use_mock_data: Om True, använd mock data
            batch_size: Antal symboler per REST batch
            batch_interval: Sekunder mellan REST batcher
            max_ws_subscriptions: Max antal WebSocket subscriptions
            ws_rotation_interval: Sekunder mellan WS rotationer
        """
        self.api_key = api_key
        self.symbols = symbols
        self.use_mock_data = use_mock_data
        
        # Initiera komponenter
        self.trending_pool = TrendingPool(
            max_history=100,
            dampening_factor=0.3
        )
        
        if not use_mock_data:
            self.rest_batcher = RestBatcher(
                api_key=api_key,
                symbols=symbols,
                batch_size=batch_size,
                batch_interval=batch_interval
            )
            
            self.ws_handler = WebSocketHandler(
                api_key=api_key,
                max_subscriptions=max_ws_subscriptions,
                rotation_interval=ws_rotation_interval
            )
        else:
            self.rest_batcher = None
            self.ws_handler = None
            logger.info("DataOrchestrator körs i mock-läge")
        
        # Tasks för async loops
        self.rest_task = None
        self.ws_listen_task = None
        self.ws_rotation_task = None
        
        # Statistik
        self.stats = {
            'start_time': datetime.now(),
            'total_symbols': len(symbols),
            'mode': 'mock' if use_mock_data else 'live'
        }
        
        logger.info(f"DataOrchestrator initialiserad: {len(symbols)} symboler, "
                   f"mode={self.stats['mode']}")
    
    async def start(self):
        """Startar alla data-insamlingsprocesser."""
        if self.use_mock_data:
            logger.info("Mock-läge aktivt, ingen data-insamling startas")
            return
        
        logger.info("Startar DataOrchestrator...")
        
        try:
            # Starta REST batch-loop
            self.rest_task = asyncio.create_task(
                self.rest_batcher.start_batch_loop(self.trending_pool)
            )
            logger.info("REST batch-loop startad")
            
            # Anslut WebSocket
            await self.ws_handler.connect()
            
            # Starta WebSocket tick-lyssnare
            self.ws_listen_task = asyncio.create_task(
                self.ws_handler.listen_for_ticks(self.trending_pool)
            )
            logger.info("WebSocket tick-lyssnare startad")
            
            # Starta WebSocket rotation-loop
            self.ws_rotation_task = asyncio.create_task(
                self._ws_rotation_loop()
            )
            logger.info("WebSocket rotation-loop startad")
            
            logger.info("DataOrchestrator fullständigt startad")
            
        except Exception as e:
            logger.error(f"Fel vid start av DataOrchestrator: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Stoppar alla data-insamlingsprocesser."""
        logger.info("Stoppar DataOrchestrator...")
        
        # Avbryt tasks
        if self.rest_task:
            self.rest_task.cancel()
        if self.ws_listen_task:
            self.ws_listen_task.cancel()
        if self.ws_rotation_task:
            self.ws_rotation_task.cancel()
        
        # Stäng WebSocket
        if self.ws_handler and self.ws_handler.is_connected:
            await self.ws_handler.disconnect()
        
        logger.info("DataOrchestrator stoppad")
    
    async def _ws_rotation_loop(self):
        """Loop som roterar WebSocket-subscriptions baserat på top-symboler."""
        while True:
            try:
                # Hämta top-symboler från trending_pool
                top_symbols = self.trending_pool.get_top_symbols(
                    count=self.ws_handler.max_subscriptions
                )
                
                # Rotera subscriptions
                await self.ws_handler.rotate_subscriptions(top_symbols)
                
                # Vänta till nästa rotation
                await asyncio.sleep(self.ws_handler.rotation_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Fel i WS rotation-loop: {e}")
                await asyncio.sleep(self.ws_handler.rotation_interval)
    
    def get_top_symbols(self, count: int = 50) -> List[str]:
        """
        Hämtar top-symboler från trending_pool.
        
        Args:
            count: Antal top-symboler att returnera
        
        Returns:
            Lista av top-symboler
        """
        return self.trending_pool.get_top_symbols(count=count)
    
    def get_market_summary(self) -> Dict[str, Any]:
        """
        Hämtar marknadsöversikt med senaste data.
        
        Returns:
            Dict med marknadsmetrics och quotes
        """
        if self.use_mock_data:
            # Returnera mock data
            from modules.data_stream.data_stream import get_data_stream
            from dash_app.config import USE_MOCK_DATA
            data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
            return data_stream.get_market_summary()
        
        # Hämta senaste snapshots från REST batcher
        snapshots = self.rest_batcher.get_all_snapshots()
        
        # Beräkna aggregerade metrics
        total_symbols = len(snapshots)
        gainers = sum(1 for q in snapshots.values() if q.get('dp', 0) > 0)
        losers = sum(1 for q in snapshots.values() if q.get('dp', 0) < 0)
        avg_change = sum(q.get('dp', 0) for q in snapshots.values()) / total_symbols if total_symbols > 0 else 0
        
        return {
            'total_symbols': total_symbols,
            'gainers': gainers,
            'losers': losers,
            'unchanged': total_symbols - gainers - losers,
            'avg_change_percent': round(avg_change, 2),
            'quotes': snapshots,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_symbol_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar senaste data för en specifik symbol.
        
        Args:
            symbol: Symbol att hämta
        
        Returns:
            Dict med symbol-data eller None
        """
        if self.use_mock_data:
            market_summary = self.get_market_summary()
            return market_summary['quotes'].get(symbol)
        
        # Hämta från REST snapshot
        snapshot = self.rest_batcher.get_latest_snapshot(symbol)
        
        # Kombinera med tick-data om tillgänglig
        if self.ws_handler:
            recent_ticks = self.ws_handler.get_recent_ticks(symbol, count=1)
            if recent_ticks:
                # Använd senaste tick price
                snapshot = snapshot.copy() if snapshot else {}
                snapshot['c'] = recent_ticks[-1]['price']
                snapshot['tick_timestamp'] = recent_ticks[-1]['timestamp'].isoformat()
        
        return snapshot
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik från alla komponenter.
        
        Returns:
            Dict med statistik
        """
        stats = {
            **self.stats,
            'uptime': (datetime.now() - self.stats['start_time']).total_seconds(),
            'trending_pool': self.trending_pool.get_stats() if self.trending_pool else {}
        }
        
        if not self.use_mock_data:
            stats['rest_batcher'] = self.rest_batcher.get_stats() if self.rest_batcher else {}
            stats['ws_handler'] = self.ws_handler.get_stats() if self.ws_handler else {}
        
        return stats
