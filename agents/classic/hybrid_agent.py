"""
HybridAgent - Multi-strategi agent

Strategi: Växlar mellan strategier beroende på marknadsregim
Spanpreferens: Adaptiv
Confidence-tröskel: 0.5
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class HybridAgent(BaseAgent):
    """
    HybridAgent kombinerar flera strategier och växlar baserat på marknadsregim.
    
    Analyserar:
    - Marknadsregim (trending vs ranging)
    - Volatilitet
    - Kombinerar momentum, reversal och breakout-strategier
    """
    
    def __init__(
        self, 
        agent_id: str = "hybrid_agent",
        lookback: int = 30
    ):
        """
        Initierar HybridAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            lookback: Antal perioder att titta tillbaka
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.CLASSIC,
            confidence_threshold=0.5,
            parameters={
                'lookback': lookback
            }
        )
        self.lookback = lookback
        self.regime_history = []
    
    def detect_regime(self, market_data: Dict[str, Any]) -> str:
        """
        Detekterar marknadsregim.
        
        Args:
            market_data: Marknadsdata
        
        Returns:
            'trending', 'ranging', eller 'volatile'
        """
        trend_score = market_data.get('trend_score', 0)
        volatility = market_data.get('volatility', 0.5)
        price_change = abs(market_data.get('price_change_pct', 0))
        
        # Trending: stark trend med måttlig volatilitet
        if abs(trend_score) > 0.6 and volatility < 0.8:
            return 'trending'
        
        # Volatile: hög volatilitet med stora prisrörelser
        elif volatility > 0.7 or price_change > 0.03:
            return 'volatile'
        
        # Ranging: låg trend och låg volatilitet
        else:
            return 'ranging'
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol med hybrid-strategi.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        regime = self.detect_regime(market_data)
        self.regime_history.append(regime)
        
        # Begränsa historik
        if len(self.regime_history) > 50:
            self.regime_history = self.regime_history[-50:]
        
        price_change = market_data.get('price_change_pct', 0)
        trend_score = market_data.get('trend_score', 0)
        volatility = market_data.get('volatility', 0.5)
        
        # Välj strategi baserat på regime
        if regime == 'trending':
            # Använd momentum-strategi
            if price_change > 0.01:
                decision = DecisionType.BUY.value
                confidence = min(0.6 + abs(price_change) * 10, 0.9)
                reasoning = f"Trending regime: Momentum BUY (change={price_change:.2%})"
            elif price_change < -0.01:
                decision = DecisionType.SELL.value
                confidence = min(0.6 + abs(price_change) * 10, 0.9)
                reasoning = f"Trending regime: Momentum SELL (change={price_change:.2%})"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Trending regime: Svag signal"
        
        elif regime == 'ranging':
            # Använd reversal-strategi
            if trend_score > 0.7:
                decision = DecisionType.SELL.value
                confidence = 0.65
                reasoning = f"Ranging regime: Överköpt, förväntar reversal"
            elif trend_score < 0.3:
                decision = DecisionType.BUY.value
                confidence = 0.65
                reasoning = f"Ranging regime: Översålt, förväntar reversal"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Ranging regime: Neutralt läge"
        
        else:  # volatile
            # Använd breakout-strategi
            if abs(price_change) > 0.025:
                if price_change > 0:
                    decision = DecisionType.BUY.value
                    reasoning = f"Volatile regime: Breakout uppåt"
                else:
                    decision = DecisionType.SELL.value
                    reasoning = f"Volatile regime: Breakout nedåt"
                confidence = min(0.7 + volatility * 0.2, 0.95)
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Volatile regime: Väntar på breakout"
        
        logger.debug(f"HybridAgent analys för {symbol}: {decision} ({confidence:.2f}), regime={regime}")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'regime': regime,
                'volatility': volatility,
                'price_change': price_change,
                'trend_score': trend_score
            }
        }
