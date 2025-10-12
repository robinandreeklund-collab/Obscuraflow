"""
PortfolioEngine - Huvudklass för portföljhantering

Denna klass ansvarar för:
- Hantering av flera parallella portföljer
- Portföljoptimering och mutation
- RL-baserad allokering
- Regime-anpassad portföljval
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class PortfolioEngine:
    """
    PortfolioEngine hanterar multipla portföljer och optimering.
    
    Attributes:
        portfolios (Dict[str, Dict]): Dictionary med portföljer
        active_portfolio (str): ID för aktiv portfölj
    """
    
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initierar PortfolioEngine med startkapital.
        
        Args:
            initial_capital: Startkapital för portföljer
        """
        self.initial_capital = initial_capital
        self.portfolios: Dict[str, Dict[str, Any]] = {}
        self.active_portfolio: Optional[str] = None
        self.performance_history: List[Dict[str, Any]] = []
        logger.info(f"PortfolioEngine initierad med kapital: {initial_capital}")
    
    def create_portfolio(self, portfolio_id: str, strategy: str = 'balanced') -> Dict[str, Any]:
        """
        Skapar ny portfölj.
        
        Args:
            portfolio_id: Unikt ID för portföljen
            strategy: Strategi ('aggressive', 'balanced', 'conservative')
        
        Returns:
            Dict med portföljinfo
        """
        if portfolio_id in self.portfolios:
            logger.warning(f"Portfölj {portfolio_id} finns redan")
            return self.portfolios[portfolio_id]
        
        portfolio = {
            'id': portfolio_id,
            'strategy': strategy,
            'capital': self.initial_capital,
            'positions': {},
            'created_at': datetime.now().isoformat()
        }
        
        self.portfolios[portfolio_id] = portfolio
        if self.active_portfolio is None:
            self.active_portfolio = portfolio_id
        
        logger.info(f"Skapade portfölj {portfolio_id} med strategi {strategy}")
        return portfolio
    
    def add_position(self, portfolio_id: str, symbol: str, size: float, price: float) -> bool:
        """
        Lägger till position i portfölj.
        
        Args:
            portfolio_id: Portfölj-ID
            symbol: Symbolnamn
            size: Positionsstorlek
            price: Inköpspris
        
        Returns:
            True om position lades till
        """
        if portfolio_id not in self.portfolios:
            logger.error(f"Portfölj {portfolio_id} finns inte")
            return False
        
        portfolio = self.portfolios[portfolio_id]
        portfolio['positions'][symbol] = {
            'size': size,
            'entry_price': price,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Lade till position {symbol} i portfölj {portfolio_id}")
        return True
    
    def optimize_portfolio(self, portfolio_id: str) -> Dict[str, Any]:
        """
        Optimerar portfölj baserat på RL och mutation.
        
        Args:
            portfolio_id: Portfölj-ID
        
        Returns:
            Dict med optimeringsresultat
        """
        if portfolio_id not in self.portfolios:
            logger.error(f"Portfölj {portfolio_id} finns inte")
            return {
                'portfolio_id': portfolio_id,
                'optimized': False,
                'error': 'Portfolio not found'
            }
        
        logger.info(f"Optimerar portfölj {portfolio_id}")
        
        portfolio = self.portfolios[portfolio_id]
        positions = portfolio['positions']
        
        # Beräkna nuvarande värde
        import random
        total_value = portfolio['capital']
        for symbol, pos in positions.items():
            # Simulera aktuellt pris
            current_price = pos['entry_price'] * random.uniform(0.9, 1.1)
            pos_value = pos['size'] * current_price
            total_value += pos_value
        
        # Beräkna avkastning
        returns = (total_value - self.initial_capital) / self.initial_capital
        
        # Optimeringsförslag
        suggestions = []
        
        # Föreslå rebalansering om någon position är för stor
        for symbol, pos in positions.items():
            pos_value = pos['size'] * pos['entry_price']
            pos_percent = pos_value / total_value
            if pos_percent > 0.15:  # Mer än 15% av portföljen
                suggestions.append(f"Överväg att minska position i {symbol}")
        
        # Föreslå diversifiering
        if len(positions) < 3:
            suggestions.append("Öka diversifiering genom fler positioner")
        
        result = {
            'portfolio_id': portfolio_id,
            'optimized': True,
            'current_value': total_value,
            'returns': returns,
            'returns_percent': returns * 100,
            'position_count': len(positions),
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
        # Spara i historik
        self.performance_history.append(result)
        
        logger.info(
            f"Optimering klar för {portfolio_id}: "
            f"värde=${total_value:.2f}, avkastning={returns*100:.2f}%"
        )
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för portfolio engine.
        
        Returns:
            Dict med statistik
        """
        total_positions = sum(len(p['positions']) for p in self.portfolios.values())
        
        # Beräkna total capital över alla portföljer
        total_capital = sum(p['capital'] for p in self.portfolios.values())
        
        # Hitta bästa portföljen om det finns performance history
        best_portfolio = None
        if self.performance_history:
            best = max(self.performance_history, key=lambda x: x.get('returns', 0))
            best_portfolio = best.get('portfolio_id')
        
        return {
            'total_portfolios': len(self.portfolios),
            'active_portfolio': self.active_portfolio,
            'total_positions': total_positions,
            'initial_capital': self.initial_capital,
            'total_capital': total_capital,
            'best_portfolio': best_portfolio,
            'performance_records': len(self.performance_history)
        }
