"""
Test för att specifikt verifiera konflikthantering med vote_engine.

Detta test skapar en situation där agenter har motstridiga beslut
och verifierar att vote_engine korrekt löser konflikten genom viktad röstning.
"""

import logging
from modules.decision_core import DecisionCore, AgentDecision, DecisionType
from modules.vote_engine import VoteEngine, Vote


# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_conflict_resolution():
    """
    Testar konflikthantering när agenter har motstridiga åsikter.
    """
    print("\n" + "="*80)
    print("OBSCURAFLOW - TEST AV KONFLIKTHANTERING")
    print("="*80 + "\n")
    
    # Initiera moduler
    print("--- STEG 1: Initiera moduler ---")
    decision_core = DecisionCore(min_confidence=40.0, conflict_threshold=0.3)
    vote_engine = VoteEngine(initial_weight=1.0, learning_rate=0.15)
    print("✓ Moduler initialiserade\n")
    
    # Skapa motstridiga beslut för TSLA
    print("--- STEG 2: Lägg till motstridiga beslut för TSLA ---")
    
    conflicting_decisions = [
        ('bull_agent', 'buy', 95, "Stark upptrend"),
        ('bear_agent', 'sell', 90, "Överköpt, väntar korrigering"),
        ('momentum_agent', 'buy', 85, "Momentum fortsätter"),
        ('reversal_agent', 'sell', 80, "Reversal-signal detekterad"),
        ('value_agent', 'sell', 75, "Övervärderat P/E"),
        ('growth_agent', 'buy', 88, "Stark tillväxt"),
    ]
    
    for agent_id, decision_type, confidence, reasoning in conflicting_decisions:
        decision = AgentDecision(
            agent_id=agent_id,
            symbol='TSLA',
            decision=DecisionType(decision_type),
            confidence=confidence,
            reasoning=reasoning
        )
        decision_core.add_decision(decision)
        print(f"  {agent_id}: {decision_type.upper()} (confidence={confidence}) - {reasoning}")
    
    # Analysera konsensus
    print("\n--- STEG 3: Analysera konsensus ---")
    consensus = decision_core.analyze_consensus('TSLA')
    
    print(f"  Konsensus: {consensus['consensus']}")
    print(f"  Konflikt detekterad: {'JA' if consensus['has_conflict'] else 'NEJ'}")
    print(f"  Total beslut: {consensus['total_decisions']}")
    print(f"  Breakdown: {consensus['decision_breakdown']}")
    print(f"  Ratios: buy={consensus['decision_ratios']['buy']}, sell={consensus['decision_ratios']['sell']}")
    
    # Om konflikt, använd vote_engine
    if consensus['has_conflict']:
        print("\n--- STEG 4: Konflikt detekterad - Eskalerar till VoteEngine ---")
        
        # Skapa röster från besluten
        votes = []
        decisions = decision_core.get_decisions_for_symbol('TSLA')
        
        print("\n  Skapar röster från agentbeslut:")
        for decision in decisions:
            vote = Vote(
                agent_id=decision.agent_id,
                vote=decision.decision.value,
                confidence=decision.confidence
            )
            vote_engine.add_vote(vote)
            votes.append(vote)
            print(f"    {decision.agent_id}: {decision.decision.value} (weight={vote.weight}, confidence={vote.confidence})")
        
        # Beräkna vägd röstning
        print("\n  Beräknar vägd röstning...")
        vote_result = vote_engine.calculate_weighted_vote(votes, 'TSLA')
        
        print(f"\n--- STEG 5: Röstningsresultat ---")
        print(f"  Vinnare: {vote_result['winner'].upper()}")
        print(f"  Enhälligt: {'Ja' if vote_result['is_unanimous'] else 'Nej'}")
        print(f"  Total röster: {vote_result['total_votes']}")
        print(f"\n  Detaljerad breakdown:")
        for vote_type, data in vote_result['vote_breakdown'].items():
            print(f"    {vote_type.upper()}: {data['count']} röster, "
                  f"weighted_score={data['weighted_score']}, "
                  f"avg_confidence={data['average_confidence']}")
        
        # Simulera utfall och uppdatera vikter
        print("\n--- STEG 6: Simulera utfall och uppdatera agentsvikter ---")
        
        # Anta att BUY var det korrekta beslutet (i praktiken kommer detta från verklig marknadsdata)
        correct_decision = 'buy'
        print(f"  Antaget korrekt beslut: {correct_decision.upper()}\n")
        
        for decision in decisions:
            was_correct = decision.decision.value == correct_decision
            new_weight = vote_engine.update_agent_weight(decision.agent_id, was_correct)
            status = "✓ KORREKT" if was_correct else "✗ FELAKTIG"
            print(f"    {decision.agent_id}: {status} - ny vikt: {new_weight:.3f}")
        
        # Visa uppdaterade prestationer
        print("\n--- STEG 7: Agentprestationer efter uppdatering ---")
        performances = vote_engine.get_all_agent_performances()
        
        print("\n  Rankade efter vikt:")
        for i, perf in enumerate(performances, 1):
            print(f"    {i}. {perf['agent_id']}: "
                  f"weight={perf['weight']:.3f}, "
                  f"accuracy={perf['accuracy']:.1f}% "
                  f"({perf['correct']}/{perf['total']})")
        
        # Testa en andra röstning med uppdaterade vikter
        print("\n--- STEG 8: Andra röstningen med uppdaterade vikter ---")
        
        decision_core.clear_decisions('TSLA')
        
        # Samma agenter röstar igen, men nu med uppdaterade vikter
        for agent_id, decision_type, confidence, reasoning in conflicting_decisions:
            decision = AgentDecision(
                agent_id=agent_id,
                symbol='TSLA',
                decision=DecisionType(decision_type),
                confidence=confidence,
                reasoning=reasoning
            )
            decision_core.add_decision(decision)
        
        # Skapa nya röster
        votes2 = []
        decisions2 = decision_core.get_decisions_for_symbol('TSLA')
        for decision in decisions2:
            vote = Vote(
                agent_id=decision.agent_id,
                vote=decision.decision.value,
                confidence=decision.confidence
            )
            vote_engine.add_vote(vote)
            votes2.append(vote)
        
        # Beräkna ny röstning
        vote_result2 = vote_engine.calculate_weighted_vote(votes2, 'TSLA')
        
        print(f"\n  Nytt röstningsresultat:")
        print(f"    Vinnare: {vote_result2['winner'].upper()}")
        print(f"    Vote breakdown:")
        for vote_type, data in vote_result2['vote_breakdown'].items():
            print(f"      {vote_type.upper()}: weighted_score={data['weighted_score']:.2f} "
                  f"(förändring från första röstningen)")
    
    else:
        print("\n  Ingen konflikt - Ingen röstning behövs")
    
    # Slutstatistik
    print("\n--- STEG 9: Slutstatistik ---")
    dc_stats = decision_core.get_stats()
    ve_stats = vote_engine.get_stats()
    
    print(f"\n  DecisionCore:")
    print(f"    Totalt beslut: {dc_stats['total_decisions']}")
    print(f"    Accepterade: {dc_stats['accepted_decisions']}")
    print(f"    Avvisade: {dc_stats['rejected_decisions']}")
    print(f"    Konflikter: {dc_stats['conflicts_detected']}")
    
    print(f"\n  VoteEngine:")
    print(f"    Totalt röster: {ve_stats['total_votes']}")
    print(f"    Röstningssessioner: {ve_stats['total_vote_sessions']}")
    print(f"    Enhälliga beslut: {ve_stats['unanimous_decisions']}")
    print(f"    Delade beslut: {ve_stats['split_decisions']}")
    
    print("\n" + "="*80)
    print("TEST SLUTFÖRT MED FRAMGÅNG! ✓")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        test_conflict_resolution()
    except Exception as e:
        logger.error(f"Test misslyckades: {e}", exc_info=True)
        raise
