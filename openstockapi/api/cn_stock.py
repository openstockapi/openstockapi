from typing import List, Dict, Any, Optional
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def cn_symbols(provider: Optional[str] = None) -> List[str]:
    """Get list of available CN stock symbols."""
    return gateway.execute(
        action="stock.symbols",
        market="cn",
        required_tier=DataTier.FREE,
        provider=provider
    )

def cn_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> Any:
    """Get historical OHLCV data for a CN stock symbol."""
    bars = gateway.execute(
        action="stock.ohlcv",
        market="cn",
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

def cn_profile(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get company profile for a CN stock symbol."""
    profile_data = gateway.execute(
        action="stock.profile",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return profile_data.model_dump()

def cn_financials(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Dict[str, Any]:
    """Get raw financial statement data for a CN stock symbol."""
    financials_data = gateway.execute(
        action="stock.financials",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    return financials_data.model_dump()

def cn_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get balance sheet for a CN stock symbol."""
    items = gateway.execute(
        action="stock.balance_sheet",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def cn_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get income statement for a CN stock symbol."""
    items = gateway.execute(
        action="stock.income_statement",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def cn_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None) -> Any:
    """Get cashflow statement for a CN stock symbol."""
    items = gateway.execute(
        action="stock.cashflow",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def cn_ratios(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get financial ratios for a CN stock symbol."""
    ratios_data = gateway.execute(
        action="stock.ratios",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return ratios_data.model_dump()

def cn_dividends(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get dividend history for a CN stock symbol."""
    dividends_data = gateway.execute(
        action="stock.dividends",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return dividends_data.model_dump()

def cn_splits(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get split history for a CN stock symbol."""
    splits_data = gateway.execute(
        action="stock.splits",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return splits_data.model_dump()

def cn_calendar(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get calendar events (earnings) for a CN stock symbol."""
    calendar_data = gateway.execute(
        action="stock.calendar",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return calendar_data.model_dump()

def cn_news(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get news for a CN stock symbol."""
    news_data = gateway.execute(
        action="stock.news",
        market="cn",
        required_tier=DataTier.FREE,
        symbol=symbol,
        provider=provider
    )
    return news_data.model_dump()

def cn_quote(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get realtime quote for a CN stock symbol."""
    quote_data = gateway.execute(
        action="stock.quote",
        market="cn",
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    return quote_data.model_dump()

def cn_tick(symbol: str, provider: Optional[str] = None) -> Any:
    """Get intraday ticks for a CN stock symbol."""
    ticks_data = gateway.execute(
        action="stock.ticks",
        market="cn",
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    data_list = [tick.model_dump() for tick in ticks_data]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def cn_order_book(symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get order book depth for a CN stock symbol."""
    book_data = gateway.execute(
        action="stock.order_book",
        market="cn",
        required_tier=DataTier.PRO,
        symbol=symbol,
        provider=provider
    )
    return book_data.model_dump()

def cn_heatmap(limit: int = 500, provider: Optional[str] = None) -> Any:
    """Get China (SSE/SZSE) stock market heatmap data (symbol, name, change, market_cap, sector, industry, logo_url)."""
    items = gateway.execute(
        action="stock.heatmap",
        market="cn",
        required_tier=DataTier.FREE,
        limit=limit,
        provider=provider
    )
    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

