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
    
    # REMOVED: Sample event generation is no longer used.
    # All events must come from actual system activity.
    
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
        # Hitta händelser mellan start och end baserat på timestamp
        start_idx = None
        end_idx = None
        
        for i, event in enumerate(self.events):
            event_desc = event.get('description', '')
            if start_event in event_desc and start_idx is None:
                start_idx = i
            if end_event in event_desc:
                end_idx = i
        
        if start_idx is None or end_idx is None or start_idx >= end_idx:
            # Fallback till enkel kedja
            chain = [start_event, end_event]
        else:
            # Bygg kedja från händelser mellan start och end
            chain = [start_event]
            for event in self.events[start_idx+1:end_idx]:
                chain.append(event.get('description', 'Unknown event'))
            chain.append(end_event)
        
        self.causal_chains.append(chain)
        logger.info(
            f"Byggde kausal kedja från '{start_event}' till '{end_event}' "
            f"({len(chain)} steg)"
        )
        
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
    
    def generate_summary(self, timeframe: str = '24h', max_events: int = 10) -> str:
        """
        Genererar sammanfattning av systemberättelsen.
        
        Args:
            timeframe: Tidsram för sammanfattning
            max_events: Max antal händelser att inkludera
        
        Returns:
            Textsammanfattning
        """
        if not self.events:
            return f"Systemsammanfattning för {timeframe}: Inga händelser registrerade"
        
        # Ta senaste händelserna
        recent_events = self.events[-max_events:]
        
        # Gruppera händelser per typ
        event_types = {}
        for event in recent_events:
            event_type = event.get('type', 'unknown')
            if event_type not in event_types:
                event_types[event_type] = []
            event_types[event_type].append(event)
        
        # Bygg sammanfattning
        summary_parts = [f"Systemsammanfattning för {timeframe}:"]
        summary_parts.append(f"Totalt {len(self.events)} händelser (visar senaste {len(recent_events)})")
        summary_parts.append("")
        
        # Summera per händelsetyp
        for event_type, events in event_types.items():
            summary_parts.append(f"- {event_type}: {len(events)} händelser")
            # Lägg till exempel på senaste händelsen av denna typ
            latest = events[-1]
            summary_parts.append(f"  Senaste: {latest.get('description', 'N/A')}")
        
        # Lägg till info om narrativ
        if self.narratives:
            summary_parts.append("")
            summary_parts.append(f"Aktiva narrativ: {len(self.narratives)}")
        
        # Lägg till info om kausala kedjor
        if self.causal_chains:
            summary_parts.append(f"Kausala kedjor: {len(self.causal_chains)}")
        
        return "\n".join(summary_parts)
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Hämtar de senaste händelserna.
        
        Args:
            limit: Max antal händelser att returnera
        
        Returns:
            Lista med senaste händelser
        """
        return self.events[-limit:] if self.events else []
    
    def get_event_groups(self) -> Dict[str, int]:
        """
        Grupperar händelser per typ och returnerar antal per typ.
        
        Returns:
            Dict med händelsetyp -> antal
        """
        event_groups = {}
        for event in self.events:
            event_type = event.get('type', 'unknown')
            event_groups[event_type] = event_groups.get(event_type, 0) + 1
        return event_groups
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för narrative engine.
        
        Returns:
            Dict med statistik
        """
        event_groups = self.get_event_groups()
        return {
            'total_events': len(self.events),
            'active_stories': len(self.narratives),
            'causal_chains': len(self.causal_chains),
            'event_groups': len(event_groups)
        }
