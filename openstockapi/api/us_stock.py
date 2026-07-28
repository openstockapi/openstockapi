from typing import List, Dict, Any, Optional
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def us_symbols(provider: Optional[str] = None) -> List[str]:
    """Get list of available US stock symbols."""
    return gateway.execute(
        action="stock.symbols",
        market="us",
        required_tier=DataTier.FREE,
        provider=provider
    )

def us_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV data for a US stock symbol."""
    bars = gateway.execute(
        action="stock.ohlcv",
        market="us",
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

def us_profile(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get company profile for a US stock symbol."""
    profile_data = gateway.execute(
        action="stock.profile",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return profile_data.model_dump()

def us_financials(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Dict[str, Any]:
    """Get raw financial statement data for a US stock symbol."""
    financials_data = gateway.execute(
        action="stock.financials",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    return financials_data.model_dump()

def us_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get balance sheet for a US stock symbol."""
    items = gateway.execute(
        action="stock.balance_sheet",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def us_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get income statement for a US stock symbol."""
    items = gateway.execute(
        action="stock.income_statement",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def us_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get cashflow statement for a US stock symbol."""
    items = gateway.execute(
        action="stock.cashflow",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def us_ratios(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get financial ratios for a US stock symbol."""
    items = gateway.execute(
        action="stock.ratios",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def us_dividends(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get dividend history for a US stock symbol."""
    dividends_data = gateway.execute(
        action="stock.dividends",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return dividends_data.model_dump()

def us_splits(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get split history for a US stock symbol."""
    splits_data = gateway.execute(
        action="stock.splits",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return splits_data.model_dump()

def us_calendar(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get calendar events (earnings, dividends) for a US stock symbol."""
    calendar_data = gateway.execute(
        action="stock.calendar",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return calendar_data.model_dump()

def us_news(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get news for a US stock symbol."""
    news_data = gateway.execute(
        action="stock.news",
        market="us",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return news_data.model_dump()

def us_heatmap(limit: int = 500, provider: Optional[str] = None) -> Any:
    """Get US stock market heatmap data (symbol, name, change, market_cap, sector, industry)."""
    items = gateway.execute(
        action="stock.heatmap",
        market="us",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

