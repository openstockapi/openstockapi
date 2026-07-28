from typing import List, Optional, Union, Any
from openstockapi.core.types import DataTier
from openstockapi.core.utils import parse_market_symbol
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def _fetch_financial(symbol: str, stmt_type: str, period: str, provider: Optional[str], market: str = "VN") -> Union[List[dict], Any]:
    symbol, market = parse_market_symbol(symbol, market)
    
    # Map raw types to standard action names
    action_map = {
        "income": "stock.income_statement",
        "balance": "stock.balance_sheet",
        "cashflow": "stock.cashflow",
        "ratios": "stock.ratios",
    }
    action = action_map.get(stmt_type, "stock.financials")

    reports = gateway.execute(
        action=action,
        market=market,
        required_tier=DataTier.FREE,
        symbol=symbol,
        period=period,
        provider=provider
    )

    data_list = [rep.model_dump() for rep in reports]
    if HAS_PANDAS:
        return pd.DataFrame(data_list)
    return data_list

def income_statement(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get income statement."""
    return _fetch_financial(symbol, "income", period, provider, market)

def balance_sheet(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get balance sheet."""
    return _fetch_financial(symbol, "balance", period, provider, market)

def cashflow(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get cashflow statement."""
    return _fetch_financial(symbol, "cashflow", period, provider, market)

def ratios(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    """Get financial ratios."""
    return _fetch_financial(symbol, "ratios", period, provider, market)
