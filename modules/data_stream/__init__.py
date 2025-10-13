"""
Data Stream Module - Realtidsdata & trendanalys

Detta modul hanterar:
- WebSocket-anslutning till Finnhub API
- REST-polling för symbolbatchar med rate limiting
- Trendanalys: volym, momentum, volatilitet
- Dynamisk prenumeration på toppsymboler
- Adaptiv batch-strategi för optimal API-användning

Kopplingar: trending_pool/, agents/, symbol_memory/
"""

from .data_stream import DataStream, get_data_stream
from .rest_batcher import RestBatcher
from .ws_handler import WebSocketHandler
from .orchestrator import DataOrchestrator

__all__ = [
    'DataStream',
    'get_data_stream',
    'RestBatcher',
    'WebSocketHandler',
    'DataOrchestrator'
]
