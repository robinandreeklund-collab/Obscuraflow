"""
Obscuraflow - Main Dash Application

Detta är huvudfilen för Obscuraflow Dash-dashboard.
Den initierar Dash-appen, registrerar callbacks och startar servern.
"""

import sys
import os

# Add project root to path if running from dash_app directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_app.layout.sidebar import create_sidebar
from dash_app.layout.header import create_header
from dash_app.layout.page_router import route_page

# Initialisera Dash-appen med Bootstrap Cerulean tema och egna CSS
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CERULEAN],
    title="Obscuraflow - AI Trading Dashboard"
)

# Server för deployment
server = app.server

# Huvudlayout
app.layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),
        dbc.Row(
            [
                dbc.Col(
                    create_sidebar(),
                    width=2,
                    lg=2,
                    md=3,
                    sm=12,
                    className="sidebar"
                ),
                dbc.Col(
                    [
                        html.Div(id='page-header'),
                        html.Div(id='page-content', className="fade-in")
                    ],
                    width=10,
                    lg=10,
                    md=9,
                    sm=12,
                    className="main-content"
                )
            ]
        )
    ],
    fluid=True,
    className="dashboard-container"
)

# Callback för sidnavigering
@app.callback(
    [Output('page-header', 'children'),
     Output('page-content', 'children')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """
    Router-callback som bestämmer vilket innehåll som ska visas baserat på URL.
    """
    return route_page(pathname)


if __name__ == '__main__':
    print("=" * 80)
    print("🌀 OBSCURAFLOW DASHBOARD")
    print("=" * 80)
    print("\nStartar Dash-servern...")
    print("Dashboard tillgänglig på: http://localhost:8050")
    print("\nTryck Ctrl+C för att stoppa servern.\n")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=8050)
