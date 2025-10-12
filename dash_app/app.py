"""
Obscuraflow - Main Dash Application

Detta är huvudfilen för Obscuraflow Dash-dashboard.
Den initierar Dash-appen, registrerar callbacks och startar servern.
"""

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
                    className="sidebar"
                ),
                dbc.Col(
                    [
                        html.Div(id='page-header'),
                        html.Div(id='page-content', className="fade-in")
                    ],
                    width=10,
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
    app.run_server(debug=True, host='0.0.0.0', port=8050)
