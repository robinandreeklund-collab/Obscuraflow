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
        logger.info(f"Löser konflikt mellan {len(conflicting_agents)} agenter")
        
        # Välj agent med högst prioritet
        winner = max(
            conflicting_agents,
            key=lambda a: self.agent_priorities.get(a, 0.5)
        )
        
        # Beräkna resolution confidence baserat på prioritetsspread
        priorities = [self.agent_priorities.get(a, 0.5) for a in conflicting_agents]
        priority_spread = max(priorities) - min(priorities)
        confidence = priority_spread  # Ju större skillnad, desto högre confidence
        
        resolution = {
            'conflicting_agents': conflicting_agents,
            'winner': winner,
            'method': 'priority_based',
            'confidence': confidence,
            'rationale': f"Agent {winner} har högst prioritet ({self.agent_priorities.get(winner, 0.5):.2f})",
            'timestamp': datetime.now().isoformat()
        }
        
        # Logga beslutet
        decision = self.make_governance_decision(
            'conflict_resolution',
            conflicting_agents,
            f"Konflikt löst till förmån för {winner}"
        )
        
        logger.info(f"Konflikt löst: vinnare={winner}, confidence={confidence:.2f}")
        return resolution
    
    def rebalance_priorities(self, performance_data: Dict[str, float]) -> Dict[str, float]:
        """
        Ombalanserar prioriteringar baserat på prestation.
        
        Args:
            performance_data: Dict med agent_id -> performance (0-1)
        
        Returns:
            Dict med nya prioriteringar
        """
        new_priorities = {}
        
        # Normalisera prestationsdata så att bästa agenten får högsta möjliga prioritet
        if performance_data:
            max_perf = max(performance_data.values())
            min_perf = min(performance_data.values())
            perf_range = max_perf - min_perf if max_perf > min_perf else 1.0
            
            for agent_id, performance in performance_data.items():
                # Normalized performance scaled to priority range
                normalized_perf = (performance - min_perf) / perf_range if perf_range > 0 else 0.5
                
                # Kombination av befintlig prioritet och performance
                old_priority = self.agent_priorities.get(agent_id, 0.5)
                
                # Exponential moving average: 70% ny performance, 30% gammal
                new_priority = 0.7 * normalized_perf + 0.3 * old_priority
                
                # Clamp till 0-1
                new_priority = max(0.0, min(1.0, new_priority))
                
                new_priorities[agent_id] = new_priority
                self.set_priority(agent_id, new_priority)
        
        logger.info(f"Ombalanserade prioriteringar för {len(new_priorities)} agenter")
        
        # Skapa decision för ombalansering
        self.make_governance_decision(
            'priority_rebalance',
            list(performance_data.keys()),
            f"Ombalansering baserat på prestation"
        )
        
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
        total_resources = sum(self.resource_allocation.values())
        active_high_priority = len([p for p in self.agent_priorities.values() if p > 0.6])
        
        # Identifiera överträdelser
        violations = []
        if total_resources > 1.0:
            violations.append(f"Total resursanvändning överstiger 1.0: {total_resources:.2f}")
        
        if active_high_priority > self.max_active_agents:
            violations.append(f"För många högt prioriterade agenter: {active_high_priority} > {self.max_active_agents}")
        
        # Åtgärda överträdelser
        actions_taken = []
        if total_resources > 1.0:
            # Skala ner alla allokationer proportionellt
            scale_factor = 1.0 / total_resources
            for agent_id in self.resource_allocation:
                self.resource_allocation[agent_id] *= scale_factor
            actions_taken.append(f"Skalade ner resurser med faktor {scale_factor:.3f}")
            logger.warning(f"Skalade ner resursallokering till 100%")
        
        result = {
            'total_resources_allocated': sum(self.resource_allocation.values()),
            'within_limits': len(violations) == 0,
            'violations': violations,
            'actions_taken': actions_taken,
            'active_agents': len([p for p in self.agent_priorities.values() if p > 0]),
            'high_priority_agents': active_high_priority,
            'timestamp': datetime.now().isoformat()
        }
        
        if violations:
            logger.warning(f"Limit violations found: {len(violations)}")
        
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
