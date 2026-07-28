from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

class HKCompanyProfile(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    headcount: Optional[int] = None
    description: Optional[str] = None
    provider: str
    market: str = "hk"
    asset_class: str = "stock"

class HKFinancials(BaseModel):
    symbol: str
    period_type: str
    available_periods: List[str]
    periods: List[Dict[str, Any]]
    provider: str
    market: str = "hk"
    asset_class: str = "stock"

class HKDividendEntry(BaseModel):
    ex_date: Optional[str] = None
    pay_date: Optional[str] = None
    amount: float
    type: Optional[str] = None

class HKDividends(BaseModel):
    symbol: str
    dividends: List[HKDividendEntry]
    provider: str
    market: str = "hk"
    asset_class: str = "stock"

class HKSplitEntry(BaseModel):
    date: str
    ratio: float

class HKSplits(BaseModel):
    symbol: str
    splits: List[HKSplitEntry]
    provider: str
    market: str = "hk"
    asset_class: str = "stock"

class HKCalendar(BaseModel):
    symbol: str
    calendar: Dict[str, Any]
    provider: str
    market: str = "hk"
    asset_class: str = "stock"

class HKNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: Union[int, str]
    publisher: Optional[str] = None
    summary: Optional[str] = None

class HKNews(BaseModel):
    symbol: str
    news: List[HKNewsEntry]
    provider: str
    market: str = "hk"
    asset_class: str = "stock"

class HKRatios(BaseModel):
    symbol: str
    ratios: Dict[str, Any]
    provider: str
    market: str = "hk"
    asset_class: str = "stock"
