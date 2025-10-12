"""
Agent Lifecycle Panel - Agent lifecycle management
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Agent Lifecycle panelen.
    """
    from modules.agent_lifecycle import AgentLifecycle
    
    lifecycle = AgentLifecycle()
    stats = lifecycle.get_statistics()
    
    header = create_header(
        "Agent Lifecycle",
        "Birth, activation, deactivation, retirement och performance tracking",
        "fas fa-heartbeat"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Active Agents",
                    stats.get('active_agents', 0),
                    icon="fas fa-check-circle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Inactive Agents",
                    stats.get('inactive_agents', 0),
                    icon="fas fa-pause-circle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Retired Agents",
                    stats.get('retired_agents', 0),
                    icon="fas fa-stop-circle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Total Born",
                    stats.get('total_agents', 0),
                    icon="fas fa-baby"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Lifecycle Distribution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['Birth', 'Active', 'Inactive', 'Retired'],
                            [
                                stats.get('birth_count', 0),
                                stats.get('active_agents', 0),
                                stats.get('inactive_agents', 0),
                                stats.get('retired_agents', 0)
                            ],
                            "Agent Lifecycle States",
                            "State",
                            "Count",
                            '#10b981'
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent Status", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Agent', 'State', 'Performance', 'Age (days)'],
                            [
                                ['MomentumAgent', '✓ Active', '85.2%', '45'],
                                ['ReversalAgent', '✓ Active', '78.5%', '42'],
                                ['BreakoutAgent', '✓ Active', '82.1%', '38'],
                                ['EchoAgent', '✓ Active', '79.8%', '35'],
                                ['FractalisAgent', '⏸ Inactive', '65.3%', '28'],
                                ['ObscuraAgent', '🛑 Retired', '45.2%', '62']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Lifecycle Events", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🐣 Birth: HybridAgent-X created (2 hours ago)", className="mb-2"),
                            html.P("✅ Activation: VoxAgent activated (5 hours ago)", className="mb-2"),
                            html.P("⏸️ Deactivation: MirageAgent deactivated (1 day ago)", className="mb-2"),
                            html.P("🛑 Retirement: LegacyAgent retired (3 days ago)", className="mb-2"),
                            html.P("📊 Performance Check: All active agents reviewed", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='lifecycle-panel-interval', interval=4000, n_intervals=0)
    ], fluid=True)
    
    return header, content
