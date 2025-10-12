"""
SelfCritique - Huvudklass för felanalys och introspektion

Denna klass ansvarar för:
- Analys av egna beslut
- Identifiering av misstag
- Post-mortem analys
- Självlärande och förbättring
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class SelfCritique:
    """
    SelfCritique hanterar felanalys och introspektion.
    
    Attributes:
        min_confidence_for_review (float): Minsta konfidensnivå för granskning
        review_history (List): Historik över granskningar
    """
    
    def __init__(self, min_confidence_for_review: float = 60.0):
        """
        Initierar SelfCritique.
        
        Args:
            min_confidence_for_review: Minsta konfidensnivå för att granska beslut
        """
        self.min_confidence_for_review = min_confidence_for_review
        self.review_history: List[Dict[str, Any]] = []
        self.error_patterns: Dict[str, int] = {}
        logger.info(f"SelfCritique initierad med min_confidence={min_confidence_for_review}")
    
    def analyze_decision(self, decision: Dict[str, Any], outcome: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar ett beslut mot dess utfall.
        
        Args:
            decision: Det ursprungliga beslutet
            outcome: Utfallet av beslutet
        
        Returns:
            Dict med analys
        """
        logger.info(f"Analyserar beslut för {decision.get('symbol', 'unknown')}")
        
        # Kodstub - implementeras senare med faktisk analys
        was_correct = outcome.get('success', False)
        confidence = decision.get('confidence', 0)
        
        review = {
            'decision': decision,
            'outcome': outcome,
            'was_correct': was_correct,
            'confidence_appropriate': confidence >= self.min_confidence_for_review,
            'timestamp': datetime.now().isoformat()
        }
        
        self.review_history.append(review)
        
        if not was_correct:
            error_type = decision.get('decision_type', 'unknown')
            self.error_patterns[error_type] = self.error_patterns.get(error_type, 0) + 1
        
        return review
    
    def identify_patterns(self) -> Dict[str, Any]:
        """
        Identifierar systematiska felmönster.
        
        Returns:
            Dict med identifierade mönster
        """
        # Kodstub
        return {
            'error_patterns': self.error_patterns,
            'total_reviews': len(self.review_history),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_improvement_suggestions(self) -> List[str]:
        """
        Genererar förbättringsförslag baserat på analys.
        
        Returns:
            Lista med förslag
        """
        # Kodstub
        suggestions = []
        
        if len(self.review_history) > 0:
            correct_count = sum(1 for r in self.review_history if r['was_correct'])
            accuracy = correct_count / len(self.review_history)
            
            if accuracy < 0.5:
                suggestions.append("Övergripande träffsäkerhet under 50% - överväg strategirevision")
        
        for error_type, count in self.error_patterns.items():
            if count > 5:
                suggestions.append(f"Många fel av typ '{error_type}' - granska denna strategi")
        
        return suggestions
    
    def post_mortem(self, trade_id: str) -> Dict[str, Any]:
        """
        Utför post-mortem analys av en trade.
        
        Args:
            trade_id: ID för trade att analysera
        
        Returns:
            Dict med post-mortem analys
        """
        # Kodstub
        logger.info(f"Utför post-mortem för trade {trade_id}")
        return {
            'trade_id': trade_id,
            'analysis': 'Post-mortem analys',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för self critique.
        
        Returns:
            Dict med statistik
        """
        if len(self.review_history) == 0:
            return {
                'total_reviews': 0,
                'accuracy': 0.0,
                'error_patterns': {}
            }
        
        correct_count = sum(1 for r in self.review_history if r['was_correct'])
        return {
            'total_reviews': len(self.review_history),
            'accuracy': correct_count / len(self.review_history),
            'error_patterns': self.error_patterns
        }
