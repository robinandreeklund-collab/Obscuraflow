"""
RiskMapper - Huvudklass för riskmatris och symbolrisk

Denna klass ansvarar för:
- Riskmatris över symboler
- Riskberäkning
- Korrelationsanalys
- Risk-adjusted sizing
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import math


logger = logging.getLogger(__name__)


class RiskMapper:
    """
    RiskMapper hanterar riskmatris och symbolrisk.
    
    Attributes:
        risk_matrix (Dict): Riskmatris för symboler
        correlations (Dict): Korrelationer mellan symbolpar
    """
    
    def __init__(self, max_portfolio_risk: float = 0.20):
        """
        Initierar RiskMapper.
        
        Args:
            max_portfolio_risk: Max total portföljrisk som procent
        """
        self.max_portfolio_risk = max_portfolio_risk
        self.risk_matrix: Dict[str, Dict[str, Any]] = {}
        self.correlations: Dict[Tuple[str, str], float] = {}
        self.risk_history: List[Dict[str, Any]] = []
        logger.info(f"RiskMapper initierad med max_portfolio_risk={max_portfolio_risk}")
    
    def calculate_symbol_risk(
        self,
        symbol: str,
        volatility: float,
        position_size: float,
        additional_factors: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Beräknar risk för en symbol.
        
        Args:
            symbol: Symbolnamn
            volatility: Volatilitet (standardavvikelse)
            position_size: Positionsstorlek
            additional_factors: Extra riskfaktorer
        
        Returns:
            Dict med riskberäkning
        """
        # Basrisk från volatilitet
        base_risk = volatility * position_size
        
        # Lägg till extra faktorer
        if additional_factors:
            for factor, value in additional_factors.items():
                base_risk *= (1 + value)
        
        risk_data = {
            'symbol': symbol,
            'base_risk': base_risk,
            'volatility': volatility,
            'position_size': position_size,
            'risk_level': self._classify_risk(base_risk),
            'timestamp': datetime.now().isoformat()
        }
        
        self.risk_matrix[symbol] = risk_data
        logger.info(f"Beräknade risk för {symbol}: {base_risk:.4f}")
        return risk_data
    
    def _classify_risk(self, risk_value: float) -> str:
        """
        Klassificerar risknivå.
        
        Args:
            risk_value: Riskvärde
        
        Returns:
            Risk-kategori
        """
        if risk_value < 0.05:
            return 'low'
        elif risk_value < 0.15:
            return 'medium'
        else:
            return 'high'
    
    def set_correlation(self, symbol1: str, symbol2: str, correlation: float) -> bool:
        """
        Sätter korrelation mellan två symboler.
        
        Args:
            symbol1: Första symbolen
            symbol2: Andra symbolen
            correlation: Korrelationsvärde (-1 till 1)
        
        Returns:
            True om korrelationen sattes
        """
        if not -1 <= correlation <= 1:
            logger.error("Korrelation måste vara mellan -1 och 1")
            return False
        
        # Normalisera ordning
        pair = tuple(sorted([symbol1, symbol2]))
        self.correlations[pair] = correlation
        logger.debug(f"Satte korrelation mellan {symbol1} och {symbol2}: {correlation}")
        return True
    
    def get_correlation(self, symbol1: str, symbol2: str) -> float:
        """
        Hämtar korrelation mellan två symboler.
        
        Args:
            symbol1: Första symbolen
            symbol2: Andra symbolen
        
        Returns:
            Korrelationsvärde (0 om okänd)
        """
        pair = tuple(sorted([symbol1, symbol2]))
        return self.correlations.get(pair, 0.0)
    
    def calculate_portfolio_risk(self, positions: Dict[str, float]) -> Dict[str, Any]:
        """
        Beräknar total portföljrisk med hänsyn till korrelationer.
        
        Args:
            positions: Dict med symbol -> position_size
        
        Returns:
            Dict med portföljrisk
        """
        symbols = list(positions.keys())
        total_risk = 0.0
        
        # Summera individuella risker
        for symbol, size in positions.items():
            if symbol in self.risk_matrix:
                symbol_risk = self.risk_matrix[symbol]['base_risk']
                total_risk += symbol_risk ** 2
        
        # Lägg till korrelationseffekter
        for i, sym1 in enumerate(symbols):
            for sym2 in symbols[i+1:]:
                if sym1 in self.risk_matrix and sym2 in self.risk_matrix:
                    corr = self.get_correlation(sym1, sym2)
                    risk1 = self.risk_matrix[sym1]['base_risk']
                    risk2 = self.risk_matrix[sym2]['base_risk']
                    total_risk += 2 * corr * risk1 * risk2
        
        negative_risk_encountered = False
        if total_risk < 0:
            logger.warning(f"Negative portfolio risk encountered ({total_risk:.6f}) due to strong negative correlations. Setting risk to 0.")
            negative_risk_encountered = True
            total_risk = 0.0
        else:
            total_risk = math.sqrt(total_risk)
        
        portfolio_risk = {
            'total_risk': total_risk,
            'risk_pct': total_risk * 100,
            'within_limits': total_risk <= self.max_portfolio_risk,
            'positions': len(positions),
            'timestamp': datetime.now().isoformat(),
            'negative_risk_encountered': negative_risk_encountered
        }
        
        self.risk_history.append(portfolio_risk)
        logger.info(f"Beräknade portföljrisk: {total_risk:.4f}")
        return portfolio_risk
    
    def get_high_risk_symbols(self, threshold: float = 0.15) -> List[str]:
        """
        Hämtar symboler med hög risk.
        
        Args:
            threshold: Risktröskelvärde
        
        Returns:
            Lista med högrisk-symboler
        """
        high_risk = [
            symbol for symbol, data in self.risk_matrix.items()
            if data['base_risk'] > threshold
        ]
        return high_risk
    
    def get_correlated_symbols(self, symbol: str, min_correlation: float = 0.7) -> List[Tuple[str, float]]:
        """
        Hämtar symboler som är starkt korrelerade med en given symbol.
        
        Args:
            symbol: Symbolnamn
            min_correlation: Minimum korrelation
        
        Returns:
            Lista med (symbol, correlation)
        """
        correlated = []
        
        for (sym1, sym2), corr in self.correlations.items():
            if abs(corr) >= min_correlation:
                if sym1 == symbol:
                    correlated.append((sym2, corr))
                elif sym2 == symbol:
                    correlated.append((sym1, corr))
        
        return correlated
    
    def suggest_risk_adjusted_size(
        self,
        symbol: str,
        desired_size: float,
        portfolio_value: float
    ) -> Dict[str, Any]:
        """
        Föreslår riskjusterad positionsstorlek.
        
        Args:
            symbol: Symbolnamn
            desired_size: Önskad storlek
            portfolio_value: Portföljvärde
        
        Returns:
            Dict med justerad storlek
        """
        if symbol not in self.risk_matrix:
            return {
                'symbol': symbol,
                'desired_size': desired_size,
                'suggested_size': desired_size,
                'adjustment': 'none',
                'reason': 'no_risk_data'
            }
        
        risk_data = self.risk_matrix[symbol]
        risk_level = risk_data['risk_level']
        base_risk = risk_data['base_risk']
        
        # Justera storlek baserat på risk
        adjustment_factors = {
            'low': 1.0,
            'medium': 0.7,
            'high': 0.4
        }
        
        factor = adjustment_factors.get(risk_level, 0.5)
        adjusted_size = desired_size * factor
        
        # Ytterligare justering baserat på portföljens totala risk
        if hasattr(self, 'risk_history') and self.risk_history:
            latest_portfolio_risk = self.risk_history[-1]['total_risk']
            if latest_portfolio_risk > self.max_portfolio_risk * 0.8:
                # Nära maxgränsen, reducera ytterligare
                additional_reduction = 0.8
                adjusted_size *= additional_reduction
                reason_addon = f', portfolio near limit ({latest_portfolio_risk:.2%})'
            else:
                reason_addon = ''
        else:
            reason_addon = ''
        
        # Säkerställ att vi inte överstiger max portfolio risk contribution
        max_single_position = portfolio_value * 0.15  # Max 15% i en position
        adjusted_size = min(adjusted_size, max_single_position)
        
        return {
            'symbol': symbol,
            'desired_size': desired_size,
            'suggested_size': adjusted_size,
            'risk_level': risk_level,
            'adjustment_factor': factor,
            'reason': f'risk_{risk_level}{reason_addon}',
            'base_risk': base_risk
        }
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """
        Hämtar sammanfattning av risk över alla symboler.
        
        Returns:
            Dict med risksammanfattning
        """
        if not self.risk_matrix:
            return {
                'tracked_symbols': 0,
                'avg_risk': 0.0,
                'high_risk_count': 0
            }
        
        risks = [data['base_risk'] for data in self.risk_matrix.values()]
        return {
            'tracked_symbols': len(self.risk_matrix),
            'avg_risk': sum(risks) / len(risks),
            'max_risk': max(risks),
            'min_risk': min(risks),
            'high_risk_count': len(self.get_high_risk_symbols())
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Hämtar statistik för risk mapper.
        
        Returns:
            Dict med statistik
        """
        return {
            'tracked_symbols': len(self.risk_matrix),
            'tracked_correlations': len(self.correlations),
            'risk_calculations': len(self.risk_history),
            'max_portfolio_risk': self.max_portfolio_risk,
            **self.get_risk_summary()
        }
