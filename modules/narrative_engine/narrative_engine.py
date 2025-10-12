"""
NarrativeEngine - Huvudklass för händelseflöde och berättelse

Denna klass ansvarar för:
- Skapande av systemberättelse
- Spårning av kausala kedjor
- Storyline-generering
- Meta-narrativ
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class NarrativeEngine:
    """
    NarrativeEngine hanterar systemberättelse och händelseflöde.
    
    Attributes:
        events (List): Lista över systemevent
        narratives (Dict): Aktiva berättelser
    """
    
    def __init__(self):
        """
        Initierar NarrativeEngine.
        """
        self.events: List[Dict[str, Any]] = []
        self.narratives: Dict[str, List[str]] = {}
        self.causal_chains: List[List[str]] = []
        logger.info("NarrativeEngine initierad")
    
    def add_event(self, event_type: str, description: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Lägger till en händelse i narrativet.
        
        Args:
            event_type: Typ av händelse
            description: Beskrivning av händelsen
            metadata: Extra metadata
        
        Returns:
            Dict med händelseinfo
        """
        event = {
            'type': event_type,
            'description': description,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.events.append(event)
        logger.debug(f"Lade till händelse: {event_type}")
        return event
    
    def create_narrative(self, narrative_id: str, title: str) -> Dict[str, Any]:
        """
        Skapar en ny berättelse.
        
        Args:
            narrative_id: Unikt ID för berättelsen
            title: Titel på berättelsen
        
        Returns:
            Dict med narrativ-info
        """
        if narrative_id in self.narratives:
            logger.warning(f"Narrativ {narrative_id} finns redan")
            return {'id': narrative_id, 'exists': True}
        
        self.narratives[narrative_id] = []
        logger.info(f"Skapade narrativ: {title}")
        return {
            'id': narrative_id,
            'title': title,
            'created_at': datetime.now().isoformat()
        }
    
    def add_to_narrative(self, narrative_id: str, event_id: str) -> bool:
        """
        Lägger till händelse i ett narrativ.
        
        Args:
            narrative_id: Narrativ-ID
            event_id: Händelse-ID
        
        Returns:
            True om händelsen lades till
        """
        if narrative_id not in self.narratives:
            logger.error(f"Narrativ {narrative_id} finns inte")
            return False
        
        self.narratives[narrative_id].append(event_id)
        return True
    
    def build_causal_chain(self, start_event: str, end_event: str) -> List[str]:
        """
        Bygger kausal kedja mellan två händelser.
        
        Args:
            start_event: Starthändelse
            end_event: Sluthändelse
        
        Returns:
            Lista med händelser i kedjan
        """
        # Kodstub - implementeras senare med faktisk kausal analys
        chain = [start_event, end_event]
        self.causal_chains.append(chain)
        logger.info(f"Byggde kausal kedja från {start_event} till {end_event}")
        return chain
    
    def get_narrative(self, narrative_id: str) -> Optional[Dict[str, Any]]:
        """
        Hämtar ett narrativ.
        
        Args:
            narrative_id: Narrativ-ID
        
        Returns:
            Dict med narrativ eller None
        """
        if narrative_id not in self.narratives:
            return None
        
        return {
            'id': narrative_id,
            'events': self.narratives[narrative_id],
            'length': len(self.narratives[narrative_id])
        }
    
    def generate_summary(self, timeframe: str = '24h') -> str:
        """
        Genererar sammanfattning av systemberättelsen.
        
        Args:
            timeframe: Tidsram för sammanfattning
        
        Returns:
            Textsammanfattning
        """
        # Kodstub
        return f"Systemsammanfattning för {timeframe}: {len(self.events)} händelser"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för narrative engine.
        
        Returns:
            Dict med statistik
        """
        return {
            'total_events': len(self.events),
            'active_narratives': len(self.narratives),
            'causal_chains': len(self.causal_chains)
        }
