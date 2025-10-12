"""
Test för att verifiera flödet mellan de fyra första modulerna:
- data_stream: Hämtar marknadsdata och analyserar trender
- trending_pool: Rankar symboler baserat på trenddata
- decision_core: Samlar agentbeslut och analyserar konsensus
- vote_engine: Löser konflikter genom viktad röstning

Detta test använder mockdata för att simulera ett komplett flöde.
"""

import logging
from modules.data_stream import DataStream
from modules.trending_pool import TrendingPool
from modules.decision_core import DecisionCore, AgentDecision, DecisionType
from modules.vote_engine import VoteEngine, Vote


# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_module_flow():
    """
    Testar det fullständiga flödet mellan alla fyra moduler med mockdata.
    """
    print("\n" + "="*80)
    print("OBSCURAFLOW - TEST AV MODULFLÖDE")
    print("="*80 + "\n")
    
    # 1. INITIERA MODULER
    print("\n--- STEG 1: Initiera moduler ---")
    
    # DataStream med mockdata
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'AMD']
    data_stream = DataStream(api_key="mock_api_key", symbols=symbols, use_mock_data=True)
    print(f"✓ DataStream initialiserad med {len(symbols)} symboler")
    
    # TrendingPool
    trending_pool = TrendingPool(max_history=50, dampening_factor=0.3)
    print("✓ TrendingPool initialiserad")
    
    # DecisionCore
    decision_core = DecisionCore(min_confidence=50.0, conflict_threshold=0.4)
    print("✓ DecisionCore initialiserad")
    
    # VoteEngine
    vote_engine = VoteEngine(initial_weight=1.0, learning_rate=0.1)
    print("✓ VoteEngine initialiserad")
    
    # 2. HÄMTA OCH ANALYSERA MARKNADSDATA
    print("\n--- STEG 2: Hämta marknadsdata och analysera trender ---")
    
    # Hämta marknadsdata
    market_data = data_stream.fetch_market_data()
    print(f"✓ Hämtade marknadsdata för {len(market_data)} symboler")
    
    # Visa exempel på marknadsdata
    if market_data:
        first_symbol = list(market_data.keys())[0]
        print(f"  Exempel ({first_symbol}): {market_data[first_symbol]}")
    
    # Analysera trender och uppdatera trending pool
    print("\n--- STEG 3: Analysera trender och uppdatera trending pool ---")
    
    for symbol in symbols:
        trend_data = data_stream.analyze_trend(symbol)
        score = trending_pool.update_symbol(symbol, trend_data)
        print(f"  {symbol}: score={score:.2f}")
    
    # Hämta rankade symboler
    ranked_symbols = trending_pool.get_ranked_symbols(limit=5)
    print(f"\n✓ Topprankade symboler:")
    for i, symbol_data in enumerate(ranked_symbols, 1):
        print(f"  {i}. {symbol_data['symbol']}: score={symbol_data['score']}")
    
    # Pool-statistik
    pool_stats = trending_pool.get_pool_stats()
    print(f"\n✓ Pool-statistik:")
    print(f"  Total symboler: {pool_stats['total_symbols']}")
    print(f"  Genomsnittligt score: {pool_stats['average_score']}")
    print(f"  Högsta score: {pool_stats['max_score']} ({pool_stats['top_symbol']['symbol']})")
    
    # 3. SIMULERA AGENTBESLUT
    print("\n--- STEG 4: Simulera agentbeslut ---")
    
    # Välj top 3 symboler för agentanalys
    top_symbols = [s['symbol'] for s in ranked_symbols[:3]]
    
    # Simulera beslut från olika agenter
    mock_agents = [
        ('momentum_agent', 'buy', 85),
        ('reversal_agent', 'sell', 75),
        ('breakout_agent', 'buy', 90),
        ('hybrid_agent', 'buy', 80),
        ('echo_agent', 'sell', 70),
        ('fractalis_agent', 'buy', 65)
    ]
    
    for symbol in top_symbols:
        print(f"\n  Symbol: {symbol}")
        for agent_id, decision_type, confidence in mock_agents:
            decision = AgentDecision(
                agent_id=agent_id,
                symbol=symbol,
                decision=DecisionType(decision_type),
                confidence=confidence,
                reasoning=f"Baserat på {agent_id} analys"
            )
            accepted = decision_core.add_decision(decision)
            if accepted:
                print(f"    ✓ {agent_id}: {decision_type} (confidence={confidence})")
    
    # 4. ANALYSERA KONSENSUS
    print("\n--- STEG 5: Analysera konsensus ---")
    
    for symbol in top_symbols:
        consensus = decision_core.analyze_consensus(symbol)
        print(f"\n  {symbol}:")
        print(f"    Konsensus: {consensus['consensus']}")
        print(f"    Konflikt: {'Ja' if consensus['has_conflict'] else 'Nej'}")
        print(f"    Total beslut: {consensus['total_decisions']}")
        print(f"    Genomsnittlig confidence: {consensus['average_confidence']}")
        print(f"    Breakdown: {consensus['decision_breakdown']}")
    
    # 5. ROUTING OCH KONFLIKTHANTERING
    print("\n--- STEG 6: Routing och konflikthantering ---")
    
    for symbol in top_symbols:
        routing_result = decision_core.route_decision(symbol)
        consensus = routing_result['consensus']
        routing = routing_result['routing']
        
        print(f"\n  {symbol}:")
        print(f"    Destination: {routing['destination']}")
        print(f"    Anledning: {routing['reason']}")
        print(f"    Prioritet: {routing['priority']}")
        
        # Om konflikt, använd vote_engine
        if consensus['has_conflict']:
            print(f"    → Eskalerar till VoteEngine")
            
            # Skapa röster från besluten
            votes = []
            decisions = decision_core.get_decisions_for_symbol(symbol)
            for decision in decisions:
                vote = Vote(
                    agent_id=decision.agent_id,
                    vote=decision.decision.value,
                    confidence=decision.confidence
                )
                vote_engine.add_vote(vote)
                votes.append(vote)
            
            # Beräkna vägd röstning
            vote_result = vote_engine.calculate_weighted_vote(votes, symbol)
            print(f"    → Röstningsresultat: {vote_result['winner']}")
            print(f"    → Enhälligt: {'Ja' if vote_result['is_unanimous'] else 'Nej'}")
            print(f"    → Vote breakdown: {vote_result['vote_breakdown']}")
    
    # 6. STATISTIK OCH SAMMANFATTNING
    print("\n--- STEG 7: Statistik och sammanfattning ---")
    
    print("\n  DecisionCore statistik:")
    dc_stats = decision_core.get_stats()
    for key, value in dc_stats.items():
        print(f"    {key}: {value}")
    
    print("\n  VoteEngine statistik:")
    ve_stats = vote_engine.get_stats()
    for key, value in ve_stats.items():
        print(f"    {key}: {value}")
    
    print("\n  Agentprestationer:")
    performances = vote_engine.get_all_agent_performances()
    for perf in performances[:5]:  # Visa top 5
        print(f"    {perf['agent_id']}: weight={perf['weight']:.2f}, accuracy={perf['accuracy']:.1f}%")
    
    # 7. TEST AV TOP SYMBOLS FRÅN DATA_STREAM
    print("\n--- STEG 8: Test av get_top_symbols() ---")
    top_from_stream = data_stream.get_top_symbols(limit=5)
    print(f"  Top 5 symboler från DataStream: {top_from_stream}")
    
    print("\n" + "="*80)
    print("TEST SLUTFÖRT MED FRAMGÅNG! ✓")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        test_module_flow()
    except Exception as e:
        logger.error(f"Test misslyckades: {e}", exc_info=True)
        raise
