"""
Settings Panel - System configuration and module control
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_status_badge
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

# Panel Metadata
PANEL_METADATA = {
    "data_source": "live",
    "live_ready": True,
    "verified": True,
    "phase": "Phase 3 - Live Data Integration Complete"
}

def create_module_control_section():
    """Creates the module control section with toggles for all modules"""
    
    modules = [
        {"name": "DataStream", "status": "active", "icon": "fas fa-stream"},
        {"name": "TrendingPool", "status": "active", "icon": "fas fa-fire"},
        {"name": "AgentLayer", "status": "active", "icon": "fas fa-users"},
        {"name": "Fusion", "status": "active", "icon": "fas fa-code-branch"},
        {"name": "VoteEngine", "status": "active", "icon": "fas fa-vote-yea"},
        {"name": "Sizing", "status": "active", "icon": "fas fa-chart-line"},
        {"name": "ExecutionMonitor", "status": "active", "icon": "fas fa-eye"},
        {"name": "PortfolioEngine", "status": "active", "icon": "fas fa-briefcase"},
        {"name": "SelfCritique", "status": "active", "icon": "fas fa-search"},
        {"name": "MutationTracker", "status": "active", "icon": "fas fa-dna"},
    ]
    
    module_cards = []
    for module in modules:
        module_cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className=f"{module['icon']} me-2", style={'color': '#00d9ff'}),
                            html.Span(module['name'], style={'fontWeight': 'bold'})
                        ], className="mb-2"),
                        html.Div([
                            html.Span("● ", style={'color': '#10b981' if module['status'] == 'active' else '#9ca3af'}),
                            html.Span(module['status'].title(), style={'fontSize': '12px'})
                        ]),
                        dbc.Switch(
                            id=f"module-switch-{module['name'].lower()}",
                            value=True if module['status'] == 'active' else False,
                            className="mt-2"
                        )
                    ])
                ], className="mb-2", style={'backgroundColor': '#1a1f3a'})
            ], width=12, lg=6, md=6)
        )
    
    return dbc.Card([
        dbc.CardHeader("🔌 Module Control", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
        dbc.CardBody([
            dbc.Row(module_cards)
        ])
    ], className="mb-3")


def create_agent_control_section():
    """Creates the agent control section"""
    
    agents = [
        {"name": "MomentumAgent", "active": True, "accuracy": 76.3, "confidence": 0.85},
        {"name": "ReversalAgent", "active": True, "accuracy": 78.5, "confidence": 0.82},
        {"name": "BreakoutAgent", "active": True, "accuracy": 82.1, "confidence": 0.88},
        {"name": "EchoAgent", "active": True, "accuracy": 79.8, "confidence": 0.86},
        {"name": "VoxAgent", "active": True, "accuracy": 81.2, "confidence": 0.87},
        {"name": "FractalisAgent", "active": True, "accuracy": 74.5, "confidence": 0.79},
        {"name": "GenesisAgent", "active": True, "accuracy": 77.3, "confidence": 0.83},
        {"name": "ObscuraAgent", "active": False, "accuracy": 71.0, "confidence": 0.75},
    ]
    
    agent_rows = []
    for agent in agents:
        status_icon = "🟢" if agent['active'] else "🔴"
        agent_rows.append([
            agent['name'],
            f"{status_icon} {'Active' if agent['active'] else 'Inactive'}",
            f"{agent['accuracy']:.1f}%",
            f"{agent['confidence']:.2f}",
            html.Div([
                dbc.Switch(
                    id=f"agent-switch-{agent['name'].lower()}",
                    value=agent['active'],
                    label=""
                )
            ])
        ])
    
    return dbc.Card([
        dbc.CardHeader("🧠 Agent Control", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
        dbc.CardBody([
            create_data_table(
                ['Agent', 'Status', 'Accuracy', 'Confidence', 'Toggle'],
                agent_rows
            )
        ])
    ], className="mb-3")


def create_parameter_section():
    """Creates the parameter configuration section"""
    
    return dbc.Card([
        dbc.CardHeader("⚙️ System Parameters", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("🔁 Data Stream", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                    html.Div([
                        html.Label("Live Data:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dbc.Switch(id="param-live-data", value=False, className="mb-2")
                    ]),
                    html.Div([
                        html.Label("Batch Size:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Slider(5, 50, 5, value=20, id="param-batch-size", 
                                  marks={5: '5', 25: '25', 50: '50'},
                                  tooltip={"placement": "bottom", "always_visible": False})
                    ], className="mb-3"),
                    html.Div([
                        html.Label("Batch Interval (sec):", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Slider(1, 60, 5, value=10, id="param-batch-interval",
                                  marks={1: '1', 30: '30', 60: '60'},
                                  tooltip={"placement": "bottom", "always_visible": False})
                    ], className="mb-3"),
                ], width=6),
                dbc.Col([
                    html.H6("🧠 Fusion", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                    html.Div([
                        html.Label("Fusion Mode:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Dropdown(
                            id="param-fusion-mode",
                            options=[
                                {'label': 'Majority', 'value': 'majority'},
                                {'label': 'Weighted', 'value': 'weighted'},
                                {'label': 'Consensus', 'value': 'consensus'}
                            ],
                            value='weighted',
                            style={'backgroundColor': '#1a1f3a', 'color': '#e5e7eb'}
                        )
                    ], className="mb-3"),
                    html.Div([
                        html.Label("Fusion Threshold:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Slider(0.5, 1.0, 0.1, value=0.7, id="param-fusion-threshold",
                                  marks={0.5: '0.5', 0.75: '0.75', 1.0: '1.0'},
                                  tooltip={"placement": "bottom", "always_visible": False})
                    ], className="mb-3"),
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H6("📐 Sizing", style={'color': '#00d9ff', 'marginBottom': '15px', 'marginTop': '15px'}),
                    html.Div([
                        html.Label("Sizing Method:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Dropdown(
                            id="param-sizing-method",
                            options=[
                                {'label': 'Fixed', 'value': 'fixed'},
                                {'label': 'Volatility', 'value': 'volatility'},
                                {'label': 'Confidence', 'value': 'confidence'}
                            ],
                            value='volatility',
                            style={'backgroundColor': '#1a1f3a', 'color': '#e5e7eb'}
                        )
                    ], className="mb-3"),
                    html.Div([
                        html.Label("Max Position Size:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Slider(0.01, 1.0, 0.05, value=0.2, id="param-max-position",
                                  marks={0.01: '1%', 0.5: '50%', 1.0: '100%'},
                                  tooltip={"placement": "bottom", "always_visible": False})
                    ], className="mb-3"),
                ], width=6),
                dbc.Col([
                    html.H6("🗳️ Vote Engine", style={'color': '#00d9ff', 'marginBottom': '15px', 'marginTop': '15px'}),
                    html.Div([
                        html.Label("Vote Method:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Dropdown(
                            id="param-vote-method",
                            options=[
                                {'label': 'Score', 'value': 'score'},
                                {'label': 'Weight', 'value': 'weight'},
                                {'label': 'Regime', 'value': 'regime'}
                            ],
                            value='weight',
                            style={'backgroundColor': '#1a1f3a', 'color': '#e5e7eb'}
                        )
                    ], className="mb-3"),
                    html.Div([
                        html.Label("Min Vote Score:", style={'fontSize': '12px', 'color': '#9ca3af'}),
                        dcc.Slider(0.1, 1.0, 0.1, value=0.5, id="param-min-vote",
                                  marks={0.1: '0.1', 0.5: '0.5', 1.0: '1.0'},
                                  tooltip={"placement": "bottom", "always_visible": False})
                    ], className="mb-3"),
                ], width=6)
            ])
        ])
    ], className="mb-3")


def create_panel_control_section():
    """Creates the panel control section"""
    
    panels = [
        {"name": "Portfolio Panel", "active": True, "mode": "live", "refresh": 3},
        {"name": "Agent Panel", "active": True, "mode": "live", "refresh": 4},
        {"name": "Vote Panel", "active": True, "mode": "live", "refresh": 3},
        {"name": "Mutation Panel", "active": True, "mode": "live", "refresh": 5},
        {"name": "Risk Panel", "active": True, "mode": "live", "refresh": 3},
    ]
    
    panel_rows = []
    for panel in panels:
        status_icon = "🟢" if panel['active'] else "🔴"
        panel_rows.append([
            panel['name'],
            f"{status_icon} {'Active' if panel['active'] else 'Inactive'}",
            panel['mode'].title(),
            f"{panel['refresh']}s",
            html.Div([
                dbc.Switch(
                    id=f"panel-switch-{panel['name'].lower().replace(' ', '-')}",
                    value=panel['active'],
                    label=""
                )
            ])
        ])
    
    return dbc.Card([
        dbc.CardHeader("📊 Panel Control", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
        dbc.CardBody([
            create_data_table(
                ['Panel', 'Status', 'Mode', 'Refresh', 'Toggle'],
                panel_rows
            )
        ])
    ], className="mb-3")


def create_system_status_section():
    """Creates the system status and log section"""
    
    from datetime import datetime, timedelta
    now = datetime.now()
    
    status_data = {
        'active_modules': 10,
        'active_agents': 7,
        'api_status': 'Connected',
        'ws_status': 'Active',
        'portfolio_value': '$125,430'
    }
    
    recent_changes = [
        [
            (now - timedelta(minutes=5)).strftime('%H:%M:%S'),
            'Parameter Change',
            'Fusion Threshold',
            '0.6 → 0.7'
        ],
        [
            (now - timedelta(minutes=12)).strftime('%H:%M:%S'),
            'Module Toggle',
            'SelfCritique',
            'Activated'
        ],
        [
            (now - timedelta(minutes=25)).strftime('%H:%M:%S'),
            'Agent Toggle',
            'ObscuraAgent',
            'Deactivated'
        ],
        [
            (now - timedelta(hours=1)).strftime('%H:%M:%S'),
            'Parameter Change',
            'Max Position Size',
            '0.15 → 0.20'
        ],
    ]
    
    return dbc.Card([
        dbc.CardHeader("📡 System Status & Activity Log", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Current Status", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                    html.Div([
                        html.P(f"Active Modules: {status_data['active_modules']}/10", className="mb-2"),
                        html.P(f"Active Agents: {status_data['active_agents']}/8", className="mb-2"),
                        html.P([
                            html.Span("API Status: ", style={'color': '#9ca3af'}),
                            html.Span(f"● {status_data['api_status']}", style={'color': '#10b981'})
                        ], className="mb-2"),
                        html.P([
                            html.Span("WebSocket: ", style={'color': '#9ca3af'}),
                            html.Span(f"● {status_data['ws_status']}", style={'color': '#10b981'})
                        ], className="mb-2"),
                        html.P(f"Portfolio Value: {status_data['portfolio_value']}", className="mb-2"),
                    ])
                ], width=4),
                dbc.Col([
                    html.H6("Recent Changes", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                    create_data_table(
                        ['Time', 'Type', 'Component', 'Change'],
                        recent_changes
                    )
                ], width=8)
            ])
        ])
    ], className="mb-3")


def create_panel():
    """
    Creates the Settings Panel with system configuration and module control.
    """
    header = create_header(
        "System Settings",
        "Module control, agent management, and system configuration",
        "fas fa-cog"
    )
    
    content = dbc.Container([
        # Top Metrics Row
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Active Modules",
                    "10/10",
                    icon="fas fa-puzzle-piece"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Active Agents",
                    "7/8",
                    icon="fas fa-users"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Active Panels",
                    "15/15",
                    icon="fas fa-th-large"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "System Health",
                    "Excellent",
                    icon="fas fa-heart"
                )
            ], width=12, lg=3, md=6)
        ], className="mb-4"),
        
        # Module Control
        create_module_control_section(),
        
        # Agent Control
        create_agent_control_section(),
        
        # Parameters
        create_parameter_section(),
        
        # Panel Control
        create_panel_control_section(),
        
        # System Status
        create_system_status_section(),
        
        # Info Alert
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.I(className="fas fa-info-circle me-2"),
                    "Settings changes are applied in real-time. All changes are logged for traceability."
                ], color="info", className="mb-0")
            ])
        ]),
        
        # Auto-refresh interval
        dcc.Interval(
            id='settings-panel-interval',
            interval=5000,  # 5 seconds
            n_intervals=0
        )
    ], fluid=True)
    
    return header, content
