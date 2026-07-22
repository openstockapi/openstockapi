from typing import Optional, Union, Any
from openstockapi.core.types import DataTier
from openstockapi.core.security import enforce_tier_and_rate_limit
from openstockapi.config.settings import DEFAULT_PROVIDER_PRIORITY
from openstockapi.providers import get_provider
from openstockapi.core.exceptions import ProviderUnavailableError

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def details(fund_id: int, provider: Optional[str] = None) -> Union[dict, Any]:
    # Mutual fund data is a FREE endpoint
    enforce_tier_and_rate_limit(DataTier.FREE, "fund.details")
    
    providers_to_try = [provider] if provider else DEFAULT_PROVIDER_PRIORITY.get("fund", ["fmarket"])
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            fund_data = p_inst.get_fund_details(fund_id)
            return fund_data.model_dump()
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching details for fund_id '{fund_id}': {last_err}")
