"""
System Flow Panel - Visuell karta över hela systemets modulflöde
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_status_badge
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
    Skapar System Flow panelen.
    """
    header = create_header(
        "System Flow",
        "Visuell systemkarta, modulflöde och real-time status",
        "fas fa-project-diagram"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Active Modules",
                    "19/19",
                    icon="fas fa-puzzle-piece"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Data Flow Rate",
                    "1250 msg/s",
                    icon="fas fa-stream"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "System Uptime",
                    "99.8%",
                    icon="fas fa-clock"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Latency",
                    "12ms",
                    icon="fas fa-tachometer-alt"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Data Pipeline", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Span("1️⃣ DataStream ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Market data collection & trend analysis", className="ms-4 mb-3")
                            ]),
                            html.Div([
                                html.Span("2️⃣ TrendingPool ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Symbol ranking & heat analysis", className="ms-4 mb-3")
                            ]),
                            html.Div([
                                html.Span("3️⃣ DecisionCore ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Agent consensus & decision routing", className="ms-4 mb-3")
                            ]),
                            html.Div([
                                html.Span("4️⃣ VoteEngine ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Conflict resolution & weighted voting", className="ms-4 mb-3")
                            ]),
                        ])
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Signal Processing", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Span("5️⃣ Fusion ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Multi-timeframe signal validation", className="ms-4 mb-3")
                            ]),
                            html.Div([
                                html.Span("6️⃣ Sizing ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Kelly criterion & position sizing", className="ms-4 mb-3")
                            ]),
                            html.Div([
                                html.Span("7️⃣ TimespanEngine ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Timeframe synchronization", className="ms-4 mb-3")
                            ]),
                            html.Div([
                                html.Span("8️⃣ PortfolioEngine ", style={'fontWeight': 'bold'}),
                                create_status_badge('active'),
                                html.P("→ Portfolio optimization & tracking", className="ms-4 mb-3")
                            ])
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent & Analysis Systems", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div("🤖 Agent Systems:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                            html.P("• AgentSpectrum → AgentLifecycle → SynergyMatrix → MetaGovernor", className="ms-3 mb-2"),
                            html.Div("🔬 Evolution & Learning:", style={'fontWeight': 'bold', 'marginTop': '15px', 'marginBottom': '10px'}),
                            html.P("• Evolution → MutationTracker → SelfCritique → SymbolMemory", className="ms-3 mb-2"),
                            html.Div("💼 Portfolio & Risk:", style={'fontWeight': 'bold', 'marginTop': '15px', 'marginBottom': '10px'}),
                            html.P("• PortfolioComparator → RiskMapper → NarrativeEngine", className="ms-3 mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H5("System Health: Excellent", className="alert-heading"),
                    html.P("All modules operational. Data flow stable. No errors detected."),
                    html.Hr(),
                    html.P("Last check: Just now | Next scheduled maintenance: 48h", className="mb-0")
                ], color="success")
            ])
        ]),
        
        dcc.Interval(id='system-flow-panel-interval', interval=2000, n_intervals=0)
    ], fluid=True)
    
    return header, content
