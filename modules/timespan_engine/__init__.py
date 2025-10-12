"""
Timespan Engine Module - Tidsramar och RL-träning

Detta modul hanterar:
- Hantering av olika tidsramar (1m, 5m, 15m, 1h, 4h, 1d)
- RL-träning per tidsram
- Tidsramspecifika strategier
- Synkronisering av data över tidsramar

Kopplingar: fusion/, data_stream/, evolution/
"""

from .timespan_engine import TimespanEngine

__all__ = ['TimespanEngine']
