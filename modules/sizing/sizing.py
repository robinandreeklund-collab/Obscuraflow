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
        volatility: Optional[float] = None,
        win_rate: Optional[float] = None,
        avg_win_loss_ratio: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Beräknar optimal positionsstorlek.
        
        Args:
            symbol: Symbolnamn
            portfolio_value: Totalt portföljvärde
            confidence: Konfidensnivå för trade (0-100)
            volatility: Volatilitet för symbolen (valfritt)
            win_rate: Historisk vinstfrekvens (0-1, valfritt)
            avg_win_loss_ratio: Genomsnittlig vinst/förlust ratio (valfritt)
        
        Returns:
            Dict med sizing-resultat
        """
        logger.info(f"Beräknar position size för {symbol}")
        
        # Bas sizing från max position size
        base_size = portfolio_value * self.max_position_size
        
        # Justera för confidence
        confidence_adjusted = base_size * (confidence / 100.0)
        
        # Kelly criterion om aktiverat och data finns
        kelly_fraction = None
        if self.use_kelly and win_rate is not None and avg_win_loss_ratio is not None:
            # Kelly formula: f = (p*b - q) / b
            # där p = win rate, q = 1-p, b = win/loss ratio
            p = win_rate
            q = 1 - p
            b = avg_win_loss_ratio
            
            kelly_fraction = (p * b - q) / b if b > 0 else 0
            # Begränsa Kelly till positiva värden och använd fractional Kelly (50%)
            kelly_fraction = max(0, min(kelly_fraction, 0.5))
            
            # Applicera Kelly
            kelly_size = portfolio_value * kelly_fraction
            confidence_adjusted = min(confidence_adjusted, kelly_size)
            
            logger.debug(f"Kelly fraction för {symbol}: {kelly_fraction:.4f}")
        
        # Volatilitetsanpassning om data finns
        volatility_adjusted = confidence_adjusted
        if volatility is not None and volatility > 0:
            # Reducera position size vid hög volatilitet
            # Använd inverse volatility scaling
            vol_factor = 1.0 / (1.0 + volatility)
            volatility_adjusted = confidence_adjusted * vol_factor
            logger.debug(f"Volatilitet {volatility:.4f} -> factor {vol_factor:.4f}")
        
        final_size = volatility_adjusted
        
        # Säkerställ att vi inte överskrider max position size
        final_size = min(final_size, portfolio_value * self.max_position_size)
        
        # Beräkna risk
        risk_amount = final_size * self.risk_per_trade
        
        result = {
            'symbol': symbol,
            'position_size': final_size,
            'position_size_percent': (final_size / portfolio_value) * 100,
            'risk_amount': risk_amount,
            'risk_percent': (risk_amount / portfolio_value) * 100,
            'confidence': confidence,
            'volatility': volatility,
            'kelly_fraction': kelly_fraction,
            'calculations': {
                'base_size': base_size,
                'confidence_adjusted': confidence_adjusted,
                'volatility_adjusted': volatility_adjusted,
                'final_size': final_size
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Spara i historik
        if symbol not in self.sizing_history:
            self.sizing_history[symbol] = []
        self.sizing_history[symbol].append(result)
        
        logger.info(
            f"Position size för {symbol}: ${final_size:.2f} "
            f"({(final_size/portfolio_value)*100:.2f}%), risk=${risk_amount:.2f}"
        )
        
        return result
    
    def update_from_outcome(self, symbol: str, outcome: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uppdaterar RL-modellen baserat på trade-utfall.
        
        Args:
            symbol: Symbolnamn
            outcome: Dict med trade-resultat (måste innehålla 'success' och 'pnl')
        
        Returns:
            Dict med uppdateringsresultat
        """
        if symbol not in self.sizing_history:
            self.sizing_history[symbol] = []
        
        # Lägg till outcome i historik
        outcome['timestamp'] = datetime.now().isoformat()
        self.sizing_history[symbol].append(outcome)
        
        # Beräkna statistik för symbolen
        symbol_outcomes = [h for h in self.sizing_history[symbol] if 'success' in h]
        
        if symbol_outcomes:
            wins = sum(1 for o in symbol_outcomes if o.get('success', False))
            total = len(symbol_outcomes)
            win_rate = wins / total
            
            # Beräkna genomsnittlig vinst/förlust
            winning_trades = [o.get('pnl', 0) for o in symbol_outcomes if o.get('success', False)]
            losing_trades = [abs(o.get('pnl', 0)) for o in symbol_outcomes if not o.get('success', False)]
            
            avg_win = sum(winning_trades) / len(winning_trades) if winning_trades else 0
            avg_loss = sum(losing_trades) / len(losing_trades) if losing_trades else 1
            
            win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
            
            result = {
                'symbol': symbol,
                'win_rate': win_rate,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'win_loss_ratio': win_loss_ratio,
                'total_outcomes': total,
                'updated': True
            }
            
            logger.info(
                f"Uppdaterade sizing för {symbol}: win_rate={win_rate:.2%}, "
                f"win/loss_ratio={win_loss_ratio:.2f}"
            )
        else:
            result = {
                'symbol': symbol,
                'updated': False,
                'reason': 'Insufficient outcome data'
            }
        
        return result
    
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
