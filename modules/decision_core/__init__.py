"""
Decision Core Module - Central beslutsmotor

Detta modul hanterar:
- Samling och validering av agentbeslut
- Routing av beslut till rätt moduler
- Loggning av beslutshierarki
- Konflikthantering och eskalering

Kopplingar: agents/, vote_engine/, fusion/, sizing/
"""

from .decision_core import DecisionCore, AgentDecision, DecisionType

__all__ = ['DecisionCore', 'AgentDecision', 'DecisionType']
