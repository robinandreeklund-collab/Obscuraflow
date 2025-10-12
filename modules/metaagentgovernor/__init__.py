"""
Meta Agent Governor Module - Agentråd och prioritering

Detta modul hanterar:
- Överordnad styrning av alla agenter
- Prioritering och resursallokering
- Meta-beslut över agentsystemet
- Konfliktlösning på högsta nivå

Kopplingar: agent_lifecycle/, vote_engine/, portfolio_engine/
"""

from .metaagentgovernor import MetaAgentGovernor

__all__ = ['MetaAgentGovernor']
