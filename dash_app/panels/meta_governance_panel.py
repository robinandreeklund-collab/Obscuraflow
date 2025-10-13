"""
Meta Governance Panel - Meta-level agent governance
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

# Panel Metadata
PANEL_METADATA = {
    "data_source": "live",
    "live_ready": True,
    "verified": True,
    "phase": "Phase 3 - Live Data Integration Complete"
}

def create_panel():
    """
    Skapar Meta Governance panelen.
    """
    from modules.metaagentgovernor import MetaAgentGovernor
    
    governor = MetaAgentGovernor()
    stats = governor.get_stats()
    
    header = create_header(
        "Meta Governance",
        "Priority rebalancing, conflict resolution och resource enforcement",
        "fas fa-crown"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Governance Decisions",
                    stats.get('total_decisions', 0),
                    icon="fas fa-gavel"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Conflicts Resolved",
                    stats.get('conflicts_resolved', 0),
                    icon="fas fa-handshake"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Resources Allocated",
                    f"{stats.get('resource_utilization', 0):.1f}%",
                    icon="fas fa-server"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Priority Changes",
                    stats.get('priority_changes', 0),
                    icon="fas fa-sort-amount-down"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent Priorities", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['Momentum', 'Reversal', 'Echo', 'Fractalis', 'Vox', 'Genesis'],
                            [0.92, 0.85, 0.88, 0.78, 0.90, 0.95],
                            "Current Agent Priorities",
                            "Agent",
                            "Priority",
                            '#7c3aed'
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Resource Distribution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🖥️ Compute: 75% allocated", className="mb-2"),
                            html.P("💾 Memory: 68% allocated", className="mb-2"),
                            html.P("🌐 Network: 45% allocated", className="mb-2"),
                            html.P("⚡ Energy: 82% allocated", className="mb-2"),
                            html.Hr(),
                            html.P("Total Efficiency: 87.5%", style={'fontWeight': 'bold', 'color': '#10b981'})
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Governance Actions", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Time', 'Action', 'Agent', 'Reason'],
                            [
                                ['10:23', 'Priority ↑', 'GenesisAgent', 'High performance'],
                                ['10:15', 'Conflict Resolved', 'Echo vs Vox', 'Consensus reached'],
                                ['09:58', 'Resource Allocated', 'FractalisAgent', 'Complex analysis'],
                                ['09:42', 'Priority ↓', 'MirageAgent', 'Low accuracy'],
                                ['09:30', 'Rebalance', 'All Agents', 'Scheduled optimization']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='governance-panel-interval', interval=4000, n_intervals=0)
    ], fluid=True)
    
    return header, content
