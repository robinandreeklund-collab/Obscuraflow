"""
Decision Core Panel - Visar agentbeslut och konsensusanalys
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Decision Core panelen med live data.
    """
    # Import modules
    from modules.decision_core import DecisionCore
    
    # Initialize with mock data
    decision_core = DecisionCore(min_confidence=50.0, conflict_threshold=0.4)
    stats = decision_core.get_stats()
    
    header = create_header(
        "Decision Core",
        "Agentbeslut, konsensusanalys och beslutsrouting",
        "fas fa-brain"
    )
    
    content = dbc.Container([
        # Metrics row
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Decisions",
                    stats.get('total_decisions', 0),
                    icon="fas fa-clipboard-check"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Consensus Rate",
                    f"{stats.get('consensus_rate', 0):.1f}%",
                    icon="fas fa-handshake"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Conflict Rate",
                    f"{stats.get('conflict_rate', 0):.1f}%",
                    icon="fas fa-exclamation-triangle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Avg Confidence",
                    f"{stats.get('average_confidence', 0):.1f}%",
                    icon="fas fa-chart-line"
                )
            ], width=3)
        ], className="mb-4"),
        
        # Decisions by type
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Decision Distribution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['BUY', 'SELL', 'HOLD'],
                            [
                                stats.get('buy_count', 0),
                                stats.get('sell_count', 0),
                                stats.get('hold_count', 0)
                            ],
                            "Decisions by Type",
                            "Decision Type",
                            "Count"
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Decisions", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Symbol', 'Decision', 'Confidence', 'Status'],
                            [
                                ['AAPL', 'BUY', '75.5%', '✓ Consensus'],
                                ['GOOGL', 'SELL', '68.2%', '⚠ Conflict'],
                                ['MSFT', 'HOLD', '82.0%', '✓ Consensus'],
                                ['TSLA', 'BUY', '71.3%', '✓ Consensus'],
                                ['AMZN', 'SELL', '65.8%', '✓ Consensus']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        # Agent activity
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent Activity", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🤖 MomentumAgent - 15 decisions (Active)", className="mb-2"),
                            html.P("🔄 ReversalAgent - 12 decisions (Active)", className="mb-2"),
                            html.P("⚡ BreakoutAgent - 18 decisions (Active)", className="mb-2"),
                            html.P("🌊 EchoAgent - 14 decisions (Active)", className="mb-2"),
                            html.P("📊 FractalisAgent - 11 decisions (Active)", className="mb-2"),
                            html.P("🗣️ VoxAgent - 16 decisions (Active)", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Auto-refresh interval
        dcc.Interval(
            id='decision-core-interval',
            interval=3000,  # 3 seconds
            n_intervals=0
        )
    ], fluid=True)
    
    return header, content
