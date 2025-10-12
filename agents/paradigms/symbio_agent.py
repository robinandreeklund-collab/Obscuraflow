"""
SymbioAgent - Relational/Cooperative Dimension

Funktion: Samverkan och co-evolution med andra agenter
Kapacitet: 50% symbiosstyrka
Lärande: Förstärker relationer som ger ömsesidig nytta
Kopplingar: synergy_matrix, vox, myco, sentio
"""

import logging
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class SymbioAgent(BaseAgent):
    """
    SymbioAgent skapar symbiotiska relationer med andra agenter.
    
    Analyserar:
    - Agentsynergier
    - Samverkansvinster
    - Relationell förstärkning
    """
    
    def __init__(
        self, 
        agent_id: str = "symbio_agent",
        symbiosis_strength: float = 0.5
    ):
        """
        Initierar SymbioAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            symbiosis_strength: Styrka på symbiotiska relationer
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.6,
            parameters={
                'symbiosis_strength': symbiosis_strength
            }
        )
        self.symbiosis_strength = symbiosis_strength
        self.symbiotic_partners: List[str] = []
        self.partner_decisions: Dict[str, str] = {}
    
    def add_symbiotic_partner(self, agent_id: str, decision: str):
        """
        Lägger till symbiotisk partner.
        
        Args:
            agent_id: Partner-ID
            decision: Partners beslut
        """
        if agent_id not in self.symbiotic_partners:
            self.symbiotic_partners.append(agent_id)
        self.partner_decisions[agent_id] = decision
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol med symbiotisk förstärkning.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        trend_score = market_data.get('trend_score', 0)
        price_change = market_data.get('price_change_pct', 0)
        
        # Analysera partners beslut
        if self.partner_decisions:
            partner_buy = sum(1 for d in self.partner_decisions.values() if d == 'buy')
            partner_sell = sum(1 for d in self.partner_decisions.values() if d == 'sell')
            total_partners = len(self.partner_decisions)
            
            # Förstärk beslut om partners är eniga
            partner_consensus = max(partner_buy, partner_sell) / total_partners if total_partners > 0 else 0
            
            if partner_buy > partner_sell:
                decision = DecisionType.BUY.value
                confidence = min(0.6 + partner_consensus * self.symbiosis_strength * 0.3, 0.95)
                reasoning = f"Symbiotisk förstärkning BUY ({partner_buy}/{total_partners} partners)"
            elif partner_sell > partner_buy:
                decision = DecisionType.SELL.value
                confidence = min(0.6 + partner_consensus * self.symbiosis_strength * 0.3, 0.95)
                reasoning = f"Symbiotisk förstärkning SELL ({partner_sell}/{total_partners} partners)"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Symbiotiska partners delade"
        else:
            # Ingen partner-input, fallback till marknadsdata
            if price_change > 0.01:
                decision = DecisionType.BUY.value
                confidence = 0.6
                reasoning = f"Ingen symbiotisk input, baserat på positiv trend"
            elif price_change < -0.01:
                decision = DecisionType.SELL.value
                confidence = 0.6
                reasoning = f"Ingen symbiotisk input, baserat på negativ trend"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.5
                reasoning = f"Ingen symbiotisk input, neutral"
        
        logger.debug(f"SymbioAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'symbiotic_partners': len(self.symbiotic_partners),
                'partner_decisions': len(self.partner_decisions)
            }
        }
