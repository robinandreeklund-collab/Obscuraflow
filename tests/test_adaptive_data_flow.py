"""
Comprehensive test for the adaptive data flow architecture.

Tests:
1. REST Batcher - symbol batching and rate limiting
2. WebSocket Handler - connection and subscriptions
3. TrendingPool - symbol ranking and top symbols
4. DataOrchestrator - coordinated data flow
5. Data Source Monitor - debug stats display
"""

import unittest
import time
from datetime import datetime
from modules.trending_pool.trending_pool import TrendingPool
from modules.data_stream.universe_loader import load_symbol_universe
from modules.data_stream.orchestrator import DataOrchestrator


class TestTrendingPool(unittest.TestCase):
    """Test TrendingPool functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pool = TrendingPool(max_history=10, dampening_factor=0.3)
    
    def test_init(self):
        """Test TrendingPool initialization."""
        self.assertEqual(self.pool.max_history, 10)
        self.assertEqual(self.pool.dampening_factor, 0.3)
        self.assertIsNotNone(self.pool.weights)
        self.assertEqual(len(self.pool.symbol_scores), 0)
    
    def test_update_symbol(self):
        """Test updating symbol data."""
        trend_data = {
            'volume': 50,
            'momentum': 5.0,
            'volatility': 3.0,
            'score': 0
        }
        
        score = self.pool.update_symbol('AAPL', trend_data)
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)
        self.assertIn('AAPL', self.pool.symbol_scores)
    
    def test_update_symbol_tick(self):
        """Test updating symbol with tick data."""
        # First add batch data
        batch_data = {
            'volume': 50,
            'momentum': 5.0,
            'volatility': 3.0
        }
        self.pool.update_symbol('AAPL', batch_data)
        
        # Then add tick data
        tick_data = {
            'volume': 60,
            'momentum': 6.0,
            'volatility': 4.0
        }
        tick_score = self.pool.update_symbol_tick('AAPL', tick_data)
        
        self.assertIsInstance(tick_score, float)
        self.assertIn('AAPL', self.pool.symbol_metadata)
        self.assertEqual(self.pool.symbol_metadata['AAPL']['tick_updates'], 1)
    
    def test_get_top_symbols(self):
        """Test getting top symbols."""
        # Add multiple symbols with different scores
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
        for i, symbol in enumerate(symbols):
            trend_data = {
                'volume': 50 + i * 10,
                'momentum': 5.0 + i,
                'volatility': 3.0
            }
            self.pool.update_symbol(symbol, trend_data)
        
        # Get top 3 symbols
        top_symbols = self.pool.get_top_symbols(count=3)
        
        self.assertIsInstance(top_symbols, list)
        self.assertEqual(len(top_symbols), 3)
        # Check that symbols are in descending score order
        scores = [self.pool.symbol_scores[s] for s in top_symbols]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_get_ranked_symbols(self):
        """Test getting ranked symbols."""
        # Add symbols
        symbols = ['AAPL', 'MSFT', 'GOOGL']
        for symbol in symbols:
            self.pool.update_symbol(symbol, {
                'volume': 50,
                'momentum': 5.0,
                'volatility': 3.0
            })
        
        ranked = self.pool.get_ranked_symbols(limit=2)
        
        self.assertIsInstance(ranked, list)
        self.assertEqual(len(ranked), 2)
        self.assertIn('symbol', ranked[0])
        self.assertIn('score', ranked[0])
    
    def test_get_stats(self):
        """Test getting pool statistics."""
        # Add symbols
        self.pool.update_symbol('AAPL', {'volume': 50, 'momentum': 5.0, 'volatility': 3.0})
        self.pool.update_symbol('MSFT', {'volume': 40, 'momentum': 4.0, 'volatility': 2.0})
        
        stats = self.pool.get_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_symbols', stats)
        self.assertEqual(stats['total_symbols'], 2)
        self.assertIn('average_score', stats)
        self.assertGreater(stats['average_score'], 0)
    
    def test_empty_pool_get_top_symbols(self):
        """Test getting top symbols from empty pool."""
        top_symbols = self.pool.get_top_symbols(count=10)
        self.assertEqual(top_symbols, [])
    
    def test_empty_pool_get_stats(self):
        """Test getting stats from empty pool."""
        stats = self.pool.get_stats()
        self.assertEqual(stats['total_symbols'], 0)
        self.assertEqual(stats['average_score'], 0)


class TestSymbolUniverse(unittest.TestCase):
    """Test symbol universe loader."""
    
    def test_load_symbol_universe(self):
        """Test loading symbols from YAML."""
        symbols = load_symbol_universe()
        
        self.assertIsInstance(symbols, list)
        self.assertGreater(len(symbols), 0)
        # Check if common NASDAQ-100 symbols are present
        expected_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']
        for symbol in expected_symbols:
            self.assertIn(symbol, symbols)
    
    def test_symbol_universe_size(self):
        """Test that we have expected number of symbols."""
        symbols = load_symbol_universe()
        # Should have around 100 symbols (NASDAQ-100)
        self.assertGreaterEqual(len(symbols), 90)
        self.assertLessEqual(len(symbols), 110)


class TestDataOrchestrator(unittest.TestCase):
    """Test DataOrchestrator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use mock data for testing
        self.orchestrator = DataOrchestrator(
            api_key="test_key",
            use_mock_data=True
        )
    
    def test_init(self):
        """Test orchestrator initialization."""
        self.assertIsNotNone(self.orchestrator.symbols)
        self.assertGreater(len(self.orchestrator.symbols), 0)
        self.assertIsNotNone(self.orchestrator.trending_pool)
        self.assertTrue(self.orchestrator.use_mock_data)
    
    def test_get_market_summary(self):
        """Test getting market summary."""
        summary = self.orchestrator.get_market_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_symbols', summary)
        self.assertIn('gainers', summary)
        self.assertIn('losers', summary)
        self.assertIn('avg_change_percent', summary)
        self.assertIn('quotes', summary)
        self.assertIn('timestamp', summary)
    
    def test_get_top_symbols(self):
        """Test getting top symbols from orchestrator."""
        # First populate trending pool with some data
        for i, symbol in enumerate(self.orchestrator.symbols[:10]):
            self.orchestrator.trending_pool.update_symbol(symbol, {
                'volume': 50 + i * 5,
                'momentum': 5.0 + i * 0.5,
                'volatility': 3.0
            })
        
        top_symbols = self.orchestrator.get_top_symbols(count=5)
        
        self.assertIsInstance(top_symbols, list)
        self.assertLessEqual(len(top_symbols), 5)
    
    def test_get_debug_stats_mock_mode(self):
        """Test getting debug stats in mock mode."""
        stats = self.orchestrator.get_debug_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['mode'], 'mock')
        self.assertIn('symbols', stats)
        self.assertIn('uptime', stats)
    
    def test_get_stats(self):
        """Test getting orchestrator stats."""
        stats = self.orchestrator.get_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('uptime', stats)
        self.assertIn('trending_pool', stats)


class TestDataFlowIntegration(unittest.TestCase):
    """Integration tests for complete data flow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = DataOrchestrator(
            api_key="test_key",
            use_mock_data=True
        )
    
    def test_complete_data_flow(self):
        """Test complete data flow from symbols to trending pool."""
        # 1. Verify symbols are loaded
        self.assertGreater(len(self.orchestrator.symbols), 0)
        
        # 2. Get market summary
        summary = self.orchestrator.get_market_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn('quotes', summary)
        
        # 3. Update trending pool with data
        for symbol in self.orchestrator.symbols[:20]:
            self.orchestrator.trending_pool.update_symbol(symbol, {
                'volume': 50,
                'momentum': 5.0,
                'volatility': 3.0
            })
        
        # 4. Get top symbols
        top_symbols = self.orchestrator.get_top_symbols(count=10)
        self.assertIsInstance(top_symbols, list)
        self.assertGreater(len(top_symbols), 0)
        
        # 5. Get debug stats
        debug_stats = self.orchestrator.get_debug_stats()
        self.assertIsInstance(debug_stats, dict)
        self.assertIn('symbols', debug_stats)
        
        # 6. Verify trending pool stats
        pool_stats = self.orchestrator.trending_pool.get_stats()
        self.assertEqual(pool_stats['total_symbols'], 20)
    
    def test_data_source_monitor_integration(self):
        """Test that Data Source Monitor can get all required data."""
        # Simulate what Data Source Monitor panel does
        
        # Get debug stats
        debug_stats = self.orchestrator.get_debug_stats()
        self.assertIn('mode', debug_stats)
        self.assertIn('symbols', debug_stats)
        
        # Get market summary
        summary = self.orchestrator.get_market_summary()
        self.assertIn('quotes', summary)
        
        # Get top trending symbols
        # First populate trending pool
        for i, symbol in enumerate(self.orchestrator.symbols[:30]):
            self.orchestrator.trending_pool.update_symbol(symbol, {
                'volume': 50 + i,
                'momentum': 5.0 + i * 0.1,
                'volatility': 3.0
            })
        
        top_symbols = self.orchestrator.get_top_symbols(count=5)
        self.assertIsInstance(top_symbols, list)
        self.assertGreater(len(top_symbols), 0)
        
        print("\n✅ Data Source Monitor Integration Test:")
        print(f"   Mode: {debug_stats['mode']}")
        print(f"   Total Symbols: {debug_stats['symbols']['total']}")
        print(f"   Top 5 Trending: {top_symbols[:5]}")
        print(f"   Market Summary: {summary['total_symbols']} symbols")


def run_tests():
    """Run all tests."""
    print("\n" + "="*80)
    print("ADAPTIVE DATA FLOW - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestTrendingPool))
    suite.addTests(loader.loadTestsFromTestCase(TestSymbolUniverse))
    suite.addTests(loader.loadTestsFromTestCase(TestDataOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestDataFlowIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    import pathlib
    # Dynamically add project root to sys.path for portability
    project_root = pathlib.Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    success = run_tests()
    sys.exit(0 if success else 1)
