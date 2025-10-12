"""
Test för agentlager

Detta test verifierar att:
- Alla agenter kan importeras och instansieras
- AgentRegistry fungerar korrekt
- Agenter kan analysera marknadsdata
- Agenter returnerar korrekta beslutsstrukturer
"""

import logging
from agents.agent_registry import get_registry
from agents.base_agent import BaseAgent, AgentType, DecisionType


# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def test_agent_layer():
    """
    Testar hela agentlagret.
    """
    print("=" * 80)
    print("TEST: AGENTLAGER - Full implementation")
    print("=" * 80)
    
    # ========================================================================
    # STEG 1: AGENT REGISTRY
    # ========================================================================
    print("\n--- STEG 1: Agent Registry ---")
    
    registry = get_registry()
    stats = registry.get_stats()
    
    print(f"✓ Registry initierat")
    print(f"  Total agenttyper: {stats['total_agent_types']}")
    print(f"  Klassiska agenter: {stats['classic_agents']}")
    print(f"  Paradigmatiska agenter: {stats['paradigmatic_agents']}")
    
    assert stats['total_agent_types'] == 16, "Förväntar 16 agenttyper"
    assert stats['classic_agents'] == 4, "Förväntar 4 klassiska agenter"
    assert stats['paradigmatic_agents'] == 12, "Expected 12 paradigmatic agents"
    
    # ========================================================================
    # STEG 2: LISTA ALLA AGENTER
    # ========================================================================
    print("\n--- STEG 2: Lista alla agenter ---")
    
    classic_agents = registry.list_agents(agent_type=AgentType.CLASSIC)
    print(f"\n✓ Klassiska agenter ({len(classic_agents)}):")
    for agent in classic_agents:
        print(f"  - {agent['name']}: {agent['description']}")
    
    paradigmatic_agents = registry.list_agents(agent_type=AgentType.PARADIGMATIC)
    print(f"\n✓ Paradigmatiska agenter ({len(paradigmatic_agents)}):")
    for agent in paradigmatic_agents:
        print(f"  - {agent['name']}: {agent['description']}")
    
    # ========================================================================
    # STEG 3: SKAPA AGENTINSTANSER
    # ========================================================================
    print("\n--- STEG 3: Skapa agentinstanser ---")
    
    # Skapa klassiska agenter
    classic_ids = ['momentum_agent', 'reversal_agent', 'breakout_agent', 'hybrid_agent']
    classic_instances = {}
    
    for agent_id in classic_ids:
        agent = registry.create_agent(agent_id)
        assert agent is not None, f"Kunde inte skapa {agent_id}"
        classic_instances[agent_id] = agent
        print(f"  ✓ Skapade {agent_id}")
    
    # Skapa paradigmatiska agenter
    paradigmatic_ids = [
        'echo_agent', 'fractalis_agent', 'vox_agent', 'myco_agent',
        'obscura_agent', 'mirage_agent', 'sentio_agent', 'reflexion_agent',
        'dimensio_agent', 'symbio_agent', 'genesis_agent', 'architectum_agent'
    ]
    paradigmatic_instances = {}
    
    for agent_id in paradigmatic_ids:
        agent = registry.create_agent(agent_id)
        assert agent is not None, f"Kunde inte skapa {agent_id}"
        paradigmatic_instances[agent_id] = agent
        print(f"  ✓ Skapade {agent_id}")
    
    print(f"\n✓ Totalt {len(classic_instances) + len(paradigmatic_instances)} agenter skapade")
    
    # ========================================================================
    # STEG 4: ANALYSERA MARKNADSDATA
    # ========================================================================
    print("\n--- STEG 4: Analysera marknadsdata ---")
    
    # Mock marknadsdata för olika scenarion
    scenarios = {
        'strong_uptrend': {
            'symbol': 'AAPL',
            'price': 175.50,
            'volume': 3000000,
            'trend_score': 0.85,
            'price_change_pct': 0.035,
            'volatility': 0.3
        },
        'downtrend': {
            'symbol': 'TSLA',
            'price': 220.00,
            'volume': 2500000,
            'trend_score': 0.25,
            'price_change_pct': -0.028,
            'volatility': 0.6
        },
        'neutral': {
            'symbol': 'MSFT',
            'price': 380.00,
            'volume': 1500000,
            'trend_score': 0.5,
            'price_change_pct': 0.005,
            'volatility': 0.4
        }
    }
    
    for scenario_name, market_data in scenarios.items():
        print(f"\n  Scenario: {scenario_name.upper()} - {market_data['symbol']}")
        print(f"    Price: ${market_data['price']:.2f}, Change: {market_data['price_change_pct']:.2%}")
        print(f"    Trend: {market_data['trend_score']:.2f}, Vol: {market_data['volatility']:.2f}")
        
        # Analysera med några klassiska agenter
        momentum = classic_instances['momentum_agent']
        result = momentum.analyze(market_data['symbol'], market_data)
        print(f"    MomentumAgent: {result['decision']} (conf={result['confidence']:.2f})")
        
        reversal = classic_instances['reversal_agent']
        result = reversal.analyze(market_data['symbol'], market_data)
        print(f"    ReversalAgent: {result['decision']} (conf={result['confidence']:.2f})")
        
        # Analysera med några paradigmatiska agenter
        fractalis = paradigmatic_instances['fractalis_agent']
        result = fractalis.analyze(market_data['symbol'], market_data)
        print(f"    FractalisAgent: {result['decision']} (conf={result['confidence']:.2f})")
        
        dimensio = paradigmatic_instances['dimensio_agent']
        result = dimensio.analyze(market_data['symbol'], market_data)
        print(f"    DimensioAgent: {result['decision']} (conf={result['confidence']:.2f})")
    
    # ========================================================================
    # STEG 5: KONSENSUSANALYS
    # ========================================================================
    print("\n--- STEG 5: Konsensusanalys ---")
    
    # Analysera ett scenario med alla agenter
    test_data = scenarios['strong_uptrend']
    all_decisions = []
    
    all_agents = {**classic_instances, **paradigmatic_instances}
    
    for agent_id, agent in all_agents.items():
        result = agent.analyze(test_data['symbol'], test_data)
        all_decisions.append({
            'agent': agent_id,
            'decision': result['decision'],
            'confidence': result['confidence']
        })
    
    # Räkna konsensus
    buy_count = sum(1 for d in all_decisions if d['decision'] == 'buy')
    sell_count = sum(1 for d in all_decisions if d['decision'] == 'sell')
    hold_count = sum(1 for d in all_decisions if d['decision'] == 'hold')
    
    print(f"\n  Analyserade {test_data['symbol']} med alla {len(all_agents)} agenter")
    print(f"  BUY:  {buy_count} agenter ({buy_count/len(all_agents)*100:.1f}%)")
    print(f"  SELL: {sell_count} agenter ({sell_count/len(all_agents)*100:.1f}%)")
    print(f"  HOLD: {hold_count} agenter ({hold_count/len(all_agents)*100:.1f}%)")
    
    # Visa top 5 mest säkra beslut
    top_decisions = sorted(all_decisions, key=lambda x: x['confidence'], reverse=True)[:5]
    print(f"\n  Top 5 mest säkra beslut:")
    for i, d in enumerate(top_decisions, 1):
        print(f"    {i}. {d['agent']}: {d['decision'].upper()} (conf={d['confidence']:.2f})")
    
    # ========================================================================
    # STEG 6: AGENTSTATISTIK
    # ========================================================================
    print("\n--- STEG 6: Agentstatistik ---")
    
    # Simulera några beslutsutfall
    momentum = classic_instances['momentum_agent']
    for i in range(10):
        outcome = 1.0 if i < 7 else 0.0  # 70% framgångsrate
        momentum.record_decision({'test': True}, outcome)
    
    stats = momentum.get_stats()
    print(f"\n  MomentumAgent efter 10 beslut:")
    print(f"    Performance score: {stats['performance_score']:.2f}")
    print(f"    Total decisions: {stats['total_decisions']}")
    print(f"    Successful: {stats['successful_decisions']}")
    
    # ========================================================================
    # STEG 7: VERIFIERING
    # ========================================================================
    print("\n--- STEG 7: Verifiering ---")
    
    registry_stats = registry.get_stats()
    assert registry_stats['active_instances'] == 16, "Förväntar 16 aktiva instanser"
    print(f"✓ Alla {registry_stats['active_instances']} agenter aktiva")
    
    # Verifiera att alla agenter returnerar korrekt struktur
    test_agent = classic_instances['momentum_agent']
    result = test_agent.analyze('TEST', test_data)
    
    required_keys = ['agent_id', 'symbol', 'decision', 'confidence', 'reasoning']
    for key in required_keys:
        assert key in result, f"Saknar nyckel {key} i resultat"
    
    assert result['decision'] in ['buy', 'sell', 'hold'], "Ogiltigt beslut"
    assert 0.0 <= result['confidence'] <= 1.0, "Confidence utanför range"
    
    print(f"✓ Beslutsstruktur verifierad")
    print(f"✓ Alla tester godkända!")
    
    print("\n" + "=" * 80)
    print("AGENTLAGER TEST KOMPLETT - ALLA TESTER GODKÄNDA")
    print("=" * 80)


if __name__ == '__main__':
    test_agent_layer()
