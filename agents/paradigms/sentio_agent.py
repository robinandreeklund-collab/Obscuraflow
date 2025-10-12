"""
SentioAgent - Emotional/Empathic Dimension

Funktion: Sentimentanalys och emotionell förstärkning
Kapacitet: 30-period buffer, fear/greed integration
Lärande: Justerar beslut baserat på marknadspsykologi
Kopplingar: sizingsentimentadapter, vote_engine, vox, symbio
"""

import logging
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent, AgentType, DecisionType


logger = logging.getLogger(__name__)


class SentioAgent(BaseAgent):
    """
    SentioAgent analyserar marknadens emotionella tillstånd.
    
    Analyserar:
    - Fear/Greed index
    - Marknadssentiment
    - Psykologiska extremer
    """
    
    def __init__(
        self, 
        agent_id: str = "sentio_agent",
        buffer_size: int = 30
    ):
        """
        Initierar SentioAgent.
        
        Args:
            agent_id: Unikt ID för agenten
            buffer_size: Antal perioder att buffra
        """
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.PARADIGMATIC,
            confidence_threshold=0.6,
            parameters={
                'buffer_size': buffer_size
            }
        )
        self.buffer_size = buffer_size
        self.sentiment_buffer: List[float] = []
    
    def calculate_sentiment(self, market_data: Dict[str, Any]) -> float:
        """
        Beräknar marknadssentiment.
        
        Args:
            market_data: Marknadsdata
        
        Returns:
            Sentiment score (-1 till 1, negativ = fear, positiv = greed)
        """
        price_change = market_data.get('price_change_pct', 0)
        volatility = market_data.get('volatility', 0.5)
        
        # Fear/Greed beräkning
        # Greed: positiva rörelser med låg volatilitet
        # Fear: negativa rörelser med hög volatilitet
        if price_change > 0:
            sentiment = price_change * 10 * (1.0 - volatility)
        else:
            sentiment = price_change * 10 * (1.0 + volatility)
        
        sentiment = max(-1.0, min(1.0, sentiment))
        return sentiment
    
    def analyze(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyserar symbol baserat på sentiment.
        
        Args:
            symbol: Symbolnamn
            market_data: Marknadsdata
        
        Returns:
            Dict med decision, confidence, reasoning
        """
        current_sentiment = self.calculate_sentiment(market_data)
        self.sentiment_buffer.append(current_sentiment)
        
        # Begränsa buffert
        if len(self.sentiment_buffer) > self.buffer_size:
            self.sentiment_buffer = self.sentiment_buffer[-self.buffer_size:]
        
        # Beräkna genomsnittligt sentiment
        avg_sentiment = sum(self.sentiment_buffer) / len(self.sentiment_buffer) if self.sentiment_buffer else 0
        
        # Extrem fear = köptillfälle (contrarian)
        # Extrem greed = säljtillfälle (contrarian)
        if avg_sentiment < -0.6:
            decision = DecisionType.BUY.value
            confidence = min(0.6 + abs(avg_sentiment) * 0.3, 0.95)
            reasoning = f"Extrem fear, contrarian BUY (sentiment={avg_sentiment:.2f})"
        elif avg_sentiment > 0.6:
            decision = DecisionType.SELL.value
            confidence = min(0.6 + abs(avg_sentiment) * 0.3, 0.95)
            reasoning = f"Extrem greed, contrarian SELL (sentiment={avg_sentiment:.2f})"
        elif avg_sentiment > 0.2:
            decision = DecisionType.BUY.value
            confidence = 0.65
            reasoning = f"Positiv sentiment, following the trend (sentiment={avg_sentiment:.2f})"
        elif avg_sentiment < -0.2:
            decision = DecisionType.SELL.value
            confidence = 0.65
            reasoning = f"Negativ sentiment, following the trend (sentiment={avg_sentiment:.2f})"
        else:
            decision = DecisionType.HOLD.value
            confidence = 0.5
            reasoning = f"Neutral sentiment (sentiment={avg_sentiment:.2f})"
        
        logger.debug(f"SentioAgent analys för {symbol}: {decision} ({confidence:.2f})")
        
        return {
            'agent_id': self.agent_id,
            'symbol': symbol,
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'metrics': {
                'current_sentiment': current_sentiment,
                'avg_sentiment': avg_sentiment,
                'buffer_size': len(self.sentiment_buffer)
            }
        }
