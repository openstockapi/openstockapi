from typing import List, Optional, Union, Any
from openstockapi.core.types import DataTier
from openstockapi.core.utils import parse_market_symbol
from openstockapi.core.gateway import gateway

# Optional import for Pandas support
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def foreign(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get foreign trading transaction details."""
    symbol, market = parse_market_symbol(symbol, market)
    records = gateway.execute(
        action="stock.foreign_trade",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        limit=limit,
        provider=provider
    )
    data_list = [rec.model_dump() for rec in records]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def insider(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get insider trading transaction details."""
    symbol, market = parse_market_symbol(symbol, market)
    records = gateway.execute(
        action="stock.insider_trade",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        limit=limit,
        provider=provider
    )
    data_list = [rec.model_dump() for rec in records]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def prop_trade(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get proprietary trading transaction details."""
    symbol, market = parse_market_symbol(symbol, market)
    records = gateway.execute(
        action="stock.prop_trade",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        limit=limit,
        provider=provider
    )
    data_list = [rec.model_dump() for rec in records]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list
