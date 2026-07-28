from typing import List, Dict, Any, Optional, Union
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway
from openstockapi.providers import get_provider

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def crypto_ohlcv(symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV klines for a cryptocurrency pair."""
    bars = gateway.execute(
        action="crypto.ohlcv",
        market="global",
        required_tier=DataTier.FREE,
        symbol=symbol,
        interval=interval,
        limit=limit,
        market_type=market_type,
        provider=provider
    )
    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

async def async_crypto_ohlcv(symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV klines asynchronously."""
    # Validate handshake first
    from openstockapi.core.security import enforce_tier_and_rate_limit
    enforce_tier_and_rate_limit(DataTier.FREE, "crypto.global.ohlcv")

    p_inst = get_provider("core")
    bars = await p_inst.async_get_crypto_ohlcv(symbol, interval, limit, market_type, provider)
    for bar in bars:
        bar.market = "global"
        bar.asset_class = "crypto"
    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def crypto_depth(symbol: str, limit: int = 100, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get order book depth bids and asks."""
    ob = gateway.execute(
        action="crypto.depth",
        market="global",
        required_tier=DataTier.PRO,
        symbol=symbol,
        limit=limit,
        provider=provider
    )
    return ob.model_dump()

def crypto_derivatives(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get derivatives metrics."""
    return gateway.execute(
        action="crypto.derivatives",
        market="global",
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )

def crypto_footprint(symbol: str, timeframe: str = "5min", limit: int = 10, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get order flow footprint heatmap data."""
    return gateway.execute(
        action="crypto.footprint",
        market="global",
        required_tier=DataTier.PREMIUM,
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
        provider=provider
    )

def simulate_leverage(symbol: str, entry_price: float, leverage: float, position_size: float, direction: str) -> Dict[str, Any]:
    """Simulate long/short leverage position margin metrics."""
    return gateway.execute(
        action="crypto.simulate",
        market="global",
        required_tier=DataTier.PRO,
        symbol=symbol,
        entry_price=entry_price,
        leverage=leverage,
        position_size=position_size,
        direction=direction
    )

def crypto_symbols(provider: Optional[str] = None) -> Dict[str, Any]:
    """Get list of supported crypto symbols."""
    return gateway.execute(
        action="crypto.symbols",
        market="global",
        required_tier=DataTier.FREE,
        provider=provider
    )

def crypto_tickers(provider: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get live tickers."""
    return gateway.execute(
        action="crypto.tickers",
        market="global",
        required_tier=DataTier.PRO,
        provider=provider
    )

def crypto_options_instruments(currency: str = "BTC", kind: str = "option", provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get active option instruments."""
    records = gateway.execute(
        action="crypto.options_instruments",
        market="global",
        required_tier=DataTier.PRO,
        currency=currency,
        kind=kind,
        provider=provider
    )
    data_list = [rec.model_dump() for rec in records]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def crypto_options_chain(currency: str = "BTC", provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get full option chain metrics."""
    records = gateway.execute(
        action="crypto.options_chain",
        market="global",
        required_tier=DataTier.PRO,
        currency=currency,
        provider=provider
    )
    data_list = [rec.model_dump() for rec in records]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def crypto_options_ticker(instrument_name: str, provider: Optional[str] = None) -> dict:
    """Get detailed ticker and Greeks for an option contract."""
    record = gateway.execute(
        action="crypto.options_ticker",
        market="global",
        required_tier=DataTier.PRO,
        instrument_name=instrument_name,
        provider=provider
    )
    return record.model_dump()

def crypto_news(limit: int = 20, provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get crypto news articles."""
    items = gateway.execute(
        action="crypto.news",
        market="global",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def crypto_events(provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get upcoming crypto calendar events."""
    items = gateway.execute(
        action="crypto.events",
        market="global",
        required_tier=DataTier.FREE,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def crypto_profile(symbol: str, provider: Optional[str] = None) -> Union[dict, Any]:
    """Get cryptocurrency token profile details (website, logo, categories, description)."""
    prof = gateway.execute(
        action="crypto.profile",
        market="global",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return prof.model_dump()

def crypto_heatmap(limit: int = 500, provider: Optional[str] = None) -> Any:
    """Get Cryptocurrency market heatmap data (symbol, name, change, market_cap, sector, industry, logo_url)."""
    items = gateway.execute(
        action="crypto.heatmap",
        market="global",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

