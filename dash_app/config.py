"""
Dashboard Configuration
Imports and exposes settings from global config for dashboard use
"""

import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import all settings from global config
from config import (
    FINNHUB_API_KEY,
    FINNHUB_REST_URL,
    FINNHUB_WS_URL,
    USE_MOCK_DATA,
    DEFAULT_SYMBOLS,
    AUTO_REFRESH_INTERVAL,
    CHART_THEME,
    QUOTE_CACHE_TTL,
    PROFILE_CACHE_TTL,
    API_RATE_LIMIT_DELAY,
    API_REQUEST_TIMEOUT,
    MIN_CONFIDENCE,
    CONFLICT_THRESHOLD,
    MAX_POSITION_SIZE,
    RISK_PER_TRADE,
    USE_KELLY_CRITERION
)

# Re-export for backward compatibility
__all__ = [
    'FINNHUB_API_KEY',
    'FINNHUB_REST_URL',
    'FINNHUB_WS_URL',
    'USE_MOCK_DATA',
    'DEFAULT_SYMBOLS',
    'AUTO_REFRESH_INTERVAL',
    'CHART_THEME',
    'QUOTE_CACHE_TTL',
    'PROFILE_CACHE_TTL',
    'API_RATE_LIMIT_DELAY',
    'API_REQUEST_TIMEOUT',
    'MIN_CONFIDENCE',
    'CONFLICT_THRESHOLD',
    'MAX_POSITION_SIZE',
    'RISK_PER_TRADE',
    'USE_KELLY_CRITERION'
]
