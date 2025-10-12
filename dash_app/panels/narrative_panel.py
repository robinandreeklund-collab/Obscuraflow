"""
Narrative Panel - Händelseflöde och systemberättelse
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Narrative Engine panelen.
    """
    from modules.narrative_engine import NarrativeEngine
    
    narrative = NarrativeEngine()
    stats = narrative.get_stats()
    
    header = create_header(
        "Narrative Engine",
        "Händelseflöde, causal chains och systemberättelse",
        "fas fa-book"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Events",
                    stats.get('total_events', 0),
                    icon="fas fa-list"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Causal Chains",
                    stats.get('causal_chains', 0),
                    icon="fas fa-link"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Event Groups",
                    stats.get('event_groups', 0),
                    icon="fas fa-object-group"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Active Stories",
                    stats.get('active_stories', 0),
                    icon="fas fa-book-open"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Narrative", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Span("10:45:23", style={'color': '#9ca3af', 'marginRight': '10px'}),
                                html.Span("📊 ", style={'fontSize': '16px'}),
                                html.Span("DecisionCore received 6 agent votes for AAPL. Consensus reached: BUY with 85% confidence.", className="mb-2")
                            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'}),
                            
                            html.Div([
                                html.Span("10:45:18", style={'color': '#9ca3af', 'marginRight': '10px'}),
                                html.Span("🤖 ", style={'fontSize': '16px'}),
                                html.Span("MomentumAgent detected strong bullish momentum in AAPL. Score: 0.92.", className="mb-2")
                            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'}),
                            
                            html.Div([
                                html.Span("10:45:12", style={'color': '#9ca3af', 'marginRight': '10px'}),
                                html.Span("📈 ", style={'fontSize': '16px'}),
                                html.Span("TrendingPool ranked AAPL at #1 with heat score 8.5. Volume spike detected.", className="mb-2")
                            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'}),
                            
                            html.Div([
                                html.Span("10:45:05", style={'color': '#9ca3af', 'marginRight': '10px'}),
                                html.Span("🔄 ", style={'fontSize': '16px'}),
                                html.Span("DataStream updated market data for 8 symbols. Trend analysis complete.", className="mb-2")
                            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'}),
                            
                            html.Div([
                                html.Span("10:44:58", style={'color': '#9ca3af', 'marginRight': '10px'}),
                                html.Span("⚡ ", style={'fontSize': '16px'}),
                                html.Span("Fusion module validated BUY signal across 3 timeframes. Convergence score: 0.88.", className="mb-2")
                            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'}),
                            
                            html.Div([
                                html.Span("10:44:52", style={'color': '#9ca3af', 'marginRight': '10px'}),
                                html.Span("💼 ", style={'fontSize': '16px'}),
                                html.Span("Sizing calculated position: 250 shares AAPL ($45,000). Kelly %: 12.5%.", className="mb-2")
                            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'}),
                        ])
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Causal Chains", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.H6("Chain #1: AAPL Buy Decision", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                            html.P("1. Market data update → ", className="mb-1"),
                            html.P("2. Trend analysis (score 8.5) → ", className="mb-1"),
                            html.P("3. Agent consensus (6 votes) → ", className="mb-1"),
                            html.P("4. Signal validation (3 TF) → ", className="mb-1"),
                            html.P("5. Position sizing (12.5%) → ", className="mb-1"),
                            html.P("6. Portfolio allocation", className="mb-3", style={'fontWeight': 'bold'}),
                            
                            html.H6("Chain #2: TSLA Conflict Resolution", style={'color': '#00d9ff', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.P("1. Mixed signals detected → ", className="mb-1"),
                            html.P("2. VoteEngine activated → ", className="mb-1"),
                            html.P("3. Weighted voting (4-2) → ", className="mb-1"),
                            html.P("4. Conflict resolved: HOLD", className="mb-1", style={'fontWeight': 'bold'})
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Event Statistics", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("📊 Decision Events: 145 (42%)", className="mb-2"),
                            html.P("🤖 Agent Events: 98 (28%)", className="mb-2"),
                            html.P("💼 Portfolio Events: 67 (19%)", className="mb-2"),
                            html.P("⚠️ Risk Events: 28 (8%)", className="mb-2"),
                            html.P("🔄 System Events: 8 (3%)", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='narrative-panel-interval', interval=2000, n_intervals=0)
    ], fluid=True)
    
    return header, content
