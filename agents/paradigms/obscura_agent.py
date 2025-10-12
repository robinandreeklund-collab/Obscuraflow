"""
ObscuraAgent - Latent/Obscure Dimension

Funktion: Identifierar dolda mönster och anomalier
Kapacitet: 2.0σ tröskel för avvikelse
Lärande: Specialiserad på icke-uppenbara signaler
Kopplingar: fusion, mirage, reflexion, self_critique
"""

import logging
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class ObscuraAgent(BaseAgent):
    """
    ObscuraAgent upptäcker dolda mönster och anomalier.
    
    Analyserar:
    - Statistiska avvikelser
    - Dolda korrelationer
    - Ovanliga marknadsförhållanden
    """
    
    def __init__(
        self, 
        agent_id: str = "obscura_agent",
        sigma_threshold: float = 2.0
    ):
        """
        Initierar ObscuraAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            sigma_threshold: Standardavvikelse-tröskel för anomalier
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.7,
            parameters={
                'sigma_threshold': sigma_threshold
            }
        )
        self.sigma_threshold = sigma_threshold
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol för dolda mönster.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        price_change = market_data.get('price_change_pct', 0)
        volatility = market_data.get('volatility', 0.5)
        volume = market_data.get('volume', 0)
        
        # Beräkna anomaliscore - hur ovanlig är situationen?
        # Hög volatilitet + extrema prisrörelser = anomali
        anomaly_score = abs(price_change) * 10 + volatility
        
        # Normalisera till sigma-skala (simulerat)
        sigma_level = anomaly_score * 2
        
        if sigma_level > self.sigma_threshold:
            # Anomali detekterad
            if price_change > 0:
                decision = DecisionType.BUY.value
                confidence = min(0.7 + (sigma_level - self.sigma_threshold) * 0.1, 0.95)
                reasoning = f"Dold uppåt-anomali detekterad (σ={sigma_level:.2f})"
            elif price_change < 0:
                decision = DecisionType.SELL.value
                confidence = min(0.7 + (sigma_level - self.sigma_threshold) * 0.1, 0.95)
                reasoning = f"Dold nedåt-anomali detekterad (σ={sigma_level:.2f})"
            else:
                decision = DecisionType.HOLD.value
                confidence = 0.6
                reasoning = f"Anomali utan klar riktning"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Inga dolda anomalier (σ={sigma_level:.2f})"
        
        logger.debug(f"ObscuraAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'sigma_level': sigma_level,
                'anomaly_score': anomaly_score
            }
        }
