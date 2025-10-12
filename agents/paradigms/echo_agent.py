"""
EchoAgent - Temporal/Reflective Dimension

Funktion: Mönsterreplikering baserat på historik
Kapacitet: 500 historiska mönster, 75% matchtröskel
Lärande: Förstärker mönster som tidigare varit framgångsrika
Kopplingar: symbol_memory, fusion, reflexion, genesis
"""

import logging
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class EchoAgent(BaseAgent):
    """
    EchoAgent identifierar och replikerar historiska mönster.
    
    Analyserar:
    - Historiska prismönster
    - Likheter med tidigare framgångsrika trades
    - Mönstermatchning med databas
    """
    
    def __init__(
        self, 
        agent_id: str = "echo_agent",
        pattern_capacity: int = 500,
        match_threshold: float = 0.75
    ):
        """
        Initierar EchoAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            pattern_capacity: Max antal mönster att lagra
            match_threshold: Tröskelvärde för mönstermatchning
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.6,
            parameters={
                'pattern_capacity': pattern_capacity,
                'match_threshold': match_threshold
            }
        )
        self.pattern_capacity = pattern_capacity
        self.match_threshold = match_threshold
        self.pattern_database: List[Dict[str, Any]] = []
    
    def store_pattern(self, pattern: Dict[str, Any], success: bool):
        """
        Lagrar ett mönster i databasen.
        
        Args:
            pattern: Mönsterdata
            success: Om mönstret var framgångsrikt
        """
        pattern['success'] = success
        self.pattern_database.append(pattern)
        
        # Begränsa storleken
        if len(self.pattern_database) > self.pattern_capacity:
            # Behåll de mest framgångsrika mönstren
            self.pattern_database.sort(key=lambda x: x.get('success', False), reverse=True)
            self.pattern_database = self.pattern_database[:self.pattern_capacity]
    
    def find_matching_patterns(self, current_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Hittar matchande mönster i databasen.
        
        Args:
            current_data: Nuvarande marknadsdata
        
        Returns:
            Lista med matchande mönster
        """
        matches = []
        current_trend = current_data.get('trend_score', 0)
        current_volatility = current_data.get('volatility', 0.5)
        
        for pattern in self.pattern_database:
            pattern_trend = pattern.get('trend_score', 0)
            pattern_volatility = pattern.get('volatility', 0.5)
            
            # Beräkna likhet
            trend_similarity = 1.0 - abs(current_trend - pattern_trend)
            volatility_similarity = 1.0 - abs(current_volatility - pattern_volatility)
            
            overall_similarity = (trend_similarity + volatility_similarity) / 2.0
            
            if overall_similarity >= self.match_threshold:
                matches.append({
                    'pattern': pattern,
                    'similarity': overall_similarity
                })
        
        return sorted(matches, key=lambda x: x['similarity'], reverse=True)
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol genom historisk mönstermatchning.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        # Hitta matchande mönster
        matches = self.find_matching_patterns(market_data)
        
        if not matches:
            # Ingen historik - neutral position
            return {
                'agent_id': self.agent_id,
                'symbol': symbol,
                'decision': DecisionType.HOLD.value,
                'confidence': 0.5,
                'reasoning': 'No matching historical patterns found',
                'metrics': {
                    'matches_found': 0,
                    'pattern_database_size': len(self.pattern_database)
                }
            }
        
        # Analysera de bästa matcherna
        top_matches = matches[:5]
        successful_matches = [m for m in top_matches if m['pattern'].get('success', False)]
        
        # Beräkna konsensus från matchande mönster
        buy_signals = sum(1 for m in successful_matches if m['pattern'].get('decision') == 'buy')
        sell_signals = sum(1 for m in successful_matches if m['pattern'].get('decision') == 'sell')
        
        # Bestäm beslut
        if buy_signals > sell_signals:
            decision = DecisionType.BUY.value
            confidence = min(0.6 + (buy_signals / len(top_matches)) * 0.3, 0.95)
            reasoning = f"Historiska mönster indikerar BUY ({buy_signals}/{len(top_matches)} matchningar)"
        elif sell_signals > buy_signals:
            decision = DecisionType.SELL.value
            confidence = min(0.6 + (sell_signals / len(top_matches)) * 0.3, 0.95)
            reasoning = f"Historiska mönster indikerar SELL ({sell_signals}/{len(top_matches)} matchningar)"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Blandade signaler från historiska mönster"
        
        logger.debug(f"EchoAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'matches_found': len(matches),
                'top_match_similarity': matches[0]['similarity'] if matches else 0,
                'successful_matches': len(successful_matches)
            }
        }
