"""
Vote Engine Module - Röstningssystem

Detta modul hanterar:
- Röstning mellan konfliktande agentbeslut
- Viktning baserat på agentprestation
- Meta-voting och beslutsaggregering
- Historik över röstningsutfall

Kopplingar: decision_core/, agents/, fusion/
"""

from .vote_engine import VoteEngine, Vote

__all__ = ['VoteEngine', 'Vote']
