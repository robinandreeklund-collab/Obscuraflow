"""
AgentSpectrum - Huvudklass för ontologisk agentförflyttning

Denna klass ansvarar för:
- Ontologisk karta över agenter
- Spårning av agentförflyttning
- Clustering och kategorisering
- Evolution av världsbild
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import math


logger = logging.getLogger(__name__)


class AgentSpectrum:
    """
    AgentSpectrum hanterar ontologisk karta och agentförflyttning.
    
    Attributes:
        agent_positions (Dict): Positioner för agenter i konceptrummet
        dimensions (List[str]): Dimensioner i spektrumet
    """
    
    def __init__(self, dimensions: Optional[List[str]] = None):
        """
        Initierar AgentSpectrum.
        
        Args:
            dimensions: Lista över dimensioner i spektrumet
        """
        self.dimensions = dimensions or [
            'risk_tolerance',
            'time_horizon',
            'analytical_depth',
            'emotional_bias',
            'adaptability'
        ]
        self.agent_positions: Dict[str, List[float]] = {}
        self.position_history: Dict[str, List[Dict[str, Any]]] = {}
        logger.info(f"AgentSpectrum initierad med dimensioner: {self.dimensions}")
    
    def place_agent(self, agent_id: str, position: List[float]) -> bool:
        """
        Placerar en agent i spektrumet.
        
        Args:
            agent_id: Agent-ID
            position: Position i alla dimensioner (0-1 för varje)
        
        Returns:
            True om agenten placerades
        """
        if len(position) != len(self.dimensions):
            logger.error(f"Position måste ha {len(self.dimensions)} dimensioner")
            return False
        
        # Validera att alla värden är 0-1
        if not all(0 <= p <= 1 for p in position):
            logger.error("Alla positioner måste vara mellan 0 och 1")
            return False
        
        self.agent_positions[agent_id] = position
        
        # Spara i historik
        if agent_id not in self.position_history:
            self.position_history[agent_id] = []
        
        self.position_history[agent_id].append({
            'position': position.copy(),
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Placerade agent {agent_id} i spektrumet")
        return True
    
    def move_agent(self, agent_id: str, dimension: str, delta: float) -> bool:
        """
        Flyttar en agent längs en dimension.
        
        Args:
            agent_id: Agent-ID
            dimension: Dimension att flytta i
            delta: Förändring (-1 till 1)
        
        Returns:
            True om agenten flyttades
        """
        if agent_id not in self.agent_positions:
            logger.error(f"Agent {agent_id} finns inte i spektrumet")
            return False
        
        if dimension not in self.dimensions:
            logger.error(f"Dimension {dimension} finns inte")
            return False
        
        dim_idx = self.dimensions.index(dimension)
        new_value = self.agent_positions[agent_id][dim_idx] + delta
        
        # Klämma värdet mellan 0 och 1
        new_value = max(0.0, min(1.0, new_value))
        
        self.agent_positions[agent_id][dim_idx] = new_value
        
        # Spara i historik
        self.position_history[agent_id].append({
            'position': self.agent_positions[agent_id].copy(),
            'dimension_moved': dimension,
            'delta': delta,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Flyttade agent {agent_id} i dimension {dimension}")
        return True
    
    def get_distance(self, agent1: str, agent2: str) -> float:
        """
        Beräknar avstånd mellan två agenter i spektrumet.
        
        Args:
            agent1: Första agenten
            agent2: Andra agenten
        
        Returns:
            Euklidiskt avstånd
        """
        if agent1 not in self.agent_positions or agent2 not in self.agent_positions:
            return float('inf')
        
        pos1 = self.agent_positions[agent1]
        pos2 = self.agent_positions[agent2]
        
        # Euklidiskt avstånd
        distance = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(pos1, pos2)))
        return distance
    
    def find_nearest_agents(self, agent_id: str, n: int = 3) -> List[Tuple[str, float]]:
        """
        Hittar närmaste agenter i spektrumet.
        
        Args:
            agent_id: Agent-ID
            n: Antal agenter att returnera
        
        Returns:
            Lista med (agent_id, distance)
        """
        if agent_id not in self.agent_positions:
            return []
        
        distances = []
        for other_id in self.agent_positions:
            if other_id != agent_id:
                distance = self.get_distance(agent_id, other_id)
                distances.append((other_id, distance))
        
        distances.sort(key=lambda x: x[1])
        return distances[:n]
    
    def cluster_agents(self, max_distance: float = 0.3) -> List[List[str]]:
        """
        Clustrar agenter baserat på närhet i spektrumet.
        
        Args:
            max_distance: Max avstånd för att tillhöra samma cluster
        
        Returns:
            Lista med clusters (listor med agent-ID)
        """
        # Implementerad greedy clustering algoritm
        clusters = []
        unclustered = set(self.agent_positions.keys())
        
        while unclustered:
            agent = unclustered.pop()
            cluster = [agent]
            
            # Hitta alla agenter inom max_distance från alla i clustret
            for other in list(unclustered):
                # Kontrollera avstånd till alla i befintligt cluster
                distances_to_cluster = [
                    self.get_distance(cluster_member, other)
                    for cluster_member in cluster
                ]
                avg_distance = sum(distances_to_cluster) / len(distances_to_cluster)
                
                if avg_distance <= max_distance:
                    cluster.append(other)
                    unclustered.remove(other)
            
            clusters.append(cluster)
        
        if clusters:
            avg_size = sum(len(c) for c in clusters) / len(clusters)
        else:
            avg_size = 0.0
        logger.info(f"Skapade {len(clusters)} clusters (avg size: {avg_size:.1f})")
        return clusters
    
    def get_agent_profile(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar profil för en agent baserat på position.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            Dict med profil
        """
        if agent_id not in self.agent_positions:
            return None
        
        position = self.agent_positions[agent_id]
        nearest = self.find_nearest_agents(agent_id, 3)
        
        # Beräkna rörlighet baserat på historik
        history = self.position_history.get(agent_id, [])
        mobility = 0.0
        if len(history) > 1:
            total_movement = 0.0
            for i in range(1, len(history)):
                prev_pos = history[i-1]['position']
                curr_pos = history[i]['position']
                movement = sum((c - p) ** 2 for c, p in zip(curr_pos, prev_pos)) ** 0.5
                total_movement += movement
            mobility = total_movement / (len(history) - 1)
        
        # Karakterisera agenten baserat på position
        characteristics = {}
        for dim, val in zip(self.dimensions, position):
            if val > 0.7:
                characteristics[dim] = 'high'
            elif val < 0.3:
                characteristics[dim] = 'low'
            else:
                characteristics[dim] = 'medium'
        
        profile = {
            'agent_id': agent_id,
            'position': {dim: val for dim, val in zip(self.dimensions, position)},
            'characteristics': characteristics,
            'mobility_score': mobility,
            'movement_history': len(history),
            'nearest_agents': nearest,
            'is_stable': mobility < 0.1
        }
        
        return profile
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för agent spectrum.
        
        Returns:
            Dict med statistik
        """
        return {
            'total_agents': len(self.agent_positions),
            'dimensions': len(self.dimensions),
            'dimension_names': self.dimensions,
            'total_movements': sum(len(v) for v in self.position_history.values())
        }
