"""
Mutation Tracker Panel - Genealogisk analys av strategimutationer
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_app.layout.header import create_header
from dash_app.components.ui_components import create_metric_card, create_data_table, create_scatter_plot
import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def create_panel():
    """
    Skapar Mutation Tracker panelen.
    """
    from modules.mutation_tracker import MutationTracker
    
    tracker = MutationTracker()
    stats = tracker.get_stats()
    
    header = create_header(
        "Mutation Tracker",
        "Genealogisk analys, lineage tracking och mutation history",
        "fas fa-dna"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Total Mutations",
                    stats.get('total_mutations', 0),
                    icon="fas fa-flask"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Active Lineages",
                    stats.get('active_lineages', 0),
                    icon="fas fa-sitemap"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Generations",
                    stats.get('max_generation', 0),
                    icon="fas fa-layer-group"
                )
            ], width=3),
            dbc.Col([
                create_metric_card(
                    "Success Rate",
                    f"{stats.get('success_rate', 0):.1f}%",
                    icon="fas fa-check-circle"
                )
            ], width=3)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Mutations", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        create_data_table(
                            ['ID', 'Parent', 'Type', 'Generation', 'Fitness'],
                            [
                                ['M-047', 'M-032', 'Parameter', '4', '0.85'],
                                ['M-048', 'M-035', 'Strategy', '5', '0.78'],
                                ['M-049', 'M-032', 'Hybrid', '4', '0.92'],
                                ['M-050', 'M-041', 'Parameter', '6', '0.68'],
                                ['M-051', 'M-047', 'Strategy', '5', '0.88']
                            ]
                        )
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Lineage Performance", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("🧬 Lineage Alpha: Gen 6, Fitness 0.92 (Best)", className="mb-2"),
                            html.P("🧬 Lineage Beta: Gen 5, Fitness 0.85", className="mb-2"),
                            html.P("🧬 Lineage Gamma: Gen 4, Fitness 0.78", className="mb-2"),
                            html.P("🧬 Lineage Delta: Gen 7, Fitness 0.88", className="mb-2"),
                            html.P("🧬 Lineage Epsilon: Gen 3, Fitness 0.72 (Retired)", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Mutation Types Distribution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.Div([
                            html.P("⚙️ Parameter Mutations: 45%", className="mb-2"),
                            html.P("🔄 Strategy Mutations: 30%", className="mb-2"),
                            html.P("🔗 Hybrid Mutations: 20%", className="mb-2"),
                            html.P("🆕 Novel Mutations: 5%", className="mb-2")
                        ])
                    ])
                ], className="mb-3")
            ], width=12)
        ]),
        
        dcc.Interval(id='mutation-panel-interval', interval=5000, n_intervals=0)
    ], fluid=True)
    
    return header, content
