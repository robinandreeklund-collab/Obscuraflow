"""
Page Router - Routes URL paths to appropriate panels
"""

from dash import html
from dash_app.layout.header import create_header
from dash_app.panels import (
    decision_core_panel,
    vote_panel,
    position_sizing_panel,
    timespan_intelligence_panel,
    multi_portfolio_panel,
    mutation_tracker_panel,
    agent_spectrum_panel,
    agent_lifecycle_panel,
    meta_governance_panel,
    portfolio_intelligence_panel,
    risk_ecosystem_panel,
    system_flow_panel,
    narrative_panel
)
import dash_bootstrap_components as dbc

def create_home_page():
    """
    Skapar startsidan för dashboarden.
    """
    header = create_header(
        "Obscuraflow Dashboard",
        "AI-drivet tradingekosystem med multi-agent intelligens",
        "fas fa-home"
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔁 Core Modules", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.P("Decision Core - Agentbeslut och konsensusanalys"),
                        html.P("Vote Engine - Viktad röstning och konfliktlösning"),
                        html.P("Position Sizing - Kelly criterion och RL-optimerad sizing"),
                        html.P("Timespan Intelligence - Multi-timeframe synchronization")
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🤖 Agent Systems", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.P("Agent Spectrum - Ontologisk positioning"),
                        html.P("Agent Lifecycle - Birth, evolution, retirement"),
                        html.P("Meta Governance - Överordnad agentstyrning"),
                        html.P("Synergy Matrix - Agent-samverkan")
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("💼 Portfolio & Risk", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.P("Multi Portfolio - Parallella portföljer"),
                        html.P("Portfolio Intelligence - Jämförelse och benchmarking"),
                        html.P("Risk Ecosystem - Risk per symbol och agent")
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔬 Analysis & Evolution", style={'backgroundColor': '#151932', 'color': '#00d9ff'}),
                    dbc.CardBody([
                        html.P("Mutation Tracker - Genealogisk analys"),
                        html.P("System Flow - Visuell systemkarta"),
                        html.P("Narrative Engine - Händelseflöde och berättelse")
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4("System Status", className="alert-heading"),
                    html.P("Alla moduler är aktiva och kopplade till live mockdata."),
                    html.Hr(),
                    html.P("Auto-uppdatering var 2-5 sekunder beroende på panel.", className="mb-0")
                ], color="success")
            ])
        ])
    ], fluid=True)
    
    return header, content


def route_page(pathname):
    """
    Router som bestämmer vilket innehåll som ska visas baserat på URL.
    
    Args:
        pathname: URL-sökväg
        
    Returns:
        Tuple: (header, content) för sidan
    """
    if pathname == '/decision-core':
        return decision_core_panel.create_panel()
    elif pathname == '/vote-panel':
        return vote_panel.create_panel()
    elif pathname == '/position-sizing':
        return position_sizing_panel.create_panel()
    elif pathname == '/timespan-intelligence':
        return timespan_intelligence_panel.create_panel()
    elif pathname == '/multi-portfolio':
        return multi_portfolio_panel.create_panel()
    elif pathname == '/mutation-tracker':
        return mutation_tracker_panel.create_panel()
    elif pathname == '/agent-spectrum':
        return agent_spectrum_panel.create_panel()
    elif pathname == '/agent-lifecycle':
        return agent_lifecycle_panel.create_panel()
    elif pathname == '/meta-governance':
        return meta_governance_panel.create_panel()
    elif pathname == '/portfolio-intelligence':
        return portfolio_intelligence_panel.create_panel()
    elif pathname == '/risk-ecosystem':
        return risk_ecosystem_panel.create_panel()
    elif pathname == '/system-flow':
        return system_flow_panel.create_panel()
    elif pathname == '/narrative':
        return narrative_panel.create_panel()
    else:
        # Default: Home page
        return create_home_page()
