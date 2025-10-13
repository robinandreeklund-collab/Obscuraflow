"""
Settings Manager - Backend API for controlling modules and agents
Handles starting/stopping modules and agents with state persistence
"""

import logging
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Path for settings state file
SETTINGS_STATE_FILE = Path(__file__).parent.parent.parent / '.settings_state.json'
SETTINGS_LOG_FILE = Path(__file__).parent.parent.parent / '.settings_log.json'


class SettingsManager:
    """
    Manages system settings with state persistence and change logging.
    Provides API for controlling modules and agents.
    """
    
    def __init__(self):
        """Initialize SettingsManager with state loading"""
        self.state = self._load_state()
        self.changes_log = []
        
    def _load_state(self) -> Dict[str, Any]:
        """Load settings state from file"""
        if SETTINGS_STATE_FILE.exists():
            try:
                with open(SETTINGS_STATE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load settings state: {e}")
        
        # Default state
        return {
            'modules': {},
            'agents': {},
            'parameters': {},
            'last_updated': None
        }
    
    def _save_state(self):
        """Save settings state to file"""
        try:
            self.state['last_updated'] = datetime.now().isoformat()
            with open(SETTINGS_STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.info("Settings state saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings state: {e}")
    
    def _log_change(self, change_type: str, component: str, old_value: Any, new_value: Any):
        """Log a settings change"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': change_type,
            'component': component,
            'old_value': str(old_value),
            'new_value': str(new_value)
        }
        
        self.changes_log.append(log_entry)
        
        # Keep only last 100 changes in memory
        if len(self.changes_log) > 100:
            self.changes_log = self.changes_log[-100:]
        
        # Append to log file
        try:
            mode = 'a' if SETTINGS_LOG_FILE.exists() else 'w'
            with open(SETTINGS_LOG_FILE, mode) as f:
                json.dump(log_entry, f)
                f.write('\n')
        except Exception as e:
            logger.error(f"Failed to log change: {e}")
    
    def get_module_status(self, module_name: str) -> bool:
        """Get module active status"""
        return self.state['modules'].get(module_name, False)
    
    def toggle_module(self, module_name: str, active: bool) -> Dict[str, Any]:
        """
        Toggle a module on/off
        
        Args:
            module_name: Name of the module
            active: True to activate, False to deactivate
            
        Returns:
            Dict with status and message
        """
        old_status = self.state['modules'].get(module_name, False)
        
        # Update state
        self.state['modules'][module_name] = active
        self._save_state()
        
        # Log change
        self._log_change('Module Toggle', module_name, old_status, active)
        
        logger.info(f"Module {module_name} toggled to {'active' if active else 'inactive'}")
        
        return {
            'success': True,
            'module': module_name,
            'status': 'active' if active else 'inactive',
            'message': f"Module {module_name} {'activated' if active else 'deactivated'}"
        }
    
    def get_agent_status(self, agent_id: str) -> bool:
        """Get agent active status"""
        return self.state['agents'].get(agent_id, False)
    
    def toggle_agent(self, agent_id: str, active: bool) -> Dict[str, Any]:
        """
        Toggle an agent on/off
        
        Args:
            agent_id: ID of the agent
            active: True to activate, False to deactivate
            
        Returns:
            Dict with status and message
        """
        old_status = self.state['agents'].get(agent_id, False)
        
        # If activating agent, try to create instance
        if active:
            try:
                from agents.agent_registry import get_registry
                registry = get_registry()
                
                # Check if already has instance
                instance = registry.get_instance(agent_id)
                if not instance:
                    # Create new instance
                    instance = registry.create_agent(agent_id)
                    if instance:
                        logger.info(f"Agent {agent_id} instance created")
                    else:
                        return {
                            'success': False,
                            'agent': agent_id,
                            'message': f"Failed to create agent {agent_id} instance"
                        }
            except Exception as e:
                logger.error(f"Error creating agent {agent_id}: {e}")
                return {
                    'success': False,
                    'agent': agent_id,
                    'message': f"Error: {str(e)}"
                }
        else:
            # If deactivating, remove instance
            try:
                from agents.agent_registry import get_registry
                registry = get_registry()
                registry.remove_instance(agent_id)
                logger.info(f"Agent {agent_id} instance removed")
            except Exception as e:
                logger.error(f"Error removing agent {agent_id}: {e}")
        
        # Update state
        self.state['agents'][agent_id] = active
        self._save_state()
        
        # Log change
        self._log_change('Agent Toggle', agent_id, old_status, active)
        
        return {
            'success': True,
            'agent': agent_id,
            'status': 'active' if active else 'inactive',
            'message': f"Agent {agent_id} {'activated' if active else 'deactivated'}"
        }
    
    def update_parameter(self, param_name: str, param_value: Any) -> Dict[str, Any]:
        """
        Update a system parameter
        
        Args:
            param_name: Name of the parameter
            param_value: New value
            
        Returns:
            Dict with status and message
        """
        old_value = self.state['parameters'].get(param_name)
        
        # Update state
        self.state['parameters'][param_name] = param_value
        self._save_state()
        
        # Log change
        self._log_change('Parameter Change', param_name, old_value, param_value)
        
        logger.info(f"Parameter {param_name} updated: {old_value} → {param_value}")
        
        return {
            'success': True,
            'parameter': param_name,
            'old_value': old_value,
            'new_value': param_value,
            'message': f"Parameter {param_name} updated successfully"
        }
    
    def get_recent_changes(self, limit: int = 10) -> list:
        """Get recent settings changes"""
        return self.changes_log[-limit:]
    
    def get_all_modules_status(self) -> Dict[str, bool]:
        """Get status of all modules"""
        return self.state['modules'].copy()
    
    def get_all_agents_status(self) -> Dict[str, bool]:
        """Get status of all agents"""
        return self.state['agents'].copy()


# Global settings manager instance
_settings_manager = None


def get_settings_manager() -> SettingsManager:
    """
    Get or create global settings manager instance
    
    Returns:
        SettingsManager instance
    """
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
