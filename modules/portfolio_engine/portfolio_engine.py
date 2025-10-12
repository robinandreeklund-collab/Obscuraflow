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
        # Kodstub - implementeras senare med faktisk optimering
        logger.info(f"Optimerar portfölj {portfolio_id}")
        return {
            'portfolio_id': portfolio_id,
            'optimized': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för portfolio engine.
        
        Returns:
            Dict med statistik
        """
        total_positions = sum(len(p['positions']) for p in self.portfolios.values())
        return {
            'total_portfolios': len(self.portfolios),
            'active_portfolio': self.active_portfolio,
            'total_positions': total_positions,
            'initial_capital': self.initial_capital
        }
