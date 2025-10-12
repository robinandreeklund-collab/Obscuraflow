"""
MirageAgent - Perceptual/Discriminative Dimension

Funktion: Filtrerar falska signaler (illusioner)
Kapacitet: 65% verklighetströskel
Lärande: Validerar mot senaste historik
Kopplingar: fusion, obscura, echo, reflexion
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class MirageAgent(BaseAgent):
    """
    MirageAgent filtrerar falska signaler och illusioner.
    
    Analyserar:
    - Signalvaliditet
    - Falska breakouts
    - Marknadspsykologiska fällor
    """
    
    def __init__(
        self, 
        agent_id: str = "mirage_agent",
        reality_threshold: float = 0.65
    ):
        """
        Initierar MirageAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            reality_threshold: Tröskel för verkliga signaler
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.65,
            parameters={
                'reality_threshold': reality_threshold
            }
        )
        self.reality_threshold = reality_threshold
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol och filtrerar falska signaler.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        price_change = market_data.get('price_change_pct', 0)
        volatility = market_data.get('volatility', 0.5)
        volume = market_data.get('volume', 0)
        trend_score = market_data.get('trend_score', 0)
        
        # Beräkna signalvaliditet
        # Verkliga signaler har både volym och konsekvent trend
        volume_confirmation = min(volume / 1000000, 1.0)
        trend_consistency = abs(trend_score - 0.5) * 2  # Avstånd från neutralt
        
        signal_validity = (volume_confirmation + trend_consistency) / 2.0
        
        if signal_validity >= self.reality_threshold:
            # Verklig signal
            if price_change > 0.01:
                decision = DecisionType.BUY.value
                confidence = min(0.65 + signal_validity * 0.25, 0.95)
                reasoning = f"Verklig BUY-signal validerad (validity={signal_validity:.2f})"
            elif price_change < -0.01:
                decision = DecisionType.SELL.value
                confidence = min(0.65 + signal_validity * 0.25, 0.95)
                reasoning = f"Verklig SELL-signal validerad (validity={signal_validity:.2f})"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.6
                reasoning = f"Verklig men neutral signal"
        else:
            # Potentiell illusion/falsk signal
            decision = DecisionType.HOLD.value
            confidence = 0.4
            reasoning = f"Potentiell falsk signal (validity={signal_validity:.2f})"
        
        logger.debug(f"MirageAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'signal_validity': signal_validity,
                'volume_confirmation': volume_confirmation,
                'trend_consistency': trend_consistency
            }
        }
