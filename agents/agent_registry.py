"""
Agent Registry - Centralt register för alla agenter i Obscuraflow

Detta register hanterar:
- Registrering av agenter
- Metadata och beskrivningar
- Agent discovery
- Agentinstansiering
"""

import logging
from typing import Dict, List, Any, Optional, Type
from agents.base_agent import BaseAgent, AgentType

# Import alla agents
from agents.classic.momentum_agent import MomentumAgent
from agents.classic.reversal_agent import ReversalAgent
from agents.classic.breakout_agent import BreakoutAgent
from agents.classic.hybrid_agent import HybridAgent

from agents.paradigms.echo_agent import EchoAgent
from agents.paradigms.fractalis_agent import FractalisAgent
from agents.paradigms.vox_agent import VoxAgent
from agents.paradigms.myco_agent import MycoAgent
from agents.paradigms.obscura_agent import ObscuraAgent
from agents.paradigms.mirage_agent import MirageAgent
from agents.paradigms.sentio_agent import SentioAgent
from agents.paradigms.reflexion_agent import ReflexionAgent
from agents.paradigms.dimensio_agent import DimensioAgent
from agents.paradigms.symbio_agent import SymbioAgent
from agents.paradigms.genesis_agent import GenesisAgent
from agents.paradigms.architectum_agent import ArchitectumAgent


logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    AgentRegistry hanterar registrering och metadata för alla agenter.
    
    Attributes:
        agents (Dict): Register över alla tillgängliga agenter
        instances (Dict): Aktiva agentinstanser
    """
    
    # Agentdefinitioner med metadata
    AGENT_CATALOG = {
        # Klassiska agenter
        'momentum_agent': {
            'class': MomentumAgent,
            'type': AgentType.CLASSIC,
            'name': 'MomentumAgent',
            'description': 'Identifierar och rider på starka prisrörelser',
            'strategy': 'Trendföljande',
            'span_preference': 'Kort (<5 min)',
            'confidence_threshold': 0.6
        },
        'reversal_agent': {
            'class': ReversalAgent,
            'type': AgentType.CLASSIC,
            'name': 'ReversalAgent',
            'description': 'Söker överköpta/översålda tillstånd för vändningar',
            'strategy': 'Mean reversion',
            'span_preference': 'Medel (5–30 min)',
            'confidence_threshold': 0.65
        },
        'breakout_agent': {
            'class': BreakoutAgent,
            'type': AgentType.CLASSIC,
            'name': 'BreakoutAgent',
            'description': 'Reagerar på prisgenombrott från konsolidering',
            'strategy': 'Volatility breakout',
            'span_preference': 'Lång (>30 min)',
            'confidence_threshold': 0.7
        },
        'hybrid_agent': {
            'class': HybridAgent,
            'type': AgentType.CLASSIC,
            'name': 'HybridAgent',
            'description': 'Växlar mellan strategier beroende på marknadsregim',
            'strategy': 'Multi-strategi',
            'span_preference': 'Adaptiv',
            'confidence_threshold': 0.5
        },
        
        # Paradigmatiska agenter
        'echo_agent': {
            'class': EchoAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'EchoAgent',
            'dimension': 'Temporal/Reflective',
            'description': 'Mönsterreplikering baserat på historik',
            'capacity': '500 historiska mönster, 75% matchtröskel',
            'connections': ['symbol_memory', 'fusion', 'reflexion', 'genesis']
        },
        'fractalis_agent': {
            'class': FractalisAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'FractalisAgent',
            'dimension': 'Spatial-Temporal/Complex',
            'description': 'Fraktalanalys över flera tidsskalor',
            'capacity': '5 samtidiga spans, självlikhetskontroll',
            'connections': ['fusion', 'timespan_engine', 'dimensio', 'architectum']
        },
        'vox_agent': {
            'class': VoxAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'VoxAgent',
            'dimension': 'Social/Collective',
            'description': 'Konsensusbyggare mellan agenter',
            'capacity': '75% rösttröskel, demokratisk beslutslogik',
            'connections': ['voteengine', 'metaagent_governor', 'symbio', 'sentio']
        },
        'myco_agent': {
            'class': MycoAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'MycoAgent',
            'dimension': 'Network/Distributed',
            'description': 'Informationsspridning genom agentnätverk',
            'capacity': '3 nivåers nätverksdjup, 85% decay rate',
            'connections': ['synergymatrix', 'symbio', 'portfolioengine']
        },
        'obscura_agent': {
            'class': ObscuraAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'ObscuraAgent',
            'dimension': 'Latent/Obscure',
            'description': 'Identifierar dolda mönster och anomalier',
            'capacity': '2.0σ tröskel för avvikelse',
            'connections': ['fusion', 'mirage', 'reflexion', 'self_critique']
        },
        'mirage_agent': {
            'class': MirageAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'MirageAgent',
            'dimension': 'Perceptual/Discriminative',
            'description': 'Filtrerar falska signaler (illusioner)',
            'capacity': '65% verklighetströskel',
            'connections': ['fusion', 'obscura', 'echo', 'reflexion']
        },
        'sentio_agent': {
            'class': SentioAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'SentioAgent',
            'dimension': 'Emotional/Empathic',
            'description': 'Sentimentanalys och emotionell förstärkning',
            'capacity': '30-period buffer, fear/greed integration',
            'connections': ['sizingsentimentadapter', 'vote_engine', 'vox', 'symbio']
        },
        'reflexion_agent': {
            'class': ReflexionAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'ReflexionAgent',
            'dimension': 'Meta-Cognitive/Reflective',
            'description': 'Självreflektion och adaptivt lärande',
            'capacity': '100 beslutshistorik, justerar baserat på träffsäkerhet',
            'connections': ['self_critique', 'evolution', 'echo', 'mirage']
        },
        'dimensio_agent': {
            'class': DimensioAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'DimensioAgent',
            'dimension': 'Hyper-Spatial/Analytical',
            'description': 'Multi-dimensionell analys',
            'capacity': '5D feature space: momentum, RSI, trend, volym, volatilitet',
            'connections': ['fusion', 'fractalis', 'architectum', 'portfolio_comparator']
        },
        'symbio_agent': {
            'class': SymbioAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'SymbioAgent',
            'dimension': 'Relational/Cooperative',
            'description': 'Samverkan och co-evolution med andra agenter',
            'capacity': '50% symbiosstyrka',
            'connections': ['synergy_matrix', 'vox', 'myco', 'sentio']
        },
        'genesis_agent': {
            'class': GenesisAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'GenesisAgent',
            'dimension': 'Origination/Generative',
            'description': 'Identifierar trendstarter och cykelbörjan',
            'capacity': 'Upptäcker inflektionspunkter och genesis moments',
            'connections': ['forecast_simulator', 'echo', 'architectum', 'fusion']
        },
        'architectum_agent': {
            'class': ArchitectumAgent,
            'type': AgentType.PARADIGMATIC,
            'name': 'ArchitectumAgent',
            'dimension': 'Structural/Constructive',
            'description': 'Strukturell analys och systembyggnad',
            'capacity': '4 nivåer: foundation, pillars, framework, roof',
            'connections': ['fusion', 'dimensio', 'reflexion', 'genesis']
        }
    }
    
    def __init__(self):
        """Initierar AgentRegistry."""
        self.instances: Dict[str, BaseAgent] = {}
        logger.info(f"AgentRegistry initierat med {len(self.AGENT_CATALOG)} agenttyper")
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar information om en agent.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            Dict med agentinformation eller None
        """
        return self.AGENT_CATALOG.get(agent_id)
    
    def list_agents(self, agent_type: Optional[AgentType] = None) -> List[Dict[str, Any]]:
        """
        Listar alla agenter eller agenter av en viss typ.
        
        Args:
            agent_type: Filtrera på agenttyp (valfritt)
        
        Returns:
            Lista med agentinformation
        """
        agents = []
        for agent_id, info in self.AGENT_CATALOG.items():
            if agent_type is None or info['type'] == agent_type:
                agents.append({
                    'id': agent_id,
                    **info
                })
        return agents
    
    def create_agent(self, agent_id: str, **kwargs) -> Optional[BaseAgent]:
        """
        Skapar en agentinstans.
        
        Args:
            agent_id: Agent-ID
            **kwargs: Parametrar till agenten
        
        Returns:
            Agentinstans eller None
        """
        info = self.get_agent_info(agent_id)
        if not info:
            logger.error(f"Agent {agent_id} finns inte i registret")
            return None
        
        try:
            agent_class = info['class']
            instance = agent_class(agent_id=agent_id, **kwargs)
            self.instances[agent_id] = instance
            logger.info(f"Skapade agent {agent_id}")
            return instance
        except Exception as e:
            logger.error(f"Kunde inte skapa agent {agent_id}: {e}")
            return None
    
    def get_instance(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Hämtar en aktiv agentinstans.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            Agentinstans eller None
        """
        return self.instances.get(agent_id)
    
    def get_all_instances(self) -> Dict[str, BaseAgent]:
        """
        Hämtar alla aktiva agentinstanser.
        
        Returns:
            Dict med alla instanser
        """
        return self.instances.copy()
    
    def remove_instance(self, agent_id: str) -> bool:
        """
        Tar bort en agentinstans.
        
        Args:
            agent_id: Agent-ID
        
        Returns:
            True om borttagen
        """
        if agent_id in self.instances:
            del self.instances[agent_id]
            logger.info(f"Tog bort agent {agent_id}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Returnerar statistik för registret.
        
        Returns:
            Dict med statistik
        """
        return {
            'total_agent_types': len(self.AGENT_CATALOG),
            'active_instances': len(self.instances),
            'classic_agents': len([a for a in self.AGENT_CATALOG.values() if a['type'] == AgentType.CLASSIC]),
            'paradigmatic_agents': len([a for a in self.AGENT_CATALOG.values() if a['type'] == AgentType.PARADIGMATIC]),
            'instance_ids': list(self.instances.keys())
        }


# Global registry instance
registry = AgentRegistry()


def get_registry() -> AgentRegistry:
    """
    Hämtar global registry-instans.
    
    Returns:
        AgentRegistry
    """
    return registry
