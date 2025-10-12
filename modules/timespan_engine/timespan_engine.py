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
        if timeframe not in self.timeframes:
            logger.error(f"Okänd tidsram: {timeframe}")
            return {
                'timeframe': timeframe,
                'success': False,
                'error': 'Unknown timeframe'
            }
        
        logger.info(f"Tränar RL-modell för tidsram {timeframe} ({episodes} episoder)")
        
        # Simulera träningsprocess
        import random
        training_metrics = {
            'episodes_completed': episodes,
            'average_reward': random.uniform(0.5, 0.9),
            'final_loss': random.uniform(0.01, 0.1),
            'convergence': random.random() > 0.3
        }
        
        # Spara modell (simulerad)
        self.rl_models[timeframe] = {
            'trained': True,
            'episodes': episodes,
            'metrics': training_metrics,
            'timestamp': datetime.now().isoformat()
        }
        
        result = {
            'timeframe': timeframe,
            'episodes': episodes,
            'trained': True,
            'metrics': training_metrics,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(
            f"RL-träning klar för {timeframe}: "
            f"avg_reward={training_metrics['average_reward']:.3f}, "
            f"converged={training_metrics['convergence']}"
        )
        
        return result
    
    def sync_timeframes(self, symbol: str) -> Dict[str, Any]:
        """
        Synkroniserar data över alla tidsramar för en symbol.
        
        Args:
            symbol: Symbolnamn
        
        Returns:
            Dict med synkroniserad data
        """
        synced_data = {}
        missing_timeframes = []
        
        for tf in self.timeframes:
            data = self.get_data(tf, symbol)
            if data:
                synced_data[tf] = data
            else:
                missing_timeframes.append(tf)
        
        # Beräkna alignment score (hur många tidsramar har data)
        alignment_score = len(synced_data) / len(self.timeframes)
        
        result = {
            'symbol': symbol,
            'synced_timeframes': list(synced_data.keys()),
            'missing_timeframes': missing_timeframes,
            'alignment_score': alignment_score,
            'data': synced_data,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(
            f"Synkroniserade {symbol}: {len(synced_data)}/{len(self.timeframes)} "
            f"tidsramar, alignment={alignment_score:.2%}"
        )
        
        return result
    
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
