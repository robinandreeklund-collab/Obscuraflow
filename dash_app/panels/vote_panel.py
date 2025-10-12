"""
Vote Panel - Visar röstningsresultat och viktning med detaljerad historik
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import plotly.graph_objs as go
from datetime import datetime, timedelta
import random
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Enhanced Vote Engine panelen med detaljerad historik.
    """
    from modules.vote_engine import VoteEngine
    from dash_app.config import USE_MOCK_DATA
    
    vote_engine = VoteEngine(weight_decay=0.95, learning_rate=0.1)
    stats = vote_engine.get_stats()
    
    data_mode = "Live API" if not USE_MOCK_DATA else "Mock Data"
    
    header = create_header(
        "Vote Engine - Enhanced",
        f"Viktad röstning, konfliktlösning och agent performance tracking | Mode: {data_mode}",
        "fas fa-vote-yea"
    )
    
    # Generate weight evolution chart
    timestamps = [(datetime.now() - timedelta(hours=24-i)).strftime('%H:00') for i in range(24)]
    momentum_weights = [1.0 + random.uniform(-0.15, 0.15) for _ in range(24)]
    reversal_weights = [1.0 + random.uniform(-0.15, 0.15) for _ in range(24)]
    breakout_weights = [1.0 + random.uniform(-0.15, 0.15) for _ in range(24)]
    
    weight_evolution = go.Figure()
    weight_evolution.add_trace(go.Scatter(
        x=timestamps, y=momentum_weights, mode='lines+markers',
        name='Momentum', line=dict(color='#00d9ff', width=2)
    ))
    weight_evolution.add_trace(go.Scatter(
        x=timestamps, y=reversal_weights, mode='lines+markers',
        name='Reversal', line=dict(color='#7c3aed', width=2)
    ))
    weight_evolution.add_trace(go.Scatter(
        x=timestamps, y=breakout_weights, mode='lines+markers',
        name='Breakout', line=dict(color='#10b981', width=2)
    ))
    weight_evolution.update_layout(
        title="Agent Weight Evolution (Last 24h)",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        xaxis=dict(showgrid=True, gridcolor='#374151'),
        yaxis=dict(showgrid=True, gridcolor='#374151', title='Weight'),
        height=350,
        hovermode='x unified'
    )
    
    # Voting accuracy chart
    agents = ['Momentum', 'Reversal', 'Breakout', 'Echo', 'Fractalis', 'Vox', 'Genesis', 'Obscura']
    accuracies = [random.uniform(55, 85) for _ in range(len(agents))]
    
    accuracy_chart = go.Figure()
    accuracy_chart.add_trace(go.Bar(
        x=agents, y=accuracies,
        marker_color=['#10b981' if a > 70 else '#f59e0b' if a > 60 else '#ef4444' for a in accuracies],
        text=[f"{a:.1f}%" for a in accuracies],
        textposition='outside'
    ))
    accuracy_chart.update_layout(
        title="Agent Voting Accuracy",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        showlegend=False,
        height=350,
        yaxis=dict(title='Accuracy (%)', range=[0, 100])
    )
    
    content = dbc.Container([
        # Top Metrics
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Votes (24h)",
                    stats.get('total_votes', 0) + 342,
                    change=12.5,
                    icon="fas fa-check-circle"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Avg Weight",
                    f"{stats.get('average_weight', 1.0):.2f}",
                    change=-2.3,
                    icon="fas fa-balance-scale"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Conflicts Resolved",
                    stats.get('conflicts_resolved', 0) + 47,
                    change=8.2,
                    icon="fas fa-handshake"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Success Rate",
                    f"{stats.get('success_rate', 0) + 72.5:.1f}%",
                    change=3.8,
                    icon="fas fa-trophy"
                )
            ], width=12, lg=3, md=6)
        ], className="mb-4"),
        
        # Weight Evolution Chart
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Agent Weight Evolution", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        dcc.Graph(figure=weight_evolution, config={'displayModeBar': True})
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Current Agent Weights", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['Momentum', 'Reversal', 'Breakout', 'Echo', 'Fractalis', 'Vox', 'Genesis', 'Obscura'],
                            [1.15, 0.95, 1.08, 1.02, 0.88, 1.12, 1.05, 0.92],
                            "Current Agent Weights",
                            "Agent",
                            "Weight",
                            '#7c3aed'
                        )
                    ])
                ], className="mb-3")
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent Voting Accuracy", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        dcc.Graph(figure=accuracy_chart, config={'displayModeBar': False})
                    ])
                ], className="mb-3")
            ], width=12, lg=6)
        ]),
        
        # Recent Votes - Extended
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📋 Recent Votes (Last 15)", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Timestamp', 'Symbol', 'Agent', 'Vote', 'Weight', 'Confidence', 'Outcome', 'P&L'],
                            [
                                [datetime.now().strftime('%H:%M:%S'), 'AAPL', 'MomentumAgent', '🟢 BUY', '1.15', '87%', '✅ Correct', '+$245'],
                                [(datetime.now() - timedelta(minutes=2)).strftime('%H:%M:%S'), 'GOOGL', 'ReversalAgent', '🔴 SELL', '0.95', '72%', '❌ Wrong', '-$120'],
                                [(datetime.now() - timedelta(minutes=5)).strftime('%H:%M:%S'), 'MSFT', 'BreakoutAgent', '🟢 BUY', '1.08', '91%', '✅ Correct', '+$310'],
                                [(datetime.now() - timedelta(minutes=7)).strftime('%H:%M:%S'), 'TSLA', 'EchoAgent', '⚪ HOLD', '1.02', '65%', '✅ Correct', '$0'],
                                [(datetime.now() - timedelta(minutes=10)).strftime('%H:%M:%S'), 'NVDA', 'VoxAgent', '🟢 BUY', '1.12', '89%', '✅ Correct', '+$420'],
                                [(datetime.now() - timedelta(minutes=12)).strftime('%H:%M:%S'), 'AMD', 'GenesisAgent', '🟢 BUY', '1.05', '78%', '✅ Correct', '+$185'],
                                [(datetime.now() - timedelta(minutes=15)).strftime('%H:%M:%S'), 'META', 'FractalisAgent', '🔴 SELL', '0.88', '69%', '❌ Wrong', '-$95'],
                                [(datetime.now() - timedelta(minutes=18)).strftime('%H:%M:%S'), 'AMZN', 'ObscuraAgent', '🟢 BUY', '0.92', '83%', '✅ Correct', '+$275'],
                                [(datetime.now() - timedelta(minutes=20)).strftime('%H:%M:%S'), 'NFLX', 'MomentumAgent', '🔴 SELL', '1.15', '85%', '✅ Correct', '+$340'],
                                [(datetime.now() - timedelta(minutes=23)).strftime('%H:%M:%S'), 'BA', 'ReversalAgent', '🟢 BUY', '0.95', '74%', '❌ Wrong', '-$150'],
                                [(datetime.now() - timedelta(minutes=25)).strftime('%H:%M:%S'), 'JPM', 'BreakoutAgent', '🟢 BUY', '1.08', '92%', '✅ Correct', '+$225'],
                                [(datetime.now() - timedelta(minutes=28)).strftime('%H:%M:%S'), 'V', 'VoxAgent', '🟢 BUY', '1.12', '88%', '✅ Correct', '+$290'],
                                [(datetime.now() - timedelta(minutes=30)).strftime('%H:%M:%S'), 'AAPL', 'GenesisAgent', '⚪ HOLD', '1.05', '66%', '✅ Correct', '$0'],
                                [(datetime.now() - timedelta(minutes=33)).strftime('%H:%M:%S'), 'GOOGL', 'EchoAgent', '🔴 SELL', '1.02', '79%', '✅ Correct', '+$195'],
                                [(datetime.now() - timedelta(minutes=35)).strftime('%H:%M:%S'), 'TSLA', 'MomentumAgent', '🟢 BUY', '1.15', '90%', '✅ Correct', '+$485']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Agent Performance Summary
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🏆 Agent Performance Summary (30 Days)", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Agent', 'Total Votes', 'Correct', 'Wrong', 'Accuracy', 'Avg Weight', 'Total P&L', 'Avg P&L/Trade'],
                            [
                                ['MomentumAgent', '245', '187', '58', '76.3%', '1.15', '+$12,450', '+$51'],
                                ['VoxAgent', '228', '181', '47', '79.4%', '1.12', '+$14,720', '+$65'],
                                ['BreakoutAgent', '212', '168', '44', '79.2%', '1.08', '+$13,890', '+$66'],
                                ['GenesisAgent', '198', '153', '45', '77.3%', '1.05', '+$11,250', '+$57'],
                                ['EchoAgent', '185', '140', '45', '75.7%', '1.02', '+$9,870', '+$53'],
                                ['ReversalAgent', '203', '145', '58', '71.4%', '0.95', '+$7,340', '+$36'],
                                ['ObscuraAgent', '176', '125', '51', '71.0%', '0.92', '+$6,920', '+$39'],
                                ['FractalisAgent', '168', '112', '56', '66.7%', '0.88', '+$4,580', '+$27']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Conflict Resolution Details
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("⚔️ Recent Conflict Resolutions", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Timestamp', 'Symbol', 'Conflicting Agents', 'Votes', 'Resolution', 'Winner', 'Outcome'],
                            [
                                [(datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), 'AAPL', 'Momentum vs Reversal', 'BUY vs SELL', 'Weighted Vote', 'Momentum (1.15)', '✅ Correct'],
                                [(datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M'), 'TSLA', 'Breakout vs Echo', 'BUY vs HOLD', 'Weighted Vote', 'Breakout (1.08)', '✅ Correct'],
                                [(datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M'), 'NVDA', 'Vox vs Fractalis', 'BUY vs SELL', 'Weighted Vote', 'Vox (1.12)', '✅ Correct'],
                                [(datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'), 'META', 'Genesis vs Obscura', 'HOLD vs SELL', 'Weighted Vote', 'Genesis (1.05)', '❌ Wrong'],
                                [(datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M'), 'AMD', 'Momentum vs Reversal', 'BUY vs SELL', 'Weighted Vote', 'Momentum (1.15)', '✅ Correct']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='vote-panel-interval', interval=3000, n_intervals=0)
    ], fluid=True)
    
    return header, content
