from typing import List, Optional, Union, Any
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def indicators(market: Optional[str] = "VN", provider: Optional[str] = None) -> Union[List[dict], Any]:
    """Get macroeconomic indicators."""
    records = gateway.execute(
        action="stock.macro_indicators",
        market=market or "VN",
        required_tier=DataTier.FREE,
        provider=provider
    )
    data_list = [rec.model_dump() for rec in records]
    if HAS_PANDAS:
        import numpy as np
        df = pd.DataFrame(data_list)
        return df.replace({np.nan: None})
    return data_list
