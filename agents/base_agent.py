"""
Base Agent - Basklass för alla agenter i Obscuraflow

Denna klass definierar det gemensamma gränssnittet som alla agenter måste implementera.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum


logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Typer av agenter"""
    CLASSIC = "classic"
    PARADIGMATIC = "paradigmatic"
    HYBRID = "hybrid"
    SPAN_HYBRID = "span_hybrid"
    META = "meta"


class DecisionType(Enum):
    """Typer av beslut"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class BaseAgent(ABC):
    """
    Basklass för alla agenter.
    
    Attributes:
        agent_id (str): Unikt ID för agenten
        agent_type (AgentType): Typ av agent
        confidence_threshold (float): Tröskelvärde för beslut
        performance_history (List): Historik över prestationer
    """
    
    def __init__(
        self, 
        agent_id: str, 
        agent_type: AgentType = AgentType.CLASSIC,
        confidence_threshold: float = 0.6,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Initierar BaseAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            agent_type: Typ av agent
            confidence_threshold: Tröskelvärde för beslut
            parameters: Agentspecifika parametrar
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.confidence_threshold = confidence_threshold
        self.parameters = parameters or {}
        self.performance_history: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        self.total_decisions = 0
        self.successful_decisions = 0
        
        logger.info(f"Initierade agent {agent_id} av typ {agent_type.value}")
    
    @abstractmethod
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar en symbol och returnerar ett beslut.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata för symbolen
        
        Returns:
            Dict med beslut, confidence och reasoning
        """
        pass
    
    def record_decision(self, decision: Dict[str, Any], outcome: Optional[float] = None):
        """
        Registrerar ett beslut och dess utfall.
        
        Args:
            decision: Beslutet som togs
            outcome: Utfall (1.0 = framgång, 0.0 = misslyckande)
        """
        self.total_decisions += 1
        
        if outcome is not None:
            if outcome > 0.5:
                self.successful_decisions += 1
            
            self.performance_history.append({
                'timestamp': datetime.now().isoformat(),
                'decision': decision,
                'outcome': outcome
            })
        
        # Begränsa historiklängd
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
    
    def get_performance_score(self) -> float:
        """
        Beräknar agentens prestandascore.
        
        Returns:
            Score mellan 0 och 1
        """
        if self.total_decisions == 0:
            return 0.5  # Neutral score vid ingen historik
        
        return self.successful_decisions / self.total_decisions
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Returnerar statistik för agenten.
        
        Returns:
            Dict med statistik
        """
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type.value,
            'confidence_threshold': self.confidence_threshold,
            'total_decisions': self.total_decisions,
            'successful_decisions': self.successful_decisions,
            'performance_score': self.get_performance_score(),
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.agent_id} (score={self.get_performance_score():.2f})>"
