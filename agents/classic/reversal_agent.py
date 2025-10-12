"""
ReversalAgent - Mean Reversion agent

Strategi: Söker överköpta/översålda tillstånd för vändningar
Spanpreferens: Medel (5–30 min)
Confidence-tröskel: 0.65
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class ReversalAgent(BaseAgent):
    """
    ReversalAgent söker efter mean reversion-möjligheter.
    
    Analyserar:
    - Överköpta/översålda nivåer
    - Prisavvikelser från medelvärde
    - Vändningsmönster
    """
    
    def __init__(
        self, 
        agent_id: str = "reversal_agent",
        lookback: int = 30,
        overbought_threshold: float = 0.7,
        oversold_threshold: float = 0.3
    ):
        """
        Initierar ReversalAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            lookback: Antal perioder att titta tillbaka
            overbought_threshold: Tröskel för överköpt
            oversold_threshold: Tröskel för översålt
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.CLASSIC,
            confidence_threshold=0.65,
            parameters={
                'lookback': lookback,
                'overbought_threshold': overbought_threshold,
                'oversold_threshold': oversold_threshold
            }
        )
        self.lookback = lookback
        self.overbought_threshold = overbought_threshold
        self.oversold_threshold = oversold_threshold
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar mean reversion-möjligheter för en symbol.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata inkl. pris, volatilitet
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        price = market_data.get('price', 0)
        trend_score = market_data.get('trend_score', 0.5)
        price_change = market_data.get('price_change_pct', 0)
        volatility = market_data.get('volatility', 0.5)
        
        # Simulera RSI-liknande indikator från trend_score och price_change
        # RSI-proxy: normalisera till 0-1 range
        rsi_proxy = 0.5 + price_change * 10  # Förenklad beräkning
        rsi_proxy = max(0.0, min(1.0, rsi_proxy))
        
        # Beräkna avståndet från medelvärde
        mean_distance = abs(rsi_proxy - 0.5)
        
        # Bestäm beslut baserat på överköpt/översålt
        if rsi_proxy < self.oversold_threshold:
            # Översålt - förvänta återhämtning
            decision = DecisionType.BUY.value
            confidence = min(0.65 + mean_distance * 0.3, 0.95)
            reasoning = f"Översålt tillstånd (RSI-proxy={rsi_proxy:.2f}), förväntar återhämtning"
        elif rsi_proxy > self.overbought_threshold:
            # Överköpt - förvänta korrigering
            decision = DecisionType.SELL.value
            confidence = min(0.65 + mean_distance * 0.3, 0.95)
            reasoning = f"Överköpt tillstånd (RSI-proxy={rsi_proxy:.2f}), förväntar korrigering"
        else:
            # Neutralt läge
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Neutralt tillstånd (RSI-proxy={rsi_proxy:.2f})"
        
        logger.debug(f"ReversalAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'rsi_proxy': rsi_proxy,
                'mean_distance': mean_distance,
                'volatility': volatility
            }
        }
