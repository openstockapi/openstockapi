from typing import List, Dict, Any, Optional
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def jp_symbols(provider: Optional[str] = None) -> List[str]:
    """Get list of available JP stock symbols."""
    return gateway.execute(
        action="stock.symbols",
        market="jp",
        required_tier=DataTier.FREE,
        provider=provider
    )

def jp_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV data for a JP stock symbol."""
    bars = gateway.execute(
        action="stock.ohlcv",
        market="jp",
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

def jp_profile(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get company profile for a JP stock symbol."""
    profile_data = gateway.execute(
        action="stock.profile",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return profile_data.model_dump()

def jp_financials(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Dict[str, Any]:
    """Get raw financial statement data for a JP stock symbol."""
    financials_data = gateway.execute(
        action="stock.financials",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    return financials_data.model_dump()

def jp_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get balance sheet for a JP stock symbol."""
    items = gateway.execute(
        action="stock.balance_sheet",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def jp_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get income statement for a JP stock symbol."""
    items = gateway.execute(
        action="stock.income_statement",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def jp_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get cashflow statement for a JP stock symbol."""
    items = gateway.execute(
        action="stock.cashflow",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def jp_ratios(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get financial ratios for a JP stock symbol."""
    ratios_data = gateway.execute(
        action="stock.ratios",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return ratios_data.model_dump()

def jp_dividends(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get dividend history for a JP stock symbol."""
    dividends_data = gateway.execute(
        action="stock.dividends",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return dividends_data.model_dump()

def jp_splits(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get split history for a JP stock symbol."""
    splits_data = gateway.execute(
        action="stock.splits",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return splits_data.model_dump()

def jp_calendar(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get calendar events (earnings, dividends) for a JP stock symbol."""
    calendar_data = gateway.execute(
        action="stock.calendar",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return calendar_data.model_dump()

def jp_news(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get news for a JP stock symbol."""
    news_data = gateway.execute(
        action="stock.news",
        market="jp",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return news_data.model_dump()

def jp_heatmap(limit: int = 500, provider: Optional[str] = None) -> Any:
    """Get Japan (TSE) stock market heatmap data (symbol, name, change, market_cap, sector, industry, logo_url)."""
    items = gateway.execute(
        action="stock.heatmap",
        market="jp",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list
