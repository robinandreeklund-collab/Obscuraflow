"""
Vote Panel - Visar röstningsresultat och viktning med detaljerad historik
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import plotly.graph_objs as go
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Panel Metadata
PANEL_METADATA = {
    "data_source": "live",
    "live_ready": True,
    "verified": True,
    "phase": "Phase 3 - Live Data Integration Complete"
}

def create_panel():
    """
    Skapar Enhanced Vote Engine panelen med detaljerad historik från live data.
    """
    from modules.vote_engine import VoteEngine
    from dash_app.config import USE_MOCK_DATA
    from modules.data_stream.data_stream import get_data_stream
    from modules.decision_core import DecisionCore
    
    vote_engine = VoteEngine(weight_decay=0.95, learning_rate=0.1)
    stats = vote_engine.get_stats()
    
    # Get market data using DataStream
    data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
    market_summary = data_stream.get_market_summary()
    quotes = market_summary['quotes']
    available_symbols = list(quotes.keys())
    
    data_mode = "Live API" if not USE_MOCK_DATA else "Mock Data"
    
    # Get actual agent decisions from DecisionCore
    decision_core = DecisionCore(use_live_data=True, generate_sample_decisions=False)
    agent_activity = decision_core.get_agent_activity()
    
    # Build recent votes table from actual agent decisions
    recent_votes_rows = []
    for decision in agent_activity[:15]:  # Last 15 decisions
        timestamp = decision.get('timestamp', datetime.now().strftime('%H:%M:%S'))
        symbol = decision.get('symbol', 'N/A')
        agent = decision.get('agent_id', 'N/A')
        action = decision.get('action', 'HOLD')
        vote_display = f"🟢 {action}" if action == 'BUY' else f"🔴 {action}" if action == 'SELL' else f"⚪ {action}"
        weight = f"{decision.get('weight', 1.0):.2f}"
        confidence = f"{int(decision.get('confidence', 0) * 100)}%"
        # Outcome based on actual decision data if available
        outcome = decision.get('outcome', '⏳ Pending')
        pnl_val = decision.get('pnl', 0)
        pnl = f"+${pnl_val:.2f}" if pnl_val > 0 else f"-${abs(pnl_val):.2f}" if pnl_val < 0 else '$0.00'
        recent_votes_rows.append([timestamp, symbol, agent, vote_display, weight, confidence, outcome, pnl])
    
    # Fallback if no decisions available
    if not recent_votes_rows:
        recent_votes_rows = [[datetime.now().strftime('%H:%M:%S'), 'N/A', 'N/A', '⚪ HOLD', '1.0', '0%', '⏳ Pending', '$0.00']]
    
    # Build conflict resolution table from actual conflicts (if tracked)
    conflict_rows = []
    # For now, conflicts would need to be tracked in VoteEngine or DecisionCore
    # Placeholder until conflict tracking is implemented
    if hasattr(vote_engine, 'get_conflicts'):
        conflicts = vote_engine.get_conflicts()
        for conflict in conflicts[:5]:
            timestamp = conflict.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M'))
            symbol = conflict.get('symbol', 'N/A')
            conflicting = conflict.get('agents', 'N/A')
            votes = conflict.get('votes', 'N/A')
            resolution = conflict.get('resolution', 'Weighted Vote')
            winner = conflict.get('winner', 'N/A')
            outcome = conflict.get('outcome', '⏳ Pending')
            conflict_rows.append([timestamp, symbol, conflicting, votes, resolution, winner, outcome])
    
    # Fallback if no conflict data
    if not conflict_rows:
        conflict_rows = [[datetime.now().strftime('%Y-%m-%d %H:%M'), 'No conflicts', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']]
    
    header = create_header(
        "Vote Engine - Enhanced",
        f"Viktad röstning, konfliktlösning och agent performance tracking | Mode: {data_mode}",
        "fas fa-vote-yea"
    )
    
    # Generate weight evolution chart from actual agent history
    timestamps = [(datetime.now() - timedelta(hours=24-i)).strftime('%H:00') for i in range(24)]
    
    # Get agent weights from historical decisions (last 24 hours)
    agent_weight_history = {}
    for decision in agent_activity:
        agent_id = decision.get('agent_id', 'unknown')
        if agent_id not in agent_weight_history:
            agent_weight_history[agent_id] = []
        agent_weight_history[agent_id].append(decision.get('weight', 1.0))
    
    # Create weight evolution lines for top agents
    weight_evolution = go.Figure()
    colors = {'momentum_agent': '#00d9ff', 'reversal_agent': '#7c3aed', 'breakout_agent': '#10b981',
              'echo_agent': '#f59e0b', 'vox_agent': '#ef4444', 'fractalis_agent': '#8b5cf6'}
    
    for agent_id, weights in list(agent_weight_history.items())[:6]:  # Top 6 agents
        # Pad or interpolate to 24 points
        if len(weights) > 24:
            weights = weights[:24]
        elif len(weights) < 24:
            weights = weights + [weights[-1] if weights else 1.0] * (24 - len(weights))
        
        agent_name = agent_id.replace('_agent', '').capitalize()
        weight_evolution.add_trace(go.Scatter(
            x=timestamps, y=weights, mode='lines+markers',
            name=agent_name, line=dict(color=colors.get(agent_id, '#9ca3af'), width=2)
        ))
    
    weight_evolution.update_layout(
        title="Agent Weight Evolution (Last 24h) - Live Data",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        xaxis=dict(showgrid=True, gridcolor='#374151'),
        yaxis=dict(showgrid=True, gridcolor='#374151', title='Weight'),
        height=350,
        hovermode='x unified'
    )
    
    # Voting accuracy chart from actual agent performance
    agent_accuracies = {}
    for decision in agent_activity:
        agent_id = decision.get('agent_id', 'unknown')
        outcome = decision.get('outcome', '')
        if agent_id not in agent_accuracies:
            agent_accuracies[agent_id] = {'correct': 0, 'total': 0}
        agent_accuracies[agent_id]['total'] += 1
        if outcome == '✅ Correct':
            agent_accuracies[agent_id]['correct'] += 1
    
    # Calculate accuracy percentages
    agent_names = []
    accuracies = []
    for agent_id, counts in agent_accuracies.items():
        agent_names.append(agent_id.replace('_agent', '').capitalize())
        accuracy = (counts['correct'] / counts['total'] * 100) if counts['total'] > 0 else 0
        accuracies.append(accuracy)
    
    # Fallback if no accuracy data
    if not agent_names:
        agent_names = ['No Data']
        accuracies = [0]
    
    accuracy_chart = go.Figure()
    accuracy_chart.add_trace(go.Bar(
        x=agent_names, y=accuracies,
        marker_color=['#10b981' if a > 70 else '#f59e0b' if a > 60 else '#ef4444' for a in accuracies],
        text=[f"{a:.1f}%" for a in accuracies],
        textposition='outside'
    ))
    accuracy_chart.update_layout(
        title="Agent Voting Accuracy - Live Data",
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
                    len(agent_activity),
                    change=0,
                    icon="fas fa-check-circle"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Avg Weight",
                    f"{stats.get('average_weight', 1.0):.2f}",
                    change=0,
                    icon="fas fa-balance-scale"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Conflicts Resolved",
                    len(conflict_rows) if conflict_rows[0][1] != 'No conflicts' else 0,
                    change=0,
                    icon="fas fa-handshake"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Success Rate",
                    f"{sum(accuracies) / len(accuracies) if accuracies and accuracies[0] > 0 else 0:.1f}%",
                    change=0,
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
                            agent_names[:8] if len(agent_names) > 1 else ['No Data'],
                            [agent_weight_history.get(agent_id, [1.0])[-1] if agent_id in agent_weight_history else 1.0 
                             for agent_id in list(agent_weight_history.keys())[:8]] if agent_weight_history else [0],
                            "Current Agent Weights - Live Data",
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
                            recent_votes_rows
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Agent Performance Summary
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🏆 Agent Performance Summary - Live Data", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Agent', 'Total Votes', 'Correct', 'Wrong', 'Accuracy', 'Avg Weight', 'Total P&L', 'Avg P&L/Trade'],
                            [
                                [
                                    agent_id.replace('_agent', '').capitalize(),
                                    str(counts['total']),
                                    str(counts['correct']),
                                    str(counts['total'] - counts['correct']),
                                    f"{(counts['correct'] / counts['total'] * 100) if counts['total'] > 0 else 0:.1f}%",
                                    f"{sum(agent_weight_history.get(agent_id, [1.0])) / len(agent_weight_history.get(agent_id, [1.0])):.2f}",
                                    f"+${sum([d.get('pnl', 0) for d in agent_activity if d.get('agent_id') == agent_id]):.2f}",
                                    f"+${sum([d.get('pnl', 0) for d in agent_activity if d.get('agent_id') == agent_id]) / counts['total'] if counts['total'] > 0 else 0:.2f}"
                                ]
                                for agent_id, counts in list(agent_accuracies.items())[:8]
                            ] if agent_accuracies else [['No Data', '0', '0', '0', '0%', '1.00', '$0', '$0']]
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
                            conflict_rows
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='vote-panel-interval', interval=3000, n_intervals=0)
    ], fluid=True)
    
    return header, content
