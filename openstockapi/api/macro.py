from typing import List, Optional, Union, Any
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

def indicators(provider: Optional[str] = None) -> Union[List[dict], Any]:
    # Macro indicators is a FREE endpoint
    enforce_tier_and_rate_limit(DataTier.FREE, "macro.indicators")
    
    providers_to_try = [provider] if provider else DEFAULT_PROVIDER_PRIORITY.get("macro", ["mbk"])
    
    last_err = None
    for p_name in providers_to_try:
        p_inst = get_provider(p_name)
        if not p_inst:
            continue
        try:
            records = p_inst.get_macro_indicators()
            data_list = [rec.model_dump() for rec in records]
            if HAS_PANDAS:
                return pd.DataFrame(data_list)
            return data_list
        except Exception as e:
            last_err = e
            continue
            
    raise ProviderUnavailableError(f"No provider succeeded in fetching macro indicators: {last_err}")
