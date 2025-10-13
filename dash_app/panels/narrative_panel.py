"""
Narrative Panel - Händelseflöde och systemberättelse
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

# Panel Metadata
PANEL_METADATA = {
    "data_source": "live",
    "live_ready": True,
    "verified": True,
    "phase": "Phase 3 - Live Data Integration Complete"
}

def create_panel():
    """
    Skapar Narrative Engine panelen.
    """
    from modules.narrative_engine import NarrativeEngine
    from datetime import datetime
    
    narrative = NarrativeEngine()
    stats = narrative.get_stats()
    recent_events = narrative.get_recent_events(limit=10)
    event_groups = narrative.get_event_groups()
    
    header = create_header(
        "Narrative Engine",
        "Händelseflöde, causal chains och systemberättelse",
        "fas fa-book"
    )
    
    # Build event display items dynamically
    event_items = []
    for event in recent_events[:6]:  # Show top 6 events
        # Parse timestamp and format it
        try:
            timestamp = datetime.fromisoformat(event['timestamp'])
            time_str = timestamp.strftime('%H:%M:%S')
        except:
            time_str = "00:00:00"
        
        icon = event.get('icon', '📋')
        description = event.get('description', 'Unknown event')
        
        event_items.append(
            html.Div([
                html.Span(time_str, style={'color': '#9ca3af', 'marginRight': '10px'}),
                html.Span(f"{icon} ", style={'fontSize': '16px'}),
                html.Span(description, className="mb-2")
            ], className="mb-3", style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'})
        )
    
    # Build event statistics dynamically
    total_events = stats.get('total_events', 0)
    event_stat_items = []
    for event_type, count in event_groups.items():
        percentage = (count / total_events * 100) if total_events > 0 else 0
        icon_map = {
            'consensus': '📊',
            'agent_signal': '🤖',
            'position_sizing': '💼',
            'data_update': '🔄',
            'trend_analysis': '📈',
            'signal_validation': '⚡'
        }
        icon = icon_map.get(event_type, '📋')
        event_stat_items.append(
            html.P(f"{icon} {event_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)", className="mb-2")
        )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Events",
                    stats.get('total_events', 0),
                    icon="fas fa-list"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Causal Chains",
                    stats.get('causal_chains', 0),
                    icon="fas fa-link"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Event Groups",
                    stats.get('event_groups', 0),
                    icon="fas fa-object-group"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Active Stories",
                    stats.get('active_stories', 0),
                    icon="fas fa-book-open"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Narrative", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div(event_items if event_items else [
                            html.P("No events yet. System is initializing...", style={'color': '#9ca3af'})
                        ])
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Causal Chains", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.H6("System Flow Example", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                            html.P("1. Market data update → ", className="mb-1"),
                            html.P("2. Trend analysis → ", className="mb-1"),
                            html.P("3. Agent consensus → ", className="mb-1"),
                            html.P("4. Signal validation → ", className="mb-1"),
                            html.P("5. Position sizing → ", className="mb-1"),
                            html.P("6. Portfolio allocation", className="mb-3", style={'fontWeight': 'bold'}),
                            
                            html.Hr(),
                            html.P(f"Active causal chains tracked: {stats.get('causal_chains', 0)}", 
                                   style={'fontStyle': 'italic', 'color': '#9ca3af'})
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Event Statistics", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div(event_stat_items if event_stat_items else [
                            html.P("No event statistics available yet.", style={'color': '#9ca3af'})
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='narrative-panel-interval', interval=2000, n_intervals=0)
    ], fluid=True)
    
    return header, content
