"""
GenesisAgent - Origination/Generative Dimension

Funktion: Identifierar trendstarter och cykelbörjan
Kapacitet: Upptäcker inflektionspunkter och genesis moments
Lärande: Specialiserad på att känna igen nya rörelser
Kopplingar: forecast_simulator, echo, architectum, fusion
"""

import logging
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class GenesisAgent(BaseAgent):
    """
    GenesisAgent identifierar början av nya trender och cykler.
    
    Analyserar:
    - Inflektionspunkter
    - Trendstarter
    - Nya cykelinitiativ
    """
    
    def __init__(
        self, 
        agent_id: str = "genesis_agent",
        lookback: int = 20
    ):
        """
        Initierar GenesisAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            lookback: Antal perioder för inflektionsdetektering
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.7,
            parameters={
                'lookback': lookback
            }
        )
        self.lookback = lookback
        self.price_history: List[float] = []
    
    def detect_inflection(self) -> bool:
        """
        Detekterar inflektionspunkt i prishistorik.
        
        Returns:
            True om inflektionspunkt detekterad
        """
        if len(self.price_history) < 3:
            return False
        
        # Enkel inflektionsdetektion: ändring i riktning
        recent = self.price_history[-3:]
        if len(recent) == 3:
            # Vändning från nedgång till uppgång
            if recent[0] > recent[1] and recent[2] > recent[1]:
                return True
            # Vändning från uppgång till nedgång
            if recent[0] < recent[1] and recent[2] < recent[1]:
                return True
        
        return False
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol för genesis moments.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        price = market_data.get('price', 0)
        price_change = market_data.get('price_change_pct', 0)
        volatility = market_data.get('volatility', 0.5)
        
        self.price_history.append(price)
        
        # Begränsa historik
        if len(self.price_history) > self.lookback:
            self.price_history = self.price_history[-self.lookback:]
        
        # Detektera inflektionspunkt
        is_inflection = self.detect_inflection()
        
        # Beräkna genesis-score baserat på nya rörelser
        # Låg volatilitet följt av ökande momentum indikerar genesis
        genesis_score = abs(price_change) * (1.0 - volatility)
        
        if is_inflection and genesis_score > 0.02:
            if price_change > 0:
                decision = DecisionType.BUY.value
                confidence = min(0.7 + genesis_score * 10, 0.95)
                reasoning = f"Genesis-moment uppåt detekterat (inflection + momentum)"
            else:
                decision = DecisionType.SELL.value
                confidence = min(0.7 + genesis_score * 10, 0.95)
                reasoning = f"Genesis-moment nedåt detekterat (inflection + momentum)"
        elif is_inflection:
            decision = DecisionType.HOLD.value
            confidence = 0.6
            reasoning = f"Inflektionspunkt men svag momentum"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Ingen genesis-signal (score={genesis_score:.3f})"
        
        logger.debug(f"GenesisAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'is_inflection': is_inflection,
                'genesis_score': genesis_score,
                'price_history_size': len(self.price_history)
            }
        }
