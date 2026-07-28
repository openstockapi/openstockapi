from typing import Optional, Union, Any
from openstockapi.core.types import DataTier
from openstockapi.core.gateway import gateway

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def details(fund_id: int, provider: Optional[str] = None) -> Union[dict, Any]:
    """Get mutual fund details."""
    fund_data = gateway.execute(
        action="stock.fund_details",
        market="VN",
        required_tier=DataTier.FREE,
        fund_id=fund_id,
        provider=provider
    )
    return fund_data.model_dump()
