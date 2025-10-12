"""
DimensioAgent - Hyper-Spatial/Analytical Dimension

Funktion: Multi-dimensionell analys
Kapacitet: 5D feature space: momentum, RSI, trend, volym, volatilitet
Lärande: Identifierar komplexa mönster i högdimensionella rum
Kopplingar: fusion, fractalis, architectum, portfolio_comparator
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class DimensioAgent(BaseAgent):
    """
    DimensioAgent analyserar data i högdimensionella rum.
    
    Analyserar:
    - 5-dimensionell feature space
    - Komplexa korrelationer
    - Hyperplane-separering
    """
    
    def __init__(
        self, 
        agent_id: str = "dimensio_agent",
        num_dimensions: int = 5
    ):
        """
        Initierar DimensioAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            num_dimensions: Antal dimensioner att analysera
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.7,
            parameters={
                'num_dimensions': num_dimensions
            }
        )
        self.num_dimensions = num_dimensions
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol i högdimensionellt rum.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        # Extrahera 5D features
        price_change = market_data.get('price_change_pct', 0)
        trend_score = market_data.get('trend_score', 0.5)
        volatility = market_data.get('volatility', 0.5)
        volume = market_data.get('volume', 0)
        
        # Normalisera volume
        volume_normalized = min(volume / 1000000, 1.0)
        
        # RSI-proxy
        rsi_proxy = 0.5 + price_change * 10
        rsi_proxy = max(0.0, min(1.0, rsi_proxy))
        
        # 5D vektor
        feature_vector = [
            price_change * 10,  # Momentum
            rsi_proxy,
            trend_score,
            volume_normalized,
            volatility
        ]
        
        # Beräkna "avstånd" från neutralpunkt i 5D-rum
        neutral_point = [0, 0.5, 0.5, 0.5, 0.5]
        
        distance = sum((f - n) ** 2 for f, n in zip(feature_vector, neutral_point)) ** 0.5
        
        # Bestäm riktning i 5D-rum
        buy_score = feature_vector[0] + feature_vector[1] + feature_vector[2]
        sell_score = -feature_vector[0] + (1 - feature_vector[1]) + (1 - feature_vector[2])
        
        if buy_score > sell_score and distance > 0.5:
            decision = DecisionType.BUY.value
            confidence = min(0.7 + distance * 0.2, 0.95)
            reasoning = f"5D-analys indikerar BUY (distance={distance:.2f})"
        elif sell_score > buy_score and distance > 0.5:
            decision = DecisionType.SELL.value
            confidence = min(0.7 + distance * 0.2, 0.95)
            reasoning = f"5D-analys indikerar SELL (distance={distance:.2f})"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Neutral position i 5D-rum (distance={distance:.2f})"
        
        logger.debug(f"DimensioAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'feature_vector': feature_vector,
                '5d_distance': distance,
                'buy_score': buy_score,
                'sell_score': sell_score
            }
        }
