"""
Risk Ecosystem Panel - Risk per symbol, agent och portfölj
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_bar_chart
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Risk Ecosystem panelen.
    """
    from modules.risk_mapper import RiskMapper
    
    risk_mapper = RiskMapper()
    stats = risk_mapper.get_stats()
    
    header = create_header(
        "Risk Ecosystem",
        "Riskmatris, symbol risk och portfolio risk mapping",
        "fas fa-shield-alt"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Risk Score",
                    f"{stats.get('total_risk_score', 0):.2f}",
                    icon="fas fa-exclamation-triangle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "High Risk Symbols",
                    stats.get('high_risk_count', 0),
                    icon="fas fa-times-circle"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Risk Concentration",
                    f"{stats.get('risk_concentration', 0):.1f}%",
                    icon="fas fa-compress"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "VaR (95%)",
                    f"${stats.get('value_at_risk', 0):,.0f}",
                    icon="fas fa-dollar-sign"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Symbol Risk Profile", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Symbol', 'Risk Score', 'Volatility', 'Beta', 'Status'],
                            [
                                ['TSLA', '8.5', 'High', '1.85', '⚠️ Warning'],
                                ['NVDA', '7.2', 'High', '1.65', '⚠️ Warning'],
                                ['AAPL', '4.3', 'Medium', '1.15', '✓ Normal'],
                                ['GOOGL', '3.8', 'Low', '0.95', '✓ Normal'],
                                ['MSFT', '3.2', 'Low', '0.85', '✓ Normal']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Risk Distribution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_bar_chart(
                            ['Market', 'Credit', 'Liquidity', 'Operational', 'Systemic'],
                            [6.8, 3.2, 2.5, 1.8, 4.5],
                            "Risk by Category",
                            "Risk Type",
                            "Score",
                            '#ef4444'
                        )
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Risk Mitigation Strategies", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🛡️ Diversification: Active (12 symbols)", className="mb-2"),
                            html.P("⚖️ Position Limits: Enforced (max 15%)", className="mb-2"),
                            html.P("🔄 Stop Losses: Implemented (5% max loss)", className="mb-2"),
                            html.P("📊 Hedging: Partial (Beta neutral 60%)", className="mb-2"),
                            html.P("💰 Cash Reserve: 15% (Ready)", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='risk-panel-interval', interval=3000, n_intervals=0)
    ], fluid=True)
    
    return header, content
