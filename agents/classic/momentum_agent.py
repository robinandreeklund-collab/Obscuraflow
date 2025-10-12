"""
MomentumAgent - Trendföljande agent

Strategi: Identifierar och rider på starka prisrörelser
Spanpreferens: Kort (<5 min)
Confidence-tröskel: 0.6
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class MomentumAgent(BaseAgent):
    """
    MomentumAgent identifierar starka trendimpulser.
    
    Analyserar:
    - Prismomentum
    - Volymökning
    - Trendriktning och styrka
    """
    
    def __init__(
        self, 
        agent_id: str = "momentum_agent",
        lookback: int = 20,
        momentum_threshold: float = 0.02
    ):
        """
        Initierar MomentumAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            lookback: Antal perioder att titta tillbaka
            momentum_threshold: Tröskelvärde för momentumstyrka
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.CLASSIC,
            confidence_threshold=0.6,
            parameters={
                'lookback': lookback,
                'momentum_threshold': momentum_threshold
            }
        )
        self.lookback = lookback
        self.momentum_threshold = momentum_threshold
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar momentumstyrka för en symbol.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata inkl. pris, volym, trend
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        price = market_data.get('price', 0)
        volume = market_data.get('volume', 0)
        trend_score = market_data.get('trend_score', 0)
        price_change = market_data.get('price_change_pct', 0)
        
        # Beräkna momentumstyrka
        momentum_strength = abs(price_change)
        volume_factor = min(volume / 1000000, 2.0)  # Normalisera volym
        
        # Kombinerad momentum-score
        momentum_score = (momentum_strength + trend_score + volume_factor) / 3.0
        
        # Bestäm beslut baserat på momentum
        if momentum_score > self.momentum_threshold and price_change > 0:
            decision = DecisionType.BUY.value
            confidence = min(0.6 + momentum_score * 0.3, 0.95)
            reasoning = f"Starkt uppåtmomentum (score={momentum_score:.3f}, change={price_change:.2%})"
        elif momentum_score > self.momentum_threshold and price_change < 0:
            decision = DecisionType.SELL.value
            confidence = min(0.6 + momentum_score * 0.3, 0.95)
            reasoning = f"Starkt nedåtmomentum (score={momentum_score:.3f}, change={price_change:.2%})"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Svagt momentum (score={momentum_score:.3f})"
        
        logger.debug(f"MomentumAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'momentum_score': momentum_score,
                'price_change': price_change,
                'volume_factor': volume_factor
            }
        }
