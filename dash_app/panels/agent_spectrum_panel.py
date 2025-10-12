"""
Agent Spectrum Panel - Ontologisk agent positioning
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_scatter_plot
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Agent Spectrum panelen.
    """
    from modules.agent_spectrum import AgentSpectrum
    
    spectrum = AgentSpectrum()
    stats = spectrum.get_stats()
    
    header = create_header(
        "Agent Spectrum",
        "Ontologisk positioning, clustering och mobility tracking",
        "fas fa-network-wired"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Agents",
                    stats.get('total_agents', 0),
                    icon="fas fa-users"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Clusters",
                    stats.get('total_clusters', 0),
                    icon="fas fa-object-group"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Avg Mobility",
                    f"{stats.get('average_mobility', 0):.2f}",
                    icon="fas fa-running"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Dimensions",
                    "3D",
                    icon="fas fa-cube"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Agent Positions", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['Agent', 'Temporal', 'Structural', 'Social', 'Cluster'],
                            [
                                ['Echo', 'High', 'Medium', 'Low', 'A'],
                                ['Fractalis', 'Medium', 'High', 'Medium', 'B'],
                                ['Vox', 'Low', 'Medium', 'High', 'C'],
                                ['Myco', 'Medium', 'Low', 'High', 'C'],
                                ['Obscura', 'High', 'Low', 'Low', 'A'],
                                ['Genesis', 'High', 'High', 'Medium', 'B']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Cluster Analysis", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🔵 Cluster A (Temporal Focus): 4 agents", className="mb-2"),
                            html.P("🟢 Cluster B (Structural Focus): 5 agents", className="mb-2"),
                            html.P("🟡 Cluster C (Social Focus): 3 agents", className="mb-2"),
                            html.P("🔴 Cluster D (Hybrid): 4 agents", className="mb-2"),
                            html.Hr(),
                            html.P("Most mobile: EchoAgent (0.85)", className="mb-2"),
                            html.P("Most stable: ArchitectumAgent (0.12)", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Dimensional Characteristics", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.H6("Temporal Dimension", style={'color': '#00d9ff'}),
                            html.P("High: Echo, Genesis, Obscura", className="mb-3"),
                            html.H6("Structural Dimension", style={'color': '#00d9ff'}),
                            html.P("High: Fractalis, Genesis, Architectum", className="mb-3"),
                            html.H6("Social Dimension", style={'color': '#00d9ff'}),
                            html.P("High: Vox, Myco, Symbio", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='spectrum-panel-interval', interval=5000, n_intervals=0)
    ], fluid=True)
    
    return header, content
