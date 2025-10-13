"""
Settings Panel Callbacks
Handles all interactions with the Settings Panel including:
- Module on/off toggles
- Agent activation/deactivation
- Parameter adjustments
"""

from dash import Input, Output, State, ALL, callback_context
from dash.exceptions import PreventUpdate
import logging

logger = logging.getLogger(__name__)


def register_settings_callbacks(app):
    """
    Register all callbacks for the Settings Panel
    
    Args:
        app: Dash app instance
    """
    
    # Module toggle callbacks
    @app.callback(
        Output({'type': 'module-switch', 'module': ALL}, 'value'),
        Input({'type': 'module-switch', 'module': ALL}, 'value'),
        State({'type': 'module-switch', 'module': ALL}, 'id'),
        prevent_initial_call=True
    )
    def handle_module_toggle(values, ids):
        """
        Handle module toggle switches
        
        Args:
            values: List of switch values (True/False)
            ids: List of switch IDs with module names
            
        Returns:
            Updated values for switches
        """
        from dash_app.utils.settings_manager import get_settings_manager
        
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        # Get which switch was toggled
        trigger = ctx.triggered[0]
        trigger_id = eval(trigger['prop_id'].split('.')[0])
        module_name = trigger_id['module']
        new_value = trigger['value']
        
        # Update via settings manager
        manager = get_settings_manager()
        result = manager.toggle_module(module_name, new_value)
        
        if result['success']:
            logger.info(f"Module {module_name} toggled to {new_value}")
        else:
            logger.error(f"Failed to toggle module {module_name}")
        
        # Return current values (they might have been updated)
        return [manager.get_module_status(id_dict['module']) for id_dict in ids]
    
    # Agent toggle callbacks
    @app.callback(
        Output({'type': 'agent-switch', 'agent': ALL}, 'value'),
        Input({'type': 'agent-switch', 'agent': ALL}, 'value'),
        State({'type': 'agent-switch', 'agent': ALL}, 'id'),
        prevent_initial_call=True
    )
    def handle_agent_toggle(values, ids):
        """
        Handle agent toggle switches
        
        Args:
            values: List of switch values (True/False)
            ids: List of switch IDs with agent IDs
            
        Returns:
            Updated values for switches
        """
        from dash_app.utils.settings_manager import get_settings_manager
        
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        # Get which switch was toggled
        trigger = ctx.triggered[0]
        trigger_id = eval(trigger['prop_id'].split('.')[0])
        agent_id = trigger_id['agent']
        new_value = trigger['value']
        
        # Update via settings manager
        manager = get_settings_manager()
        result = manager.toggle_agent(agent_id, new_value)
        
        if result['success']:
            logger.info(f"Agent {agent_id} toggled to {new_value}")
        else:
            logger.error(f"Failed to toggle agent {agent_id}: {result.get('message', '')}")
        
        # Return current values from agent registry
        from agents.agent_registry import get_registry
        registry = get_registry()
        
        return [registry.get_instance(id_dict['agent']) is not None for id_dict in ids]
    
    # Parameter update callbacks
    @app.callback(
        Output('param-update-status', 'children'),
        [
            Input('param-live-data', 'value'),
            Input('param-batch-size', 'value'),
            Input('param-batch-interval', 'value'),
            Input('param-fusion-mode', 'value'),
            Input('param-fusion-threshold', 'value'),
            Input('param-sizing-method', 'value'),
            Input('param-max-position', 'value'),
            Input('param-vote-method', 'value'),
            Input('param-min-vote', 'value'),
        ],
        prevent_initial_call=True
    )
    def handle_parameter_updates(live_data, batch_size, batch_interval, 
                                 fusion_mode, fusion_threshold,
                                 sizing_method, max_position,
                                 vote_method, min_vote):
        """
        Handle parameter updates from sliders and dropdowns
        
        Returns:
            Status message for parameter updates
        """
        from dash_app.utils.settings_manager import get_settings_manager
        import dash_app.config as dash_config
        import config as root_config
        
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        # Get which parameter was changed
        trigger = ctx.triggered[0]
        param_id = trigger['prop_id'].split('.')[0]
        param_value = trigger['value']
        
        manager = get_settings_manager()
        
        # Map parameter IDs to config updates
        param_map = {
            'param-live-data': ('USE_MOCK_DATA', not param_value),
            'param-batch-size': ('REST_BATCH_SIZE', param_value),
            'param-batch-interval': ('BATCH_INTERVAL_SEC', param_value),
            'param-fusion-mode': ('FUSION_MODE', param_value),
            'param-fusion-threshold': ('FUSION_THRESHOLD', param_value),
            'param-sizing-method': ('SIZING_METHOD', param_value),
            'param-max-position': ('MAX_POSITION_SIZE', param_value),
            'param-vote-method': ('VOTE_METHOD', param_value),
            'param-min-vote': ('MIN_VOTE_SCORE', param_value),
        }
        
        if param_id in param_map:
            param_name, value = param_map[param_id]
            
            # Update settings manager
            result = manager.update_parameter(param_name, value)
            
            # Update config if it exists
            if hasattr(dash_config, param_name):
                setattr(dash_config, param_name, value)
            if hasattr(root_config, param_name):
                setattr(root_config, param_name, value)
            
            logger.info(f"Parameter {param_name} updated to {value}")
            
            return f"✅ {param_name} updated"
        
        raise PreventUpdate
