"""
Fusion Module - Multi-timeframe signalvalidering

Detta modul hanterar:
- Signalvalidering över flera tidsramar
- Konfirmering av trendriktningar
- Filtrera brus och falska signaler
- Sammanvägning av tidsspann

Kopplingar: decision_core/, timespan_engine/, data_stream/
"""

from .fusion import Fusion

__all__ = ['Fusion']
