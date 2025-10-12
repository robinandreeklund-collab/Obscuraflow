"""
Portfolio Intelligence Panel - Portföljjämförelse och benchmarking
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_line_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Portfolio Intelligence panelen.
    """
    from modules.portfolio_comparator import PortfolioComparator
    
    comparator = PortfolioComparator()
    stats = comparator.get_statistics()
    
    header = create_header(
        "Portfolio Intelligence",
        "Jämförelse, benchmarking och meta-portfolio optimization",
        "fas fa-chart-pie"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Portfolios Tracked",
                    stats.get('portfolios_tracked', 0),
                    icon="fas fa-folder-open"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Benchmarks",
                    stats.get('benchmarks', 3),
                    icon="fas fa-flag"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Best Alpha",
                    "+12.5%",
                    icon="fas fa-trophy"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Meta Portfolio",
                    "$485K",
                    change=8.5,
                    icon="fas fa-layer-group"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Performance Comparison", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Portfolio', 'Return', 'Alpha', 'Beta', 'Sharpe'],
                            [
                                ['Aggressive', '+18.2%', '+12.5%', '1.35', '1.45'],
                                ['Balanced', '+12.5%', '+6.8%', '0.95', '1.68'],
                                ['Conservative', '+8.3%', '+2.6%', '0.65', '1.82'],
                                ['S&P 500', '+5.7%', '0.0%', '1.0', '1.25'],
                                ['Meta Portfolio', '+14.8%', '+9.1%', '1.05', '1.72']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Risk Metrics", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("📊 Avg Volatility: 18.5%", className="mb-2"),
                            html.P("📉 Max Drawdown: -12.3%", className="mb-2"),
                            html.P("🎯 Win Rate: 68.5%", className="mb-2"),
                            html.P("💰 Profit Factor: 2.15", className="mb-2"),
                            html.Hr(),
                            html.P("Risk-Adjusted Return: 1.58", style={'fontWeight': 'bold', 'color': '#10b981'})
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Correlation Matrix", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("Aggressive ↔ Balanced: 0.75", className="mb-2"),
                            html.P("Aggressive ↔ Conservative: 0.45", className="mb-2"),
                            html.P("Balanced ↔ Conservative: 0.82", className="mb-2"),
                            html.P("Meta ↔ S&P 500: 0.68", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='portfolio-intel-panel-interval', interval=5000, n_intervals=0)
    ], fluid=True)
    
    return header, content
