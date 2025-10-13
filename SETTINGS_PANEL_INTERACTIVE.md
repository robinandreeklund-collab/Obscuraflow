# Settings Panel - Full Interactivity Implementation

## Overview

The Settings Panel now has full interactivity with Dash callbacks and a backend API for actually starting/stopping modules and agents.

## Architecture

### Components

1. **Settings Manager** (`dash_app/utils/settings_manager.py`)
   - Backend API for controlling system components
   - State persistence to `.settings_state.json`
   - Change logging to `.settings_log.json`
   - Module on/off control
   - Agent activation/deactivation
   - Parameter management

2. **Settings Callbacks** (`dash_app/callbacks/settings_callbacks.py`)
   - Dash callbacks for UI interactions
   - Pattern-matching callbacks for dynamic components
   - Module toggle handlers
   - Agent toggle handlers
   - Parameter update handlers

3. **Settings Panel** (`dash_app/panels/settings_panel.py`)
   - Interactive UI with pattern-matching IDs
   - Module control switches (enabled)
   - Agent control switches (enabled)
   - Parameter sliders and dropdowns
   - Live data integration

## Features

### 1. Module Control

**Functionality:**
- Toggle any of the 10 system modules on/off
- Real-time status indicators
- State persistence across sessions

**Implementation:**
```python
# Pattern-matching callback
@app.callback(
    Output({'type': 'module-switch', 'module': ALL}, 'value'),
    Input({'type': 'module-switch', 'module': ALL}, 'value'),
    ...
)
```

**Supported Modules:**
- DataStream
- TrendingPool
- Fusion
- VoteEngine
- Sizing
- PortfolioEngine
- SelfCritique
- MutationTracker
- DecisionCore
- TimespanEngine

### 2. Agent Control

**Functionality:**
- Activate/deactivate any of the 16 agents
- Creates agent instances when activated
- Removes instances when deactivated
- Real-time status from agent registry

**Implementation:**
```python
# Pattern-matching callback
@app.callback(
    Output({'type': 'agent-switch', 'agent': ALL}, 'value'),
    Input({'type': 'agent-switch', 'agent': ALL}, 'value'),
    ...
)
```

**Supported Agents (16):**
- Classic (4): MomentumAgent, ReversalAgent, BreakoutAgent, HybridAgent
- Paradigmatic (12): EchoAgent, FractalisAgent, VoxAgent, MycoAgent, ObscuraAgent, MirageAgent, SentioAgent, ReflexionAgent, DimensioAgent, SymbioAgent, GenesisAgent, ArchitectumAgent

### 3. Parameter Management

**Functionality:**
- Update system parameters in real-time
- Sliders for numeric values
- Dropdowns for categorical values
- Automatic config updates

**Supported Parameters:**
- **Data Stream:** Live/Mock toggle, batch size, batch interval
- **Fusion:** Mode, threshold
- **Sizing:** Method, max position size
- **Vote Engine:** Method, min vote score

### 4. State Persistence

**Files:**
- `.settings_state.json` - Current system state
- `.settings_log.json` - Complete change history

**State Structure:**
```json
{
  "modules": {
    "DataStream": true,
    "Fusion": false,
    ...
  },
  "agents": {
    "momentum_agent": true,
    "echo_agent": false,
    ...
  },
  "parameters": {
    "FUSION_THRESHOLD": 0.75,
    "MAX_POSITION_SIZE": 0.2,
    ...
  },
  "last_updated": "2025-10-13T12:00:00"
}
```

## Usage

### Starting a Module

1. Navigate to Settings Panel (`/settings`)
2. Find the module in Module Control section
3. Toggle the switch to ON
4. Status indicator turns green
5. Change is logged and persisted

### Activating an Agent

1. Navigate to Settings Panel
2. Find the agent in Agent Control table
3. Toggle the switch to ON
4. Agent instance is created via registry
5. Status shows "🟢 Active"
6. Change is logged and persisted

### Updating Parameters

1. Navigate to Settings Panel
2. Find parameter in System Parameters section
3. Adjust slider or select from dropdown
4. Change is applied immediately to config
5. Change is logged and persisted

## API Reference

### SettingsManager

```python
from dash_app.utils.settings_manager import get_settings_manager

manager = get_settings_manager()

# Module control
manager.toggle_module('DataStream', True)  # Activate
manager.toggle_module('DataStream', False)  # Deactivate
status = manager.get_module_status('DataStream')

# Agent control
manager.toggle_agent('momentum_agent', True)  # Activate
manager.toggle_agent('momentum_agent', False)  # Deactivate
status = manager.get_agent_status('momentum_agent')

# Parameter management
manager.update_parameter('FUSION_THRESHOLD', 0.8)

# Get recent changes
changes = manager.get_recent_changes(limit=10)
```

### Callbacks Registration

```python
from dash_app.callbacks.settings_callbacks import register_settings_callbacks

register_settings_callbacks(app)
```

## Benefits

1. **Real Control:** Actually controls system components, not just UI mockup
2. **State Persistence:** Settings survive across restarts
3. **Change Logging:** Complete audit trail of all changes
4. **Pattern Matching:** Scalable callback architecture
5. **Error Handling:** Graceful handling of failures
6. **Live Data:** Integration with agent registry and modules

## Testing

### Unit Tests
```bash
python3 -c "
from dash_app.utils.settings_manager import get_settings_manager
manager = get_settings_manager()

# Test module toggle
result = manager.toggle_module('DataStream', True)
assert result['success'] == True

# Test agent toggle
result = manager.toggle_agent('momentum_agent', True)
assert result['success'] == True

# Test parameter update
result = manager.update_parameter('FUSION_THRESHOLD', 0.75)
assert result['success'] == True
"
```

### Integration Test
```bash
# Start dashboard
python3 dash_app/app.py

# Navigate to http://localhost:8050/settings
# Toggle switches and verify behavior
```

## Future Enhancements

1. **Role-based Access:** Different permission levels
2. **Scheduled Changes:** Schedule parameter changes
3. **Rollback:** Undo recent changes
4. **Bulk Operations:** Activate/deactivate multiple components
5. **Presets:** Save/load configuration presets
6. **Notifications:** Alert on critical changes
7. **Validation:** Advanced parameter validation
8. **Dependencies:** Check module dependencies before toggling

## Technical Details

### Pattern-Matching Callbacks

Using Dash pattern-matching callbacks for dynamic components:

```python
# ID structure
{'type': 'module-switch', 'module': 'DataStream'}
{'type': 'agent-switch', 'agent': 'momentum_agent'}

# Callback matches ALL instances
Input({'type': 'module-switch', 'module': ALL}, 'value')
```

### State Management

- Settings state stored in `.settings_state.json` at project root
- Changes logged to `.settings_log.json` with timestamps
- In-memory cache for fast access
- Automatic save on every change

### Agent Instance Management

When activating an agent:
1. Check if instance already exists
2. If not, create via agent registry
3. Update state file
4. Log change

When deactivating an agent:
1. Remove instance from registry
2. Update state file
3. Log change

## Status

✅ **Fully Implemented and Tested**
- All components working
- State persistence operational
- Callbacks registered
- Integration complete
- Documentation provided
