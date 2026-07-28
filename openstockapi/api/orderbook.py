from typing import Optional, Union, Any, List
from openstockapi.core.types import DataTier
from openstockapi.core.utils import parse_market_symbol
from openstockapi.core.gateway import gateway

# Optional import for Pandas support
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def bid_ask(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    """Get stock bid/ask level details."""
    symbol, market = parse_market_symbol(symbol, market)
    ob = gateway.execute(
        action="stock.order_book",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    return ob.model_dump()

def depth(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    """Get stock order book depth details."""
    symbol, market = parse_market_symbol(symbol, market)
    ob = gateway.execute(
        action="stock.order_book",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    return ob.model_dump()

def ticks(symbol: str, limit: int = 100, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get intraday ticks transaction history."""
    symbol, market = parse_market_symbol(symbol, market)
    # Default priority config in execute when provider is None will override defaults
    entries = gateway.execute(
        action="stock.ticks",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        limit=limit,
        provider=provider
    )
    data_list = [entry.model_dump() for entry in entries]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list
