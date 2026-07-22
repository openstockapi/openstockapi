from typing import List, Union, Optional, Any
from openstockapi.core.types import DataTier
from openstockapi.core.security import enforce_tier_and_rate_limit
from openstockapi.core.utils import parse_market_symbol
from openstockapi.config.settings import get_default_providers
from openstockapi.providers import get_provider
from openstockapi.core.exceptions import ProviderUnavailableError
from openstockapi.core.models import OHLCVBar, CompanyProfile, RealtimeQuote

# Optional import for Pandas support
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def ohlcv(symbol: str, resolution: str = "1D", start: Optional[str] = None, end: Optional[str] = None, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    # 1. Enforce safety checks
    enforce_tier_and_rate_limit(DataTier.FREE, "stock.ohlcv")

    # 2. Standardize inputs & parse market
    symbol, market = parse_market_symbol(symbol, market)
    if start is None:
        start = "2020-01-01"
    if end is None:
        import datetime
        end = datetime.datetime.now().strftime("%Y-%m-%d")

    # 3. Resolve provider priority list
    providers_to_try = [provider] if provider else get_default_providers("ohlcv", market)

    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            bars = p_inst.get_ohlcv(symbol, resolution, start, end)
            data_list = [bar.model_dump() for bar in bars]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue

    raise ProviderUnavailableError(f"No provider succeeded in fetching OHLCV for '{symbol}' (market={market}): {last_err}")

async def async_ohlcv(symbol: str, resolution: str = "1D", start: Optional[str] = None, end: Optional[str] = None, provider: Optional[str] = None, market: str = "VN") -> Union[List[dict], Any]:
    enforce_tier_and_rate_limit(DataTier.FREE, "stock.ohlcv")
    symbol, market = parse_market_symbol(symbol, market)
    if start is None:
        start = "2020-01-01"
    if end is None:
        import datetime
        end = datetime.datetime.now().strftime("%Y-%m-%d")

    providers_to_try = [provider] if provider else get_default_providers("ohlcv", market)

    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            bars = await p_inst.async_get_ohlcv(symbol, resolution, start, end)
            data_list = [bar.model_dump() for bar in bars]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue

    raise ProviderUnavailableError(f"No provider succeeded in fetching async OHLCV for '{symbol}' (market={market}): {last_err}")

def profile(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    enforce_tier_and_rate_limit(DataTier.FREE, "stock.profile")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("profile", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            prof = p_inst.get_company_profile(symbol)
            return prof.model_dump()
        except Exception as e:
            last_err = e
            continue

    raise ProviderUnavailableError(f"No provider succeeded in fetching profile for '{symbol}' (market={market}): {last_err}")

def quote(symbol: str, provider: Optional[str] = None, market: str = "VN") -> Union[dict, Any]:
    # PREMIUM / PRO Tier endpoint
    enforce_tier_and_rate_limit(DataTier.PRO, "stock.quote")
    symbol, market = parse_market_symbol(symbol, market)
    
    providers_to_try = [provider] if provider else get_default_providers("quote", market)
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            q = p_inst.get_realtime_quote(symbol)
            return q.model_dump()
        except Exception as e:
            last_err = e
            continue

    raise ProviderUnavailableError(f"No provider succeeded in fetching quote for '{symbol}' (market={market}): {last_err}")

