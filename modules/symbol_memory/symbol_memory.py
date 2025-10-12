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
        # Kodstub - implementeras senare med faktisk pattern recognition
        if symbol not in self.patterns:
            self.patterns[symbol] = []
        
        return self.patterns[symbol]
    
    def get_symbol_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Hämtar profil för en symbol baserat på historik.
        
        Args:
            symbol: Symbolnamn
        
        Returns:
            Dict med symbolprofil
        """
        history = self.get_history(symbol)
        
        # Kodstub
        return {
            'symbol': symbol,
            'total_events': len(history),
            'patterns': len(self.patterns.get(symbol, [])),
            'first_seen': history[0]['timestamp'] if history else None,
            'last_seen': history[-1]['timestamp'] if history else None
        }
    
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
