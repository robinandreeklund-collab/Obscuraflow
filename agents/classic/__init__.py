"""
Classic Agents - Klassiska tradingagenter

4 klassiska agenter:
- MomentumAgent: Trendföljande
- ReversalAgent: Mean reversion
- BreakoutAgent: Volatility breakout
- HybridAgent: Multi-strategi
"""

from agents.classic.momentum_agent import MomentumAgent
from agents.classic.reversal_agent import ReversalAgent
from agents.classic.breakout_agent import BreakoutAgent
from agents.classic.hybrid_agent import HybridAgent

__all__ = ['MomentumAgent', 'ReversalAgent', 'BreakoutAgent', 'HybridAgent']
