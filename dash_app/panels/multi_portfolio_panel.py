"""
Multi Portfolio Panel - Parallella portföljer med olika strategier
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_line_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Multi Portfolio panelen.
    """
    from modules.portfolio_engine import PortfolioEngine
    
    portfolio = PortfolioEngine()
    stats = portfolio.get_stats()
    
    header = create_header(
        "Multi Portfolio",
        "Parallella portföljer, mutation och performance tracking",
        "fas fa-briefcase"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Active Portfolios",
                    stats.get('active_portfolios', 0),
                    icon="fas fa-folder-open"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Total Value",
                    f"${stats.get('total_value', 0):,.0f}",
                    change=12.5,
                    icon="fas fa-dollar-sign"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Best Performer",
                    "+18.2%",
                    icon="fas fa-trophy"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Avg Return",
                    f"{stats.get('average_return', 0):.2f}%",
                    icon="fas fa-chart-line"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Portfolio Overview", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Portfolio', 'Value', 'Return', 'Sharpe', 'Status'],
                            [
                                ['Aggressive', '$125,000', '+18.2%', '1.45', '✓ Active'],
                                ['Balanced', '$110,000', '+12.5%', '1.68', '✓ Active'],
                                ['Conservative', '$95,000', '+8.3%', '1.82', '✓ Active'],
                                ['Experimental', '$78,000', '+5.1%', '0.95', '🔬 Testing'],
                                ['Hybrid-A', '$102,000', '+14.7%', '1.52', '✓ Active']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Asset Allocation", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("📊 Tech Stocks: 45%", className="mb-2"),
                            html.P("💰 Finance: 20%", className="mb-2"),
                            html.P("🏭 Industrial: 15%", className="mb-2"),
                            html.P("🛡️ Defensive: 12%", className="mb-2"),
                            html.P("💵 Cash: 8%", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dcc.Interval(id='portfolio-panel-interval', interval=4000, n_intervals=0)
    ], fluid=True)
    
    return header, content
