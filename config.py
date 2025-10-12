"""
Global Configuration for Obscuraflow Project
Centralized configuration for API keys, data sources, and system settings
"""

import os

# ============================================================================
# Finnhub API Configuration
# ============================================================================

# Primary Finnhub API key
# Can be overridden by environment variable FINNHUB_API_KEY for security
FINNHUB_API_KEY = os.environ.get(
    "FINNHUB_API_KEY", 
    "d3in10hr01qmn7fkr2a0d3in10hr01qmn7fkr2ag"
)

# API endpoints
FINNHUB_REST_URL = "https://finnhub.io/api/v1"
FINNHUB_WS_URL = "wss://ws.finnhub.io"

# ============================================================================
# Data Source Configuration
# ============================================================================

# Data Source Toggle
# Set to False to use real Finnhub API data, True for mock data
# Can be overridden by environment variable USE_MOCK_DATA
USE_MOCK_DATA = os.environ.get("USE_MOCK_DATA", "true").lower() == "true"

# Default symbols to track (Nasdaq-100 selection)
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

# ============================================================================
# Dashboard Settings
# ============================================================================

# Auto-refresh interval for panels (milliseconds)
AUTO_REFRESH_INTERVAL = 1000

# Chart theme
CHART_THEME = 'plotly_dark'

# Dashboard server settings
DASHBOARD_HOST = os.environ.get("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.environ.get("DASHBOARD_PORT", "8050"))
DASHBOARD_DEBUG = os.environ.get("DASHBOARD_DEBUG", "true").lower() == "true"

# ============================================================================
# API Client Settings
# ============================================================================

# Cache TTL settings (seconds)
QUOTE_CACHE_TTL = 60      # 60 seconds for quote data
PROFILE_CACHE_TTL = 3600  # 1 hour for company profile data

# Rate limiting
API_RATE_LIMIT_DELAY = 0.1  # 100ms between API calls

# Request timeout (seconds)
API_REQUEST_TIMEOUT = 10

# ============================================================================
# Logging Configuration
# ============================================================================

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# Module Settings
# ============================================================================

# Decision Core
MIN_CONFIDENCE = 50.0
CONFLICT_THRESHOLD = 0.4

# Position Sizing
MAX_POSITION_SIZE = 0.2
RISK_PER_TRADE = 0.02
USE_KELLY_CRITERION = True

# Portfolio Engine
MAX_PORTFOLIOS = 10
PORTFOLIO_REBALANCE_INTERVAL = 3600  # seconds

# Agent Settings
AGENT_TIMEOUT = 30  # seconds
MAX_CONCURRENT_AGENTS = 20

# ============================================================================
# System Information
# ============================================================================

PROJECT_NAME = "Obscuraflow"
VERSION = "1.0.0"
DESCRIPTION = "AI-driven trading ecosystem with multi-agent intelligence"
