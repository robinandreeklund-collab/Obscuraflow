"""
VoxAgent - Social/Collective Dimension

Funktion: Konsensusbyggare mellan agenter
Kapacitet: 75% rösttröskel, demokratisk beslutslogik
Lärande: Förstärks vid träffsäkra gruppbeslut
Kopplingar: voteengine, metaagent_governor, symbio, sentio
"""

import logging
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class VoxAgent(BaseAgent):
    """
    VoxAgent bygger konsensus genom att analysera andra agenters beslut.
    
    Analyserar:
    - Agentröster och viktningar
    - Gruppkonsensus
    - Demokratiska beslutsprocesser
    """
    
    def __init__(
        self, 
        agent_id: str = "vox_agent",
        consensus_threshold: float = 0.75
    ):
        """
        Initierar VoxAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            consensus_threshold: Tröskel för konsensus
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.65,
            parameters={
                'consensus_threshold': consensus_threshold
            }
        )
        self.consensus_threshold = consensus_threshold
        self.other_agent_decisions: List[Dict[str, Any]] = []
    
    def add_agent_decision(self, decision: Dict[str, Any]):
        """
        Lägger till en annan agents beslut.
        
        Args:
            decision: Beslut från annan agent
        """
        self.other_agent_decisions.append(decision)
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol genom konsensusbyggande.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        # Om vi har andra agentbeslut, använd dem
        if self.other_agent_decisions:
            buy_votes = sum(1 for d in self.other_agent_decisions if d.get('decision') == 'buy')
            sell_votes = sum(1 for d in self.other_agent_decisions if d.get('decision') == 'sell')
            total_votes = len(self.other_agent_decisions)
            
            buy_ratio = buy_votes / total_votes if total_votes > 0 else 0
            sell_ratio = sell_votes / total_votes if total_votes > 0 else 0
            
            if buy_ratio >= self.consensus_threshold:
                decision = DecisionType.BUY.value
                confidence = min(0.65 + buy_ratio * 0.3, 0.95)
                reasoning = f"Stark konsensus för BUY ({buy_votes}/{total_votes} agenter)"
            elif sell_ratio >= self.consensus_threshold:
                decision = DecisionType.SELL.value
                confidence = min(0.65 + sell_ratio * 0.3, 0.95)
                reasoning = f"Stark konsensus för SELL ({sell_votes}/{total_votes} agenter)"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Ingen stark konsensus ({buy_votes} buy, {sell_votes} sell av {total_votes})"
        else:
            # Fallback på marknadsdata
            trend_score = market_data.get('trend_score', 0)
            if trend_score > 0.7:
                decision = DecisionType.BUY.value
                confidence = 0.65
                reasoning = f"Ingen agent-input, baserat på stark trend"
            elif trend_score < 0.3:
                decision = DecisionType.SELL.value
                confidence = 0.65
                reasoning = f"Ingen agent-input, baserat på svag trend"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Ingen agent-input, neutral marknadsdata"
        
        logger.debug(f"VoxAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'agent_decisions_considered': len(self.other_agent_decisions)
            }
        }
