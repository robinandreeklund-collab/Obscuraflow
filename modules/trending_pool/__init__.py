"""
Trending Pool Module - Market Heat Engine

Detta modul hanterar:
- Identifiering och rankning av aktiva symboler
- Stabilisering av trenddata
- Score-beräkning med viktning
- Historikcache och fluktuationsdämpning

Kopplingar: data_stream/, agents/, decision_core/, fusion/
"""

from .trending_pool import TrendingPool

__all__ = ['TrendingPool']
