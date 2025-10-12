"""
Panel Auto-Update Callbacks
Provides automatic real-time updates for all dashboard panels using a global refresh interval
"""

from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
from dash_app.layout.page_router import route_page
import dash_app.config as dash_config
import config as root_config


def register_panel_callbacks(app):
    """
    Registrerar en global auto-refresh callback som uppdaterar alla paneler automatiskt.
    Använder panel-specifika intervals som redan finns i varje panel.
    
    Not: Dash visar console warnings när callbacks refererar till komponenter som inte finns
    i den aktuella layouten. Detta är förväntat beteende och påverkar inte funktionaliteten.
    Endast intervals som faktiskt finns i DOM kan trigga uppdateringar.
    """
    
    # Lista över alla panel intervals som kan trigga uppdateringar
    # Dessa måste matcha interval-IDs i panelerna
    panel_intervals = [
        'decision-core-panel-interval',
        'vote-panel-interval',
        'sizing-panel-interval',
        'timespan-panel-interval',
        'portfolio-panel-interval',
        'mutation-panel-interval',
        'spectrum-panel-interval',
        'lifecycle-panel-interval',
        'governance-panel-interval',
        'portfolio-intel-panel-interval',
        'risk-panel-interval',
        'system-flow-panel-interval',
        'narrative-panel-interval',
        'data-source-panel-interval',
        'portfolio-dev-panel-interval'
    ]
    
    # Skapa Inputs för alla möjliga intervals
    # Dash hanterar automatiskt fall där intervallet inte finns i DOM
    interval_inputs = [Input(interval_id, 'n_intervals') for interval_id in panel_intervals]
    
    @app.callback(
        [Output('page-header', 'children', allow_duplicate=True),
         Output('page-content', 'children', allow_duplicate=True)],
        interval_inputs,
        [State('url', 'pathname'),
         State('data-source-store', 'data')],
        prevent_initial_call=True
    )
    def auto_update_all_panels(*args):
        """
        Uppdaterar paneler automatiskt när något interval triggas.
        Endast intervals som finns i aktuell layout kan faktiskt trigga denna callback.
        """
        # Kontrollera att callback faktiskt triggades av en komponent
        ctx = callback_context
        if not ctx.triggered or ctx.triggered[0]['prop_id'] == '.':
            raise PreventUpdate
        
        # De sista två argumenten är States (pathname och data_source)
        pathname = args[-2]
        data_source = args[-1]
        
        # Kontrollera om något interval faktiskt triggade
        # (annars är alla None och vi ska inte uppdatera)
        interval_values = args[:-2]  # Alla utom de två sista (States)
        if all(v is None or v == 0 for v in interval_values):
            raise PreventUpdate
        
        # Update configs
        use_mock = (data_source == 'mock')
        dash_config.USE_MOCK_DATA = use_mock
        root_config.USE_MOCK_DATA = use_mock
        
        # Returnera uppdaterad panel
        return route_page(pathname)
