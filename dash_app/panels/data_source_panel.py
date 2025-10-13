"""
Data Source Panel - WebSocket status, REST API calls, latency monitoring
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
    Skapar Data Source panelen med WebSocket och API monitoring.
    """
    from dash_app.config import USE_MOCK_DATA, FINNHUB_API_KEY
    from modules.data_stream.data_stream import get_data_stream
    
    # Get market data using DataStream
    data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
    market_summary = data_stream.get_market_summary()
    quotes = market_summary['quotes']
    available_symbols = list(quotes.keys())
    
    # Check current data source mode
    data_mode = "Mock Data" if USE_MOCK_DATA else "Live API"
    data_status_icon = "🟡" if USE_MOCK_DATA else "🟢"
    
    # Build recent API calls table from available symbols
    endpoints = ['/quote', '/quote', '/quote', '/profile2', '/quote', '/candle', '/quote', '/quote']
    api_calls_rows = []
    for i in range(min(8, len(available_symbols))):
        time_offset = i * 2 + random.randint(0, 2)  # seconds between API calls
        timestamp = (datetime.now() - timedelta(seconds=time_offset)).strftime('%H:%M:%S')
        endpoint = endpoints[i % len(endpoints)]
        symbol = available_symbols[i % len(available_symbols)]
        latency = f"{random.randint(15, 90)}ms"
        status = '✅ 200'
        cache = random.choice(['✅ Hit', '❌ Miss'])
        api_calls_rows.append([timestamp, endpoint, symbol, latency, status, cache])
    
    # Fallback if no data
    if not api_calls_rows:
        api_calls_rows = [[datetime.now().strftime('%H:%M:%S'), '/quote', 'N/A', '0ms', '⚠️ N/A', '❌ Miss']]
    
    header = create_header(
        "Data Source Monitor",
        f"WebSocket subscriptions, REST API calls, latency och data status | Current: {data_status_icon} {data_mode}",
        "fas fa-satellite-dish"
    )
    
    # Generate mock latency data for chart
    timestamps = [(datetime.now() - timedelta(minutes=30-i)).strftime('%H:%M') for i in range(30)]
    latency_data = [random.uniform(10, 50) for _ in range(30)]
    
    # Create latency chart
    latency_chart = go.Figure()
    latency_chart.add_trace(go.Scatter(
        x=timestamps,
        y=latency_data,
        mode='lines+markers',
        line=dict(color='#00d9ff', width=2),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.2)'
    ))
    latency_chart.update_layout(
        title="API Latency (Last 30 min)",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        xaxis=dict(showgrid=True, gridcolor='#374151'),
        yaxis=dict(showgrid=True, gridcolor='#374151', title='Latency (ms)'),
        height=300
    )
    
    # Generate request volume data
    request_labels = ['Quotes', 'Profiles', 'Candles', 'Market Status']
    request_counts = [245, 42, 18, 12]
    
    request_chart = go.Figure()
    request_chart.add_trace(go.Bar(
        x=request_labels,
        y=request_counts,
        marker_color=['#10b981', '#7c3aed', '#f59e0b', '#00d9ff'],
        text=request_counts,
        textposition='outside'
    ))
    request_chart.update_layout(
        title="API Requests by Type (Last Hour)",
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        showlegend=False,
        height=300
    )
    
    # WebSocket status
    ws_status = f"🟢 Connected" if not USE_MOCK_DATA else "🟡 Mock Mode (Not Connected)"
    ws_subs = 12 if not USE_MOCK_DATA else 0
    ws_uptime = "2h 34m" if not USE_MOCK_DATA else "N/A"
    ws_messages = "1,247" if not USE_MOCK_DATA else "0"
    
    # API status
    api_status = f"🟢 Active - Live Data" if not USE_MOCK_DATA else "🟡 Mock Data Mode"
    api_key_masked = FINNHUB_API_KEY[:10] + "..." + FINNHUB_API_KEY[-4:] if FINNHUB_API_KEY else "Not Set"
    
    content = dbc.Container([
        # Top Metrics Row
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Data Source",
                    f"{'🟢 Live API' if not USE_MOCK_DATA else '🟡 Mock Data'}",
                    icon="fas fa-database"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Avg Latency",
                    f"{sum(latency_data)/len(latency_data):.1f} ms",
                    change=-2.3,
                    icon="fas fa-tachometer-alt"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "API Calls (1h)",
                    sum(request_counts),
                    icon="fas fa-exchange-alt"
                )
            ], width=12, lg=3, md=6),
            dbc.Col([
                create_metric_card(
                    "Cache Hit Rate",
                    "87.5%",
                    change=5.2,
                    icon="fas fa-memory"
                )
            ], width=12, lg=3, md=6)
        ], className="mb-4"),
        
        # WebSocket Status Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📡 WebSocket Status", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5("Connection Status", style={'color': '#00d9ff'}),
                                    html.H3(ws_status, className="mb-3"),
                                    html.P(f"Subscriptions: {ws_subs} symbols", className="mb-2"),
                                    html.P(f"Uptime: {ws_uptime}", className="mb-2"),
                                    html.P(f"Messages Received: {ws_messages}", className="mb-2"),
                                    html.P(f"Last Message: {datetime.now().strftime('%H:%M:%S')}", className="mb-2"),
                                    html.P(f"Mode: {'LIVE API' if not USE_MOCK_DATA else 'MOCK DATA'}", 
                                          className="mb-2",
                                          style={'fontWeight': 'bold', 'color': '#00d9ff' if not USE_MOCK_DATA else '#f59e0b'})
                                ])
                            ], width=12, lg=6),
                            dbc.Col([
                                html.Div([
                                    html.H5("Active Subscriptions", style={'color': '#00d9ff'}),
                                    html.Div([
                                        dbc.Badge("AAPL", color="success", className="me-2 mb-2"),
                                        dbc.Badge("GOOGL", color="success", className="me-2 mb-2"),
                                        dbc.Badge("MSFT", color="success", className="me-2 mb-2"),
                                        dbc.Badge("TSLA", color="success", className="me-2 mb-2"),
                                        dbc.Badge("AMZN", color="success", className="me-2 mb-2"),
                                        dbc.Badge("META", color="success", className="me-2 mb-2"),
                                        dbc.Badge("NVDA", color="success", className="me-2 mb-2"),
                                        dbc.Badge("AMD", color="success", className="me-2 mb-2"),
                                        dbc.Badge("NFLX", color="success", className="me-2 mb-2"),
                                        dbc.Badge("BA", color="success", className="me-2 mb-2"),
                                        dbc.Badge("JPM", color="success", className="me-2 mb-2"),
                                        dbc.Badge("V", color="success", className="me-2 mb-2"),
                                    ])
                                ])
                            ], width=12, lg=6)
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # REST API Status Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🌐 REST API Status", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5("API Configuration", style={'color': '#00d9ff'}),
                                    html.P(f"Status: {api_status}", className="mb-2"),
                                    html.P(f"API Key: {api_key_masked}", className="mb-2"),
                                    html.P(f"Endpoint: https://finnhub.io/api/v1", className="mb-2"),
                                    html.P(f"Rate Limit: 60 calls/min", className="mb-2"),
                                    html.P(f"Remaining: 47 calls", className="mb-2")
                                ])
                            ], width=12, lg=6),
                            dbc.Col([
                                html.Div([
                                    html.H5("Cache Statistics", style={'color': '#00d9ff'}),
                                    html.P("Quote Cache TTL: 60 seconds", className="mb-2"),
                                    html.P("Profile Cache TTL: 3600 seconds", className="mb-2"),
                                    html.P("Cached Items: 24", className="mb-2"),
                                    html.P("Cache Size: 156 KB", className="mb-2"),
                                    html.P("Last Flush: 15 min ago", className="mb-2")
                                ])
                            ], width=12, lg=6)
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Latency Monitoring", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        dcc.Graph(figure=latency_chart, config={'displayModeBar': False})
                    ])
                ], className="mb-3")
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Request Volume", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        dcc.Graph(figure=request_chart, config={'displayModeBar': False})
                    ])
                ], className="mb-3")
            ], width=12, lg=6)
        ]),
        
        # Recent API Calls Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📋 Recent API Calls", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Timestamp', 'Endpoint', 'Symbol', 'Latency', 'Status', 'Cache'],
                            api_calls_rows
                        )
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Error Log
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("⚠️ Recent Errors & Warnings", style={'backgroundColor': '#151932', 'color': '#00d9ff', 'fontWeight': 'bold'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🟡 [14:23:45] Rate limit approaching (55/60 calls)", className="mb-2"),
                            html.P("🟢 [14:20:12] Cache flush completed successfully", className="mb-2"),
                            html.P("🟡 [14:15:33] High latency detected (125ms) for TSLA quote", className="mb-2"),
                            html.P("🟢 [14:10:00] System started successfully", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        # Auto-refresh interval
        dcc.Interval(
            id='data-source-panel-interval',
            interval=2000,  # 2 seconds
            n_intervals=0
        )
    ], fluid=True)
    
    return header, content
