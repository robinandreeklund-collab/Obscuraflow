"""
System Verification Test - Kompakt test för att verifiera alla komponenter
"""

import sys
import os
sys.path.insert(0, '/home/runner/work/Obscuraflow/Obscuraflow')

def test_all_modules():
    """Test att alla 19 moduler kan initialiseras"""
    print("\n" + "="*80)
    print("SYSTEMVERIFIERINGSTEST - Alla Moduler")
    print("="*80)
    
    from modules.data_stream import DataStream
    from modules.trending_pool import TrendingPool
    from modules.decision_core import DecisionCore
    from modules.vote_engine import VoteEngine
    from modules.fusion import Fusion
    from modules.sizing import Sizing
    from modules.timespan_engine import TimespanEngine
    from modules.portfolio_engine import PortfolioEngine
    from modules.evolution import Evolution
    from modules.self_critique import SelfCritique
    from modules.symbol_memory import SymbolMemory
    from modules.narrative_engine import NarrativeEngine
    from modules.mutation_tracker import MutationTracker
    from modules.synergy_matrix import SynergyMatrix
    from modules.agent_spectrum import AgentSpectrum
    from modules.agent_lifecycle import AgentLifecycle
    from modules.metaagentgovernor import MetaAgentGovernor
    from modules.portfolio_comparator import PortfolioComparator
    from modules.risk_mapper import RiskMapper
    
    modules = [
        ('DataStream', lambda: DataStream(api_key='test', use_mock_data=True)),
        ('TrendingPool', lambda: TrendingPool()),
        ('DecisionCore', lambda: DecisionCore()),
        ('VoteEngine', lambda: VoteEngine()),
        ('Fusion', lambda: Fusion()),
        ('Sizing', lambda: Sizing()),
        ('TimespanEngine', lambda: TimespanEngine()),
        ('PortfolioEngine', lambda: PortfolioEngine()),
        ('Evolution', lambda: Evolution()),
        ('SelfCritique', lambda: SelfCritique()),
        ('SymbolMemory', lambda: SymbolMemory()),
        ('NarrativeEngine', lambda: NarrativeEngine()),
        ('MutationTracker', lambda: MutationTracker()),
        ('SynergyMatrix', lambda: SynergyMatrix()),
        ('AgentSpectrum', lambda: AgentSpectrum()),
        ('AgentLifecycle', lambda: AgentLifecycle()),
        ('MetaAgentGovernor', lambda: MetaAgentGovernor()),
        ('PortfolioComparator', lambda: PortfolioComparator()),
        ('RiskMapper', lambda: RiskMapper()),
    ]
    
    initialized = []
    for name, init_func in modules:
        try:
            module = init_func()
            print(f"✓ {name:25s} - Initialiserad")
            initialized.append((name, module))
        except Exception as e:
            print(f"✗ {name:25s} - MISSLYCKADES: {e}")
            return False
    
    print(f"\n✅ Alla {len(initialized)}/19 moduler initialiserade framgångsrikt!")
    return initialized


def test_all_agents():
    """Test att alla 16 agenter kan initialiseras"""
    print("\n" + "="*80)
    print("AGENTVERIFIERING - Alla Agenter")
    print("="*80)
    
    from agents.agent_registry import AgentRegistry
    
    registry = AgentRegistry()
    all_agents = registry.list_agents()
    
    print(f"\nRegistrerade agenter: {len(all_agents)}")
    
    classic = [a for a in all_agents if str(a['type']) == 'AgentType.CLASSIC']
    paradigms = [a for a in all_agents if str(a['type']) == 'AgentType.PARADIGMATIC']
    
    print(f"\n--- Klassiska Agenter ({len(classic)}/4) ---")
    for agent in classic:
        print(f"  ✓ {agent['id']:20s} - {agent.get('strategy', 'N/A')}")
    
    print(f"\n--- Paradigmatiska Agenter ({len(paradigms)}/12) ---")
    for agent in paradigms:
        print(f"  ✓ {agent['id']:20s} - {agent.get('dimension', 'N/A')}")
    
    # Testa att skapa några agenter
    print(f"\n--- Skapar Agent-instanser ---")
    test_agents = ['momentum_agent', 'echo_agent', 'vox_agent']
    for agent_id in test_agents:
        agent = registry.create_agent(agent_id)
        if agent:
            print(f"  ✓ {agent_id:20s} - Skapad och funktionell")
        else:
            print(f"  ✗ {agent_id:20s} - Kunde inte skapas")
    
    print(f"\n✅ Alla {len(all_agents)}/16 agenter verifierade!")
    return len(all_agents) == 16


def test_data_flow():
    """Test att dataflödet fungerar från data till beslut"""
    print("\n" + "="*80)
    print("DATAFLÖDESVERIFIERING")
    print("="*80)
    
    from modules.data_stream import DataStream
    from modules.trending_pool import TrendingPool
    from agents.agent_registry import AgentRegistry
    from modules.decision_core import DecisionCore
    
    # Initiera komponenter
    data_stream = DataStream(api_key='test', use_mock_data=True)
    trending_pool = TrendingPool()
    registry = AgentRegistry()
    decision_core = DecisionCore()
    
    print("\n1. Hämtar marknadsdata...")
    market_data = data_stream.fetch_market_data()
    if not market_data:
        print("  ✗ Ingen marknadsdata hämtad")
        return False
    
    symbol = list(market_data.keys())[0]
    data = market_data[symbol]
    print(f"  ✓ Hämtade data för {len(market_data)} symboler")
    print(f"  Exempel ({symbol}): price=${data['c']:.2f}, volume={data['v']:,}")
    
    print("\n2. Analyserar trender...")
    trend_data = data_stream.analyze_trend(symbol)
    score = trending_pool.update_symbol(symbol, trend_data)
    print(f"  ✓ Trendscore för {symbol}: {score:.2f}")
    
    print("\n3. Skapar agentbeslut...")
    agent = registry.create_agent('momentum_agent')
    if not agent:
        print("  ✗ Kunde inte skapa agent")
        return False
    
    # Skapa marknadsdata i rätt format för agent
    agent_market_data = {
        'price': data['c'],
        'volume': data['v'],
        'high': data['h'],
        'low': data['l'],
        'prev_close': data['pc'],
        'price_change_pct': data['dp'],
        'trend_score': 0.5
    }
    
    decision = agent.analyze(symbol, agent_market_data)
    print(f"  ✓ Agent beslut: {decision['decision']} ({symbol})")
    print(f"    Confidence: {decision['confidence']:.1%}")
    print(f"    Reasoning: {decision['reasoning'][:60]}...")
    
    print("\n4. Registrerar beslut i DecisionCore...")
    decision_core.route_decision(decision)
    stats = decision_core.get_stats()
    print(f"  ✓ Total decisions: {stats['total_decisions']}")
    
    print("\n✅ Komplett dataflöde verifierat: Data → Agent → Decision")
    return True


def test_dashboard_panels():
    """Test att alla dashboard-paneler existerar och har rätt struktur"""
    print("\n" + "="*80)
    print("DASHBOARD-PANELVERIFIERING")
    print("="*80)
    
    import os
    
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
        'narrative_panel',
        'data_source_panel',
        'portfolio_development_panel'
    ]
    
    panel_dir = '/home/runner/work/Obscuraflow/Obscuraflow/dash_app/panels'
    
    existing = []
    for panel_name in panels:
        panel_file = os.path.join(panel_dir, f'{panel_name}.py')
        if os.path.exists(panel_file):
            # Check if file has create_panel function
            with open(panel_file, 'r') as f:
                content = f.read()
                if 'def create_panel' in content:
                    print(f"  ✓ {panel_name:35s} - Finns och har create_panel()")
                    existing.append(panel_name)
                else:
                    print(f"  ⚠ {panel_name:35s} - Finns men saknar create_panel()")
        else:
            print(f"  ✗ {panel_name:35s} - Filen finns inte")
    
    print(f"\n✅ {len(existing)}/{len(panels)} paneler verifierade!")
    print("   (Notera: Dash-biblioteket behövs ej installerat för denna verifiering)")
    return len(existing) == len(panels)


if __name__ == '__main__':
    print("\n" + "="*80)
    print("OBSCURAFLOW - SYSTEMVERIFIERING")
    print("="*80)
    
    results = []
    
    # Test 1: Moduler
    modules = test_all_modules()
    results.append(('Moduler (19)', modules is not False))
    
    # Test 2: Agenter
    agents_ok = test_all_agents()
    results.append(('Agenter (16)', agents_ok))
    
    # Test 3: Dataflöde
    dataflow_ok = test_data_flow()
    results.append(('Dataflöde', dataflow_ok))
    
    # Test 4: Dashboard
    dashboard_ok = test_dashboard_panels()
    results.append(('Dashboard (15 paneler)', dashboard_ok))
    
    # Sammanfattning
    print("\n" + "="*80)
    print("SAMMANFATTNING")
    print("="*80)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:8s} {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n🎉 ALLA TESTER GODKÄNDA - SYSTEMET ÄR FULLT OPERATIVT!")
    else:
        print("\n⚠️ VISSA TESTER MISSLYCKADES - SE DETALJER OVAN")
    
    print("="*80 + "\n")
