"""
ReflexionAgent - Meta-Cognitive/Reflective Dimension

Funktion: Självreflektion och adaptivt lärande
Kapacitet: 100 beslutshistorik, justerar baserat på träffsäkerhet
Lärande: Lär sig från misstag och förbättrar sin logik
Kopplingar: self_critique, evolution, echo, mirage
"""

import logging
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class ReflexionAgent(BaseAgent):
    """
    ReflexionAgent utför självreflektion och lär från misstag.
    
    Analyserar:
    - Egen beslutshistorik
    - Framgångsfrekvens per strategi
    - Adaptiva justeringar
    """
    
    def __init__(
        self, 
        agent_id: str = "reflexion_agent",
        history_capacity: int = 100
    ):
        """
        Initierar ReflexionAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            history_capacity: Max antal beslut att komma ihåg
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.65,
            parameters={
                'history_capacity': history_capacity
            }
        )
        self.history_capacity = history_capacity
        self.reflection_history: List[Dict[str, Any]] = []
    
    def reflect_on_performance(self) -> Dict[str, float]:
        """
        Reflekterar över tidigare prestationer.
        
        Returns:
            Dict med prestandametrik per strategi
        """
        if not self.reflection_history:
            return {}
        
        # Analysera framgång per beslut typ
        buy_success = [h for h in self.reflection_history if h['decision'] == 'buy' and h.get('success', False)]
        sell_success = [h for h in self.reflection_history if h['decision'] == 'sell' and h.get('success', False)]
        
        buy_total = [h for h in self.reflection_history if h['decision'] == 'buy']
        sell_total = [h for h in self.reflection_history if h['decision'] == 'sell']
        
        return {
            'buy_accuracy': len(buy_success) / len(buy_total) if buy_total else 0.5,
            'sell_accuracy': len(sell_success) / len(sell_total) if sell_total else 0.5
        }
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol med självreflektion.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        # Reflektera över tidigare prestationer
        performance = self.reflect_on_performance()
        
        price_change = market_data.get('price_change_pct', 0)
        trend_score = market_data.get('trend_score', 0)
        
        # Justera beslut baserat på tidigare framgång
        buy_accuracy = performance.get('buy_accuracy', 0.5)
        sell_accuracy = performance.get('sell_accuracy', 0.5)
        
        if price_change > 0.01 and buy_accuracy > 0.6:
            decision = DecisionType.BUY.value
            confidence = min(0.65 + buy_accuracy * 0.25, 0.95)
            reasoning = f"Reflektiv BUY baserat på tidigare framgång (accuracy={buy_accuracy:.2f})"
        elif price_change < -0.01 and sell_accuracy > 0.6:
            decision = DecisionType.SELL.value
            confidence = min(0.65 + sell_accuracy * 0.25, 0.95)
            reasoning = f"Reflektiv SELL baserat på tidigare framgång (accuracy={sell_accuracy:.2f})"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Låg confidence från reflektion (buy={buy_accuracy:.2f}, sell={sell_accuracy:.2f})"
        
        # Lagra beslut för framtida reflektion
        self.reflection_history.append({
            'decision': decision,
            'confidence': confidence,
            'market_data': market_data
        })
        
        if len(self.reflection_history) > self.history_capacity:
            self.reflection_history = self.reflection_history[-self.history_capacity:]
        
        logger.debug(f"ReflexionAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'buy_accuracy': buy_accuracy,
                'sell_accuracy': sell_accuracy,
                'reflection_history_size': len(self.reflection_history)
            }
        }
