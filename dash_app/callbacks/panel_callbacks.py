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
    Använder en global interval komponent för att trigga uppdateringar.
    """
    
    @app.callback(
        [Output('page-header', 'children', allow_duplicate=True),
         Output('page-content', 'children', allow_duplicate=True)],
        [Input('global-refresh-interval', 'n_intervals')],
        [State('url', 'pathname'),
         State('data-source-store', 'data')],
        prevent_initial_call=True
    )
    def auto_update_all_panels(n_intervals, pathname, data_source):
        """
        Uppdaterar paneler automatiskt var 3:e sekund via global interval.
        Detta säkerställer att alla paneler får färsk data regelbundet.
        """
        # Kontrollera att callback faktiskt triggades
        ctx = callback_context
        if not ctx.triggered or ctx.triggered[0]['prop_id'] == '.':
            raise PreventUpdate
        
        # Skip if we don't have a pathname (shouldn't happen but safety check)
        if not pathname:
            raise PreventUpdate
        
        # Update configs
        use_mock = (data_source == 'mock')
        dash_config.USE_MOCK_DATA = use_mock
        root_config.USE_MOCK_DATA = use_mock
        
        # Returnera uppdaterad panel med färsk data
        return route_page(pathname)
