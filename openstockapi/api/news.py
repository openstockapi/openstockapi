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

def news(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get news articles for a company/symbol across stock, crypto, and forex."""
    symbol, market = parse_market_symbol(symbol, market)

    if market == "CRYPTO":
        action = "crypto.news"
        resolved_market = "global"
    elif market == "FOREX":
        action = "forex.news"
        resolved_market = "global"
    else:
        action = "stock.company_news"
        resolved_market = market

    items = gateway.execute(
        action=action,
        market=resolved_market,
        required_tier=DataTier.FREE,
        symbol=symbol,
        limit=limit,
        provider=provider
    )

    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def events(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get calendar events for a company/symbol across stock, crypto, and forex."""
    symbol, market = parse_market_symbol(symbol, market)

    if market == "CRYPTO":
        action = "crypto.events"
        resolved_market = "global"
    elif market == "FOREX":
        action = "forex.events"
        resolved_market = "global"
    else:
        action = "stock.company_events"
        resolved_market = market

    items = gateway.execute(
        action=action,
        market=resolved_market,
        required_tier=DataTier.FREE,
        symbol=symbol,
        limit=limit,
        provider=provider
    )

    data_list = [item.model_dump() for item in items]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list
