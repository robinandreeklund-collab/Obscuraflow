"""
Sizing - Huvudklass för position sizing med RL

Denna klass ansvarar för:
- Beräkning av optimal positionsstorlek
- Reinforcement learning för sizing-optimering
- Riskjusterad sizing
- Anpassning till marknadsregim
"""

import logging
from typing import Dict, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class Sizing:
    """
    Sizing hanterar dynamisk positionsstorlek med RL.
    
    Attributes:
        max_position_size (float): Maximal positionsstorlek som procent av portfölj
        risk_per_trade (float): Risk per trade som procent
        use_kelly (bool): Använd Kelly criterion
    """
    
    def __init__(
        self,
        max_position_size: float = 0.1,
        risk_per_trade: float = 0.02,
        use_kelly: bool = False
    ):
        """
        Initierar Sizing med risk-parametrar.
        
        Args:
            max_position_size: Max position size som procent (0.1 = 10%)
            risk_per_trade: Risk per trade som procent (0.02 = 2%)
            use_kelly: Om True, använd Kelly criterion
        """
        self.max_position_size = max_position_size
        self.risk_per_trade = risk_per_trade
        self.use_kelly = use_kelly
        self.sizing_history: Dict[str, list] = {}
        logger.info(f"Sizing initierad med max_position_size={max_position_size}")
    
    def calculate_position_size(
        self,
        symbol: str,
        portfolio_value: float,
        confidence: float,
        volatility: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Beräknar optimal positionsstorlek.
        
        Args:
            symbol: Symbolnamn
            portfolio_value: Totalt portföljvärde
            confidence: Konfidensnivå för trade (0-100)
            volatility: Volatilitet för symbolen (valfritt)
        
        Returns:
            Dict med sizing-resultat
        """
        logger.info(f"Beräknar position size för {symbol}")
        
        # Kodstub - implementeras senare med faktisk RL och Kelly
        base_size = portfolio_value * self.max_position_size
        confidence_adjusted = base_size * (confidence / 100.0)
        
        return {
            'symbol': symbol,
            'position_size': confidence_adjusted,
            'position_size_percent': (confidence_adjusted / portfolio_value) * 100,
            'risk_amount': confidence_adjusted * self.risk_per_trade,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
    
    def update_from_outcome(self, symbol: str, outcome: Dict[str, Any]) -> None:
        """
        Uppdaterar RL-modellen baserat på trade-utfall.
        
        Args:
            symbol: Symbolnamn
            outcome: Dict med trade-resultat
        """
        # Kodstub - implementeras senare med RL-träning
        if symbol not in self.sizing_history:
            self.sizing_history[symbol] = []
        self.sizing_history[symbol].append(outcome)
        logger.info(f"Uppdaterade sizing history för {symbol}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för sizing-beslut.
        
        Returns:
            Dict med statistik
        """
        return {
            'symbols_tracked': len(self.sizing_history),
            'total_calculations': sum(len(v) for v in self.sizing_history.values()),
            'max_position_size': self.max_position_size,
            'risk_per_trade': self.risk_per_trade
        }
