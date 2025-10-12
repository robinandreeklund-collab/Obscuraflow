"""
SynergyMatrix - Huvudklass för agent-samverkan och konfliktanalys

Denna klass ansvarar för:
- Analys av agentsamverkan
- Konfliktdetektion
- Synergimatris
- Samarbetsmönster
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime


logger = logging.getLogger(__name__)


class SynergyMatrix:
    """
    SynergyMatrix hanterar agent-samverkan och konfliktanalys.
    
    Attributes:
        matrix (Dict): Synergimatris mellan agentpar
        conflicts (List): Lista över detekterade konflikter
    """
    
    def __init__(self):
        """
        Initierar SynergyMatrix.
        """
        self.matrix: Dict[Tuple[str, str], float] = {}
        self.conflicts: List[Dict[str, Any]] = []
        self.collaboration_history: Dict[str, List[Dict[str, Any]]] = {}
        logger.info("SynergyMatrix initierad")
    
    def record_interaction(
        self,
        agent1: str,
        agent2: str,
        interaction_type: str,
        outcome: float
    ) -> bool:
        """
        Registrerar interaktion mellan två agenter.
        
        Args:
            agent1: Första agenten
            agent2: Andra agenten
            interaction_type: Typ av interaktion ('agreement', 'conflict', 'neutral')
            outcome: Utfall av interaktionen (-1 till 1)
        
        Returns:
            True om interaktionen registrerades
        """
        # Normalisera ordning så a-b == b-a
        pair = tuple(sorted([agent1, agent2]))
        
        # Uppdatera matris
        if pair not in self.matrix:
            self.matrix[pair] = 0.0
        
        # Exponentiell medelvärde för att väga nyare interaktioner högre
        alpha = 0.3
        self.matrix[pair] = alpha * outcome + (1 - alpha) * self.matrix[pair]
        
        # Spara i historik
        key = f"{agent1}_{agent2}"
        if key not in self.collaboration_history:
            self.collaboration_history[key] = []
        
        self.collaboration_history[key].append({
            'type': interaction_type,
            'outcome': outcome,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.debug(f"Registrerade interaktion mellan {agent1} och {agent2}: {interaction_type}")
        return True
    
    def detect_conflict(self, agent1: str, agent2: str, threshold: float = -0.3) -> bool:
        """
        Detekterar konflikt mellan två agenter.
        
        Args:
            agent1: Första agenten
            agent2: Andra agenten
            threshold: Tröskelvärde för konflikt (negativt värde)
        
        Returns:
            True om konflikt detekterades
        """
        pair = tuple(sorted([agent1, agent2]))
        
        if pair not in self.matrix:
            return False
        
        if self.matrix[pair] < threshold:
            conflict = {
                'agent1': agent1,
                'agent2': agent2,
                'synergy_score': self.matrix[pair],
                'timestamp': datetime.now().isoformat()
            }
            self.conflicts.append(conflict)
            logger.warning(f"Konflikt detekterad mellan {agent1} och {agent2}")
            return True
        
        return False
    
    def get_synergy(self, agent1: str, agent2: str) -> float:
        """
        Hämtar synergiscore mellan två agenter.
        
        Args:
            agent1: Första agenten
            agent2: Andra agenten
        
        Returns:
            Synergiscore (-1 till 1)
        """
        pair = tuple(sorted([agent1, agent2]))
        return self.matrix.get(pair, 0.0)
    
    def get_best_partners(self, agent: str, n: int = 3) -> List[Tuple[str, float]]:
        """
        Hämtar bästa samarbetspartners för en agent.
        
        Args:
            agent: Agentnamn
            n: Antal partners att returnera
        
        Returns:
            Lista med (partner, synergy_score)
        """
        partners = []
        
        for (a1, a2), score in self.matrix.items():
            if agent in (a1, a2):
                partner = a2 if a1 == agent else a1
                partners.append((partner, score))
        
        partners.sort(key=lambda x: x[1], reverse=True)
        
        if partners:
            logger.info(f"Hittade {len(partners)} partners för {agent}, bästa: {partners[0][0]} (score={partners[0][1]:.3f})")
        
        return partners[:n]
    
    def get_conflict_agents(self, agent: str, threshold: float = -0.3) -> List[str]:
        """
        Hämtar agenter som en agent är i konflikt med.
        
        Args:
            agent: Agentnamn
            threshold: Tröskelvärde för konflikt
        
        Returns:
            Lista med konflikt-agenter
        """
        conflicts = []
        
        for (a1, a2), score in self.matrix.items():
            if score < threshold and agent in (a1, a2):
                conflict_agent = a2 if a1 == agent else a1
                conflicts.append(conflict_agent)
        
        if conflicts:
            logger.warning(f"Agent {agent} har {len(conflicts)} konfliktande agenter")
        
        return conflicts
    
    def get_matrix_summary(self) -> Dict[str, Any]:
        """
        Hämtar sammanfattning av synergimatrisen.
        
        Returns:
            Dict med sammanfattning
        """
        if not self.matrix:
            return {
                'total_pairs': 0,
                'avg_synergy': 0.0,
                'high_synergy_pairs': 0,
                'conflict_pairs': 0,
                'neutral_pairs': 0
            }
        
        scores = list(self.matrix.values())
        avg_synergy = sum(scores) / len(scores)
        high_synergy = sum(1 for s in scores if s > 0.5)
        conflict_pairs = sum(1 for s in scores if s < -0.3)
        neutral_pairs = sum(1 for s in scores if -0.3 <= s <= 0.5)
        
        # Beräkna standard deviation för synergifördelning
        if len(scores) > 1:
            variance = sum((s - avg_synergy) ** 2 for s in scores) / len(scores)
            std_dev = variance ** 0.5
        else:
            std_dev = 0.0
        
        return {
            'total_pairs': len(self.matrix),
            'avg_synergy': avg_synergy,
            'std_dev_synergy': std_dev,
            'high_synergy_pairs': high_synergy,
            'conflict_pairs': conflict_pairs,
            'neutral_pairs': neutral_pairs,
            'synergy_distribution': {
                'positive': high_synergy,
                'neutral': neutral_pairs,
                'negative': conflict_pairs
            }
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för synergy matrix.
        
        Returns:
            Dict med statistik
        """
        return {
            'total_agent_pairs': len(self.matrix),
            'total_conflicts': len(self.conflicts),
            'total_interactions': sum(len(v) for v in self.collaboration_history.values()),
            **self.get_matrix_summary()
        }
