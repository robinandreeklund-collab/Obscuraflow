"""
TrendingPool - Market Heat Engine för symbolranking

Denna klass ansvarar för:
- Identifiering och rankning av aktiva symboler
- Stabilisering av trenddata
- Score-beräkning med viktning
- Historikcache och fluktuationsdämpning
"""

import logging
from typing import List, Dict, Optional, Any
from collections import deque
from datetime import datetime


logger = logging.getLogger(__name__)


class TrendingPool:
    """
    TrendingPool hanterar symbolranking och identifierar heta marknader.
    
    Attributes:
        max_history: Antal historiska datapoints att spara per symbol
        dampening_factor: Faktor för fluktuationsdämpning (0-1)
        weights: Viktning för olika metriker i score-beräkning
    """
    
    def __init__(
        self, 
        max_history: int = 100,
        dampening_factor: float = 0.3,
        weights: Optional[Dict[str, float]] = None
    ):
        """
        Initierar TrendingPool med konfigurerbara parametrar.
        
        Args:
            max_history: Max antal historiska datapoints per symbol
            dampening_factor: Dämpningsfaktor för fluktuationer (0-1)
            weights: Viktning för metriker {'volume': 0.4, 'momentum': 0.3, 'volatility': 0.3}
        """
        self.max_history = max_history
        self.dampening_factor = dampening_factor
        self.weights = weights or {
            'volume': 0.4,
            'momentum': 0.3,
            'volatility': 0.3
        }
        
        # Cache för symboldata
        self.symbol_history: Dict[str, deque] = {}
        self.symbol_scores: Dict[str, float] = {}
        self.symbol_metadata: Dict[str, Dict[str, Any]] = {}
        
        logger.info(
            f"TrendingPool initialiserad (history={max_history}, "
            f"dampening={dampening_factor}, weights={self.weights})"
        )
    
    def update_symbol(self, symbol: str, trend_data: Dict[str, float]) -> float:
        """
        Uppdaterar trenddata för en symbol och beräknar nytt score.
        
        Args:
            symbol: Tickersymbol
            trend_data: Dict med 'volume', 'momentum', 'volatility', 'score'
        
        Returns:
            Dämpat och stabiliserat score för symbolen
        """
        # Initiera historik om symbolen är ny
        if symbol not in self.symbol_history:
            self.symbol_history[symbol] = deque(maxlen=self.max_history)
            self.symbol_scores[symbol] = 0.0
            self.symbol_metadata[symbol] = {
                'first_seen': datetime.now().isoformat(),
                'update_count': 0,
                'batch_updates': 0,
                'tick_updates': 0,
                'last_batch_update': None,
                'last_tick_update': None
            }
        
        # Lägg till ny datapoint
        trend_data_copy = trend_data.copy()
        trend_data_copy['timestamp'] = datetime.now()
        trend_data_copy['source'] = 'batch'  # Markera som batch-data
        self.symbol_history[symbol].append(trend_data_copy)
        
        self.symbol_metadata[symbol]['update_count'] += 1
        self.symbol_metadata[symbol]['batch_updates'] += 1
        self.symbol_metadata[symbol]['last_update'] = datetime.now().isoformat()
        self.symbol_metadata[symbol]['last_batch_update'] = datetime.now().isoformat()
        
        # Beräkna score från trend_data om inte redan satt
        if 'score' not in trend_data or trend_data['score'] == 0:
            raw_score = self._calculate_trend_score(trend_data)
        else:
            raw_score = trend_data['score']
        
        # Hämta gammalt score
        old_score = self.symbol_scores[symbol]
        
        # Exponentiell utjämning för att dämpa fluktuationer
        dampened_score = (
            self.dampening_factor * raw_score + 
            (1 - self.dampening_factor) * old_score
        )
        
        self.symbol_scores[symbol] = dampened_score
        
        logger.debug(
            f"Symbol {symbol} uppdaterad (batch): "
            f"score={dampened_score:.2f} (raw={raw_score:.2f})"
        )
        
        return dampened_score
    
    def update_symbol_tick(self, symbol: str, tick_data: Dict[str, float]) -> float:
        """
        Uppdaterar symbol med tick-data från WebSocket.
        Används för högfrekventa uppdateringar med lägre vikt.
        
        Args:
            symbol: Tickersymbol
            tick_data: Dict med 'volume', 'momentum', 'volatility'
        
        Returns:
            Uppdaterat score för symbolen
        """
        # Initiera historik om symbolen är ny
        if symbol not in self.symbol_history:
            self.symbol_history[symbol] = deque(maxlen=self.max_history)
            self.symbol_scores[symbol] = 0.0
            self.symbol_metadata[symbol] = {
                'first_seen': datetime.now().isoformat(),
                'update_count': 0,
                'batch_updates': 0,
                'tick_updates': 0,
                'last_batch_update': None,
                'last_tick_update': None
            }
        
        # Lägg till tick-data med lägre vikt
        tick_data_copy = tick_data.copy()
        tick_data_copy['timestamp'] = datetime.now()
        tick_data_copy['source'] = 'tick'  # Markera som tick-data
        self.symbol_history[symbol].append(tick_data_copy)
        
        self.symbol_metadata[symbol]['update_count'] += 1
        self.symbol_metadata[symbol]['tick_updates'] += 1
        self.symbol_metadata[symbol]['last_update'] = datetime.now().isoformat()
        self.symbol_metadata[symbol]['last_tick_update'] = datetime.now().isoformat()
        
        # Beräkna score från tick_data med lägre vikt (30% av normal vikt)
        tick_score = self._calculate_trend_score(tick_data) * 0.3
        old_score = self.symbol_scores[symbol]
        
        # Mycket lätt utjämning för ticks (10% weight på nytt värde)
        dampened_score = 0.1 * tick_score + 0.9 * old_score
        
        self.symbol_scores[symbol] = dampened_score
        
        logger.debug(
            f"Symbol {symbol} uppdaterad (tick): "
            f"score={dampened_score:.2f} (tick={tick_score:.2f})"
        )
        
        return dampened_score
    
    def _calculate_trend_score(self, data: Dict[str, float]) -> float:
        """
        Beräknar trend score från metriker.
        
        Args:
            data: Dict med 'volume', 'momentum', 'volatility'
        
        Returns:
            Beräknat trend score
        """
        volume = data.get('volume', 0)
        momentum = abs(data.get('momentum', 0))  # Absolut momentum
        volatility = data.get('volatility', 0)
        
        # Viktad summa
        score = (
            self.weights['volume'] * min(volume, 100) +  # Cap volym vid 100
            self.weights['momentum'] * min(momentum, 10) +  # Cap momentum vid 10%
            self.weights['volatility'] * min(volatility, 10)  # Cap volatilitet vid 10%
        )
        
        return score
    
    def get_ranked_symbols(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Hämtar rankade symboler baserat på deras score.
        
        Args:
            limit: Max antal symboler att returnera (None = alla)
        
        Returns:
            Lista med dicts innehållande symbol, score och metadata
        """
        # Sortera symboler efter score
        ranked = sorted(
            self.symbol_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Begränsa resultat om limit anges
        if limit:
            ranked = ranked[:limit]
        
        # Bygg resultat med metadata
        result = []
        for symbol, score in ranked:
            metadata = self.symbol_metadata.get(symbol, {})
            history = list(self.symbol_history.get(symbol, []))
            
            result.append({
                'symbol': symbol,
                'score': round(score, 2),
                'update_count': metadata.get('update_count', 0),
                'first_seen': metadata.get('first_seen'),
                'last_update': metadata.get('last_update'),
                'history_length': len(history)
            })
        
        logger.info(f"Returnerar {len(result)} rankade symboler")
        return result
    
    def get_symbol_trend(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar trendinformation för en specifik symbol.
        
        Args:
            symbol: Tickersymbol
        
        Returns:
            Dict med score, metadata och historik, eller None om symbolen inte finns
        """
        if symbol not in self.symbol_scores:
            logger.warning(f"Symbol {symbol} finns inte i poolen")
            return None
        
        history = list(self.symbol_history[symbol])
        metadata = self.symbol_metadata[symbol]
        
        # Beräkna trendstatistik
        if history:
            latest = history[-1]
            avg_score = sum(h.get('score', 0) for h in history) / len(history)
            trend_direction = 'up' if len(history) >= 2 and history[-1].get('score', 0) > history[-2].get('score', 0) else 'down'
        else:
            latest = {}
            avg_score = 0
            trend_direction = 'neutral'
        
        return {
            'symbol': symbol,
            'current_score': self.symbol_scores[symbol],
            'average_score': round(avg_score, 2),
            'trend_direction': trend_direction,
            'latest_data': latest,
            'metadata': metadata,
            'history': history
        }
    
    def clear_symbol(self, symbol: str) -> bool:
        """
        Tar bort en symbol från poolen.
        
        Args:
            symbol: Tickersymbol att ta bort
        
        Returns:
            True om symbolen togs bort, False om den inte fanns
        """
        if symbol in self.symbol_scores:
            del self.symbol_scores[symbol]
            del self.symbol_history[symbol]
            del self.symbol_metadata[symbol]
            logger.info(f"Symbol {symbol} borttagen från poolen")
            return True
        return False
    
    def get_top_symbols(self, count: int = 50) -> List[str]:
        """
        Hämtar top N symboler baserat på score.
        
        Args:
            count: Antal top-symboler att returnera
        
        Returns:
            Lista med symboler sorterade efter score (högst först)
        """
        if not self.symbol_scores:
            return []
        
        # Sortera efter score (högst först)
        ranked = sorted(
            self.symbol_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Returnera top N symboler
        top_symbols = [symbol for symbol, score in ranked[:count]]
        
        logger.debug(f"Returnerar top {count} symboler: {top_symbols[:10]}...")
        return top_symbols
    
    def get_pool_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik om hela poolen.
        
        Returns:
            Dict med poolstatistik
        """
        if not self.symbol_scores:
            return {
                'total_symbols': 0,
                'average_score': 0,
                'top_symbol': None,
                'bottom_symbol': None
            }
        
        scores = list(self.symbol_scores.values())
        symbols = list(self.symbol_scores.keys())
        
        ranked = sorted(self.symbol_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_symbols': len(symbols),
            'average_score': round(sum(scores) / len(scores), 2),
            'max_score': round(max(scores), 2),
            'min_score': round(min(scores), 2),
            'top_symbol': {'symbol': ranked[0][0], 'score': round(ranked[0][1], 2)},
            'bottom_symbol': {'symbol': ranked[-1][0], 'score': round(ranked[-1][1], 2)}
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Alias för get_pool_stats() för kompatibilitet.
        
        Returns:
            Dict med poolstatistik
        """
        return self.get_pool_stats()
