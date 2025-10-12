"""
Portfolio Development Panel - Detailed portfolio tracking with history, trades, and performance
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table
import plotly.graph_objs as go
from datetime import datetime, timedelta
import random
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')


def create_panel():
    """
    Skapar Portfolio Development panelen med detaljerad historik och trades.
    """
    from modules.portfolio_engine import PortfolioEngine
    
    # Initialize portfolio engine
    portfolio_engine = PortfolioEngine(initial_capital=100000.0)
    
    # Create sample portfolios
    portfolio_engine.create_portfolio('aggressive', 'aggressive')
    portfolio_engine.create_portfolio('balanced', 'balanced')
    portfolio_engine.create_portfolio('conservative', 'conservative')
    
    header = create_header(
        "Portfolio Development",
        "Detaljerad portfolioutveckling med historik, trades och performance-analys",
        "fas fa-chart-area"
    )
    
    # Generate historical performance data (30 days)
    days = 30
    base_value = 100000
    dates = [(datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d') for i in range(days)]
    
    # Aggressive portfolio (higher volatility)
    aggressive_values = [base_value]
    for i in range(1, days):
        change = random.uniform(-0.03, 0.04)
        aggressive_values.append(aggressive_values[-1] * (1 + change))
    
    # Balanced portfolio (moderate volatility)
    balanced_values = [base_value]
    for i in range(1, days):
        change = random.uniform(-0.02, 0.025)
        balanced_values.append(balanced_values[-1] * (1 + change))
    
    # Conservative portfolio (low volatility)
    conservative_values = [base_value]
    for i in range(1, days):
        change = random.uniform(-0.01, 0.015)
        conservative_values.append(conservative_values[-1] * (1 + change))
    
    # Create portfolio performance chart
    perf_chart = go.Figure()
    
    perf_chart.add_trace(go.Scatter(
        x=dates,
        y=aggressive_values,
        mode='lines',
        name='Aggressive',
        line=dict(color='#ef4444', width=2)
    ))
    
    perf_chart.add_trace(go.Scatter(
        x=dates,
        y=balanced_values,
        mode='lines',
        name='Balanced',
        line=dict(color='#00d9ff', width=2)
    ))
    
    perf_chart.add_trace(go.Scatter(
        x=dates,
        y=conservative_values,
        mode='lines',
        name='Conservative',
        line=dict(color='#10b981', width=2)
    ))
    
    perf_chart.update_layout(
        title="Portfolio Value Development (30 Days)",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        xaxis=dict(showgrid=True, gridcolor='#374151'),
        yaxis=dict(showgrid=True, gridcolor='#374151', title='Value ($)'),
        hovermode='x unified',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Calculate returns
    agg_return = ((aggressive_values[-1] - aggressive_values[0]) / aggressive_values[0]) * 100
    bal_return = ((balanced_values[-1] - balanced_values[0]) / balanced_values[0]) * 100
    con_return = ((conservative_values[-1] - conservative_values[0]) / conservative_values[0]) * 100
    
    # Create daily returns distribution
    daily_returns = [(aggressive_values[i] / aggressive_values[i-1] - 1) * 100 for i in range(1, len(aggressive_values))]
    
    returns_chart = go.Figure()
    returns_chart.add_trace(go.Histogram(
        x=daily_returns,
        nbinsx=15,
        marker_color='#7c3aed',
        opacity=0.75
    ))
    returns_chart.update_layout(
        title="Daily Returns Distribution (Aggressive)",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        xaxis=dict(title='Daily Return (%)', showgrid=True, gridcolor='#374151'),
        yaxis=dict(title='Frequency', showgrid=True, gridcolor='#374151'),
        height=300
    )
    
    # Asset allocation pie chart
    allocation_chart = go.Figure()
    allocation_chart.add_trace(go.Pie(
        labels=['Tech', 'Finance', 'Industrial', 'Healthcare', 'Cash'],
        values=[45, 20, 15, 12, 8],
        marker=dict(colors=['#00d9ff', '#7c3aed', '#f59e0b', '#10b981', '#9ca3af']),
        hole=0.4
    ))
    allocation_chart.update_layout(
        title="Asset Allocation (Balanced Portfolio)",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        height=300,
        showlegend=True
    )
    
    content = dbc.Container([
        # Top Metrics Row
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Portfolio Value",
                    f"${aggressive_values[-1]:,.0f}",
                    change=agg_return,
                    icon="fas fa-wallet"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "30-Day Return",
                    f"+{agg_return:.2f}%",
                    change=agg_return,
                    icon="fas fa-trending-up"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Win Rate",
                    "68.5%",
                    change=3.2,
                    icon="fas fa-trophy"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Sharpe Ratio",
                    "1.85",
                    change=0.15,
                    icon="fas fa-chart-line"
                )
            ], width=12, lg=3, md=6)
        ], className="mb-4"),
        
        # Portfolio Performance Chart
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Portfolio Performance", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        dcc.Graph(figure=perf_chart, config={'displayModeBar': True})
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Portfolio Comparison
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Portfolio Comparison", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Portfolio', 'Strategy', 'Current Value', '30D Return', 'Sharpe', 'Max Drawdown', 'Status'],
                            [
                                ['Aggressive', 'Growth-focused', f'${aggressive_values[-1]:,.0f}', f'+{agg_return:.2f}%', '1.45', '-8.5%', '✅ Active'],
                                ['Balanced', 'Mixed approach', f'${balanced_values[-1]:,.0f}', f'+{bal_return:.2f}%', '1.85', '-5.2%', '✅ Active'],
                                ['Conservative', 'Capital preservation', f'${conservative_values[-1]:,.0f}', f'+{con_return:.2f}%', '2.12', '-2.8%', '✅ Active'],
                                ['Experimental', 'RL-optimized', '$98,450', '-1.55%', '0.85', '-12.3%', '🔬 Testing']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Returns Distribution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        dcc.Graph(figure=returns_chart, config={'displayModeBar': False})
                    ])
                ], className="mb-3")
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Asset Allocation", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        dcc.Graph(figure=allocation_chart, config={'displayModeBar': False})
                    ])
                ], className="mb-3")
            ], width=12, lg=6)
        ]),
        
        # Recent Trades
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("💼 Recent Trades (Last 10)", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Timestamp', 'Portfolio', 'Type', 'Symbol', 'Quantity', 'Price', 'Value', 'P&L'],
                            [
                                [datetime.now().strftime('%Y-%m-%d %H:%M'), 'Aggressive', '🟢 BUY', 'NVDA', '50', '$485.20', '$24,260', '-'],
                                [(datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'), 'Balanced', '🔴 SELL', 'AAPL', '100', '$182.50', '$18,250', '+$1,250'],
                                [(datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M'), 'Aggressive', '🟢 BUY', 'TSLA', '30', '$248.75', '$7,463', '-'],
                                [(datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'), 'Conservative', '🟢 BUY', 'JPM', '75', '$151.30', '$11,348', '-'],
                                [(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M'), 'Balanced', '🔴 SELL', 'GOOGL', '50', '$142.80', '$7,140', '+$890'],
                                [(datetime.now() - timedelta(days=1, hours=3)).strftime('%Y-%m-%d %H:%M'), 'Aggressive', '🟢 BUY', 'AMD', '150', '$128.45', '$19,268', '-'],
                                [(datetime.now() - timedelta(days=1, hours=6)).strftime('%Y-%m-%d %H:%M'), 'Conservative', '🔴 SELL', 'BA', '40', '$225.60', '$9,024', '+$680'],
                                [(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M'), 'Balanced', '🟢 BUY', 'MSFT', '60', '$378.90', '$22,734', '-'],
                                [(datetime.now() - timedelta(days=2, hours=4)).strftime('%Y-%m-%d %H:%M'), 'Aggressive', '🔴 SELL', 'META', '35', '$325.40', '$11,389', '+$1,540'],
                                [(datetime.now() - timedelta(days=2, hours=7)).strftime('%Y-%m-%d %H:%M'), 'Conservative', '🟢 BUY', 'V', '45', '$265.75', '$11,959', '-']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Current Positions
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📦 Current Positions (Aggressive Portfolio)", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Symbol', 'Quantity', 'Entry Price', 'Current Price', 'Market Value', 'P&L', 'P&L %', 'Weight'],
                            [
                                ['NVDA', '50', '$485.20', '$492.35', '$24,618', '+$358', '+1.5%', '24.6%'],
                                ['TSLA', '30', '$248.75', '$255.80', '$7,674', '+$212', '+2.8%', '7.7%'],
                                ['AMD', '150', '$128.45', '$131.20', '$19,680', '+$413', '+2.1%', '19.7%'],
                                ['AAPL', '85', '$178.30', '$181.25', '$15,406', '+$251', '+1.7%', '15.4%'],
                                ['GOOGL', '60', '$138.90', '$141.50', '$8,490', '+$156', '+1.9%', '8.5%'],
                                ['MSFT', '45', '$375.20', '$382.10', '$17,195', '+$311', '+1.8%', '17.2%'],
                                ['META', '20', '$315.60', '$322.40', '$6,448', '+$136', '+2.2%', '6.4%']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Performance Metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Performance Metrics (30 Days)", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H6("Risk Metrics", style={'color': '#00d9ff'}),
                                    html.P("Volatility: 18.5%", className="mb-2"),
                                    html.P("Max Drawdown: -8.5%", className="mb-2"),
                                    html.P("Beta: 1.15", className="mb-2"),
                                    html.P("VaR (95%): -$4,250", className="mb-2")
                                ])
                            ], width=12, lg=3, md=6),
                            dbc.Col([
                                html.Div([
                                    html.H6("Return Metrics", style={'color': '#00d9ff'}),
                                    html.P(f"Total Return: +{agg_return:.2f}%", className="mb-2"),
                                    html.P("Annualized: +38.5%", className="mb-2"),
                                    html.P("Win Rate: 68.5%", className="mb-2"),
                                    html.P("Profit Factor: 2.15", className="mb-2")
                                ])
                            ], width=12, lg=3, md=6),
                            dbc.Col([
                                html.Div([
                                    html.H6("Trade Statistics", style={'color': '#00d9ff'}),
                                    html.P("Total Trades: 47", className="mb-2"),
                                    html.P("Winning Trades: 32", className="mb-2"),
                                    html.P("Losing Trades: 15", className="mb-2"),
                                    html.P("Avg Trade: +$285", className="mb-2")
                                ])
                            ], width=12, lg=3, md=6),
                            dbc.Col([
                                html.Div([
                                    html.H6("Efficiency Metrics", style={'color': '#00d9ff'}),
                                    html.P("Sharpe Ratio: 1.85", className="mb-2"),
                                    html.P("Sortino Ratio: 2.45", className="mb-2"),
                                    html.P("Calmar Ratio: 4.53", className="mb-2"),
                                    html.P("Information Ratio: 0.82", className="mb-2")
                                ])
                            ], width=12, lg=3, md=6)
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Auto-refresh interval
        dcc.Interval(
            id='portfolio-dev-panel-interval',
            interval=5000,  # 5 seconds
            n_intervals=0
        )
    ], fluid=True)
    
    return header, content
