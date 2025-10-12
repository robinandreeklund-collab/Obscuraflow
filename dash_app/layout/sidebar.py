"""
Sidebar - Navigation menu för Obscuraflow Dashboard
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    """
    Skapar sidofältet med navigation till alla paneler.
    """
    return html.Div(
        [
            # Logo
            html.Div(
                "🌀 OBSCURAFLOW",
                className="sidebar-logo"
            ),
            
            html.Hr(style={'borderColor': '#374151'}),
            
            # Navigation
            html.Nav(
                dbc.Nav(
                    [
                        dbc.NavLink(
                            [html.I(className="fas fa-home me-2"), "Dashboard"],
                            href="/",
                            className="sidebar-nav-link",
                            active="exact"
                        ),
                        
                        html.Hr(style={'borderColor': '#374151', 'margin': '10px 0'}),
                        
                        html.Div("📊 CORE MODULES", style={'color': '#9ca3af', 'fontSize': '12px', 'marginBottom': '10px', 'textTransform': 'uppercase'}),
                        
                        dbc.NavLink(
                            [html.I(className="fas fa-brain me-2"), "Decision Core"],
                            href="/decision-core",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-vote-yea me-2"), "Vote Engine"],
                            href="/vote-panel",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-chart-line me-2"), "Position Sizing"],
                            href="/position-sizing",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-clock me-2"), "Timespan Intelligence"],
                            href="/timespan-intelligence",
                            className="sidebar-nav-link"
                        ),
                        
                        html.Hr(style={'borderColor': '#374151', 'margin': '10px 0'}),
                        
                        html.Div("🤖 AGENT SYSTEMS", style={'color': '#9ca3af', 'fontSize': '12px', 'marginBottom': '10px', 'textTransform': 'uppercase'}),
                        
                        dbc.NavLink(
                            [html.I(className="fas fa-network-wired me-2"), "Agent Spectrum"],
                            href="/agent-spectrum",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-heartbeat me-2"), "Agent Lifecycle"],
                            href="/agent-lifecycle",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-crown me-2"), "Meta Governance"],
                            href="/meta-governance",
                            className="sidebar-nav-link"
                        ),
                        
                        html.Hr(style={'borderColor': '#374151', 'margin': '10px 0'}),
                        
                        html.Div("💼 PORTFOLIO & RISK", style={'color': '#9ca3af', 'fontSize': '12px', 'marginBottom': '10px', 'textTransform': 'uppercase'}),
                        
                        dbc.NavLink(
                            [html.I(className="fas fa-briefcase me-2"), "Multi Portfolio"],
                            href="/multi-portfolio",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-chart-pie me-2"), "Portfolio Intelligence"],
                            href="/portfolio-intelligence",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-shield-alt me-2"), "Risk Ecosystem"],
                            href="/risk-ecosystem",
                            className="sidebar-nav-link"
                        ),
                        
                        html.Hr(style={'borderColor': '#374151', 'margin': '10px 0'}),
                        
                        html.Div("🔬 ANALYSIS & EVOLUTION", style={'color': '#9ca3af', 'fontSize': '12px', 'marginBottom': '10px', 'textTransform': 'uppercase'}),
                        
                        dbc.NavLink(
                            [html.I(className="fas fa-dna me-2"), "Mutation Tracker"],
                            href="/mutation-tracker",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-project-diagram me-2"), "System Flow"],
                            href="/system-flow",
                            className="sidebar-nav-link"
                        ),
                        dbc.NavLink(
                            [html.I(className="fas fa-book me-2"), "Narrative Engine"],
                            href="/narrative",
                            className="sidebar-nav-link"
                        ),
                    ],
                    vertical=True,
                    pills=True,
                ),
                className="sidebar-nav"
            ),
            
            html.Hr(style={'borderColor': '#374151', 'marginTop': '20px'}),
            
            # Data Source Toggle
            html.Div(
                [
                    html.Div("Data Source", style={'fontSize': '12px', 'color': '#9ca3af', 'marginBottom': '8px', 'textAlign': 'center'}),
                    dbc.RadioItems(
                        id='data-source-toggle',
                        options=[
                            {'label': ' Mock Data', 'value': 'mock'},
                            {'label': ' Live API', 'value': 'live'}
                        ],
                        value='mock',
                        inline=False,
                        style={'fontSize': '13px', 'color': '#e5e7eb'}
                    )
                ],
                style={'padding': '10px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px', 'marginTop': '10px'}
            ),
            
            html.Hr(style={'borderColor': '#374151', 'marginTop': '15px'}),
            
            # Status indicator
            html.Div(
                [
                    html.Div("System Status", style={'fontSize': '12px', 'color': '#9ca3af', 'marginBottom': '5px'}),
                    html.Div(
                        [
                            html.Span("● ", style={'color': '#10b981'}),
                            html.Span("Active", style={'color': '#10b981', 'fontSize': '14px'})
                        ],
                        id='system-status-indicator'
                    )
                ],
                style={'textAlign': 'center', 'marginTop': '15px'}
            )
        ],
        className="sidebar",
        style={
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '250px',
            'padding': '20px',
            'backgroundColor': '#151932',
            'overflowY': 'auto'
        }
    )
