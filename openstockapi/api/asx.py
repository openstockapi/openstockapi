from typing import List, Dict, Any, Optional
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def asx_symbols(provider: Optional[str] = None) -> List[str]:
    """Get list of available ASX symbols."""
    return gateway.execute(
        action="stock.symbols",
        market="au",
        required_tier=DataTier.FREE,
        provider=provider
    )

def asx_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV data for an ASX symbol."""
    bars = gateway.execute(
        action="stock.ohlcv",
        market="au",
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

def asx_profile(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get company profile for an ASX symbol."""
    profile_data = gateway.execute(
        action="stock.profile",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return profile_data.model_dump()

def asx_financials(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get raw financial statement data and ratios for an ASX symbol."""
    financials_data = gateway.execute(
        action="stock.financials",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return financials_data.model_dump()

def asx_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get balance sheet for an ASX symbol."""
    items = gateway.execute(
        action="stock.balance_sheet",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def asx_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get income statement for an ASX symbol."""
    items = gateway.execute(
        action="stock.income_statement",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def asx_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get cashflow statement for an ASX symbol."""
    items = gateway.execute(
        action="stock.cashflow",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def asx_ratios(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get financial ratios for an ASX symbol."""
    items = gateway.execute(
        action="stock.ratios",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def asx_dividends(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get historical and upcoming dividends for an ASX symbol."""
    dividends_data = gateway.execute(
        action="stock.dividends",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return dividends_data.model_dump()

def asx_announcements(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get corporate announcements for an ASX symbol."""
    announcements_data = gateway.execute(
        action="stock.announcements",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return announcements_data.model_dump()

def asx_news(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get news articles for an ASX symbol."""
    news_data = gateway.execute(
        action="stock.news",
        market="au",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return news_data.model_dump()

def asx_heatmap(limit: int = 500, provider: Optional[str] = None) -> Any:
    """Get ASX stock market heatmap data (symbol, name, change, market_cap, sector, industry)."""
    items = gateway.execute(
        action="stock.heatmap",
        market="au",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list
