"""
Components - Återanvändbara UI-komponenter
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

def create_metric_card(label, value, change=None, icon=None):
    """
    Skapar ett metrics-kort.
    
    Args:
        label: Etikett för metriken
        value: Värde
        change: Förändring (valfritt, kan vara positiv eller negativ)
        icon: Font Awesome icon (valfritt)
    """
    card_content = []
    
    if icon:
        card_content.append(
            html.I(className=f"{icon}", style={'fontSize': '24px', 'color': '#00d9ff', 'marginBottom': '10px'})
        )
    
    card_content.append(
        html.Div(label, className="metric-label")
    )
    
    card_content.append(
        html.Div(value, className="metric-value")
    )
    
    if change is not None:
        change_class = "positive" if change >= 0 else "negative"
        change_symbol = "↑" if change >= 0 else "↓"
        card_content.append(
            html.Div(
                f"{change_symbol} {abs(change):.2f}%",
                className=f"metric-change {change_class}"
            )
        )
    
    return dbc.Card(
        dbc.CardBody(card_content),
        className="metric-card"
    )


def create_data_table(headers, rows, table_id=None):
    """
    Skapar en datatabell.
    
    Args:
        headers: Lista med kolumnrubriker
        rows: Lista med rader (varje rad är en lista med värden)
        table_id: ID för tabellen (valfritt)
    """
    return html.Div(
        [
            html.Table(
                [
                    html.Thead(
                        html.Tr([html.Th(header) for header in headers])
                    ),
                    html.Tbody(
                        [
                            html.Tr([html.Td(cell) for cell in row])
                            for row in rows
                        ]
                    )
                ],
                id=table_id,
                style={'width': '100%'}
            )
        ],
        style={'overflowX': 'auto'}
    )


def create_line_chart(x_data, y_data, title, x_label="Time", y_label="Value"):
    """
    Skapar ett linjediagram.
    
    Args:
        x_data: X-axel data
        y_data: Y-axel data
        title: Diagramtitel
        x_label: X-axel label
        y_label: Y-axel label
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        line=dict(color='#00d9ff', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb'),
        hovermode='x unified'
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_bar_chart(x_data, y_data, title, x_label="Category", y_label="Value", color='#00d9ff'):
    """
    Skapar ett stapeldiagram.
    
    Args:
        x_data: X-axel data (kategorier)
        y_data: Y-axel data (värden)
        title: Diagramtitel
        x_label: X-axel label
        y_label: Y-axel label
        color: Färg på staplarna
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        marker_color=color
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb')
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_scatter_plot(x_data, y_data, labels, title, x_label="X", y_label="Y"):
    """
    Skapar ett scatter plot.
    
    Args:
        x_data: X-axel data
        y_data: Y-axel data
        labels: Labels för varje punkt
        title: Diagramtitel
        x_label: X-axel label
        y_label: Y-axel label
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers+text',
        text=labels,
        textposition="top center",
        marker=dict(
            size=12,
            color=y_data,
            colorscale='Viridis',
            showscale=True
        )
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        plot_bgcolor='#1a1f3a',
        paper_bgcolor='#151932',
        font=dict(color='#e5e7eb')
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_status_badge(status, text=None):
    """
    Skapar en status-badge.
    
    Args:
        status: Status ('active', 'inactive', 'warning', 'error')
        text: Text att visa (valfritt, annars används status)
    """
    colors = {
        'active': '#10b981',
        'inactive': '#9ca3af',
        'warning': '#f59e0b',
        'error': '#ef4444'
    }
    
    return html.Span(
        [
            html.Span("● ", style={'color': colors.get(status, '#9ca3af')}),
            html.Span(text or status.capitalize())
        ],
        style={'fontSize': '14px', 'fontWeight': '500'}
    )


def create_loading_spinner():
    """
    Skapar en loading spinner.
    """
    return html.Div(
        className="loading-spinner"
    )
