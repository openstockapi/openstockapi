from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ForeignTradingEntry(BaseModel):
    symbol: str
    date: datetime
    buy_volume: float
    buy_value: float
    sell_volume: float
    sell_value: float
    net_volume: float
    net_value: float
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class PropTradingEntry(BaseModel):
    symbol: str
    date: datetime
    buy_volume: float
    buy_value: float
    sell_volume: float
    sell_value: float
    net_volume: float
    net_value: float
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class InsiderTradingEntry(BaseModel):
    symbol: str
    trader_name: str
    position: Optional[str] = None
    relationship: Optional[str] = None
    action_type: str  # "Buy" or "Sell"
    registered_volume: float
    actual_volume: Optional[float] = None
    trade_status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    post_volume: float
    provider: str
    market: str = "vn"
    asset_class: str = "stock"
