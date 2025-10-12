#!/usr/bin/env python
"""
Obscuraflow Dashboard - Startup Script

Detta script startar Obscuraflow Dash-dashboarden.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dash_app.app import app

if __name__ == '__main__':
    print("=" * 80)
    print("🌀 OBSCURAFLOW DASHBOARD")
    print("=" * 80)
    print("\nStartar Dash-servern...")
    print("Dashboard tillgänglig på: http://localhost:8050")
    print("\nTryck Ctrl+C för att stoppa servern.\n")
    print("=" * 80)
    
    app.run_server(debug=True, host='0.0.0.0', port=8050)
