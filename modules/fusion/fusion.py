"""
Fusion - Huvudklass för multi-timeframe signalvalidering

Denna klass ansvarar för:
- Validering av signaler över flera tidsramar
- Identifiering av konvergerande trender
- Filtrera brus och falska signaler
- Sammanvägning av tidsspann för robusta beslut
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class Fusion:
    """
    Fusion hanterar signalvalidering över flera tidsramar.
    
    Attributes:
        timeframes (List[str]): Lista över tidsramar att analysera
        min_confirmations (int): Minimum antal bekräftelser för giltig signal
    """
    
    def __init__(self, timeframes: Optional[List[str]] = None, min_confirmations: int = 2):
        """
        Initierar Fusion med tidsramar och konfirmeringskrav.
        
        Args:
            timeframes: Lista över tidsramar (t.ex. ['1m', '5m', '15m', '1h'])
            min_confirmations: Minimum antal tidsramar som måste bekräfta signal
        """
        self.timeframes = timeframes or ['1m', '5m', '15m', '1h']
        self.min_confirmations = min_confirmations
        self.signal_cache: Dict[str, Dict[str, Any]] = {}
        logger.info(f"Fusion initierad med tidsramar: {self.timeframes}")
    
    def validate_signal(self, symbol: str, signal_type: str, confidence: float, timeframe_signals: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Validerar en signal över flera tidsramar.
        
        Args:
            symbol: Symbolnamn
            signal_type: Typ av signal ('buy', 'sell', 'hold')
            confidence: Konfidensnivå för signalen
            timeframe_signals: Signaler per tidsram (optional)
        
        Returns:
            Dict med valideringsresultat
        """
        logger.info(f"Validerar {signal_type} signal för {symbol}")
        
        # Om inga timeframe-signaler, simulera baserat på huvudsignal
        if timeframe_signals is None:
            import random
            timeframe_signals = {}
            for tf in self.timeframes:
                # Högre sannolikhet för överensstämmelse med huvudsignal
                if random.random() < 0.7:
                    timeframe_signals[tf] = signal_type
                else:
                    alternatives = ['buy', 'sell', 'hold']
                    alternatives.remove(signal_type)
                    timeframe_signals[tf] = random.choice(alternatives)
        
        # Räkna bekräftelser
        confirmations = sum(1 for sig in timeframe_signals.values() if sig == signal_type)
        confirmation_rate = confirmations / len(self.timeframes)
        
        # Signal valideras om minst min_confirmations tidsramar bekräftar
        validated = confirmations >= self.min_confirmations
        
        # Justera confidence baserat på bekräftelser
        adjusted_confidence = confidence * (0.5 + 0.5 * confirmation_rate)
        
        result = {
            'symbol': symbol,
            'signal_type': signal_type,
            'validated': validated,
            'confirmations': confirmations,
            'confirmation_rate': confirmation_rate,
            'timeframe_signals': timeframe_signals,
            'original_confidence': confidence,
            'adjusted_confidence': adjusted_confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache resultatet
        if symbol not in self.signal_cache:
            self.signal_cache[symbol] = []
        self.signal_cache[symbol].append(result)
        
        logger.info(
            f"Signal för {symbol}: validated={validated}, "
            f"confirmations={confirmations}/{len(self.timeframes)}, "
            f"adjusted_confidence={adjusted_confidence:.2f}"
        )
        
        return result
    
    def get_convergence(self, symbol: str) -> Dict[str, Any]:
        """
        Analyserar konvergens mellan tidsramar för en symbol.
        
        Args:
            symbol: Symbolnamn
        
        Returns:
            Dict med konvergensdata
        """
        if symbol not in self.signal_cache or not self.signal_cache[symbol]:
            return {
                'symbol': symbol,
                'convergence_score': 0.0,
                'aligned_timeframes': [],
                'dominant_signal': None
            }
        
        # Ta senaste signalen för symbolen
        latest_signal = self.signal_cache[symbol][-1]
        timeframe_signals = latest_signal.get('timeframe_signals', {})
        
        if not timeframe_signals:
            return {
                'symbol': symbol,
                'convergence_score': 0.0,
                'aligned_timeframes': [],
                'dominant_signal': None
            }
        
        # Räkna förekomster av varje signaltyp
        signal_counts = {}
        for sig in timeframe_signals.values():
            signal_counts[sig] = signal_counts.get(sig, 0) + 1
        
        # Hitta dominerande signal
        dominant_signal = max(signal_counts.items(), key=lambda x: x[1])
        dominant_type = dominant_signal[0]
        dominant_count = dominant_signal[1]
        
        # Beräkna convergence score (hur många tidsramar som är överens)
        convergence_score = dominant_count / len(timeframe_signals)
        
        # Lista tidsramar som är alignade med dominant signal
        aligned_timeframes = [
            tf for tf, sig in timeframe_signals.items() 
            if sig == dominant_type
        ]
        
        result = {
            'symbol': symbol,
            'convergence_score': convergence_score,
            'aligned_timeframes': aligned_timeframes,
            'dominant_signal': dominant_type,
            'signal_breakdown': signal_counts,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.debug(
            f"Konvergens för {symbol}: score={convergence_score:.2f}, "
            f"dominant={dominant_type}, aligned={len(aligned_timeframes)}"
        )
        
        return result
    
    def clear_cache(self, symbol: Optional[str] = None) -> int:
        """
        Rensar signalcache.
        
        Args:
            symbol: Specifik symbol att rensa, eller None för alla
        
        Returns:
            Antal poster som rensades
        """
        if symbol:
            if symbol in self.signal_cache:
                del self.signal_cache[symbol]
                return 1
            return 0
        else:
            count = len(self.signal_cache)
            self.signal_cache.clear()
            return count

    def get_stats(self) -> Dict[str, Any]:
        """
        Returnerar statistik om Fusion-instansen för övervakning.
        
        Returns:
            Dict med statistikdata
        """
        return {
            'cached_signals': len(self.signal_cache),
            'timeframes': self.timeframes,
            'min_confirmations': self.min_confirmations
        }
