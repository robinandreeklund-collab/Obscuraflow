"""
PortfolioComparator - Huvudklass för portföljjämförelse

Denna klass ansvarar för:
- Jämförelse mellan portföljer
- Prestanda-ranking
- Benchmarking
- Portföljrekommendationer
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime


logger = logging.getLogger(__name__)


class PortfolioComparator:
    """
    PortfolioComparator hanterar portföljjämförelse.
    
    Attributes:
        portfolios (Dict): Portföljer att jämföra
        benchmarks (Dict): Benchmark-portföljer
    """
    
    def __init__(self):
        """
        Initierar PortfolioComparator.
        """
        self.portfolios: Dict[str, Dict[str, Any]] = {}
        self.benchmarks: Dict[str, Dict[str, Any]] = {}
        self.comparison_history: List[Dict[str, Any]] = []
        logger.info("PortfolioComparator initierad")
    
    def add_portfolio(self, portfolio_id: str, portfolio_data: Dict[str, Any]) -> bool:
        """
        Lägger till portfölj för jämförelse.
        
        Args:
            portfolio_id: Portfölj-ID
            portfolio_data: Portföljdata (positions, performance, etc.)
        
        Returns:
            True om portföljen lades till
        """
        self.portfolios[portfolio_id] = portfolio_data
        logger.info(f"Lade till portfölj {portfolio_id} för jämförelse")
        return True
    
    def add_benchmark(self, benchmark_id: str, benchmark_data: Dict[str, Any]) -> bool:
        """
        Lägger till benchmark för jämförelse.
        
        Args:
            benchmark_id: Benchmark-ID
            benchmark_data: Benchmark-data
        
        Returns:
            True om benchmark lades till
        """
        self.benchmarks[benchmark_id] = benchmark_data
        logger.info(f"Lade till benchmark {benchmark_id}")
        return True
    
    def compare_portfolios(self, portfolio_ids: List[str]) -> Dict[str, Any]:
        """
        Jämför flera portföljer.
        
        Args:
            portfolio_ids: Lista med portfölj-ID att jämföra
        
        Returns:
            Dict med jämförelseresultat
        """
        if not all(pid in self.portfolios for pid in portfolio_ids):
            logger.error("En eller flera portföljer finns inte")
            return {}
        
        # Kodstub - implementeras senare med faktisk jämförelse
        comparison = {
            'portfolios': portfolio_ids,
            'metrics': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Beräkna grundläggande metrik
        for pid in portfolio_ids:
            portfolio = self.portfolios[pid]
            comparison['metrics'][pid] = {
                'return': portfolio.get('return', 0.0),
                'risk': portfolio.get('risk', 0.0),
                'sharpe': portfolio.get('sharpe', 0.0)
            }
        
        self.comparison_history.append(comparison)
        logger.info(f"Jämförde {len(portfolio_ids)} portföljer")
        return comparison
    
    def rank_portfolios(self, metric: str = 'sharpe') -> List[Tuple[str, float]]:
        """
        Rankar portföljer baserat på en metrik.
        
        Args:
            metric: Metrik att ranka på ('return', 'sharpe', 'risk')
        
        Returns:
            Lista med (portfolio_id, metric_value) sorterad
        """
        rankings = []
        
        for pid, portfolio in self.portfolios.items():
            value = portfolio.get(metric, 0.0)
            rankings.append((pid, value))
        
        # Sortera - högre är bättre utom för risk
        reverse = metric != 'risk'
        rankings.sort(key=lambda x: x[1], reverse=reverse)
        
        logger.info(f"Rankade {len(rankings)} portföljer baserat på {metric}")
        return rankings
    
    def compare_to_benchmark(self, portfolio_id: str, benchmark_id: str) -> Dict[str, Any]:
        """
        Jämför portfölj mot benchmark.
        
        Args:
            portfolio_id: Portfölj-ID
            benchmark_id: Benchmark-ID
        
        Returns:
            Dict med jämförelse
        """
        if portfolio_id not in self.portfolios:
            logger.error(f"Portfölj {portfolio_id} finns inte")
            return {}
        
        if benchmark_id not in self.benchmarks:
            logger.error(f"Benchmark {benchmark_id} finns inte")
            return {}
        
        portfolio = self.portfolios[portfolio_id]
        benchmark = self.benchmarks[benchmark_id]
        
        # Kodstub
        comparison = {
            'portfolio': portfolio_id,
            'benchmark': benchmark_id,
            'alpha': portfolio.get('return', 0.0) - benchmark.get('return', 0.0),
            'relative_performance': portfolio.get('return', 0.0) / max(benchmark.get('return', 1.0), 0.01),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Jämförde {portfolio_id} mot benchmark {benchmark_id}")
        return comparison
    
    def get_best_portfolio(self, metric: str = 'sharpe') -> Optional[str]:
        """
        Hämtar bästa portföljen baserat på metrik.
        
        Args:
            metric: Metrik att optimera för
        
        Returns:
            Portfolio-ID eller None
        """
        rankings = self.rank_portfolios(metric)
        if rankings:
            return rankings[0][0]
        return None
    
    def create_meta_portfolio(self, portfolio_ids: List[str], weights: List[float]) -> Dict[str, Any]:
        """
        Skapar meta-portfölj från flera portföljer.
        
        Args:
            portfolio_ids: Lista med portfölj-ID
            weights: Vikter för varje portfölj (måste summera till 1.0)
        
        Returns:
            Dict med meta-portfölj
        """
        if len(portfolio_ids) != len(weights):
            logger.error("Antal portföljer och vikter måste matcha")
            return {}
        
        if abs(sum(weights) - 1.0) > 0.01:
            logger.error("Vikter måste summera till 1.0")
            return {}
        
        # Kodstub
        meta_portfolio = {
            'type': 'meta',
            'components': list(zip(portfolio_ids, weights)),
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"Skapade meta-portfölj från {len(portfolio_ids)} portföljer")
        return meta_portfolio
    
    def get_recommendations(self, min_sharpe: float = 1.0) -> List[str]:
        """
        Hämtar portföljrekommendationer baserat på kriterier.
        
        Args:
            min_sharpe: Minimum Sharpe ratio
        
        Returns:
            Lista med rekommenderade portfölj-ID
        """
        recommendations = []
        
        for pid, portfolio in self.portfolios.items():
            sharpe = portfolio.get('sharpe', 0.0)
            if sharpe >= min_sharpe:
                recommendations.append(pid)
        
        logger.info(f"Hittade {len(recommendations)} rekommenderade portföljer")
        return recommendations
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för portfolio comparator.
        
        Returns:
            Dict med statistik
        """
        return {
            'total_portfolios': len(self.portfolios),
            'total_benchmarks': len(self.benchmarks),
            'comparisons_made': len(self.comparison_history)
        }
