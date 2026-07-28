from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

class USCompanyProfile(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    headcount: Optional[int] = None
    description: Optional[str] = None
    provider: str
    market: str = "us"
    asset_class: str = "stock"

class USFinancials(BaseModel):
    symbol: str
    period_type: str
    available_periods: List[str]
    periods: List[Dict[str, Any]]
    provider: str
    market: str = "us"
    asset_class: str = "stock"

class USDividendEntry(BaseModel):
    ex_date: Optional[str] = None
    pay_date: Optional[str] = None
    amount: float
    type: Optional[str] = None

class USDividends(BaseModel):
    symbol: str
    dividends: List[USDividendEntry]
    provider: str
    market: str = "us"
    asset_class: str = "stock"

class USSplitEntry(BaseModel):
    date: str
    ratio: float

class USSplits(BaseModel):
    symbol: str
    splits: List[USSplitEntry]
    provider: str
    market: str = "us"
    asset_class: str = "stock"

class USCalendar(BaseModel):
    symbol: str
    calendar: Dict[str, Any]
    provider: str
    market: str = "us"
    asset_class: str = "stock"

class USNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: Union[int, str]
    publisher: Optional[str] = None
    summary: Optional[str] = None

class USNews(BaseModel):
    symbol: str
    news: List[USNewsEntry]
    provider: str
    market: str = "us"
    asset_class: str = "stock"
