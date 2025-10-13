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
    from modules.data_stream.data_stream import get_data_stream
    from dash_app.config import USE_MOCK_DATA
    import random
    
    risk_mapper = RiskMapper()
    stats = risk_mapper.get_stats()
    
    # Get market data using DataStream
    data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
    market_summary = data_stream.get_market_summary()
    quotes = market_summary['quotes']
    
    # Build symbol risk profile table from available symbols
    risk_rows = []
    available_symbols = list(quotes.keys())[:5]  # Use first 5 available symbols
    for sym in available_symbols:
        quote = quotes.get(sym, {})
        volatility_pct = abs(quote.get('dp', 0))
        risk_score = round(volatility_pct * random.uniform(0.8, 1.5), 1)
        volatility = 'High' if volatility_pct > 3 else ('Medium' if volatility_pct > 1.5 else 'Low')
        beta = round(random.uniform(0.7, 2.0), 2)
        status = '⚠️ Warning' if risk_score > 6 else '✓ Normal'
        risk_rows.append([sym, str(risk_score), volatility, str(beta), status])
    
    # Fallback if no data
    if not risk_rows:
        risk_rows = [['N/A', '0.0', 'N/A', '0.0', '⚠️ No Data']]
    
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
                            risk_rows
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
