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

def news(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    # News is a FREE endpoint
    enforce_tier_and_rate_limit(DataTier.FREE, "news")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("news", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            items = p_inst.get_company_news(symbol, limit)
            data_list = [item.model_dump() for item in items]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching news for symbol '{symbol}' (market={market}): {last_err}")

def events(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.FREE, "events")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("events", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            items = p_inst.get_company_events(symbol, limit)
            data_list = [item.model_dump() for item in items]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching events for symbol '{symbol}' (market={market}): {last_err}")

