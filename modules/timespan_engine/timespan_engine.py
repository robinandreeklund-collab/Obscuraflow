"""
TimespanEngine - Huvudklass för tidsramar och RL-träning

Denna klass ansvarar för:
- Hantering av olika tidsramar
- RL-träning per tidsram
- Tidsramspecifika strategier
- Datasynkronisering över tidsramar
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class TimespanEngine:
    """
    TimespanEngine hanterar olika tidsramar och RL-träning.
    
    Attributes:
        timeframes (List[str]): Lista över aktiva tidsramar
        primary_timeframe (str): Primär tidsram för beslut
    """
    
    def __init__(self, timeframes: Optional[List[str]] = None, primary_timeframe: str = '15m'):
        """
        Initierar TimespanEngine med tidsramar.
        
        Args:
            timeframes: Lista över tidsramar att hantera
            primary_timeframe: Primär tidsram för beslut
        """
        self.timeframes = timeframes or ['1m', '5m', '15m', '1h', '4h', '1d']
        self.primary_timeframe = primary_timeframe
        self.timeframe_data: Dict[str, Dict[str, Any]] = {}
        self.rl_models: Dict[str, Any] = {}
        logger.info(f"TimespanEngine initierad med tidsramar: {self.timeframes}")
    
    def add_data(self, timeframe: str, symbol: str, data: Dict[str, Any]) -> bool:
        """
        Lägger till data för en specifik tidsram och symbol.
        
        Args:
            timeframe: Tidsram (t.ex. '15m')
            symbol: Symbolnamn
            data: Marknadsdata
        
        Returns:
            True om data lades till
        """
        if timeframe not in self.timeframes:
            logger.warning(f"Okänd tidsram: {timeframe}")
            return False
        
        if timeframe not in self.timeframe_data:
            self.timeframe_data[timeframe] = {}
        
        self.timeframe_data[timeframe][symbol] = data
        logger.debug(f"Lade till data för {symbol} i tidsram {timeframe}")
        return True
    
    def get_data(self, timeframe: str, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar data för specifik tidsram och symbol.
        
        Args:
            timeframe: Tidsram
            symbol: Symbolnamn
        
        Returns:
            Data eller None
        """
        if timeframe in self.timeframe_data:
            return self.timeframe_data[timeframe].get(symbol)
        return None
    
    def train_rl_model(self, timeframe: str, episodes: int = 100) -> Dict[str, Any]:
        """
        Tränar RL-modell för specifik tidsram.
        
        Args:
            timeframe: Tidsram att träna för
            episodes: Antal träningsepisoder
        
        Returns:
            Dict med träningsresultat
        """
        # Kodstub - implementeras senare med faktisk RL-träning
        logger.info(f"Tränar RL-modell för tidsram {timeframe}")
        return {
            'timeframe': timeframe,
            'episodes': episodes,
            'trained': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def sync_timeframes(self, symbol: str) -> Dict[str, Any]:
        """
        Synkroniserar data över alla tidsramar för en symbol.
        
        Args:
            symbol: Symbolnamn
        
        Returns:
            Dict med synkroniserad data
        """
        # Kodstub
        return {
            'symbol': symbol,
            'synced_timeframes': self.timeframes,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för timespan engine.
        
        Returns:
            Dict med statistik
        """
        return {
            'active_timeframes': len(self.timeframes),
            'primary_timeframe': self.primary_timeframe,
            'total_data_points': sum(len(v) for v in self.timeframe_data.values()),
            'rl_models_trained': len(self.rl_models)
        }
