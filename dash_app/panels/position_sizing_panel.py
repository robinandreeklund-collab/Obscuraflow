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
    
    sizing = Sizing(base_capital=100000, max_position_pct=20.0)
    stats = sizing.get_statistics()
    
    header = create_header(
        "Position Sizing",
        "Kelly criterion, volatility-adjusted sizing och RL-optimering",
        "fas fa-chart-line"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Base Capital",
                    f"${stats.get('base_capital', 100000):,.0f}",
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
                    "Max Position %",
                    f"{stats.get('max_position_pct', 20.0):.1f}%",
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
                            [
                                ['AAPL', '250 shares', '12.5%', 'Medium', '$45,000'],
                                ['GOOGL', '180 shares', '10.2%', 'Low', '$38,000'],
                                ['TSLA', '120 shares', '15.8%', 'High', '$28,000'],
                                ['MSFT', '200 shares', '11.0%', 'Low', '$42,000'],
                                ['NVDA', '150 shares', '13.2%', 'High', '$35,000']
                            ]
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
