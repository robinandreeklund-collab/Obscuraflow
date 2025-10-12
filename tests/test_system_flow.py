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
- synergy_matrix: Analyserar agentsamverkan och konflikter
- agent_spectrum: Hanterar ontologisk agentförflyttning
- agent_lifecycle: Hanterar agentens livscykel
- metaagentgovernor: Överordnad styrning av agenter
- portfolio_comparator: Jämför portföljer
- risk_mapper: Riskmatris och symbolrisk

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
from modules.synergy_matrix import SynergyMatrix
from modules.agent_spectrum import AgentSpectrum
from modules.agent_lifecycle import AgentLifecycle
from modules.metaagentgovernor import MetaAgentGovernor
from modules.portfolio_comparator import PortfolioComparator
from modules.risk_mapper import RiskMapper


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
    
    # Nya moduler
    synergy_matrix = SynergyMatrix()
    print("✓ SynergyMatrix initialiserad")
    
    agent_spectrum = AgentSpectrum()
    print("✓ AgentSpectrum initialiserad")
    
    agent_lifecycle = AgentLifecycle(retirement_threshold=0.3, max_age=1000)
    print("✓ AgentLifecycle initialiserad")
    
    meta_governor = MetaAgentGovernor(max_active_agents=10)
    print("✓ MetaAgentGovernor initialiserad")
    
    portfolio_comparator = PortfolioComparator()
    print("✓ PortfolioComparator initialiserad")
    
    risk_mapper = RiskMapper(max_portfolio_risk=0.20)
    print("✓ RiskMapper initialiserad")
    
    print(f"\n✓ Alla 19 moduler initialiserade framgångsrikt!")
    
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
    # STEG 14: AGENT LIFECYCLE OCH SYNERGY MATRIX
    # ========================================================================
    print("\n--- STEG 14: Agent lifecycle och synergy matrix ---")
    
    # Skapa agenter med agent lifecycle
    agent_types = [
        ('momentum_agent', 'momentum'),
        ('reversal_agent', 'reversal'),
        ('breakout_agent', 'breakout'),
        ('hybrid_agent', 'hybrid')
    ]
    
    print("\n  Skapar och aktiverar agenter:")
    for agent_id, agent_type in agent_types:
        agent_lifecycle.birth_agent(agent_id, agent_type, {'lookback': 20})
        agent_lifecycle.activate_agent(agent_id)
        print(f"    ✓ {agent_id}: skapad och aktiverad")
    
    # Placera agenter i spektrum
    print("\n  Placerar agenter i ontologiskt spektrum:")
    import random
    for agent_id, _ in agent_types:
        position = [random.uniform(0.2, 0.8) for _ in range(5)]
        agent_spectrum.place_agent(agent_id, position)
        profile = agent_spectrum.get_agent_profile(agent_id)
        print(f"    ✓ {agent_id}: placerad, mobility={profile['mobility_score']:.3f}")
    
    # Registrera interaktioner i synergy matrix
    print("\n  Registrerar agentinteraktioner:")
    for i, (agent1_id, _) in enumerate(agent_types):
        for agent2_id, _ in agent_types[i+1:]:
            # Simulera interaktion
            outcome = random.uniform(-0.5, 0.8)
            interaction_type = 'agreement' if outcome > 0 else 'conflict'
            synergy_matrix.record_interaction(agent1_id, agent2_id, interaction_type, outcome)
    
    synergy = synergy_matrix.get_synergy('momentum_agent', 'breakout_agent')
    print(f"    Synergy momentum-breakout: {synergy:.3f}")
    
    # Hitta bästa partners
    best_partners = synergy_matrix.get_best_partners('momentum_agent', 2)
    if best_partners:
        print(f"    Bästa partners för momentum_agent: {best_partners[0][0]} (score={best_partners[0][1]:.3f})")
    
    # ========================================================================
    # STEG 15: META GOVERNOR OCH PRIORITERING
    # ========================================================================
    print("\n--- STEG 15: Meta governor och agentprioriter ing ---")
    
    # Sätt prioriteringar
    print("\n  Sätter agentprioriteringar:")
    for agent_id, _ in agent_types:
        priority = random.uniform(0.4, 0.9)
        meta_governor.set_priority(agent_id, priority)
        meta_governor.allocate_resources(agent_id, 0.2)
    
    # Ombalansera baserat på performance
    performance_data = {agent_id: random.uniform(0.5, 0.9) for agent_id, _ in agent_types}
    new_priorities = meta_governor.rebalance_priorities(performance_data)
    print(f"    ✓ Ombalanserade {len(new_priorities)} agentprioriteringar")
    
    # Testa konfliktlösning
    conflict_resolution = meta_governor.resolve_conflict(
        ['momentum_agent', 'reversal_agent'],
        {'reason': 'opposing_signals'}
    )
    print(f"    Konfliktlösning: vinnare={conflict_resolution['winner']}")
    
    # Enforce limits
    enforcement = meta_governor.enforce_limits()
    print(f"    Resurser inom gränser: {enforcement['within_limits']}")
    
    # ========================================================================
    # STEG 16: RISK MAPPING OCH PORTFOLIOJÄMFÖRELSE
    # ========================================================================
    print("\n--- STEG 16: Risk mapping och portföljjämförelse ---")
    
    # Beräkna risk för symboler
    print("\n  Beräknar symbolrisk:")
    for symbol in top_symbols[:3]:
        volatility = random.uniform(0.10, 0.25)
        position_size = 5000.0
        risk_data = risk_mapper.calculate_symbol_risk(symbol, volatility, position_size)
        print(f"    {symbol}: risk={risk_data['base_risk']:.4f}, level={risk_data['risk_level']}")
    
    # Sätt korrelationer
    risk_mapper.set_correlation('AAPL', 'MSFT', 0.7)
    risk_mapper.set_correlation('GOOGL', 'META', 0.65)
    
    # Beräkna portföljrisk
    positions = {symbol: 5000.0 for symbol in top_symbols[:3]}
    portfolio_risk = risk_mapper.calculate_portfolio_risk(positions)
    print(f"\n    Portföljrisk: {portfolio_risk['total_risk']:.4f} ({portfolio_risk['risk_pct']:.2f}%)")
    print(f"    Inom gränser: {portfolio_risk['within_limits']}")
    
    # Risk-adjusted sizing
    adjusted = risk_mapper.suggest_risk_adjusted_size('TSLA', 10000.0, 100000.0)
    print(f"    Risk-adjusted size för TSLA: ${adjusted['suggested_size']:.2f} (factor={adjusted.get('adjustment_factor', 1.0):.2f})")
    
    # Jämför portföljer
    print("\n  Jämför portföljer:")
    portfolio_comparator.add_portfolio('main_portfolio', {
        'return': 0.15,
        'risk': 0.12,
        'sharpe': 1.25,
        'win_rate': 0.62
    })
    portfolio_comparator.add_portfolio('aggressive_portfolio', {
        'return': 0.22,
        'risk': 0.18,
        'sharpe': 1.22,
        'win_rate': 0.58
    })
    
    comparison = portfolio_comparator.compare_portfolios(['main_portfolio', 'aggressive_portfolio'])
    print(f"    Vinnare: {comparison.get('overall_winner', 'N/A')}")
    
    # Lägg till benchmark
    portfolio_comparator.add_benchmark('sp500', {'return': 0.10, 'risk': 0.15})
    bench_comp = portfolio_comparator.compare_to_benchmark('main_portfolio', 'sp500')
    print(f"    Alpha vs S&P500: {bench_comp['alpha']:.4f}")
    
    # ========================================================================
    # STEG 17: AGENT SPECTRUM CLUSTERING
    # ========================================================================
    print("\n--- STEG 17: Agent spectrum clustering ---")
    
    # Flytta några agenter i spektrumet
    agent_spectrum.move_agent('momentum_agent', 'risk_tolerance', 0.1)
    agent_spectrum.move_agent('reversal_agent', 'adaptability', -0.15)
    
    # Hitta närmaste agenter
    nearest = agent_spectrum.find_nearest_agents('momentum_agent', 2)
    if nearest:
        print(f"\n  Närmaste agenter till momentum_agent:")
        for agent_id, distance in nearest:
            print(f"    {agent_id}: distance={distance:.3f}")
    
    # Cluster agents
    clusters = agent_spectrum.cluster_agents(max_distance=0.5)
    print(f"\n  Skapade {len(clusters)} agent-clusters")
    for i, cluster in enumerate(clusters):
        print(f"    Cluster {i+1}: {len(cluster)} agenter")
    
    # ========================================================================
    # STEG 18: SLUTSTATISTIK FRÅN ALLA MODULER
    # ========================================================================
    print("\n--- STEG 18: Slutstatistik från alla moduler ---")
    
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
        'MutationTracker': mutation_tracker.get_stats(),
        'SynergyMatrix': synergy_matrix.get_stats(),
        'AgentSpectrum': agent_spectrum.get_stats(),
        'AgentLifecycle': agent_lifecycle.get_stats(),
        'MetaAgentGovernor': meta_governor.get_stats(),
        'PortfolioComparator': portfolio_comparator.get_stats(),
        'RiskMapper': risk_mapper.get_stats()
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
    print(f"\nAlla 19 moduler testade och integrerade:")
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
    print(f"  • Agentsynergi och konflikter analyserade")
    print(f"  • Ontologisk agentförflyttning spårad")
    print(f"  • Agentlivscykel hanterad")
    print(f"  • Meta-governance och prioritering genomförd")
    print(f"  • Portföljer jämförda och benchmarkade")
    print(f"  • Risk mappning och justering utförd")
    print("\n" + "="*80 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        test_system_flow()
    except Exception as e:
        logger.error(f"Test misslyckades: {e}", exc_info=True)
        raise
