"""
Portfolio Comparator Module - Portföljjämförelse

Detta modul hanterar:
- Jämförelse mellan olika portföljer
- Meta-portföljer och portföljhierarki
- Benchmarking och prestanda-ranking
- Portföljrekommendationer

Kopplingar: portfolio_engine/, risk_mapper/, evolution/
"""

from .portfolio_comparator import PortfolioComparator

__all__ = ['PortfolioComparator']
