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

# Import and register panel auto-update callbacks
from dash_app.callbacks.panel_callbacks import register_panel_callbacks
register_panel_callbacks(app)

# Huvudlayout
app.layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='data-source-store', data='mock'),  # Store for data source state
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

# Callback för data source toggle
@app.callback(
    Output('data-source-store', 'data'),
    [Input('data-source-toggle', 'value')]
)
def update_data_source(value):
    """
    Uppdaterar data source store när toggle ändras.
    """
    return value

# Callback för sidnavigering
@app.callback(
    [Output('page-header', 'children'),
     Output('page-content', 'children')],
    [Input('url', 'pathname'),
     Input('data-source-store', 'data')]
)
def display_page(pathname, data_source):
    """
    Router-callback som bestämmer vilket innehåll som ska visas baserat på URL.
    """
    # Update config based on toggle
    # Import both dash_app.config and root config to update both
    import dash_app.config as dash_config
    import config as root_config
    
    # Update both configs to ensure consistency
    use_mock = (data_source == 'mock')
    dash_config.USE_MOCK_DATA = use_mock
    root_config.USE_MOCK_DATA = use_mock
    
    return route_page(pathname)


if __name__ == '__main__':
    import config as root_config
    
    print("=" * 80)
    print("🌀 OBSCURAFLOW DASHBOARD")
    print("=" * 80)
    print("\nStartar Dash-servern...")
    print(f"Dashboard tillgänglig på: http://{root_config.DASHBOARD_HOST}:{root_config.DASHBOARD_PORT}")
    print(f"\n📊 Finnhub API Key: {root_config.FINNHUB_API_KEY[:10]}...{root_config.FINNHUB_API_KEY[-4:]}")
    print(f"🔄 Data Source: {'Mock Data' if root_config.USE_MOCK_DATA else 'Live API'}")
    print("\nTryck Ctrl+C för att stoppa servern.\n")
    print("=" * 80)
    
    app.run(
        debug=root_config.DASHBOARD_DEBUG, 
        host=root_config.DASHBOARD_HOST, 
        port=root_config.DASHBOARD_PORT
    )
