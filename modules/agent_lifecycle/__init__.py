"""
Agent Lifecycle Module - Agentens livscykel

Detta modul hanterar:
- Agentens livscykel från födelse till pension
- Prestandabaserad livslängd
- Aktivering och deaktivering av agenter
- Livscykelmetrik och tracking

Kopplingar: agent_spectrum/, evolution/, metaagentgovernor/
"""

from .agent_lifecycle import AgentLifecycle

__all__ = ['AgentLifecycle']
