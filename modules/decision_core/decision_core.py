"""
DecisionCore - Central beslutsmotor för agentbeslut

Denna klass ansvarar för:
- Samling och validering av agentbeslut
- Routing av beslut till rätt moduler
- Loggning av beslutshierarki
- Konflikthantering och eskalering
"""

import logging
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Typer av beslut som agenter kan ta"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


@dataclass
class AgentDecision:
    """
    Representerar ett beslut från en agent.
    
    Attributes:
        agent_id: Identifierare för agenten
        symbol: Tickersymbol beslutet gäller
        decision: Typ av beslut (buy/sell/hold)
        confidence: Konfidensgrad (0-100)
        reasoning: Textförklaring av beslutet
        timestamp: Tidpunkt för beslutet
        metadata: Extra data från agenten
    """
    agent_id: str
    symbol: str
    decision: DecisionType
    confidence: float
    reasoning: str = ""
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validera och sätt defaults efter init"""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}
        
        # Validera confidence
        if not 0 <= self.confidence <= 100:
            raise ValueError(f"Confidence måste vara mellan 0 och 100, fick {self.confidence}")
        
        # Konvertera string till DecisionType om nödvändigt
        if isinstance(self.decision, str):
            self.decision = DecisionType(self.decision.lower())
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertera till dict för serialisering"""
        result = asdict(self)
        result['decision'] = self.decision.value
        return result


class DecisionCore:
    """
    DecisionCore samlar och processar agentbeslut.
    
    Attributes:
        min_confidence: Minsta konfidensgrad för att acceptera beslut
        conflict_threshold: Tröskelvärde för att identifiera konflikt
    """
    
    def __init__(
        self,
        min_confidence: float = 50.0,
        conflict_threshold: float = 0.5,
        use_live_data: bool = True
    ):
        """
        Initierar DecisionCore.
        
        Args:
            min_confidence: Minsta konfidensgrad (0-100)
            conflict_threshold: Andel motsatta beslut för konflikt (0-1)
            use_live_data: Om True, använd live data från DataStream och agenter
        """
        self.min_confidence = min_confidence
        self.conflict_threshold = conflict_threshold
        self.use_live_data = use_live_data
        
        # Storage för beslut
        self.decisions: List[AgentDecision] = []
        self.decision_history: List[Dict[str, Any]] = []
        
        # Statistik
        self.stats = {
            'total_decisions': 0,
            'accepted_decisions': 0,
            'rejected_decisions': 0,
            'conflicts_detected': 0,
            'buy_count': 0,
            'sell_count': 0,
            'hold_count': 0,
            'consensus_count': 0,
            'conflict_count': 0
        }
        
        # Initialize agents and data stream if using live data
        if use_live_data:
            self._initialize_live_system()
        
        logger.info(
            f"DecisionCore initialiserad (min_confidence={min_confidence}, "
            f"conflict_threshold={conflict_threshold}, use_live_data={use_live_data})"
        )
    
    # REMOVED: Sample decision generation is no longer used.
    # All decisions must come from live agents analyzing real market data.
    
    def _initialize_live_system(self) -> None:
        """
        Initialiserar live-systemet med DataStream och agenter.
        """
        try:
            # Import här för att undvika cirkulära imports
            from modules.data_stream.data_stream import get_data_stream
            from agents.agent_registry import get_registry
            
            # Försök hämta config, fallback till mock om den inte finns
            try:
                from dash_app.config import USE_MOCK_DATA
            except:
                USE_MOCK_DATA = True
                logger.info("Config inte tillgänglig, använder mock data")
            
            # Hämta DataStream
            self.data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
            
            # Hämta agent registry
            self.agent_registry = get_registry()
            
            # Skapa agentinstanser för analys - aktivera alla tillgängliga agenter
            self._active_agents = {}
            agent_types = [
                # Klassiska agenter
                'momentum_agent', 'reversal_agent', 'breakout_agent', 'hybrid_agent',
                # Paradigmatiska agenter
                'echo_agent', 'fractalis_agent', 'vox_agent', 'myco_agent', 
                'obscura_agent', 'mirage_agent', 'sentio_agent', 'reflexion_agent',
                'dimensio_agent', 'symbio_agent', 'genesis_agent', 'architectum_agent'
            ]
            
            for agent_type in agent_types:
                try:
                    agent_info = self.agent_registry.get_agent_info(agent_type)
                    if agent_info:
                        agent_class = agent_info['class']
                        agent_instance = agent_class(agent_id=agent_type)
                        self._active_agents[agent_type] = agent_instance
                        logger.info(f"Aktiverade agent: {agent_type}")
                except Exception as e:
                    logger.warning(f"Kunde inte aktivera agent {agent_type}: {e}")
            
            logger.info(f"Live-system initialiserat med {len(self._active_agents)} agenter")
            
            # Generera initiala beslut från live data
            self._refresh_live_decisions()
            
        except Exception as e:
            logger.error(f"Kunde inte initialisera live-system: {e}")
            self.use_live_data = False
            # No fallback to sample data - system must use live data or remain empty
            logger.warning("DecisionCore will remain empty until live system is properly initialized")
    
    def _refresh_live_decisions(self) -> None:
        """
        Uppdaterar beslut baserat på live marknadsdata och agentanalys.
        """
        if not self.use_live_data or not hasattr(self, 'data_stream'):
            return
        
        try:
            # Rensa gamla beslut för att få fräsch data
            old_count = len(self.decisions)
            self.decisions = []
            
            # Reset consensus/conflict counters
            self.stats['consensus_count'] = 0
            self.stats['conflict_count'] = 0
            self.stats['buy_count'] = 0
            self.stats['sell_count'] = 0
            self.stats['hold_count'] = 0
            
            # Hämta live marknadsdata
            market_summary = self.data_stream.get_market_summary()
            quotes = market_summary.get('quotes', {})
            
            # Analysera alla tillgängliga symboler (upp till 50 subscriptions)
            symbols = list(quotes.keys())[:50]
            
            decisions_made = 0
            for symbol in symbols:
                quote_data = quotes.get(symbol, {})
                
                # Förbered marknadsdata för agenter
                market_data = {
                    'price': quote_data.get('c', 0),  # current price
                    'volume': quote_data.get('v', 0),  # volume
                    'trend_score': (quote_data.get('c', 0) - quote_data.get('o', 0)) / max(quote_data.get('o', 1), 0.01),
                    'price_change_pct': quote_data.get('dp', 0) / 100.0,  # daily percent change
                    'high': quote_data.get('h', 0),
                    'low': quote_data.get('l', 0),
                    'open': quote_data.get('o', 0)
                }
                
                # Låt varje agent analysera symbolen
                for agent_id, agent in self._active_agents.items():
                    try:
                        analysis = agent.analyze(symbol, market_data)
                        
                        # Konvertera till AgentDecision
                        decision = AgentDecision(
                            agent_id=analysis['agent_id'],
                            symbol=symbol,
                            decision=analysis['decision'],
                            confidence=analysis['confidence'] * 100,  # Convert to 0-100 scale
                            reasoning=analysis['reasoning'],
                            metadata=analysis.get('metrics', {})
                        )
                        
                        # Lägg till beslut (med validering)
                        if self.add_decision(decision):
                            decisions_made += 1
                            
                    except Exception as e:
                        logger.warning(f"Agent {agent_id} kunde inte analysera {symbol}: {e}")
            
            logger.info(
                f"Live decisions refresh: {decisions_made} nya beslut genererade "
                f"(rensade {old_count} gamla)"
            )
            
            # Analyze consensus for all symbols to update consensus/conflict counts
            all_symbols = self.get_all_symbols()
            for symbol in all_symbols:
                self.analyze_consensus(symbol)
            
        except Exception as e:
            logger.error(f"Kunde inte refresha live beslut: {e}")
    
    def add_decision(self, decision: AgentDecision) -> bool:
        """
        Lägger till ett agentbeslut efter validering.
        
        Args:
            decision: AgentDecision objekt
        
        Returns:
            True om beslutet accepterades, False annars
        """
        self.stats['total_decisions'] += 1
        
        # Validera konfidensgrad
        if decision.confidence < self.min_confidence:
            logger.info(
                f"Beslut från {decision.agent_id} avvisat: "
                f"confidence {decision.confidence} < {self.min_confidence}"
            )
            self.stats['rejected_decisions'] += 1
            return False
        
        # Lägg till beslut
        self.decisions.append(decision)
        self.stats['accepted_decisions'] += 1
        
        # Track decision type counts
        decision_type = decision.decision.value.lower()
        if decision_type == 'buy':
            self.stats['buy_count'] += 1
        elif decision_type == 'sell':
            self.stats['sell_count'] += 1
        elif decision_type == 'hold':
            self.stats['hold_count'] += 1
        
        logger.info(
            f"Beslut accepterat från {decision.agent_id}: "
            f"{decision.decision.value} {decision.symbol} "
            f"(confidence={decision.confidence})"
        )
        
        return True
    
    def get_decisions_for_symbol(self, symbol: str) -> List[AgentDecision]:
        """
        Hämtar alla beslut för en specifik symbol.
        
        Args:
            symbol: Tickersymbol
        
        Returns:
            Lista med beslut för symbolen
        """
        return [d for d in self.decisions if d.symbol == symbol]
    
    def analyze_consensus(self, symbol: str) -> Dict[str, Any]:
        """
        Analyserar konsensus för en symbol över alla agentbeslut.
        
        Args:
            symbol: Tickersymbol att analysera
        
        Returns:
            Dict med konsensusanalys
        """
        symbol_decisions = self.get_decisions_for_symbol(symbol)
        
        if not symbol_decisions:
            return {
                'symbol': symbol,
                'consensus': None,
                'has_conflict': False,
                'total_decisions': 0,
                'decision_breakdown': {}
            }
        
        # Räkna beslut per typ
        decision_counts = {
            DecisionType.BUY: 0,
            DecisionType.SELL: 0,
            DecisionType.HOLD: 0
        }
        
        total_confidence = 0
        for decision in symbol_decisions:
            decision_counts[decision.decision] += 1
            total_confidence += decision.confidence
        
        # Hitta majoritetsbeslutet
        max_count = max(decision_counts.values())
        majority_decisions = [
            dt for dt, count in decision_counts.items() 
            if count == max_count
        ]
        
        # Beräkna konfliktgrad
        total = len(symbol_decisions)
        buy_ratio = decision_counts[DecisionType.BUY] / total
        sell_ratio = decision_counts[DecisionType.SELL] / total
        hold_ratio = decision_counts[DecisionType.HOLD] / total
        
        # Konflikt om buy och sell båda är över tröskeln och hold inte dominerar
        has_conflict = (
            buy_ratio >= self.conflict_threshold and 
            sell_ratio >= self.conflict_threshold and
            hold_ratio < self.conflict_threshold
        )
        
        if has_conflict:
            self.stats['conflicts_detected'] += 1
            self.stats['conflict_count'] += 1
            logger.warning(
                f"Konflikt detekterad för {symbol}: "
                f"{buy_ratio:.1%} buy, {sell_ratio:.1%} sell"
            )
        else:
            self.stats['consensus_count'] += 1
        
        return {
            'symbol': symbol,
            'consensus': majority_decisions[0].value if len(majority_decisions) == 1 else None,
            'has_conflict': has_conflict,
            'total_decisions': total,
            'average_confidence': round(total_confidence / total, 2),
            'decision_breakdown': {
                'buy': decision_counts[DecisionType.BUY],
                'sell': decision_counts[DecisionType.SELL],
                'hold': decision_counts[DecisionType.HOLD]
            },
            'decision_ratios': {
                'buy': round(buy_ratio, 2),
                'sell': round(sell_ratio, 2),
                'hold': round(decision_counts[DecisionType.HOLD] / total, 2)
            }
        }
    
    def get_all_symbols(self) -> List[str]:
        """
        Hämtar alla unika symboler som det finns beslut för.
        
        Returns:
            Lista med unika symboler
        """
        return list(set(d.symbol for d in self.decisions))
    
    def route_decision(self, symbol: str) -> Dict[str, Any]:
        """
        Routar beslut för en symbol till lämplig modul.
        
        Args:
            symbol: Tickersymbol
        
        Returns:
            Dict med routing-information och nästa steg
        """
        consensus = self.analyze_consensus(symbol)
        
        # Bestäm routing baserat på konsensus och konflikt
        if consensus['has_conflict']:
            routing = {
                'destination': 'vote_engine',
                'reason': 'Konflikt detekterad, eskalerar till röstning',
                'priority': 'high'
            }
        elif consensus['consensus'] is None:
            routing = {
                'destination': 'hold',
                'reason': 'Ingen tydlig konsensus, håller position',
                'priority': 'low'
            }
        elif consensus['consensus'] in ['buy', 'sell']:
            routing = {
                'destination': 'fusion',
                'reason': 'Tydlig konsensus, skickar till signalvalidering',
                'priority': 'medium',
                'next_step': 'sizing' if consensus['average_confidence'] > 70 else 'hold'
            }
        else:
            routing = {
                'destination': 'hold',
                'reason': 'Hold-konsensus',
                'priority': 'low'
            }
        
        result = {
            'symbol': symbol,
            'consensus': consensus,
            'routing': routing,
            'timestamp': datetime.now().isoformat()
        }
        
        # Logga till historik
        self.decision_history.append(result)
        
        logger.info(
            f"Routing för {symbol}: {routing['destination']} "
            f"(reason: {routing['reason']})"
        )
        
        return result
    
    def clear_decisions(self, symbol: Optional[str] = None) -> int:
        """
        Rensar beslut, antingen för en specifik symbol eller alla.
        
        Args:
            symbol: Specifik symbol att rensa, eller None för alla
        
        Returns:
            Antal beslut som rensades
        """
        if symbol:
            before = len(self.decisions)
            self.decisions = [d for d in self.decisions if d.symbol != symbol]
            cleared = before - len(self.decisions)
            logger.info(f"Rensade {cleared} beslut för {symbol}")
        else:
            cleared = len(self.decisions)
            self.decisions = []
            logger.info(f"Rensade alla {cleared} beslut")
        
        return cleared
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för DecisionCore.
        
        Returns:
            Dict med statistik
        """
        # Calculate consensus and conflict rates
        total_decisions = self.stats['total_decisions']
        if total_decisions > 0:
            consensus_rate = (self.stats.get('consensus_count', 0) / total_decisions) * 100
            conflict_rate = (self.stats.get('conflict_count', 0) / total_decisions) * 100
        else:
            consensus_rate = 0.0
            conflict_rate = 0.0
        
        # Calculate average confidence
        if self.decisions:
            avg_confidence = sum(d.confidence for d in self.decisions) / len(self.decisions)
        else:
            avg_confidence = 0.0
        
        return {
            **self.stats,
            'active_decisions': len(self.decisions),
            'unique_symbols': len(self.get_all_symbols()),
            'decisions_in_history': len(self.decision_history),
            'consensus_rate': consensus_rate,
            'conflict_rate': conflict_rate,
            'average_confidence': avg_confidence
        }
    
    def get_agent_activity(self) -> Dict[str, Dict[str, Any]]:
        """
        Hämtar aktivitet per agent.
        Refreshar live decisions vid varje anrop för att hålla data aktuell.
        
        Returns:
            Dict med agent_id -> activity stats
        """
        # Refresh decisions from live data if enabled
        if self.use_live_data:
            self._refresh_live_decisions()
        
        agent_activity = {}
        
        for decision in self.decisions:
            agent_id = decision.agent_id
            if agent_id not in agent_activity:
                agent_activity[agent_id] = {
                    'decision_count': 0,
                    'avg_confidence': 0,
                    'decisions': [],
                    'status': 'Active'
                }
            
            agent_activity[agent_id]['decision_count'] += 1
            agent_activity[agent_id]['decisions'].append(decision.to_dict())
        
        # Calculate average confidence for each agent
        for agent_id, activity in agent_activity.items():
            if activity['decision_count'] > 0:
                confidences = [d['confidence'] for d in activity['decisions']]
                activity['avg_confidence'] = sum(confidences) / len(confidences)
        
        return agent_activity
