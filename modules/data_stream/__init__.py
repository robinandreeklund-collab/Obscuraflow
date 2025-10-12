"""
Data Stream Module - Realtidsdata & trendanalys

Detta modul hanterar:
- WebSocket-anslutning till Finnhub API
- REST-polling för symbolbatchar
- Trendanalys: volym, momentum, volatilitet
- Dynamisk prenumeration på toppsymboler

Kopplingar: trending_pool/, agents/, symbol_memory/
"""

from .data_stream import DataStream

__all__ = ['DataStream']
