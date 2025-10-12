"""
Test för Dash Dashboard
Verifierar att dashboarden kan startas och alla paneler är tillgängliga.
"""

import sys
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def test_dashboard_import():
    """Test att appen kan importeras"""
    from dash_app.app import app
    assert app is not None
    print("✓ App import successful")

def test_layout_components():
    """Test att layout-komponenter finns"""
    from dash_app.layout import sidebar, header, page_router
    assert sidebar.create_sidebar is not None
    assert header.create_header is not None
    assert page_router.route_page is not None
    print("✓ Layout components OK")

def test_all_panels():
    """Test att alla paneler kan importeras"""
    panels = [
        'decision_core_panel',
        'vote_panel',
        'position_sizing_panel',
        'timespan_intelligence_panel',
        'multi_portfolio_panel',
        'mutation_tracker_panel',
        'agent_spectrum_panel',
        'agent_lifecycle_panel',
        'meta_governance_panel',
        'portfolio_intelligence_panel',
        'risk_ecosystem_panel',
        'system_flow_panel',
        'narrative_panel'
    ]
    
    for panel in panels:
        module = __import__(f'dash_app.panels.{panel}', fromlist=[panel])
        assert module.create_panel is not None
        print(f"✓ {panel} OK")

def test_ui_components():
    """Test att UI-komponenter finns"""
    from dash_app.components import ui_components
    assert ui_components.create_metric_card is not None
    assert ui_components.create_data_table is not None
    assert ui_components.create_line_chart is not None
    assert ui_components.create_bar_chart is not None
    print("✓ UI components OK")

def test_routing():
    """Test att routing fungerar för alla URL:er"""
    from dash_app.layout.page_router import route_page
    
    routes = [
        '/',
        '/decision-core',
        '/vote-panel',
        '/position-sizing',
        '/timespan-intelligence',
        '/multi-portfolio',
        '/mutation-tracker',
        '/agent-spectrum',
        '/agent-lifecycle',
        '/meta-governance',
        '/portfolio-intelligence',
        '/risk-ecosystem',
        '/system-flow',
        '/narrative'
    ]
    
    for route in routes:
        header, content = route_page(route)
        assert header is not None
        assert content is not None
        print(f"✓ Route {route} OK")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("OBSCURAFLOW DASHBOARD - TEST")
    print("="*80 + "\n")
    
    try:
        test_dashboard_import()
        test_layout_components()
        test_ui_components()
        test_all_panels()
        test_routing()
        
        print("\n" + "="*80)
        print("ALLA TESTER GODKÄNDA! ✓")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST MISSLYCKADES: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
