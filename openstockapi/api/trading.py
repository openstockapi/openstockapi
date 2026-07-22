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

def foreign(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.PRO, "trading.foreign")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("trading", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            records = p_inst.get_foreign_trading(symbol, limit)
            data_list = [rec.model_dump() for rec in records]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
    raise ProviderUnavailableError(f"No provider succeeded in fetching foreign trading for '{symbol}' (market={market}): {last_err}")

def insider(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.PRO, "trading.insider")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("trading", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            records = p_inst.get_insider_trading(symbol, limit)
            data_list = [rec.model_dump() for rec in records]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
    raise ProviderUnavailableError(f"No provider succeeded in fetching insider transactions for '{symbol}' (market={market}): {last_err}")

def prop_trade(symbol: str, limit: int = 10, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.PRO, "trading.prop_trade")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("trading", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            records = p_inst.get_prop_trading(symbol, limit)
            data_list = [rec.model_dump() for rec in records]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
    raise ProviderUnavailableError(f"No provider succeeded in fetching proprietary trading for '{symbol}' (market={market}): {last_err}")

