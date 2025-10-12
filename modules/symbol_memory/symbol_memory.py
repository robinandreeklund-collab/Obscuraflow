"""
SymbolMemory - Huvudklass för symbolspecifik historik

Denna klass ansvarar för:
- Lagring av symbolspecifik historik
- Pattern recognition per symbol
- Beteendeanalys
- Long-term memory
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import deque


logger = logging.getLogger(__name__)


class SymbolMemory:
    """
    SymbolMemory hanterar historik och minne för varje symbol.
    
    Attributes:
        max_history_size (int): Max antal poster att lagra per symbol
        memory (Dict): Minneslager för symboler
    """
    
    def __init__(self, max_history_size: int = 1000):
        """
        Initierar SymbolMemory.
        
        Args:
            max_history_size: Max antal historikposter per symbol
        """
        self.max_history_size = max_history_size
        self.memory: Dict[str, deque] = {}
        self.patterns: Dict[str, List[Dict[str, Any]]] = {}
        logger.info(f"SymbolMemory initierad med max_history_size={max_history_size}")
    
    def add_event(self, symbol: str, event: Dict[str, Any]) -> bool:
        """
        Lägger till en händelse för en symbol.
        
        Args:
            symbol: Symbolnamn
            event: Händelsedata
        
        Returns:
            True om händelsen lades till
        """
        if symbol not in self.memory:
            self.memory[symbol] = deque(maxlen=self.max_history_size)
        
        event['timestamp'] = datetime.now().isoformat()
        self.memory[symbol].append(event)
        logger.debug(f"Lade till händelse för {symbol}")
        return True
    
    def get_history(self, symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Hämtar historik för en symbol.
        
        Args:
            symbol: Symbolnamn
            limit: Max antal poster att returnera
        
        Returns:
            Lista med historik
        """
        if symbol not in self.memory:
            return []
        
        history = list(self.memory[symbol])
        if limit:
            return history[-limit:]
        return history
    
    def identify_patterns(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Identifierar mönster för en symbol.
        
        Args:
            symbol: Symbolnamn
        
        Returns:
            Lista med identifierade mönster
        """
        if symbol not in self.memory or len(self.memory[symbol]) < 5:
            # Inte tillräckligt med data för pattern recognition
            return []
        
        if symbol not in self.patterns:
            self.patterns[symbol] = []
        
        history = list(self.memory[symbol])
        detected_patterns = []
        
        # Pattern 1: Volatilitetsspike
        if len(history) >= 10:
            recent_volatility = [e.get('volatility', 0) for e in history[-10:] 
                               if 'volatility' in e]
            if recent_volatility:
                avg_vol = sum(recent_volatility) / len(recent_volatility)
                if recent_volatility[-1] > avg_vol * 1.5:
                    detected_patterns.append({
                        'type': 'volatility_spike',
                        'description': 'Ökad volatilitet detekterad',
                        'value': recent_volatility[-1],
                        'average': avg_vol,
                        'timestamp': datetime.now().isoformat()
                    })
        
        # Pattern 2: Trendomvändning
        prices = [e.get('price', 0) for e in history[-5:] if 'price' in e]
        if len(prices) >= 5:
            # Kolla om trend vänder
            first_half_trend = prices[2] - prices[0]
            second_half_trend = prices[4] - prices[2]
            
            if first_half_trend > 0 and second_half_trend < 0:
                detected_patterns.append({
                    'type': 'trend_reversal_down',
                    'description': 'Uppåtgående trend vänder nedåt',
                    'timestamp': datetime.now().isoformat()
                })
            elif first_half_trend < 0 and second_half_trend > 0:
                detected_patterns.append({
                    'type': 'trend_reversal_up',
                    'description': 'Nedåtgående trend vänder uppåt',
                    'timestamp': datetime.now().isoformat()
                })
        
        # Pattern 3: Volymspike
        volumes = [e.get('volume', 0) for e in history[-10:] if 'volume' in e]
        if volumes and len(volumes) >= 5:
            avg_volume = sum(volumes[:-1]) / len(volumes[:-1])
            if volumes[-1] > avg_volume * 2:
                detected_patterns.append({
                    'type': 'volume_spike',
                    'description': 'Ovanligt hög volym',
                    'value': volumes[-1],
                    'average': avg_volume,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Lägg till nya mönster i patterns
        self.patterns[symbol].extend(detected_patterns)
        
        # Begränsa antal sparade mönster per symbol
        if len(self.patterns[symbol]) > 50:
            self.patterns[symbol] = self.patterns[symbol][-50:]
        
        if detected_patterns:
            logger.info(f"Identifierade {len(detected_patterns)} mönster för {symbol}")
        
        return detected_patterns
    
    def get_symbol_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Hämtar profil för en symbol baserat på historik.
        
        Args:
            symbol: Symbolnamn
        
        Returns:
            Dict med symbolprofil
        """
        history = self.get_history(symbol)
        
        if not history:
            return {
                'symbol': symbol,
                'total_events': 0,
                'patterns': 0,
                'profile': 'unknown'
            }
        
        # Beräkna profilstatistik
        prices = [e.get('price', 0) for e in history if 'price' in e]
        volumes = [e.get('volume', 0) for e in history if 'volume' in e]
        
        profile = {
            'symbol': symbol,
            'total_events': len(history),
            'patterns': len(self.patterns.get(symbol, [])),
            'first_seen': history[0].get('timestamp'),
            'last_seen': history[-1].get('timestamp')
        }
        
        # Statistik om priser
        if prices:
            profile['price_stats'] = {
                'min': min(prices),
                'max': max(prices),
                'avg': sum(prices) / len(prices),
                'latest': prices[-1]
            }
            
            # Beräkna volatilitet (standardavvikelse)
            avg_price = profile['price_stats']['avg']
            variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
            profile['price_stats']['volatility'] = variance ** 0.5
        
        # Statistik om volym
        if volumes:
            profile['volume_stats'] = {
                'min': min(volumes),
                'max': max(volumes),
                'avg': sum(volumes) / len(volumes),
                'latest': volumes[-1]
            }
        
        # Klassificera symbol baserat på beteende
        if prices and len(prices) >= 5:
            price_change = (prices[-1] - prices[0]) / prices[0] if prices[0] > 0 else 0
            if price_change > 0.1:
                profile['trend'] = 'bullish'
            elif price_change < -0.1:
                profile['trend'] = 'bearish'
            else:
                profile['trend'] = 'neutral'
        
        return profile
    
    def clear_history(self, symbol: Optional[str] = None) -> int:
        """
        Rensar historik.
        
        Args:
            symbol: Specifik symbol eller None för alla
        
        Returns:
            Antal poster som rensades
        """
        if symbol:
            if symbol in self.memory:
                count = len(self.memory[symbol])
                del self.memory[symbol]
                if symbol in self.patterns:
                    del self.patterns[symbol]
                logger.info(f"Rensade historik för {symbol}")
                return count
            return 0
        else:
            total = sum(len(m) for m in self.memory.values())
            self.memory.clear()
            self.patterns.clear()
            logger.info(f"Rensade all historik ({total} poster)")
            return total
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för symbol memory.
        
        Returns:
            Dict med statistik
        """
        return {
            'tracked_symbols': len(self.memory),
            'total_events': sum(len(m) for m in self.memory.values()),
            'total_patterns': sum(len(p) for p in self.patterns.values()),
            'max_history_size': self.max_history_size
        }
