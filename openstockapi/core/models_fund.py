from pydantic import BaseModel
from typing import List, Optional

class FundHolding(BaseModel):
    ticker: str
    name: Optional[str] = None
    net_asset_percent: float
    asset_value: Optional[float] = None
    volume: Optional[float] = None

class FundDetails(BaseModel):
    fund_id: int
    name: str
    short_name: str
    code: str
    price: float
    nav: float
    expected_return: Optional[float] = None
    management_fee: Optional[float] = None
    description: Optional[str] = None
    holdings: List[FundHolding]
    provider: str
