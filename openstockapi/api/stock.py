import datetime
from typing import List, Union, Optional, Any
from openstockapi.core.types import DataTier
from openstockapi.core.utils import parse_market_symbol
from openstockapi.core.gateway import gateway
from openstockapi.core.exceptions import ProviderUnavailableError
from openstockapi.providers import get_provider

# Optional import for Pandas support
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def ohlcv(symbol: str, resolution: str = "1D", start: Optional[str] = None, end: Optional[str] = None, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get historical OHLCV candles."""
    symbol, market = parse_market_symbol(symbol, market)
    if start is None:
        start = "2020-01-01"
    if end is None:
        end = datetime.datetime.now().strftime("%Y-%m-%d")

    bars = gateway.execute(
        action="stock.ohlcv",
        market=market,
        required_tier=DataTier.FREE,
        symbol=symbol,
        resolution=resolution,
        from_date=start,
        to_date=end,
        provider=provider
    )

    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

async def async_ohlcv(symbol: str, resolution: str = "1D", start: Optional[str] = None, end: Optional[str] = None, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get historical OHLCV candles asynchronously."""
    symbol, market = parse_market_symbol(symbol, market)
    if start is None:
        start = "2020-01-01"
    if end is None:
        end = datetime.datetime.now().strftime("%Y-%m-%d")

    # Gateway validate first
    from openstockapi.core.security import enforce_tier_and_rate_limit
    asset_class = "stock"
    market_code = market.lower()
    enforce_tier_and_rate_limit(DataTier.FREE, f"{asset_class}.{market_code}.ohlcv")

    # Resolve provider and call asynchronously (bypassing normal gateway sync dispatch)
    from openstockapi.config.settings import get_default_providers
    providers_to_try = [provider] if provider else get_default_providers("ohlcv", market)

    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            if p_name == "core":
                bars = await p_inst.async_get_ohlcv(symbol, resolution, start, end, market=market)
            else:
                bars = await p_inst.async_get_ohlcv(symbol, resolution, start, end)
            for bar in bars:
                bar.market = market_code
                bar.asset_class = asset_class
            data_list = [bar.model_dump() for bar in bars]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue

    raise ProviderUnavailableError(f"No provider succeeded in fetching async OHLCV for '{symbol}' (market={market}): {last_err}")

def profile(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    """Get corporate profile details."""
    symbol, market = parse_market_symbol(symbol, market)
    prof = gateway.execute(
        action="stock.profile",
        market=market,
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return prof.model_dump()


def derivative_profile(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    """Get derivative profile details (Futures/Warrants).
    
    Tier: PRO
    """
    symbol, market = parse_market_symbol(symbol, market)
    
    # Gateways and security limits
    from openstockapi.core.security import enforce_tier_and_rate_limit
    asset_class = "stock"
    market_code = market.lower()
    enforce_tier_and_rate_limit(DataTier.PRO, f"{asset_class}.{market_code}.derivative_profile")
    
    prof = gateway.execute(
        action="stock.derivative_profile",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    return prof.model_dump()


def quote(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    """Get real-time stock quote."""
    symbol, market = parse_market_symbol(symbol, market)
    q = gateway.execute(
        action="stock.quote",
        market=market,
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    return q.model_dump()

def symbols(provider: Optional[str] = None, market: str = "VN") -> List[str]:
    """Get list of active stock symbols for a given market."""
    return gateway.execute(
        action="stock.symbols",
        market=market,
        required_tier=DataTier.FREE,
        provider=provider
    )

def heatmap(limit: int = 500, provider: Optional[str] = None, market: str = "VN") -> Any:
    """Get stock market heatmap data for a given market."""
    items = gateway.execute(
        action="stock.heatmap",
        market=market,
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list
