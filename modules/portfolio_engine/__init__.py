"""
Portfolio Engine Module - Portföljhantering

Detta modul hanterar:
- Hantering av multipla portföljer
- Portföljmutation och optimering
- RL-träning för portföljallokering
- Regime-baserad portföljval

Kopplingar: sizing/, portfolio_comparator/, risk_mapper/, evolution/
"""

from .portfolio_engine import PortfolioEngine

__all__ = ['PortfolioEngine']
