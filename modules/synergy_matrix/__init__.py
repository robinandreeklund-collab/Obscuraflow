"""
Synergy Matrix Module - Agent-samverkan och konfliktanalys

Detta modul hanterar:
- Analys av agentsamverkan
- Konfliktdetektion mellan agenter
- Synergimatris för agentpar
- Samarbetsmönster

Kopplingar: vote_engine/, agent_lifecycle/, narrative_engine/
"""

from .synergy_matrix import SynergyMatrix

__all__ = ['SynergyMatrix']
