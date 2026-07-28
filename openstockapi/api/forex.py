from typing import Dict, Any, Optional, List, Union
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def forex_rates(base: str = "USD", provider: Optional[str] = None) -> Dict[str, Any]:
    """Get currency exchange rates from a base currency."""
    return gateway.execute(
        action="forex.rates",
        market="global",
        required_tier=DataTier.FREE,
        base=base,
        provider=provider
    )

def forex_ohlcv(symbol: Optional[str] = None, base: Optional[str] = None, target: Optional[str] = None, range_val: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV chart bars for a forex pair."""
    bars = gateway.execute(
        action="forex.ohlcv",
        market="global",
        required_tier=DataTier.FREE,
        symbol=symbol,
        base=base,
        target=target,
        range_val=range_val,
        interval=interval,
        provider=provider
    )
    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def commodities_prices(symbol: str, range_val: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical prices for commodities (e.g., GOLD, SILVER, CRUDE_OIL)."""
    bars = gateway.execute(
        action="forex.commodities",
        market="global",
        required_tier=DataTier.FREE,
        symbol=symbol,
        range_val=range_val,
        interval=interval,
        provider=provider
    )
    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def global_indices_etf(symbol: str, range_val: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical price data for major indices and ETFs (e.g., SPY, QQQ)."""
    bars = gateway.execute(
        action="forex.indices_etf",
        market="global",
        required_tier=DataTier.FREE,
        symbol=symbol,
        range_val=range_val,
        interval=interval,
        provider=provider
    )
    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def compare_rates(base: str = "USD") -> Dict[str, Any]:
    """Compare exchange rates between different brokerages and source providers."""
    return gateway.execute(
        action="forex.compare",
        market="global",
        required_tier=DataTier.PRO,
        base=base
    )

def forex_symbols(provider: Optional[str] = None) -> Dict[str, Any]:
    """Get list of supported forex, commodities, and index/ETF symbols."""
    return gateway.execute(
        action="forex.symbols",
        market="global",
        required_tier=DataTier.FREE,
        provider=provider
    )

def forex_news(limit: int = 20, provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get latest forex and financial news."""
    items = gateway.execute(
        action="forex.news",
        market="global",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def forex_events(provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get global macro economic calendar events."""
    items = gateway.execute(
        action="forex.events",
        market="global",
        required_tier=DataTier.FREE,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def forex_profile(symbol: str, provider: Optional[str] = None) -> Union[dict, Any]:
    """Get forex currency pair profile details (base/quote, category, flag logo URLs)."""
    prof = gateway.execute(
        action="forex.profile",
        market="global",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return prof.model_dump()
