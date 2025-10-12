"""
Header - Dynamisk header för varje panel
"""

from dash import html
import dash_bootstrap_components as dbc

def create_header(title, subtitle=None, icon=None):
    """
    Skapar en header för en panel.
    
    Args:
        title: Huvudtitel
        subtitle: Undertitel (valfritt)
        icon: Font Awesome icon class (valfritt)
    """
    header_content = []
    
    if icon:
        header_content.append(html.I(className=f"{icon} me-2"))
    
    header_content.append(html.Span(title))
    
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2(
                    header_content,
                    className="dashboard-title",
                    style={'marginBottom': '10px'}
                ),
                html.P(
                    subtitle or "",
                    className="dashboard-subtitle",
                    style={'color': '#9ca3af'}
                ) if subtitle else None
            ]
        ),
        className="dashboard-header",
        style={'marginBottom': '20px'}
    )
