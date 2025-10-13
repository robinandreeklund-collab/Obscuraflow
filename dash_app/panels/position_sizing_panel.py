"""
Position Sizing Panel - Kelly criterion och RL-optimerad sizing
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_line_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Position Sizing panelen.
    """
    from modules.sizing import Sizing
    from modules.data_stream.data_stream import get_data_stream
    from dash_app.config import USE_MOCK_DATA
    import random
    
    sizing = Sizing(max_position_size=0.2, risk_per_trade=0.02, use_kelly=True)
    stats = sizing.get_stats()
    
    # Get market data using DataStream
    data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
    market_summary = data_stream.get_market_summary()
    quotes = market_summary['quotes']
    
    # Build current positions table from available symbols
    positions_rows = []
    available_symbols = list(quotes.keys())[:5]  # Use first 5 available symbols
    for sym in available_symbols:
        quote = quotes.get(sym, {})
        price = quote.get('c', 100)
        shares = random.randint(100, 300)
        kelly_pct = f"{random.uniform(8, 16):.1f}%"
        volatility = random.choice(['Low', 'Medium', 'High'])
        allocation = f"${int(price * shares):,}"
        positions_rows.append([sym, f'{shares} shares', kelly_pct, volatility, allocation])
    
    # Fallback if no data
    if not positions_rows:
        positions_rows = [['N/A', '0 shares', '0%', 'N/A', '$0']]
    
    header = create_header(
        "Position Sizing",
        "Kelly criterion, volatility-adjusted sizing och RL-optimering",
        "fas fa-chart-line"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Capital",
                    "$100,000",
                    icon="fas fa-wallet"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Active Positions",
                    stats.get('active_positions', 0),
                    icon="fas fa-tasks"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Max Position Size",
                    f"{stats.get('max_position_size', 0.2)*100:.1f}%",
                    icon="fas fa-percentage"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Total Allocated",
                    f"${stats.get('total_allocated', 0):,.0f}",
                    icon="fas fa-dollar-sign"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Current Positions", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Symbol', 'Size', 'Kelly %', 'Volatility', 'Allocation'],
                            positions_rows
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Sizing Profile Performance", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("📊 Conservative Profile: +12.5% (Active)", className="mb-2"),
                            html.P("⚡ Aggressive Profile: +18.2% (Inactive)", className="mb-2"),
                            html.P("🎯 Balanced Profile: +15.8% (Active)", className="mb-2"),
                            html.P("🔬 Experimental Profile: +8.3% (Training)", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dcc.Interval(id='sizing-panel-interval', interval=4000, n_intervals=0)
    ], fluid=True)
    
    return header, content
