"""
AgentLifecycle - Huvudklass för agentens livscykel

Denna klass ansvarar för:
- Hantering av agentlivscykel
- Födelse och pension
- Aktivering och deaktivering
- Livscykelmetrik
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


logger = logging.getLogger(__name__)


class LifecycleStage(Enum):
    """Stadier i agentens livscykel"""
    CREATED = "created"
    TRAINING = "training"
    ACTIVE = "active"
    DORMANT = "dormant"
    RETIRED = "retired"


class AgentLifecycle:
    """
    AgentLifecycle hanterar agentens livscykel.
    
    Attributes:
        agents (Dict): Dictionary med agenter och deras status
        retirement_threshold (float): Prestandatröskelvärde för pension
    """
    
    def __init__(self, retirement_threshold: float = 0.3, max_age: int = 1000):
        """
        Initierar AgentLifecycle.
        
        Args:
            retirement_threshold: Tröskelvärde för pension (0-1)
            max_age: Max ålder innan automatisk pension
        """
        self.retirement_threshold = retirement_threshold
        self.max_age = max_age
        self.agents: Dict[str, Dict[str, Any]] = {}
        logger.info(f"AgentLifecycle initierad med retirement_threshold={retirement_threshold}")
    
    def birth_agent(self, agent_id: str, agent_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skapar ny agent.
        
        Args:
            agent_id: Unikt ID för agenten
            agent_type: Typ av agent
            parameters: Agentparametrar
        
        Returns:
            Dict med agentinfo
        """
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} finns redan")
            return self.agents[agent_id]
        
        agent = {
            'id': agent_id,
            'type': agent_type,
            'parameters': parameters,
            'stage': LifecycleStage.CREATED.value,
            'age': 0,
            'performance': 0.5,  # Neutral start
            'created_at': datetime.now().isoformat(),
            'last_active': None
        }
        
        self.agents[agent_id] = agent
        logger.info(f"Skapade agent {agent_id} av typ {agent_type}")
        return agent
    
    def activate_agent(self, agent_id: str) -> bool:
        """
        Aktiverar en agent.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            True om agenten aktiverades
        """
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} finns inte")
            return False
        
        agent = self.agents[agent_id]
        
        if agent['stage'] == LifecycleStage.RETIRED.value:
            logger.warning(f"Kan inte aktivera pensionerad agent {agent_id}")
            return False
        
        agent['stage'] = LifecycleStage.ACTIVE.value
        agent['last_active'] = datetime.now().isoformat()
        logger.info(f"Aktiverade agent {agent_id}")
        return True
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """
        Deaktiverar en agent.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            True om agenten deaktiverades
        """
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]['stage'] = LifecycleStage.DORMANT.value
        logger.info(f"Deaktiverade agent {agent_id}")
        return True
    
    def retire_agent(self, agent_id: str, reason: str = "performance") -> bool:
        """
        Pensionerar en agent.
        
        Args:
            agent_id: Agent-ID
            reason: Anledning till pension
        
        Returns:
            True om agenten pensionerades
        """
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]['stage'] = LifecycleStage.RETIRED.value
        self.agents[agent_id]['retirement_reason'] = reason
        self.agents[agent_id]['retired_at'] = datetime.now().isoformat()
        logger.info(f"Pensionerade agent {agent_id}, anledning: {reason}")
        return True
    
    def update_performance(self, agent_id: str, performance: float) -> bool:
        """
        Uppdaterar agentprestation och kontrollerar pensionskrav.
        
        Args:
            agent_id: Agent-ID
            performance: Prestandavärde (0-1)
        
        Returns:
            True om prestationen uppdaterades
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent['performance'] = performance
        agent['age'] += 1
        
        # Kontrollera pensionskrav
        if performance < self.retirement_threshold:
            logger.warning(f"Agent {agent_id} presterar under tröskelvärde")
            self.retire_agent(agent_id, "low_performance")
        elif agent['age'] >= self.max_age:
            self.retire_agent(agent_id, "max_age")
        
        return True
    
    def get_active_agents(self) -> List[str]:
        """
        Hämtar alla aktiva agenter.
        
        Returns:
            Lista med aktiva agent-ID
        """
        return [
            aid for aid, agent in self.agents.items()
            if agent['stage'] == LifecycleStage.ACTIVE.value
        ]
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar status för en agent.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            Dict med status
        """
        if agent_id not in self.agents:
            return None
        
        return self.agents[agent_id].copy()
    
    def get_lifecycle_stats(self) -> Dict[str, Any]:
        """
        Hämtar livscykelstatistik.
        
        Returns:
            Dict med statistik per stage
        """
        stats = {stage.value: 0 for stage in LifecycleStage}
        
        for agent in self.agents.values():
            stats[agent['stage']] += 1
        
        return stats
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för agent lifecycle.
        
        Returns:
            Dict med statistik
        """
        active = len(self.get_active_agents())
        avg_age = sum(a['age'] for a in self.agents.values()) / len(self.agents) if self.agents else 0
        avg_perf = sum(a['performance'] for a in self.agents.values()) / len(self.agents) if self.agents else 0
        
        return {
            'total_agents': len(self.agents),
            'active_agents': active,
            'avg_age': avg_age,
            'avg_performance': avg_perf,
            'lifecycle_distribution': self.get_lifecycle_stats()
        }
