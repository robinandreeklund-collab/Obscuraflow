"""
MycoAgent - Network/Distributed Dimension

Funktion: Informationsspridning genom agentnätverk
Kapacitet: 3 nivåers nätverksdjup, 85% decay rate
Lärande: Diffunderar insikter till andra agenter
Kopplingar: synergymatrix, symbio, portfolioengine
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class MycoAgent(BaseAgent):
    """
    MycoAgent sprider information genom nätverket som ett mycel.
    
    Analyserar:
    - Nätverkseffekter
    - Informationsdiffusion
    - Relationer mellan agenter
    """
    
    def __init__(
        self, 
        agent_id: str = "myco_agent",
        network_depth: int = 3,
        decay_rate: float = 0.85
    ):
        """
        Initierar MycoAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            network_depth: Djup i nätverket
            decay_rate: Hur snabbt information försvagas
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.6,
            parameters={
                'network_depth': network_depth,
                'decay_rate': decay_rate
            }
        )
        self.network_depth = network_depth
        self.decay_rate = decay_rate
        self.network_signals = {}
    
    def propagate_signal(self, signal: str, strength: float, depth: int = 0):
        """
        Propagerar en signal genom nätverket.
        
        Args:
            signal: Signaltyp (buy/sell)
            strength: Signalstyrka
            depth: Nuvarande djup i nätverket
        """
        if depth >= self.network_depth:
            return
        
        decayed_strength = strength * (self.decay_rate ** depth)
        self.network_signals[signal] = self.network_signals.get(signal, 0) + decayed_strength
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol genom nätverkseffekter.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        trend_score = market_data.get('trend_score', 0)
        volatility = market_data.get('volatility', 0.5)
        
        # Simulera nätverkssignaler
        network_buy_signal = self.network_signals.get('buy', 0)
        network_sell_signal = self.network_signals.get('sell', 0)
        
        # Kombinera nätverkssignaler med marknadsdata
        combined_buy = network_buy_signal + max(0, trend_score)
        combined_sell = network_sell_signal + max(0, -trend_score)
        
        if combined_buy > combined_sell and combined_buy > 0.5:
            decision = DecisionType.BUY.value
            confidence = min(0.6 + combined_buy * 0.3, 0.95)
            reasoning = f"Nätverket indikerar BUY (network_signal={network_buy_signal:.2f})"
        elif combined_sell > combined_buy and combined_sell > 0.5:
            decision = DecisionType.SELL.value
            confidence = min(0.6 + combined_sell * 0.3, 0.95)
            reasoning = f"Nätverket indikerar SELL (network_signal={network_sell_signal:.2f})"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Svaga nätverkssignaler"
        
        logger.debug(f"MycoAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'network_buy_signal': network_buy_signal,
                'network_sell_signal': network_sell_signal,
                'network_depth': self.network_depth
            }
        }
