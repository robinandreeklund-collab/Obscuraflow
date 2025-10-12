"""
ArchitectumAgent - Structural/Constructive Dimension

Funktion: Strukturell analys och systembyggnad
Kapacitet: 4 nivåer: foundation, pillars, framework, roof
Lärande: Aktiveras vid strukturscore > 70%
Kopplingar: fusion, dimensio, reflexion, genesis
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class ArchitectumAgent(BaseAgent):
    """
    ArchitectumAgent analyserar marknadsstruktur i lager.
    
    Analyserar:
    - Strukturella nivåer (foundation, pillars, framework, roof)
    - Byggstenar för trender
    - Arkitektonisk integritet
    """
    
    def __init__(
        self, 
        agent_id: str = "architectum_agent",
        structure_threshold: float = 0.7
    ):
        """
        Initierar ArchitectumAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            structure_threshold: Tröskel för strukturscore
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.7,
            parameters={
                'structure_threshold': structure_threshold
            }
        )
        self.structure_threshold = structure_threshold
    
    def analyze_structure(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Analyserar marknadsstruktur i 4 nivåer.
        
        Args:
            market_data: Marknadsdata
        
        Returns:
            Dict med strukturscores per nivå
        """
        trend_score = market_data.get('trend_score', 0)
        volatility = market_data.get('volatility', 0.5)
        volume = market_data.get('volume', 0)
        price_change = market_data.get('price_change_pct', 0)
        
        # Foundation: Volymbas
        foundation = min(volume / 1000000, 1.0)
        
        # Pillars: Trend-stabilitet
        pillars = abs(trend_score - 0.5) * 2  # Avstånd från neutral
        
        # Framework: Konsistens (låg volatilitet + tydlig trend)
        framework = (1.0 - volatility) * pillars
        
        # Roof: Momentumtak
        roof = abs(price_change) * 10
        roof = min(roof, 1.0)
        
        return {
            'foundation': foundation,
            'pillars': pillars,
            'framework': framework,
            'roof': roof
        }
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol med strukturanalys.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        structure = self.analyze_structure(market_data)
        
        # Beräkna total strukturscore
        structure_score = sum(structure.values()) / 4.0
        
        price_change = market_data.get('price_change_pct', 0)
        
        if structure_score > self.structure_threshold:
            # Stark struktur - följ riktningen
            if price_change > 0:
                decision = DecisionType.BUY.value
                confidence = min(0.7 + structure_score * 0.2, 0.95)
                reasoning = f"Stark uppåtstruktur (score={structure_score:.2f})"
            elif price_change < 0:
                decision = DecisionType.SELL.value
                confidence = min(0.7 + structure_score * 0.2, 0.95)
                reasoning = f"Stark nedåtstruktur (score={structure_score:.2f})"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.6
                reasoning = f"Stark struktur men ingen klar riktning"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Svag marknadsstruktur (score={structure_score:.2f})"
        
        logger.debug(f"ArchitectumAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'structure_score': structure_score,
                'foundation': structure['foundation'],
                'pillars': structure['pillars'],
                'framework': structure['framework'],
                'roof': structure['roof']
            }
        }
