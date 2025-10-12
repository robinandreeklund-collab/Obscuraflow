"""
Evolution Module - Strategimutation

Detta modul hanterar:
- Mutation och evolution av strategier
- Genetiska algoritmer för strategi-optimering
- A/B-testning av strategivarianter
- Överlevnad av fittest strategies

Kopplingar: portfolio_engine/, mutation_tracker/, agent_lifecycle/
"""

from .evolution import Evolution

__all__ = ['Evolution']
