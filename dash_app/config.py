"""
Dashboard Configuration
Centralized configuration for API keys and data sources
"""

import os
# Finnhub API Configuration
# Load API key from environment variable for security
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY")

# Data Source Toggle
# Set to False to use real Finnhub API data, True for mock data
USE_MOCK_DATA = True

# Default symbols to track
DEFAULT_SYMBOLS = [
    'AAPL',   # Apple
    'GOOGL',  # Google
    'MSFT',   # Microsoft
    'TSLA',   # Tesla
    'AMZN',   # Amazon
    'META',   # Meta
    'NVDA',   # NVIDIA
    'AMD',    # AMD
    'NFLX',   # Netflix
    'BA',     # Boeing
    'JPM',    # JPMorgan
    'V'       # Visa
]

# Dashboard settings
AUTO_REFRESH_INTERVAL = 5000  # milliseconds
CHART_THEME = 'plotly_dark'

# API endpoints
FINNHUB_REST_URL = "https://finnhub.io/api/v1"
FINNHUB_WS_URL = "wss://ws.finnhub.io"
