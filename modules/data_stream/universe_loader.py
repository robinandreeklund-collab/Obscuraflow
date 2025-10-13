"""
Universe Loader - Laddar symboluniversum från konfigurationsfil

Denna modul:
- Laddar NASDAQ-100 symboler från YAML-fil
- Validerar symbolformat
- Tillhandahåller centraliserad symbolhantering
"""

import os
import yaml
import logging
from typing import List, Set

logger = logging.getLogger(__name__)


def load_symbol_universe(path: str = None) -> List[str]:
    """
    Laddar symboluniversum från YAML-fil.
    
    Args:
        path: Sökväg till YAML-fil (optional). Om None, använd default-fil.
    
    Returns:
        Lista av symboler
    
    Raises:
        FileNotFoundError: Om filen inte hittas
        ValueError: Om filen har ogiltigt format
    """
    if path is None:
        # Default path relativ till denna fil
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "config", "nasdaq100_symbols.yaml")
    
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        
        if not isinstance(data, dict) or "nasdaq_100" not in data:
            raise ValueError("YAML-filen måste innehålla 'nasdaq_100' nyckel")
        
        symbols = data["nasdaq_100"]
        
        if not isinstance(symbols, list):
            raise ValueError("'nasdaq_100' måste vara en lista")
        
        # Ta bort kommentarer och formatera symboler
        cleaned_symbols = []
        for symbol in symbols:
            if isinstance(symbol, str):
                # Ta bort kommentarer och whitespace
                clean_symbol = symbol.split('#')[0].strip()
                if clean_symbol:
                    cleaned_symbols.append(clean_symbol)
        
        logger.info(f"Laddade {len(cleaned_symbols)} symboler från {path}")
        return cleaned_symbols
    
    except FileNotFoundError:
        logger.error(f"Kunde inte hitta symboluniversum-fil: {path}")
        # Fallback till minimal lista
        fallback = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "UNH", "JNJ"]
        logger.warning(f"Använder fallback-lista med {len(fallback)} symboler")
        return fallback
    
    except Exception as e:
        logger.error(f"Fel vid laddning av symboluniversum: {e}")
        # Fallback till minimal lista
        fallback = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "UNH", "JNJ"]
        logger.warning(f"Använder fallback-lista med {len(fallback)} symboler")
        return fallback


def get_valid_symbols_set() -> Set[str]:
    """
    Returnerar set av giltiga symboler för snabb lookup.
    
    Returns:
        Set av symboler
    """
    return set(load_symbol_universe())


def validate_symbol(symbol: str) -> bool:
    """
    Validerar om en symbol finns i universummet.
    
    Args:
        symbol: Symbol att validera
    
    Returns:
        True om symbolen är giltig, False annars
    """
    valid_symbols = get_valid_symbols_set()
    return symbol.upper() in valid_symbols


# Cache för att undvika att läsa filen varje gång
_cached_symbols = None
_cached_symbols_set = None


def get_cached_symbols() -> List[str]:
    """
    Returnerar cachad lista av symboler.
    
    Returns:
        Lista av symboler
    """
    global _cached_symbols
    if _cached_symbols is None:
        _cached_symbols = load_symbol_universe()
    return _cached_symbols


def get_cached_symbols_set() -> Set[str]:
    """
    Returnerar cachad set av symboler.
    
    Returns:
        Set av symboler
    """
    global _cached_symbols_set
    if _cached_symbols_set is None:
        _cached_symbols_set = set(get_cached_symbols())
    return _cached_symbols_set


def reload_symbols():
    """
    Laddar om symboluniversum (tömmer cache).
    """
    global _cached_symbols, _cached_symbols_set
    _cached_symbols = None
    _cached_symbols_set = None
    logger.info("Symboluniversum-cache tömd, laddar om...")
