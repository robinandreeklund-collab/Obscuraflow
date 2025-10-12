"""
Test för att verifiera det fullständiga systemflödet mellan ALLA moduler:
- data_stream: Hämtar marknadsdata och analyserar trender
- trending_pool: Rankar symboler baserat på trenddata
- decision_core: Samlar agentbeslut och analyserar konsensus
- vote_engine: Löser konflikter genom viktad röstning
- fusion: Validerar signaler över flera tidsramar
- sizing: Beräknar optimal positionsstorlek
- timespan_engine: Hanterar data över tidsramar
- portfolio_engine: Hanterar portföljer och positioner
- evolution: Evolverar strategier
- self_critique: Analyserar beslut och fel
- symbol_memory: Lagrar symbolspecifik historik
- narrative_engine: Bygger systemberättelse
- mutation_tracker: Spårar strategimutationer

Detta test simulerar ett komplett tradingflöde från datahämtning till portföljoptimering.
"""

import logging
from modules.data_stream import DataStream
from modules.trending_pool import TrendingPool
from modules.decision_core import DecisionCore, AgentDecision, DecisionType
from modules.vote_engine import VoteEngine, Vote
from modules.fusion import Fusion
from modules.sizing import Sizing
from modules.timespan_engine import TimespanEngine
from modules.portfolio_engine import PortfolioEngine
from modules.evolution import Evolution
from modules.self_critique import SelfCritique
from modules.symbol_memory import SymbolMemory
from modules.narrative_engine import NarrativeEngine
from modules.mutation_tracker import MutationTracker


# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_system_flow():
    """
    Testar det fullständiga systemflödet mellan alla moduler med mockdata.
    Detta test simulerar ett komplett tradingscenario.
    """
    print("\n" + "="*80)
    print("OBSCURAFLOW - KOMPLETT SYSTEMFLÖDESTEST")
    print("="*80 + "\n")
    
    # ========================================================================
    # STEG 1: INITIERA ALLA MODULER
    # ========================================================================
    print("\n--- STEG 1: Initiera alla moduler ---")
    
    # Kärnmoduler
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'AMD']
    data_stream = DataStream(api_key="mock_api_key", symbols=symbols, use_mock_data=True)
    print(f"✓ DataStream initialiserad med {len(symbols)} symboler")
    
    trending_pool = TrendingPool(max_history=50, dampening_factor=0.3)
    print("✓ TrendingPool initialiserad")
    
    decision_core = DecisionCore(min_confidence=50.0, conflict_threshold=0.4)
    print("✓ DecisionCore initialiserad")
    
    vote_engine = VoteEngine(initial_weight=1.0, learning_rate=0.1)
    print("✓ VoteEngine initialiserad")
    
    # Validerings- och sizing-moduler
    fusion = Fusion(timeframes=['1m', '5m', '15m', '1h'], min_confirmations=2)
    print("✓ Fusion initialiserad")
    
    sizing = Sizing(max_position_size=0.1, risk_per_trade=0.02, use_kelly=True)
    print("✓ Sizing initialiserad")
    
    timespan_engine = TimespanEngine(
        timeframes=['1m', '5m', '15m', '1h', '4h', '1d'],
        primary_timeframe='15m'
    )
    print("✓ TimespanEngine initialiserad")
    
    # Portfölj- och evolutionsmoduler
    portfolio_engine = PortfolioEngine(initial_capital=100000.0)
    print("✓ PortfolioEngine initialiserad")
    
    evolution = Evolution(mutation_rate=0.1, population_size=10)
    print("✓ Evolution initialiserad")
    
    # Analys- och minnesmoduler
    self_critique = SelfCritique(min_confidence_for_review=60.0)
    print("✓ SelfCritique initialiserad")
    
    symbol_memory = SymbolMemory(max_history_size=1000)
    print("✓ SymbolMemory initialiserad")
    
    narrative_engine = NarrativeEngine()
    print("✓ NarrativeEngine initialiserad")
    
    mutation_tracker = MutationTracker()
    print("✓ MutationTracker initialiserad")
    
    print(f"\n✓ Alla 13 moduler initialiserade framgångsrikt!")
    
    # ========================================================================
    # STEG 2: HÄMTA OCH ANALYSERA MARKNADSDATA
    # ========================================================================
    print("\n--- STEG 2: Hämta marknadsdata och analysera trender ---")
    
    narrative_engine.add_event(
        'system_start',
        'Systemet startar marknadsanalys',
        {'symbols': len(symbols)}
    )
    
    # Hämta marknadsdata
    market_data = data_stream.fetch_market_data()
    print(f"✓ Hämtade marknadsdata för {len(market_data)} symboler")
    
    # Visa exempel
    if market_data:
        first_symbol = list(market_data.keys())[0]
        print(f"  Exempel ({first_symbol}): price=${market_data[first_symbol]['price']:.2f}, "
              f"volume={market_data[first_symbol]['volume']}")
    
    # Analysera trender och uppdatera trending pool
    print("\n--- STEG 3: Analysera trender och uppdatera trending pool ---")
    
    for symbol in symbols:
        trend_data = data_stream.analyze_trend(symbol)
        score = trending_pool.update_symbol(symbol, trend_data)
        
        # Lagra i symbol memory
        symbol_memory.add_event(symbol, {
            'type': 'trend_analysis',
            'score': score,
            'data': trend_data
        })
        
        # Lägg till data för timespan engine
        for timeframe in timespan_engine.timeframes:
            timespan_engine.add_data(timeframe, symbol, {
                'price': market_data.get(symbol, {}).get('price', 0),
                'volume': market_data.get(symbol, {}).get('volume', 0),
                'trend_score': score
            })
        
        print(f"  {symbol}: trend_score={score:.2f}")
    
    # Hämta rankade symboler
    ranked_symbols = trending_pool.get_ranked_symbols(limit=5)
    print(f"\n✓ Topprankade symboler:")
    for i, symbol_data in enumerate(ranked_symbols, 1):
        print(f"  {i}. {symbol_data['symbol']}: score={symbol_data['score']:.2f}")
    
    narrative_engine.add_event(
        'trend_analysis_complete',
        f'Trendanalys klar för {len(symbols)} symboler',
        {'top_symbol': ranked_symbols[0]['symbol']}
    )
    
    # ========================================================================
    # STEG 4: SKAPA OCH EVOLVA STRATEGIER
    # ========================================================================
    print("\n--- STEG 4: Skapa och evolva handelsstrategier ---")
    
    # Skapa initiala strategier
    base_strategies = [
        ('momentum_strategy', {'lookback': 20, 'threshold': 0.05}),
        ('reversal_strategy', {'lookback': 10, 'threshold': 0.03}),
        ('breakout_strategy', {'lookback': 15, 'threshold': 0.07})
    ]
    
    for strategy_id, params in base_strategies:
        strategy = evolution.create_strategy(strategy_id, params)
        mutation_tracker.track_mutation(
            mutation_id=strategy_id,
            parent_id=None,
            mutation_type='initial',
            changes=params
        )
        print(f"  ✓ Skapade strategi: {strategy_id}")
    
    # Simulera prestation och evolva
    for strategy_id, _ in base_strategies:
        import random
        fitness = random.uniform(0.5, 0.9)
        evolution.evaluate_fitness(strategy_id, fitness)
        mutation_tracker.record_performance(strategy_id, fitness)
    
    # Evolva en generation
    evolution_result = evolution.evolve_generation()
    print(f"  ✓ Evolverade till generation {evolution_result['generation']}")
    print(f"    Mutationer skapade: {evolution_result.get('mutations_created', 0)}")
    
    narrative_engine.add_event(
        'strategy_evolution',
        f"Strategier evolverade till generation {evolution_result['generation']}",
        {'mutations': evolution_result.get('mutations_created', 0)}
    )
    
    # ========================================================================
    # STEG 5: SIMULERA AGENTBESLUT OCH KONSENSUSANALYS
    # ========================================================================
    print("\n--- STEG 5: Simulera agentbeslut och analysera konsensus ---")
    
    # Välj top 3 symboler för trading
    top_symbols = [s['symbol'] for s in ranked_symbols[:3]]
    
    # Simulera beslut från agenter
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
            decision_core.add_decision(decision)
            print(f"    ✓ {agent_id}: {decision_type} (confidence={confidence})")
        
        # Logga till narrative
        narrative_engine.add_event(
            'agent_decisions',
            f'Agenter analyserade {symbol}',
            {'agent_count': len(mock_agents)}
        )
    
    # ========================================================================
    # STEG 6: ROUTING, KONFLIKTHANTERING OCH SIGNALVALIDERING
    # ========================================================================
    print("\n--- STEG 6: Routing, konflikthantering och signalvalidering ---")
    
    for symbol in top_symbols:
        # Analysera konsensus
        consensus = decision_core.analyze_consensus(symbol)
        
        # Routing
        routing_result = decision_core.route_decision(symbol)
        routing = routing_result['routing']
        
        print(f"\n  {symbol}:")
        print(f"    Konsensus: {consensus['consensus']}")
        print(f"    Konflikt: {'Ja' if consensus['has_conflict'] else 'Nej'}")
        print(f"    Destination: {routing['destination']}")
        
        # Hantera enligt routing
        if consensus['has_conflict']:
            print(f"    → Eskalerar till VoteEngine")
            
            # Skapa röster
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
            final_decision = vote_result['winner']
            print(f"    → Röstningsresultat: {final_decision}")
            
            narrative_engine.add_event(
                'vote_resolution',
                f'Konflikt för {symbol} löst via röstning: {final_decision}',
                {'votes': len(votes)}
            )
        elif routing['destination'] == 'fusion':
            print(f"    → Validerar signal via Fusion")
            
            # Validera signal över tidsramar
            signal_type = consensus['consensus']
            confidence = consensus['average_confidence']
            
            validation = fusion.validate_signal(symbol, signal_type, confidence)
            print(f"    → Validerad: {validation['validated']}, "
                  f"bekräftelser: {validation['confirmations']}/{len(fusion.timeframes)}")
            
            # Analysera konvergens
            convergence = fusion.get_convergence(symbol)
            print(f"    → Konvergens: {convergence['convergence_score']:.2%}")
            
            final_decision = signal_type if validation['validated'] else 'hold'
            
            narrative_engine.add_event(
                'signal_validation',
                f'Signal för {symbol} validerad: {final_decision}',
                {'convergence': convergence['convergence_score']}
            )
        else:
            final_decision = 'hold'
        
        # Identifiera mönster i symbol memory
        patterns = symbol_memory.identify_patterns(symbol)
        if patterns:
            print(f"    → Mönster identifierade: {len(patterns)}")
            for pattern in patterns[:2]:  # Visa max 2
                print(f"      • {pattern['type']}: {pattern['description']}")
    
    # ========================================================================
    # STEG 7: POSITION SIZING OCH PORTFÖLJHANTERING
    # ========================================================================
    print("\n--- STEG 7: Position sizing och portföljhantering ---")
    
    # Skapa portföljer
    portfolio_engine.create_portfolio('main_portfolio', strategy='balanced')
    portfolio_engine.create_portfolio('aggressive_portfolio', strategy='aggressive')
    print("✓ Skapade 2 portföljer")
    
    # Beräkna position sizes för de symboler vi vill handla
    portfolio_value = 100000.0
    
    for symbol in top_symbols[:2]:  # Ta top 2
        consensus = decision_core.analyze_consensus(symbol)
        
        if consensus['consensus'] in ['buy', 'sell']:
            # Synkronisera timeframes
            sync_result = timespan_engine.sync_timeframes(symbol)
            print(f"\n  {symbol}:")
            print(f"    Tidsramar synkroniserade: {sync_result['alignment_score']:.2%}")
            
            # Beräkna position size
            sizing_result = sizing.calculate_position_size(
                symbol=symbol,
                portfolio_value=portfolio_value,
                confidence=consensus['average_confidence'],
                volatility=0.15,  # Simulerad volatilitet
                win_rate=0.6,
                avg_win_loss_ratio=1.5
            )
            
            print(f"    Position size: ${sizing_result['position_size']:.2f} "
                  f"({sizing_result['position_size_percent']:.2f}%)")
            print(f"    Risk: ${sizing_result['risk_amount']:.2f}")
            
            if sizing_result['kelly_fraction']:
                print(f"    Kelly fraction: {sizing_result['kelly_fraction']:.4f}")
            
            # Lägg till position i portfölj
            price = market_data.get(symbol, {}).get('price', 100)
            shares = sizing_result['position_size'] / price
            
            portfolio_engine.add_position('main_portfolio', symbol, shares, price)
            print(f"    ✓ Position tillagd i portfölj: {shares:.2f} aktier @ ${price:.2f}")
            
            narrative_engine.add_event(
                'position_opened',
                f'Position öppnad i {symbol}',
                {'size': sizing_result['position_size'], 'shares': shares}
            )
    
    # ========================================================================
    # STEG 8: PORTFÖLJOPTIMERING OCH ANALYS
    # ========================================================================
    print("\n--- STEG 8: Portföljoptimering och analys ---")
    
    # Optimera portfölj
    optimization = portfolio_engine.optimize_portfolio('main_portfolio')
    print(f"\n  Portföljoptimering:")
    print(f"    Nuvarande värde: ${optimization['current_value']:.2f}")
    print(f"    Avkastning: {optimization['returns_percent']:.2f}%")
    print(f"    Positioner: {optimization['position_count']}")
    
    if optimization['suggestions']:
        print(f"    Förslag:")
        for suggestion in optimization['suggestions']:
            print(f"      • {suggestion}")
    
    narrative_engine.add_event(
        'portfolio_optimization',
        f'Portfölj optimerad',
        {'value': optimization['current_value'], 'returns': optimization['returns_percent']}
    )
    
    # ========================================================================
    # STEG 9: SIMULERA TRADE-UTFALL OCH SJÄLVKRITIK
    # ========================================================================
    print("\n--- STEG 9: Simulera trade-utfall och självkritik ---")
    
    import random
    for symbol in top_symbols[:2]:
        # Simulera trade outcome
        trade_success = random.choice([True, False])
        pnl = random.uniform(-500, 1000) if trade_success else random.uniform(-1000, -100)
        
        outcome = {
            'symbol': symbol,
            'success': trade_success,
            'pnl': pnl,
            'duration': random.randint(1, 10)
        }
        
        print(f"\n  Trade-utfall för {symbol}:")
        print(f"    Framgång: {'Ja' if trade_success else 'Nej'}")
        print(f"    PnL: ${pnl:.2f}")
        
        # Uppdatera sizing med outcome
        sizing_update = sizing.update_from_outcome(symbol, outcome)
        if sizing_update.get('updated'):
            print(f"    ✓ Sizing uppdaterad: win_rate={sizing_update['win_rate']:.2%}")
        
        # Analysera med self-critique
        decision_data = {
            'symbol': symbol,
            'confidence': consensus['average_confidence'],
            'decision_type': consensus['consensus'],
            'entry_reason': 'Konsensus från agenter'
        }
        
        review = self_critique.analyze_decision(decision_data, outcome)
        print(f"    Self-critique: {'Korrekt' if review['was_correct'] else 'Felaktig'}")
        
        # Post-mortem analys
        trade_data = {
            **outcome,
            'confidence': decision_data['confidence'],
            'entry_reason': decision_data['entry_reason'],
            'trade_id': f"trade_{symbol}_001"
        }
        
        post_mortem = self_critique.post_mortem(f"trade_{symbol}_001", trade_data)
        if post_mortem.get('lessons_learned'):
            print(f"    Lärdomar:")
            for lesson in post_mortem['lessons_learned'][:2]:
                print(f"      • {lesson}")
        
        narrative_engine.add_event(
            'trade_completed',
            f'Trade i {symbol} avslutad: {"vinst" if trade_success else "förlust"}',
            {'pnl': pnl}
        )
    
    # ========================================================================
    # STEG 10: PATTERN RECOGNITION OCH MÖNSTERANALYS
    # ========================================================================
    print("\n--- STEG 10: Pattern recognition och mönsteranalys ---")
    
    # Identifiera felmönster
    error_patterns = self_critique.identify_patterns()
    print(f"\n  Felmönster identifierade: {error_patterns['pattern_count']}")
    if error_patterns['patterns_found']:
        for pattern in error_patterns['patterns_found'][:3]:
            print(f"    • {pattern['type']}: {pattern['description']} "
                  f"({pattern['occurrences']} ggr)")
    
    # Få förbättringsförslag
    suggestions = self_critique.get_improvement_suggestions()
    if suggestions:
        print(f"\n  Förbättringsförslag:")
        for suggestion in suggestions:
            print(f"    • {suggestion}")
    
    # Symbol profiles
    print(f"\n  Symbolprofiler:")
    for symbol in top_symbols[:2]:
        profile = symbol_memory.get_symbol_profile(symbol)
        print(f"    {symbol}: {profile.get('total_events', 0)} händelser, "
              f"trend={profile.get('trend', 'unknown')}")
    
    # ========================================================================
    # STEG 11: TIMESPAN RL-TRÄNING
    # ========================================================================
    print("\n--- STEG 11: RL-träning för tidsramar ---")
    
    # Träna RL-modeller för olika tidsramar
    for timeframe in ['15m', '1h']:
        training = timespan_engine.train_rl_model(timeframe, episodes=50)
        print(f"  ✓ RL-modell tränad för {timeframe}: "
              f"avg_reward={training['metrics']['average_reward']:.3f}")
    
    # ========================================================================
    # STEG 12: MUTATION OCH GENEALOGIANALYS
    # ========================================================================
    print("\n--- STEG 12: Mutation och genealogianalys ---")
    
    # Jämför generationer
    if evolution.generation > 0:
        comparison = mutation_tracker.compare_generations(0, evolution.generation)
        print(f"\n  Generationsjämförelse (Gen 0 vs Gen {evolution.generation}):")
        print(f"    Gen 0 prestanda: {comparison['gen1_avg_performance']:.3f}")
        print(f"    Gen {evolution.generation} prestanda: {comparison['gen2_avg_performance']:.3f}")
        print(f"    Förbättring: {comparison['improvement_percent']:.2f}%")
    
    # Bästa släktlinje
    best_lineage = mutation_tracker.get_best_lineage()
    if best_lineage:
        print(f"\n  Bästa släktlinje: {' → '.join(best_lineage)}")
    
    # ========================================================================
    # STEG 13: NARRATIV OCH KAUSAL ANALYS
    # ========================================================================
    print("\n--- STEG 13: Narrativ och kausal analys ---")
    
    # Skapa narrativ
    narrative_engine.create_narrative('trading_session_1', 'Trading Session 1')
    
    # Bygg kausal kedja
    causal_chain = narrative_engine.build_causal_chain(
        'Systemet startar marknadsanalys',
        'Trade i NVDA avslutad'
    )
    print(f"\n  Kausal kedja byggd: {len(causal_chain)} steg")
    
    # Generera sammanfattning
    summary = narrative_engine.generate_summary(timeframe='session', max_events=15)
    print(f"\n  Systemberättelse:")
    for line in summary.split('\n')[:10]:  # Visa första 10 rader
        print(f"    {line}")
    
    # ========================================================================
    # STEG 14: SLUTSTATISTIK FRÅN ALLA MODULER
    # ========================================================================
    print("\n--- STEG 14: Slutstatistik från alla moduler ---")
    
    stats = {
        'DataStream': data_stream.get_stats() if hasattr(data_stream, 'get_stats') else {},
        'TrendingPool': trending_pool.get_pool_stats(),
        'DecisionCore': decision_core.get_stats(),
        'VoteEngine': vote_engine.get_stats(),
        'Fusion': fusion.get_stats(),
        'Sizing': sizing.get_stats(),
        'TimespanEngine': timespan_engine.get_stats(),
        'PortfolioEngine': portfolio_engine.get_stats(),
        'Evolution': evolution.get_stats(),
        'SelfCritique': self_critique.get_stats(),
        'SymbolMemory': symbol_memory.get_stats(),
        'NarrativeEngine': narrative_engine.get_stats(),
        'MutationTracker': mutation_tracker.get_stats()
    }
    
    print("\n  Modulstatistik:")
    for module_name, module_stats in stats.items():
        print(f"\n  {module_name}:")
        for key, value in list(module_stats.items())[:4]:  # Visa max 4 stats per modul
            print(f"    {key}: {value}")
    
    # ========================================================================
    # SLUTSATS
    # ========================================================================
    print("\n" + "="*80)
    print("SYSTEMFLÖDESTEST SLUTFÖRT MED FRAMGÅNG! ✓")
    print("="*80)
    print(f"\nAlla 13 moduler testade och integrerade:")
    print(f"  • Marknadsdata inhämtad och analyserad")
    print(f"  • Agentbeslut samlade och konsensus analyserad")
    print(f"  • Signaler validerade över tidsramar")
    print(f"  • Position sizing beräknad med Kelly criterion")
    print(f"  • Portföljer skapade och optimerade")
    print(f"  • Strategier evolverade via genetiska algoritmer")
    print(f"  • Självkritik och förbättringsförslag genererade")
    print(f"  • Mönster identifierade i symbolbeteende")
    print(f"  • RL-modeller tränade för tidsramar")
    print(f"  • Mutationer spårade och analyserade")
    print(f"  • Systemberättelse och kausal analys byggd")
    print("\n" + "="*80 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        test_system_flow()
    except Exception as e:
        logger.error(f"Test misslyckades: {e}", exc_info=True)
        raise
