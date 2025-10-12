"""
Sizing Module - Position sizing med RL

Detta modul hanterar:
- Dynamisk positionsstorlek baserat på risk
- Reinforcement learning för sizing-optimering
- Kelly criterion och andra sizing-strategier
- Anpassning baserat på marknadsregim

Kopplingar: portfolio_engine/, decision_core/, risk_mapper/
"""

from .sizing import Sizing

__all__ = ['Sizing']
