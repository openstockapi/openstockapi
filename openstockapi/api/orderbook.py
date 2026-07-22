from typing import Optional, Union, Any, List
from openstockapi.core.types import DataTier
from openstockapi.core.security import enforce_tier_and_rate_limit
from openstockapi.core.utils import clean_symbol, parse_market_symbol
from openstockapi.config.settings import get_default_providers
from openstockapi.providers import get_provider
from openstockapi.core.exceptions import ProviderUnavailableError

# Optional import for Pandas support
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def bid_ask(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    # PRO or PREMIUM Tier required
    enforce_tier_and_rate_limit(DataTier.PRO, "orderbook.bid_ask")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("orderbook", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            ob = p_inst.get_order_book(symbol)
            return ob.model_dump()
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching order book for '{symbol}' (market={market}): {last_err}")

def depth(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    # 10-level depth api
    enforce_tier_and_rate_limit(DataTier.PRO, "orderbook.depth")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else ["dnse"]
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            ob = p_inst.get_order_book(symbol)
            return ob.model_dump()
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching depth for '{symbol}' (market={market}): {last_err}")

def ticks(symbol: str, limit: int = 100, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.PRO, "orderbook.ticks")
    symbol, market = parse_market_symbol(symbol, market)
    
    # Priority for ticks: mas, then kbs
    providers_to_try = [provider] if provider else ["mas", "kbs"]
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            entries = p_inst.get_intraday_ticks(symbol, limit)
            data_list = [entry.model_dump() for entry in entries]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching ticks for '{symbol}' (market={market}): {last_err}")

