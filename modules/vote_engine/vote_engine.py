"""
VoteEngine - Röstningssystem för agentbeslut

Denna klass ansvarar för:
- Röstning mellan konfliktande agentbeslut
- Viktning baserat på agentprestation
- Meta-voting och beslutsaggregering
- Historik över röstningsutfall
"""

import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


logger = logging.getLogger(__name__)


@dataclass
class Vote:
    """
    Representerar en röst från en agent.
    
    Attributes:
        agent_id: Identifierare för agenten
        vote: Röstval (buy/sell/hold)
        weight: Vikt för rösten baserat på agentprestation
        confidence: Konfidensgrad (0-100)
        timestamp: Tidpunkt för rösten
    """
    agent_id: str
    vote: str
    weight: float = 1.0
    confidence: float = 50.0
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        """Validera och sätt defaults efter init"""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        
        # Validera vote
        valid_votes = ['buy', 'sell', 'hold']
        if self.vote.lower() not in valid_votes:
            raise ValueError(f"Vote måste vara en av {valid_votes}, fick {self.vote}")
        self.vote = self.vote.lower()
        
        # Validera weight
        if self.weight < 0:
            raise ValueError(f"Weight måste vara >= 0, fick {self.weight}")
        
        # Validera confidence
        if not 0 <= self.confidence <= 100:
            raise ValueError(f"Confidence måste vara mellan 0 och 100, fick {self.confidence}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertera till dict för serialisering"""
        return asdict(self)


class VoteEngine:
    """
    VoteEngine hanterar röstning mellan agenter vid beslutskonflikter.
    
    Attributes:
        agent_weights: Dict som mappar agent_id till vikt
        weight_decay: Decay-faktor för viktuppdatering
        learning_rate: Hastighet för viktjustering
    """
    
    def __init__(
        self,
        initial_weight: float = 1.0,
        weight_decay: float = 0.95,
        learning_rate: float = 0.1
    ):
        """
        Initierar VoteEngine.
        
        Args:
            initial_weight: Startvikt för nya agenter
            weight_decay: Decay-faktor för viktuppdatering (0-1)
            learning_rate: Hastighet för viktjustering (0-1)
        """
        self.initial_weight = initial_weight
        self.weight_decay = weight_decay
        self.learning_rate = learning_rate
        
        # Storage
        self.agent_weights: Dict[str, float] = defaultdict(lambda: initial_weight)
        self.vote_history: List[Dict[str, Any]] = []
        self.agent_performance: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {'correct': 0, 'incorrect': 0, 'total': 0}
        )
        
        # Statistik
        self.stats = {
            'total_votes': 0,
            'total_vote_sessions': 0,
            'unanimous_decisions': 0,
            'split_decisions': 0
        }
        
        logger.info(
            f"VoteEngine initialiserad (initial_weight={initial_weight}, "
            f"weight_decay={weight_decay}, learning_rate={learning_rate})"
        )
    
    def add_vote(self, vote: Vote) -> bool:
        """
        Lägger till en röst från en agent.
        
        Args:
            vote: Vote objekt
        
        Returns:
            True om rösten accepterades
        """
        # Sätt vikt från agent_weights om den finns
        vote.weight = self.agent_weights[vote.agent_id]
        
        self.stats['total_votes'] += 1
        
        logger.debug(
            f"Röst från {vote.agent_id}: {vote.vote} "
            f"(weight={vote.weight:.2f}, confidence={vote.confidence})"
        )
        
        return True
    
    def calculate_weighted_vote(
        self, 
        votes: List[Vote],
        symbol: str
    ) -> Dict[str, Any]:
        """
        Beräknar vägd röstning för en lista av röster.
        
        Args:
            votes: Lista med Vote-objekt
            symbol: Symbol som röstningen gäller
        
        Returns:
            Dict med röstningsresultat
        """
        if not votes:
            logger.warning(f"Inga röster att beräkna för {symbol}")
            return {
                'symbol': symbol,
                'winner': None,
                'total_votes': 0,
                'vote_breakdown': {}
            }
        
        self.stats['total_vote_sessions'] += 1
        
        # Beräkna viktad summa per valalternativ
        weighted_totals = defaultdict(float)
        vote_counts = defaultdict(int)
        confidence_totals = defaultdict(float)
        
        for vote in votes:
            # Viktad poäng = weight * confidence/100
            weighted_score = vote.weight * (vote.confidence / 100)
            weighted_totals[vote.vote] += weighted_score
            vote_counts[vote.vote] += 1
            confidence_totals[vote.vote] += vote.confidence
        
        # Hitta vinnaren
        if not weighted_totals:
            winner = None
        else:
            winner = max(weighted_totals.items(), key=lambda x: x[1])
            winner = winner[0]
        
        # Kontrollera om beslutet är enhälligt
        unique_votes = len(set(v.vote for v in votes))
        is_unanimous = unique_votes == 1
        
        if is_unanimous:
            self.stats['unanimous_decisions'] += 1
        else:
            self.stats['split_decisions'] += 1
        
        # Bygg resultat
        result = {
            'symbol': symbol,
            'winner': winner,
            'total_votes': len(votes),
            'is_unanimous': is_unanimous,
            'vote_breakdown': {
                vote_type: {
                    'count': vote_counts[vote_type],
                    'weighted_score': round(weighted_totals[vote_type], 2),
                    'average_confidence': round(
                        confidence_totals[vote_type] / vote_counts[vote_type], 2
                    ) if vote_counts[vote_type] > 0 else 0
                }
                for vote_type in weighted_totals.keys()
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Logga till historik
        self.vote_history.append({
            **result,
            'votes': [v.to_dict() for v in votes]
        })
        
        logger.info(
            f"Röstningsresultat för {symbol}: {winner} "
            f"({'enhälligt' if is_unanimous else 'delat'})"
        )
        
        return result
    
    def update_agent_weight(
        self,
        agent_id: str,
        was_correct: bool,
        performance_boost: float = 1.2,
        performance_penalty: float = 0.8
    ) -> float:
        """
        Uppdaterar en agents vikt baserat på prestation.
        
        Args:
            agent_id: Agent identifierare
            was_correct: Om agentens beslut var korrekt
            performance_boost: Multiplikator för korrekta beslut
            performance_penalty: Multiplikator för felaktiga beslut
        
        Returns:
            Nya vikten för agenten
        """
        current_weight = self.agent_weights[agent_id]
        
        # Uppdatera prestationsstatistik
        self.agent_performance[agent_id]['total'] += 1
        if was_correct:
            self.agent_performance[agent_id]['correct'] += 1
            # Öka vikt vid korrekt beslut
            new_weight = current_weight * performance_boost
        else:
            self.agent_performance[agent_id]['incorrect'] += 1
            # Minska vikt vid felaktigt beslut
            new_weight = current_weight * performance_penalty
        
        # Applicera learning rate och decay
        adjusted_weight = (
            current_weight + 
            self.learning_rate * (new_weight - current_weight)
        ) * self.weight_decay
        
        # Sätt minimum på 0.1 för att inte eliminera agenter helt
        adjusted_weight = max(0.1, adjusted_weight)
        
        self.agent_weights[agent_id] = adjusted_weight
        
        logger.info(
            f"Agent {agent_id} vikt uppdaterad: "
            f"{current_weight:.2f} → {adjusted_weight:.2f} "
            f"({'korrekt' if was_correct else 'felaktig'})"
        )
        
        return adjusted_weight
    
    def get_agent_weight(self, agent_id: str) -> float:
        """
        Hämtar vikten för en agent.
        
        Args:
            agent_id: Agent identifierare
        
        Returns:
            Agentens aktuella vikt
        """
        return self.agent_weights[agent_id]
    
    def get_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """
        Hämtar prestationsstatistik för en agent.
        
        Args:
            agent_id: Agent identifierare
        
        Returns:
            Dict med prestationsdata
        """
        perf = self.agent_performance[agent_id]
        total = perf['total']
        
        if total == 0:
            accuracy = 0.0
        else:
            accuracy = (perf['correct'] / total) * 100
        
        return {
            'agent_id': agent_id,
            'weight': self.agent_weights[agent_id],
            'correct': perf['correct'],
            'incorrect': perf['incorrect'],
            'total': total,
            'accuracy': round(accuracy, 2)
        }
    
    def get_all_agent_performances(self) -> List[Dict[str, Any]]:
        """
        Hämtar prestationsstatistik för alla agenter.
        
        Returns:
            Lista med prestationsdata för alla agenter
        """
        agents = set(list(self.agent_weights.keys()) + list(self.agent_performance.keys()))
        performances = []
        
        for agent_id in agents:
            performances.append(self.get_agent_performance(agent_id))
        
        # Sortera efter vikt
        performances.sort(key=lambda x: x['weight'], reverse=True)
        
        return performances
    
    def reset_agent_weight(self, agent_id: str) -> float:
        """
        Återställer en agents vikt till initial_weight.
        
        Args:
            agent_id: Agent identifierare
        
        Returns:
            Den nya vikten
        """
        self.agent_weights[agent_id] = self.initial_weight
        logger.info(f"Agent {agent_id} vikt återställd till {self.initial_weight}")
        return self.initial_weight
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för VoteEngine.
        
        Returns:
            Dict med statistik
        """
        return {
            **self.stats,
            'total_agents': len(self.agent_weights),
            'vote_sessions_in_history': len(self.vote_history)
        }
