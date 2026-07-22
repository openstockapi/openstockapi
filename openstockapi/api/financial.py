from typing import List, Optional, Union, Any
from openstockapi.core.types import DataTier
from openstockapi.core.security import enforce_tier_and_rate_limit
from openstockapi.core.utils import parse_market_symbol
from openstockapi.config.settings import get_default_providers
from openstockapi.providers import get_provider
from openstockapi.core.exceptions import ProviderUnavailableError

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def _fetch_financial(symbol: str, stmt_type: str, period: str, provider: Optional[str], market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.FREE, f"financial.{stmt_type}")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("financials", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            reports = p_inst.get_financial_statements(symbol, stmt_type, period)
            data_list = [rep.model_dump() for rep in reports]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue

    raise ProviderUnavailableError(f"No provider succeeded in fetching financial statement '{stmt_type}' for '{symbol}' (market={market}): {last_err}")

def income_statement(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    return _fetch_financial(symbol, "income", period, provider, market)

def balance_sheet(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    return _fetch_financial(symbol, "balance", period, provider, market)

def cashflow(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    return _fetch_financial(symbol, "cashflow", period, provider, market)

def ratios(symbol: str, period: str = "Q", provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    return _fetch_financial(symbol, "ratios", period, provider, market)

