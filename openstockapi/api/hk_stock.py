from typing import List, Dict, Any, Optional
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def hk_symbols(provider: Optional[str] = None) -> List[str]:
    """Get list of available HK stock symbols."""
    return gateway.execute(
        action="stock.symbols",
        market="hk",
        required_tier=DataTier.FREE,
        provider=provider
    )

def hk_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV data for a HK stock symbol."""
    bars = gateway.execute(
        action="stock.ohlcv",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        range=range,
        interval=interval,
        provider=provider
    )
    data_list = [bar.model_dump() for bar in bars]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def hk_profile(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get company profile for a HK stock symbol."""
    profile_data = gateway.execute(
        action="stock.profile",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return profile_data.model_dump()

def hk_financials(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Dict[str, Any]:
    """Get raw financial statement data for a HK stock symbol."""
    financials_data = gateway.execute(
        action="stock.financials",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    return financials_data.model_dump()

def hk_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get balance sheet for a HK stock symbol."""
    items = gateway.execute(
        action="stock.balance_sheet",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def hk_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get income statement for a HK stock symbol."""
    items = gateway.execute(
        action="stock.income_statement",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def hk_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get cashflow statement for a HK stock symbol."""
    items = gateway.execute(
        action="stock.cashflow",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def hk_ratios(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get financial ratios for a HK stock symbol."""
    ratios_data = gateway.execute(
        action="stock.ratios",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return ratios_data.model_dump()

def hk_dividends(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get dividend history for a HK stock symbol."""
    dividends_data = gateway.execute(
        action="stock.dividends",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return dividends_data.model_dump()

def hk_splits(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get split history for a HK stock symbol."""
    splits_data = gateway.execute(
        action="stock.splits",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return splits_data.model_dump()

def hk_calendar(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get calendar events (earnings) for a HK stock symbol."""
    calendar_data = gateway.execute(
        action="stock.calendar",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return calendar_data.model_dump()

def hk_news(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get news for a HK stock symbol."""
    news_data = gateway.execute(
        action="stock.news",
        market="hk",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return news_data.model_dump()

def hk_heatmap(limit: int = 500, provider: Optional[str] = None) -> Any:
    """Get Hong Kong (HKEX) stock market heatmap data (symbol, name, change, market_cap, sector, industry, logo_url)."""
    items = gateway.execute(
        action="stock.heatmap",
        market="hk",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

