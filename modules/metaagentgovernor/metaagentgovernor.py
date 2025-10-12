"""
MetaAgentGovernor - Huvudklass för agentråd och prioritering

Denna klass ansvarar för:
- Överordnad styrning av agenter
- Prioritering och resursallokering
- Meta-beslut
- Konfliktlösning på högsta nivå
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class MetaAgentGovernor:
    """
    MetaAgentGovernor hanterar överordnad styrning av agenter.
    
    Attributes:
        agent_priorities (Dict): Prioriteringar för agenter
        resource_limits (Dict): Resursgränser
    """
    
    def __init__(self, max_active_agents: int = 10):
        """
        Initierar MetaAgentGovernor.
        
        Args:
            max_active_agents: Max antal samtidigt aktiva agenter
        """
        self.max_active_agents = max_active_agents
        self.agent_priorities: Dict[str, float] = {}
        self.resource_allocation: Dict[str, float] = {}
        self.governance_decisions: List[Dict[str, Any]] = []
        logger.info(f"MetaAgentGovernor initierad med max_active_agents={max_active_agents}")
    
    def set_priority(self, agent_id: str, priority: float) -> bool:
        """
        Sätter prioritet för en agent.
        
        Args:
            agent_id: Agent-ID
            priority: Prioritet (0-1, högre är viktigare)
        
        Returns:
            True om prioritet sattes
        """
        if not 0 <= priority <= 1:
            logger.error("Prioritet måste vara mellan 0 och 1")
            return False
        
        self.agent_priorities[agent_id] = priority
        logger.info(f"Satte prioritet {priority} för agent {agent_id}")
        return True
    
    def allocate_resources(self, agent_id: str, resources: float) -> bool:
        """
        Allokerar resurser till en agent.
        
        Args:
            agent_id: Agent-ID
            resources: Resursandel (0-1)
        
        Returns:
            True om resurser allokerades
        """
        total_allocated = sum(self.resource_allocation.values())
        
        if total_allocated + resources > 1.0:
            logger.warning(f"Kan inte allokera {resources}, totalt skulle överstiga 1.0")
            return False
        
        self.resource_allocation[agent_id] = resources
        logger.info(f"Allokerade {resources} resurser till {agent_id}")
        return True
    
    def make_governance_decision(
        self,
        decision_type: str,
        affected_agents: List[str],
        rationale: str
    ) -> Dict[str, Any]:
        """
        Fattar ett övergripande beslut.
        
        Args:
            decision_type: Typ av beslut
            affected_agents: Berörda agenter
            rationale: Motivering
        
        Returns:
            Dict med beslut
        """
        decision = {
            'type': decision_type,
            'affected_agents': affected_agents,
            'rationale': rationale,
            'timestamp': datetime.now().isoformat()
        }
        
        self.governance_decisions.append(decision)
        logger.info(f"Fattade governance-beslut: {decision_type}")
        return decision
    
    def resolve_conflict(
        self,
        conflicting_agents: List[str],
        conflict_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Löser konflikt mellan agenter på högsta nivå.
        
        Args:
            conflicting_agents: Lista med konfliktande agenter
            conflict_data: Data om konflikten
        
        Returns:
            Dict med resolution
        """
        # Kodstub - implementeras senare med faktisk konfliktlösning
        logger.info(f"Löser konflikt mellan {len(conflicting_agents)} agenter")
        
        # Välj agent med högst prioritet
        winner = max(
            conflicting_agents,
            key=lambda a: self.agent_priorities.get(a, 0.5)
        )
        
        resolution = {
            'conflicting_agents': conflicting_agents,
            'winner': winner,
            'method': 'priority_based',
            'timestamp': datetime.now().isoformat()
        }
        
        return resolution
    
    def rebalance_priorities(self, performance_data: Dict[str, float]) -> Dict[str, float]:
        """
        Ombalanserar prioriteringar baserat på prestation.
        
        Args:
            performance_data: Dict med agent_id -> performance
        
        Returns:
            Dict med nya prioriteringar
        """
        # Kodstub - implementeras senare med faktisk ombalansering
        new_priorities = {}
        
        for agent_id, performance in performance_data.items():
            # Enkelt: bättre prestation = högre prioritet
            new_priority = min(1.0, performance * 1.2)
            new_priorities[agent_id] = new_priority
            self.set_priority(agent_id, new_priority)
        
        logger.info(f"Ombalanserade prioriteringar för {len(new_priorities)} agenter")
        return new_priorities
    
    def get_top_priority_agents(self, n: int = 5) -> List[tuple]:
        """
        Hämtar agenter med högst prioritet.
        
        Args:
            n: Antal agenter att returnera
        
        Returns:
            Lista med (agent_id, priority)
        """
        sorted_agents = sorted(
            self.agent_priorities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_agents[:n]
    
    def enforce_limits(self) -> Dict[str, Any]:
        """
        Enforcar resursgränser och begränsningar.
        
        Returns:
            Dict med enforcement-resultat
        """
        # Kodstub
        total_resources = sum(self.resource_allocation.values())
        
        result = {
            'total_resources_allocated': total_resources,
            'within_limits': total_resources <= 1.0,
            'active_agents': len([p for p in self.agent_priorities.values() if p > 0]),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för meta agent governor.
        
        Returns:
            Dict med statistik
        """
        return {
            'managed_agents': len(self.agent_priorities),
            'total_resources_allocated': sum(self.resource_allocation.values()),
            'governance_decisions': len(self.governance_decisions),
            'max_active_agents': self.max_active_agents
        }
