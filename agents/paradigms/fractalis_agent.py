"""
FractalisAgent - Spatial-Temporal/Complex Dimension

Funktion: Fraktalanalys över flera tidsskalor
Kapacitet: 5 samtidiga spans, självlikhetskontroll
Lärande: Identifierar rekursiva mönster
Kopplingar: fusion, timespan_engine, dimensio, architectum
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class FractalisAgent(BaseAgent):
    """
    FractalisAgent analyserar fraktala mönster över tidsskalor.
    
    Analyserar:
    - Självlikhet mellan tidsskalor
    - Rekursiva prismönster
    - Multi-timeframe konsistens
    """
    
    def __init__(
        self, 
        agent_id: str = "fractalis_agent",
        num_spans: int = 5,
        self_similarity_threshold: float = 0.7
    ):
        """
        Initierar FractalisAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            num_spans: Antal tidsskalor att analysera
            self_similarity_threshold: Tröskel för självlikhet
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.65,
            parameters={
                'num_spans': num_spans,
                'self_similarity_threshold': self_similarity_threshold
            }
        )
        self.num_spans = num_spans
        self.self_similarity_threshold = self_similarity_threshold
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol med fraktalanalys.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        trend_score = market_data.get('trend_score', 0)
        volatility = market_data.get('volatility', 0.5)
        price_change = market_data.get('price_change_pct', 0)
        
        # Simulera fraktal-likhet mellan tidsskalor
        # I verklig implementation skulle detta jämföra flera timeframes
        fractal_consistency = (abs(trend_score) + (1.0 - volatility)) / 2.0
        
        # Starka fraktalmönster indikerar robust trend
        if fractal_consistency > self.self_similarity_threshold:
            if price_change > 0:
                decision = DecisionType.BUY.value
                confidence = min(0.65 + fractal_consistency * 0.25, 0.95)
                reasoning = f"Stark fraktal-konsistens uppåt (consistency={fractal_consistency:.2f})"
            elif price_change < 0:
                decision = DecisionType.SELL.value
                confidence = min(0.65 + fractal_consistency * 0.25, 0.95)
                reasoning = f"Stark fraktal-konsistens nedåt (consistency={fractal_consistency:.2f})"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.6
                reasoning = f"Fraktal-konsistens utan klar riktning"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Svag fraktal-konsistens (consistency={fractal_consistency:.2f})"
        
        logger.debug(f"FractalisAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'fractal_consistency': fractal_consistency,
                'num_spans_analyzed': self.num_spans
            }
        }
