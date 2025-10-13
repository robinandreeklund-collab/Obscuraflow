"""
REST Batcher - Hanterar REST API-anrop i batcher för att undvika rate limits

Denna modul:
- Delar upp symboler i små batcher (6 batcher × 10 symboler)
- Kör varje batch var 10:e sekund → ≈60 calls/min
- Pushar data till trending_pool för analys
- Respekterar Finnhub API:s rate limits (60 calls/minut)
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class RestBatcher:
    """
    Hanterar REST API-anrop i batcher för att respektera rate limits.
    
    Attributes:
        api_key: Finnhub API-nyckel
        symbols: Lista över symboler att övervaka
        batch_size: Antal symboler per batch (default 10)
        batch_interval: Sekunder mellan batcher (default 10)
        max_calls_per_minute: Max antal API-calls per minut (default 60)
    """
    
    def __init__(
        self,
        api_key: str,
        symbols: List[str],
        batch_size: int = 10,
        batch_interval: float = 10.0,
        max_calls_per_minute: int = 60
    ):
        """
        Initierar REST Batcher.
        
        Args:
            api_key: Finnhub API-nyckel
            symbols: Lista över symboler att övervaka
            batch_size: Antal symboler per batch
            batch_interval: Sekunder mellan batcher
            max_calls_per_minute: Max antal API-calls per minut
        """
        self.api_key = api_key
        self.symbols = symbols
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self.max_calls_per_minute = max_calls_per_minute
        
        # Skapa batcher
        self.batches = self._create_batches()
        self.current_batch_index = 0
        
        # Rate limiting tracking
        self.call_timestamps = deque(maxlen=max_calls_per_minute)
        
        # Senaste snapshot-data per symbol
        self.snapshot_cache: Dict[str, Dict[str, Any]] = {}
        
        # Statistik
        self.stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'rate_limited_calls': 0,
            'last_batch_time': None,
            'last_successful_symbol': None
        }
        
        logger.info(f"RestBatcher initialiserad: {len(self.batches)} batcher, "
                   f"{self.batch_size} symboler/batch, {self.batch_interval}s intervall")
    
    def _create_batches(self) -> List[List[str]]:
        """
        Delar upp symboler i batcher.
        
        Returns:
            Lista av batcher (varje batch är en lista av symboler)
        """
        batches = []
        for i in range(0, len(self.symbols), self.batch_size):
            batch = self.symbols[i:i + self.batch_size]
            batches.append(batch)
        return batches
    
    def _check_rate_limit(self) -> bool:
        """
        Kollar om vi kan göra ett API-anrop utan att överskrida rate limit.
        
        Returns:
            True om vi kan göra anropet, False annars
        """
        now = time.time()
        
        # Ta bort gamla timestamps (äldre än 1 minut)
        while self.call_timestamps and now - self.call_timestamps[0] > 60:
            self.call_timestamps.popleft()
        
        # Kolla om vi har utrymme för fler anrop
        return len(self.call_timestamps) < self.max_calls_per_minute
    
    def _record_api_call(self):
        """Registrera ett API-anrop för rate limiting."""
        self.call_timestamps.append(time.time())
        self.stats['total_calls'] += 1
    
    async def fetch_batch(self, batch: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Hämtar marknadsdata för en batch av symboler.
        
        Args:
            batch: Lista av symboler att hämta
        
        Returns:
            Dict med marknadsdata per symbol
        """
        try:
            # Importera FinnhubClient här för att undvika cirkulära beroenden
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            dash_app_path = os.path.join(project_root, 'dash_app')
            if dash_app_path not in sys.path:
                sys.path.insert(0, dash_app_path)
            
            from dash_app.utils.finnhub_client import FinnhubClient
            
            client = FinnhubClient(self.api_key)
            batch_data = {}
            
            for symbol in batch:
                # Kolla rate limit innan varje anrop
                if not self._check_rate_limit():
                    logger.warning(f"Rate limit nådd, pausar hämtning för {symbol}")
                    self.stats['rate_limited_calls'] += 1
                    await asyncio.sleep(1.0)  # Vänta lite innan nästa försök
                    continue
                
                self._record_api_call()
                
                # Hämta quote
                quote = client.get_quote(symbol)
                
                # Check if we got a rate limit error from the API
                if quote and quote.get('error') == 'rate_limit':
                    logger.warning(f"API rate limit hit for {symbol}, backing off")
                    self.stats['rate_limited_calls'] += 1
                    self.stats['failed_calls'] += 1
                    # Back off for a bit
                    await asyncio.sleep(2.0)
                    continue
                
                if quote and quote.get('c', 0) > 0:
                    batch_data[symbol] = quote
                    self.snapshot_cache[symbol] = {
                        **quote,
                        'timestamp': datetime.now(),
                        'symbol': symbol
                    }
                    self.stats['successful_calls'] += 1
                    self.stats['last_successful_symbol'] = symbol
                else:
                    logger.debug(f"Ingen giltig data för {symbol}")
                    self.stats['failed_calls'] += 1
                
                # Liten paus mellan symboler för att sprida ut anropen
                # 1 second per call to stay within 60 calls/minute limit
                await asyncio.sleep(1.0)
            
            self.stats['last_batch_time'] = datetime.now()
            logger.info(f"Hämtade batch: {len(batch_data)}/{len(batch)} symboler lyckades")
            
            return batch_data
            
        except Exception as e:
            logger.error(f"Fel vid hämtning av batch: {e}")
            self.stats['failed_calls'] += len(batch)
            return {}
    
    async def run_next_batch(self) -> Dict[str, Dict[str, Any]]:
        """
        Kör nästa batch i rotation.
        
        Returns:
            Dict med marknadsdata för batchen
        """
        if not self.batches:
            logger.warning("Inga batcher att köra")
            return {}
        
        # Hämta nästa batch
        batch = self.batches[self.current_batch_index]
        logger.debug(f"Kör batch {self.current_batch_index + 1}/{len(self.batches)}: {batch}")
        
        # Hämta data
        batch_data = await self.fetch_batch(batch)
        
        # Gå till nästa batch (rotera)
        self.current_batch_index = (self.current_batch_index + 1) % len(self.batches)
        
        return batch_data
    
    async def start_batch_loop(self, trending_pool=None):
        """
        Startar en kontinuerlig loop som kör batcher med intervall.
        
        Args:
            trending_pool: TrendingPool-instans att uppdatera (optional)
        """
        logger.info("Startar REST batch-loop...")
        
        while True:
            try:
                # Kör nästa batch
                batch_data = await self.run_next_batch()
                
                # Uppdatera trending_pool om tillgänglig
                if trending_pool and batch_data:
                    for symbol, data in batch_data.items():
                        # Beräkna trend_data från quote
                        trend_data = {
                            'volume': data.get('v', 0) / 1000000,  # Volym i miljoner
                            'momentum': data.get('dp', 0),  # Prisförändring i %
                            'volatility': abs(data.get('dp', 0)),
                            'score': 0  # Kommer beräknas av trending_pool
                        }
                        trending_pool.update_symbol(symbol, trend_data)
                
                # Vänta till nästa batch
                await asyncio.sleep(self.batch_interval)
                
            except Exception as e:
                logger.error(f"Fel i batch-loop: {e}")
                await asyncio.sleep(self.batch_interval)
    
    def get_latest_snapshot(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar senaste snapshot för en symbol från cache.
        
        Args:
            symbol: Symbol att hämta
        
        Returns:
            Snapshot-data eller None
        """
        return self.snapshot_cache.get(symbol)
    
    def get_all_snapshots(self) -> Dict[str, Dict[str, Any]]:
        """
        Hämtar alla senaste snapshots från cache.
        
        Returns:
            Dict med alla snapshot-data
        """
        return self.snapshot_cache.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik om batch-körningar.
        
        Returns:
            Dict med statistik
        """
        success_rate = (
            self.stats['successful_calls'] / self.stats['total_calls'] * 100
            if self.stats['total_calls'] > 0 else 0
        )
        
        return {
            **self.stats,
            'success_rate': round(success_rate, 1),
            'batches_count': len(self.batches),
            'symbols_per_batch': self.batch_size,
            'batch_interval': self.batch_interval,
            'cache_size': len(self.snapshot_cache)
        }
