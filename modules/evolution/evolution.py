"""
Evolution - Huvudklass för strategimutation

Denna klass ansvarar för:
- Mutation och evolution av strategier
- Genetiska algoritmer
- Fitness-evaluering
- Strategi-selektion
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import random


logger = logging.getLogger(__name__)


class Evolution:
    """
    Evolution hanterar mutation och evolution av strategier.
    
    Attributes:
        mutation_rate (float): Sannolikhet för mutation (0-1)
        population_size (int): Antal strategier i populationen
    """
    
    def __init__(self, mutation_rate: float = 0.1, population_size: int = 10):
        """
        Initierar Evolution med mutation-parametrar.
        
        Args:
            mutation_rate: Sannolikhet för mutation (0-1)
            population_size: Storlek på strategipopulation
        """
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.strategies: Dict[str, Dict[str, Any]] = {}
        self.generation = 0
        logger.info(f"Evolution initierad med mutation_rate={mutation_rate}")
    
    def create_strategy(self, strategy_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skapar ny strategi.
        
        Args:
            strategy_id: Unikt ID för strategin
            parameters: Strategiparametrar
        
        Returns:
            Dict med strategiinfo
        """
        strategy = {
            'id': strategy_id,
            'parameters': parameters,
            'fitness': 0.0,
            'generation': self.generation,
            'created_at': datetime.now().isoformat()
        }
        
        self.strategies[strategy_id] = strategy
        logger.info(f"Skapade strategi {strategy_id}")
        return strategy
    
    def mutate_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """
        Muterar en strategi.
        
        Args:
            strategy_id: Strategi-ID att mutera
        
        Returns:
            Dict med ny muterad strategi eller None
        """
        if strategy_id not in self.strategies:
            logger.error(f"Strategi {strategy_id} finns inte")
            return None
        
        if random.random() > self.mutation_rate:
            return None  # Ingen mutation denna gång
        
        # Kodstub - implementeras senare med faktisk mutation
        parent = self.strategies[strategy_id]
        mutated_id = f"{strategy_id}_mut_{self.generation}"
        
        mutated_strategy = {
            'id': mutated_id,
            'parameters': parent['parameters'].copy(),  # I verkligheten muteras dessa
            'fitness': 0.0,
            'generation': self.generation,
            'parent': strategy_id,
            'created_at': datetime.now().isoformat()
        }
        
        self.strategies[mutated_id] = mutated_strategy
        logger.info(f"Muterade strategi {strategy_id} till {mutated_id}")
        return mutated_strategy
    
    def evaluate_fitness(self, strategy_id: str, performance: float) -> bool:
        """
        Utvärderar fitness för en strategi.
        
        Args:
            strategy_id: Strategi-ID
            performance: Prestandavärde
        
        Returns:
            True om fitness uppdaterades
        """
        if strategy_id not in self.strategies:
            return False
        
        self.strategies[strategy_id]['fitness'] = performance
        logger.debug(f"Uppdaterade fitness för {strategy_id}: {performance}")
        return True
    
    def evolve_generation(self) -> Dict[str, Any]:
        """
        Evolverar till nästa generation.
        
        Returns:
            Dict med evolutionsresultat
        """
        self.generation += 1
        # Kodstub - implementeras senare med selektion och mutation
        logger.info(f"Evolverade till generation {self.generation}")
        return {
            'generation': self.generation,
            'strategies': len(self.strategies),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_best_strategies(self, n: int = 3) -> List[Dict[str, Any]]:
        """
        Hämtar de bästa strategierna.
        
        Args:
            n: Antal strategier att returnera
        
        Returns:
            Lista med bästa strategier
        """
        sorted_strategies = sorted(
            self.strategies.values(),
            key=lambda x: x['fitness'],
            reverse=True
        )
        return sorted_strategies[:n]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för evolution.
        
        Returns:
            Dict med statistik
        """
        return {
            'generation': self.generation,
            'total_strategies': len(self.strategies),
            'mutation_rate': self.mutation_rate,
            'population_size': self.population_size
        }
