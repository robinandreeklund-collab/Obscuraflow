"""
Timespan Intelligence Panel - Multi-timeframe synchronization
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Timespan Intelligence panelen.
    """
    from modules.timespan_engine import TimespanEngine
    
    timespan = TimespanEngine()
    stats = timespan.get_stats()
    
    header = create_header(
        "Timespan Intelligence",
        "Multi-timeframe synchronization och RL-träning",
        "fas fa-clock"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Active Timeframes",
                    stats.get('active_timeframes', 5),
                    icon="fas fa-stream"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Sync Score",
                    f"{stats.get('sync_score', 0.85):.2f}",
                    icon="fas fa-sync"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "RL Episodes",
                    stats.get('rl_episodes', 0),
                    icon="fas fa-brain"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Reward",
                    f"{stats.get('total_reward', 0):.2f}",
                    icon="fas fa-award"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Timeframe Status", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Timeframe', 'Status', 'Signals', 'Confidence'],
                            [
                                ['1 min', '✓ Active', '125', '78%'],
                                ['5 min', '✓ Active', '98', '82%'],
                                ['15 min', '✓ Active', '67', '85%'],
                                ['1 hour', '✓ Active', '34', '88%'],
                                ['4 hour', '✓ Active', '18', '91%'],
                                ['1 day', '⚠ Syncing', '8', '75%']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Convergence Analysis", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA'],
                            [0.85, 0.78, 0.92, 0.68, 0.88],
                            "Timeframe Convergence Score",
                            "Symbol",
                            "Score",
                            '#10b981'
                        )
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dcc.Interval(id='timespan-panel-interval', interval=5000, n_intervals=0)
    ], fluid=True)
    
    return header, content
