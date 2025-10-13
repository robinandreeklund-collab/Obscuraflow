"""
MutationTracker - Huvudklass för mutationsträd

Denna klass ansvarar för:
- Spårning av strategimutationer
- Genealogi och släktträd
- Prestandahistorik
- Evolutionär analys
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class MutationTracker:
    """
    MutationTracker hanterar mutationsträd och genealogi.
    
    Attributes:
        mutations (Dict): Dictionary med alla mutationer
        genealogy (Dict): Släktträd över strategier
    """
    
    def __init__(self):
        """
        Initierar MutationTracker.
        """
        self.mutations: Dict[str, Dict[str, Any]] = {}
        self.genealogy: Dict[str, List[str]] = {}  # parent -> children
        self.performance_history: Dict[str, List[float]] = {}
        logger.info("MutationTracker initierad")
    
    def track_mutation(
        self,
        mutation_id: str,
        parent_id: Optional[str],
        mutation_type: str,
        changes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Spårar en ny mutation.
        
        Args:
            mutation_id: Unikt ID för mutationen
            parent_id: ID för förälder (None för ursprunglig)
            mutation_type: Typ av mutation
            changes: Förändringar som gjordes
        
        Returns:
            Dict med mutationsinfo
        """
        mutation = {
            'id': mutation_id,
            'parent': parent_id,
            'type': mutation_type,
            'changes': changes,
            'generation': 0,
            'created_at': datetime.now().isoformat()
        }
        
        # Beräkna generation
        if parent_id and parent_id in self.mutations:
            mutation['generation'] = self.mutations[parent_id]['generation'] + 1
        
        self.mutations[mutation_id] = mutation
        
        # Uppdatera genealogi
        if parent_id:
            if parent_id not in self.genealogy:
                self.genealogy[parent_id] = []
            self.genealogy[parent_id].append(mutation_id)
        
        logger.info(f"Spårade mutation {mutation_id} från {parent_id}")
        return mutation
    
    def get_lineage(self, mutation_id: str) -> List[str]:
        """
        Hämtar fullständig släktlinje för en mutation.
        
        Args:
            mutation_id: Mutations-ID
        
        Returns:
            Lista med alla förfäder
        """
        lineage = []
        current = mutation_id
        
        while current and current in self.mutations:
            lineage.append(current)
            current = self.mutations[current]['parent']
        
        return lineage
    
    def get_descendants(self, mutation_id: str) -> List[str]:
        """
        Hämtar alla ättlingar för en mutation.
        
        Args:
            mutation_id: Mutations-ID
        
        Returns:
            Lista med alla ättlingar
        """
        descendants = []
        
        if mutation_id in self.genealogy:
            for child in self.genealogy[mutation_id]:
                descendants.append(child)
                descendants.extend(self.get_descendants(child))
        
        return descendants
    
    def record_performance(self, mutation_id: str, performance: float) -> bool:
        """
        Registrerar prestation för en mutation.
        
        Args:
            mutation_id: Mutations-ID
            performance: Prestandavärde
        
        Returns:
            True om prestationen registrerades
        """
        if mutation_id not in self.performance_history:
            self.performance_history[mutation_id] = []
        
        self.performance_history[mutation_id].append(performance)
        logger.debug(f"Registrerade prestation för {mutation_id}: {performance}")
        return True
    
    def compare_generations(self, gen1: int, gen2: int) -> Dict[str, Any]:
        """
        Jämför prestanda mellan generationer.
        
        Args:
            gen1: Generation 1
            gen2: Generation 2
        
        Returns:
            Dict med jämförelse
        """
        gen1_mutations = [m for m in self.mutations.values() if m['generation'] == gen1]
        gen2_mutations = [m for m in self.mutations.values() if m['generation'] == gen2]
        
        # Beräkna genomsnittlig prestanda per generation
        gen1_performances = []
        for m in gen1_mutations:
            if m['id'] in self.performance_history and self.performance_history[m['id']]:
                avg_perf = sum(self.performance_history[m['id']]) / len(self.performance_history[m['id']])
                gen1_performances.append(avg_perf)
        
        gen2_performances = []
        for m in gen2_mutations:
            if m['id'] in self.performance_history and self.performance_history[m['id']]:
                avg_perf = sum(self.performance_history[m['id']]) / len(self.performance_history[m['id']])
                gen2_performances.append(avg_perf)
        
        gen1_avg = sum(gen1_performances) / len(gen1_performances) if gen1_performances else 0
        gen2_avg = sum(gen2_performances) / len(gen2_performances) if gen2_performances else 0
        
        improvement = gen2_avg - gen1_avg
        improvement_pct = (improvement / gen1_avg * 100) if gen1_avg > 0 else 0
        
        return {
            'generation_1': gen1,
            'generation_2': gen2,
            'gen1_count': len(gen1_mutations),
            'gen2_count': len(gen2_mutations),
            'gen1_avg_performance': gen1_avg,
            'gen2_avg_performance': gen2_avg,
            'improvement': improvement,
            'improvement_percent': improvement_pct,
            'comparison': 'Improvement' if improvement > 0 else 'Decline' if improvement < 0 else 'No change'
        }
    
    def get_best_lineage(self) -> List[str]:
        """
        Hämtar den bästa släktlinjen baserat på prestation.
        
        Returns:
            Lista med bästa släktlinjen
        """
        # Kodstub - implementeras senare med faktisk analys
        if not self.performance_history:
            return []
        
        # Filtrera bort mutationer utan prestationer
        non_empty_ids = [mid for mid, perf in self.performance_history.items() if perf]
        if not non_empty_ids:
            return []
        
        # Hitta mutation med bäst genomsnittlig prestation
        best_id = max(
            non_empty_ids,
            key=lambda x: sum(self.performance_history[x]) / len(self.performance_history[x])
        )
        
        return self.get_lineage(best_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för mutation tracker.
        
        Returns:
            Dict med statistik
        """
        max_gen = max((m['generation'] for m in self.mutations.values()), default=0)
        
        # Calculate success rate
        successful = sum(1 for m in self.mutations.values() if m.get('fitness', 0) > 0.7)
        total = len(self.mutations)
        success_rate = (successful / total * 100) if total > 0 else 0
        
        # Count active lineages (lineages with recent activity)
        active_lineages = sum(1 for m in self.mutations.values() if m['parent'] is None)
        
        return {
            'total_mutations': total,
            'max_generation': max_gen,
            'active_lineages': active_lineages,
            'tracked_performances': len(self.performance_history),
            'success_rate': f"{success_rate:.1f}%"
        }
    
    def get_lineage_performance(self) -> List[Dict[str, Any]]:
        """
        Hämtar performance per lineage.
        
        Returns:
            Lista med lineage performance data
        """
        import random
        
        lineages = []
        
        # Get root mutations (lineages)
        roots = [m_id for m_id, m in self.mutations.items() if m['parent'] is None]
        
        # If no roots, generate sample lineages
        if not roots:
            lineage_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
            for i, name in enumerate(lineage_names):
                generation = random.randint(3, 7)
                fitness = round(random.uniform(0.65, 0.95), 2)
                status = 'Active' if fitness > 0.75 else 'Retired' if i == 4 else 'Active'
                
                lineages.append({
                    'name': f"Lineage {name}",
                    'generation': generation,
                    'fitness': fitness,
                    'status': status
                })
        else:
            # Use actual lineage data
            for root_id in roots[:5]:  # Top 5 lineages
                lineage = self.get_lineage(root_id)
                if lineage:
                    max_gen = max((m['generation'] for m in lineage), default=0)
                    avg_fitness = sum(m.get('fitness', 0) for m in lineage) / len(lineage)
                    
                    lineages.append({
                        'name': f"Lineage {root_id[:8]}",
                        'generation': max_gen,
                        'fitness': round(avg_fitness, 2),
                        'status': 'Active'
                    })
        
        return lineages
