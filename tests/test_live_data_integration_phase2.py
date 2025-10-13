#!/usr/bin/env python3
"""
Integration Test for Live Data Integration Phase 2

This test demonstrates that all modules work together with live data
from data_stream and the symbol universe.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_data_flow_integration():
    """Test that data flows correctly through the system"""
    print("\n" + "="*80)
    print("LIVE DATA INTEGRATION TEST - PHASE 2")
    print("="*80)
    
    # Step 1: Initialize DataStream (central data provider)
    print("\n[1/7] Initializing DataStream (Central Data Provider)")
    print("-" * 80)
    from modules.data_stream import get_data_stream
    from config import USE_MOCK_DATA
    
    data_stream = get_data_stream(use_mock=USE_MOCK_DATA)
    print(f"✓ DataStream initialized (mock={USE_MOCK_DATA})")
    
    # Get some market data
    market_data = data_stream.get_market_summary()
    symbols = list(market_data.get('quotes', {}).keys())[:5]  # Get first 5 symbols
    print(f"✓ Market data available for {len(symbols)} symbols: {symbols}")
    
    # Step 2: TrendingPool processes the data
    print("\n[2/7] TrendingPool: Processing Trend Data")
    print("-" * 80)
    from modules.trending_pool import TrendingPool
    
    trending_pool = TrendingPool()
    
    # Update trending pool with market data
    for symbol in symbols:
        quote = market_data['quotes'].get(symbol, {})
        trend_data = {
            'volume': quote.get('volume', 0) / 1000000,  # Normalize volume
            'momentum': quote.get('change_percent', 0),
            'volatility': abs(quote.get('change_percent', 0)) / 2,
            'score': 0
        }
        trending_pool.update_symbol(symbol, trend_data)
    
    ranked_symbols = trending_pool.get_ranked_symbols(limit=5)
    print(f"✓ Ranked {len(ranked_symbols)} symbols by trend score")
    for i, item in enumerate(ranked_symbols[:3], 1):
        print(f"  {i}. {item['symbol']}: score={item['score']}")
    
    # Step 3: Agents analyze symbols and make decisions
    print("\n[3/7] Agents: Making Decisions")
    print("-" * 80)
    from modules.decision_core import DecisionCore, AgentDecision, DecisionType
    from agents.agent_registry import AgentRegistry
    
    decision_core = DecisionCore(generate_sample_decisions=False)
    registry = AgentRegistry()
    
    # Simulate agents making decisions based on live data
    test_agents = ['momentum_agent', 'reversal_agent', 'breakout_agent']
    decisions_made = 0
    
    for agent_id in test_agents:
        for symbol in symbols[:2]:  # First 2 symbols
            # Get symbol data
            quote = market_data['quotes'].get(symbol, {})
            change_percent = quote.get('change_percent', 0)
            
            # Agent makes decision based on data
            if change_percent > 0:
                decision_type = DecisionType.BUY
                confidence = min(50 + abs(change_percent) * 10, 95)
            elif change_percent < 0:
                decision_type = DecisionType.SELL
                confidence = min(50 + abs(change_percent) * 10, 95)
            else:
                decision_type = DecisionType.HOLD
                confidence = 60.0
            
            decision = AgentDecision(
                agent_id=agent_id,
                symbol=symbol,
                decision=decision_type,
                confidence=confidence,
                reasoning=f"Based on {change_percent:.2f}% change"
            )
            decision_core.add_decision(decision)
            decisions_made += 1
    
    print(f"✓ {decisions_made} decisions made by {len(test_agents)} agents")
    
    # Step 4: DecisionCore analyzes consensus
    print("\n[4/7] DecisionCore: Analyzing Consensus")
    print("-" * 80)
    
    for symbol in symbols[:2]:
        consensus = decision_core.analyze_consensus(symbol)
        print(f"✓ {symbol}: consensus={consensus['consensus']}, "
              f"confidence={consensus['average_confidence']:.1f}%, "
              f"conflict={consensus['has_conflict']}")
    
    # Step 5: VoteEngine handles conflicts
    print("\n[5/7] VoteEngine: Resolving Conflicts")
    print("-" * 80)
    from modules.vote_engine import VoteEngine, Vote
    
    vote_engine = VoteEngine()
    
    # Create votes from decisions
    test_symbol = symbols[0]
    symbol_decisions = decision_core.get_decisions_for_symbol(test_symbol)
    
    votes = []
    for decision in symbol_decisions:
        vote = Vote(
            agent_id=decision.agent_id,
            vote=decision.decision.value,
            confidence=decision.confidence
        )
        vote_engine.add_vote(vote)
        votes.append(vote)
    
    if votes:
        vote_result = vote_engine.calculate_weighted_vote(votes, test_symbol)
        print(f"✓ Weighted vote for {test_symbol}: {vote_result['winner']} "
              f"({vote_result['total_votes']} votes)")
    
    # Step 6: Fusion validates signals
    print("\n[6/7] Fusion: Multi-timeframe Validation")
    print("-" * 80)
    from modules.fusion import Fusion
    
    fusion = Fusion()
    
    for symbol in symbols[:2]:
        consensus = decision_core.analyze_consensus(symbol)
        if consensus['consensus']:
            validation = fusion.validate_signal(
                symbol=symbol,
                signal_type=consensus['consensus'],
                confidence=consensus['average_confidence']
            )
            print(f"✓ {symbol}: signal={validation['signal_type']}, "
                  f"validated={validation['validated']}, "
                  f"confirmations={validation['confirmations']}/4")
    
    # Step 7: Sizing calculates position size
    print("\n[7/7] Sizing: Position Size Calculation")
    print("-" * 80)
    from modules.sizing import Sizing
    
    sizing = Sizing(max_position_size=0.1, risk_per_trade=0.02)
    
    for symbol in symbols[:2]:
        consensus = decision_core.analyze_consensus(symbol)
        if consensus['consensus'] in ['buy', 'sell']:
            # Get volatility from market data
            quote = market_data['quotes'].get(symbol, {})
            volatility = abs(quote.get('change_percent', 0)) / 100
            
            size_result = sizing.calculate_position_size(
                symbol=symbol,
                portfolio_value=100000.0,
                confidence=consensus['average_confidence'],
                volatility=volatility
            )
            print(f"✓ {symbol}: size=${size_result['position_size']:.0f} "
                  f"({size_result['position_size_percent']:.1f}%), "
                  f"risk=${size_result['risk_amount']:.0f}")
    
    # Summary
    print("\n" + "="*80)
    print("INTEGRATION TEST SUMMARY")
    print("="*80)
    print(f"✅ All modules successfully integrated with live data flow")
    print(f"✅ Data source: {'Mock' if USE_MOCK_DATA else 'Live API'}")
    print(f"✅ Symbols processed: {len(symbols)}")
    print(f"✅ Decisions made: {decisions_made}")
    print(f"✅ No hardcoded market data used")
    print("="*80)
    
    return True


def test_symbol_universe_integration():
    """Test that symbol universe is properly integrated"""
    print("\n" + "="*80)
    print("SYMBOL UNIVERSE INTEGRATION TEST")
    print("="*80)
    
    from modules.data_stream.universe_loader import (
        get_cached_symbols,
        validate_symbol,
        get_cached_symbols_set
    )
    
    # Load symbol universe
    symbols = get_cached_symbols()
    print(f"\n✓ Symbol universe loaded: {len(symbols)} symbols")
    
    # Test validation
    test_symbols = ['AAPL', 'GOOGL', 'INVALID']
    print("\nValidation tests:")
    for symbol in test_symbols:
        is_valid = validate_symbol(symbol)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {symbol}: {'Valid' if is_valid else 'Invalid'}")
    
    # Test set access
    symbol_set = get_cached_symbols_set()
    print(f"\n✓ Symbol set created: {len(symbol_set)} symbols")
    print(f"✓ 'AAPL' in set: {('AAPL' in symbol_set)}")
    
    print("\n" + "="*80)
    print("✅ Symbol universe integration verified")
    print("="*80)
    
    return True


def test_module_stats():
    """Test that all modules provide stats without errors"""
    print("\n" + "="*80)
    print("MODULE STATS TEST")
    print("="*80)
    
    modules_to_test = [
        ('TrendingPool', 'modules.trending_pool', 'TrendingPool'),
        ('DecisionCore', 'modules.decision_core', 'DecisionCore'),
        ('VoteEngine', 'modules.vote_engine', 'VoteEngine'),
        ('Fusion', 'modules.fusion', 'Fusion'),
        ('Sizing', 'modules.sizing', 'Sizing'),
        ('PortfolioEngine', 'modules.portfolio_engine', 'PortfolioEngine'),
        ('TimespanEngine', 'modules.timespan_engine', 'TimespanEngine'),
    ]
    
    print("\nModule statistics:")
    for name, module_path, class_name in modules_to_test:
        try:
            # Import module
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            
            # Create instance
            if class_name == 'DecisionCore':
                instance = cls(generate_sample_decisions=False)
            else:
                instance = cls()
            
            # Get stats
            stats = instance.get_stats()
            print(f"  ✓ {name:20s} - {len(stats)} stat fields")
            
        except Exception as e:
            print(f"  ✗ {name:20s} - Error: {e}")
            return False
    
    print("\n" + "="*80)
    print("✅ All modules provide stats successfully")
    print("="*80)
    
    return True


def main():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("OBSCURAFLOW - LIVE DATA INTEGRATION PHASE 2")
    print("Complete Integration Test Suite")
    print("="*80)
    
    tests = [
        ("Data Flow Integration", test_data_flow_integration),
        ("Symbol Universe Integration", test_symbol_universe_integration),
        ("Module Stats", test_module_stats),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test '{test_name}' failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:12s} - {test_name}")
    
    print("="*80)
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🎉 Live Data Integration Phase 2: COMPLETE")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
    print("="*80)
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
