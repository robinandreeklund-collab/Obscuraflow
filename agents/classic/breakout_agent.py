"""
BreakoutAgent - Volatility Breakout agent

Strategi: Reagerar på prisgenombrott från konsolidering
Spanpreferens: Lång (>30 min)
Confidence-tröskel: 0.7
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class BreakoutAgent(BaseAgent):
    """
    BreakoutAgent identifierar prisgenombrott från konsolideringsfaser.
    
    Analyserar:
    - Volatilitetsökningar
    - Volymspikes
    - Prisgenombrott från ranges
    """
    
    def __init__(
        self, 
        agent_id: str = "breakout_agent",
        lookback: int = 50,
        volatility_threshold: float = 1.5,
        volume_spike_threshold: float = 1.8
    ):
        """
        Initierar BreakoutAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            lookback: Antal perioder att titta tillbaka
            volatility_threshold: Tröskel för volatilitetsökning
            volume_spike_threshold: Tröskel för volymspike
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.CLASSIC,
            confidence_threshold=0.7,
            parameters={
                'lookback': lookback,
                'volatility_threshold': volatility_threshold,
                'volume_spike_threshold': volume_spike_threshold
            }
        )
        self.lookback = lookback
        self.volatility_threshold = volatility_threshold
        self.volume_spike_threshold = volume_spike_threshold
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar breakout-möjligheter för en symbol.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata inkl. pris, volym, volatilitet
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        price = market_data.get('price', 0)
        volume = market_data.get('volume', 0)
        price_change = market_data.get('price_change_pct', 0)
        volatility = market_data.get('volatility', 0.5)
        trend_score = market_data.get('trend_score', 0)
        
        # Beräkna breakout-indikatorer
        # Normalisera volym (anta genomsnitt runt 1M)
        avg_volume = 1000000
        volume_ratio = volume / avg_volume if volume > 0 else 1.0
        
        # Breakout-styrka baserat på volatilitet och volym
        breakout_strength = (volatility + volume_ratio) / 2.0
        
        # Starka prisrörelser indikerar breakout
        price_momentum = abs(price_change)
        
        # Kombinerad breakout-score
        breakout_score = (breakout_strength + price_momentum * 10) / 2.0
        
        # Bestäm beslut baserat på breakout
        if breakout_score > self.volatility_threshold and price_change > 0:
            decision = DecisionType.BUY.value
            confidence = min(0.7 + breakout_score * 0.1, 0.95)
            reasoning = f"Uppåtbreakout detekterat (score={breakout_score:.2f}, vol_ratio={volume_ratio:.2f})"
        elif breakout_score > self.volatility_threshold and price_change < 0:
            decision = DecisionType.SELL.value
            confidence = min(0.7 + breakout_score * 0.1, 0.95)
            reasoning = f"Nedåtbreakout detekterat (score={breakout_score:.2f}, vol_ratio={volume_ratio:.2f})"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Ingen breakout detekterad (score={breakout_score:.2f})"
        
        logger.debug(f"BreakoutAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'breakout_score': breakout_score,
                'volume_ratio': volume_ratio,
                'volatility': volatility,
                'price_momentum': price_momentum
            }
        }
