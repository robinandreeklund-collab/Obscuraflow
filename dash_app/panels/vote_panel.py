"""
Vote Panel - Visar röstningsresultat och viktning
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Vote Engine panelen.
    """
    from modules.vote_engine import VoteEngine
    
    vote_engine = VoteEngine(weight_decay=0.95, learning_rate=0.1)
    stats = vote_engine.get_statistics()
    
    header = create_header(
        "Vote Engine",
        "Viktad röstning, konfliktlösning och agent performance tracking",
        "fas fa-vote-yea"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Votes",
                    stats.get('total_votes', 0),
                    icon="fas fa-check-circle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Avg Weight",
                    f"{stats.get('average_weight', 1.0):.2f}",
                    icon="fas fa-balance-scale"
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
                    "Success Rate",
                    f"{stats.get('success_rate', 0):.1f}%",
                    icon="fas fa-trophy"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent Weights", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['Momentum', 'Reversal', 'Breakout', 'Echo', 'Fractalis', 'Vox'],
                            [1.15, 0.95, 1.08, 1.02, 0.88, 1.12],
                            "Current Agent Weights",
                            "Agent",
                            "Weight",
                            '#7c3aed'
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Votes", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Agent', 'Vote', 'Weight', 'Outcome'],
                            [
                                ['MomentumAgent', 'BUY', '1.15', '✓ Correct'],
                                ['ReversalAgent', 'SELL', '0.95', '✗ Wrong'],
                                ['BreakoutAgent', 'BUY', '1.08', '✓ Correct'],
                                ['EchoAgent', 'HOLD', '1.02', '✓ Correct'],
                                ['VoxAgent', 'BUY', '1.12', '✓ Correct']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dcc.Interval(id='vote-panel-interval', interval=3000, n_intervals=0)
    ], fluid=True)
    
    return header, content
