from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

class JPCompanyProfile(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    headcount: Optional[int] = None
    description: Optional[str] = None
    provider: str
    market: str = "jp"
    asset_class: str = "stock"

class JPFinancials(BaseModel):
    symbol: str
    period_type: str
    available_periods: List[str]
    periods: List[Dict[str, Any]]
    provider: str
    market: str = "jp"
    asset_class: str = "stock"

class JPDividendEntry(BaseModel):
    ex_date: Optional[str] = None
    pay_date: Optional[str] = None
    amount: float
    type: Optional[str] = None

class JPDividends(BaseModel):
    symbol: str
    dividends: List[JPDividendEntry]
    provider: str
    market: str = "jp"
    asset_class: str = "stock"

class JPSplitEntry(BaseModel):
    date: str
    ratio: float

class JPSplits(BaseModel):
    symbol: str
    splits: List[JPSplitEntry]
    provider: str
    market: str = "jp"
    asset_class: str = "stock"

class JPCalendar(BaseModel):
    symbol: str
    calendar: Dict[str, Any]
    provider: str
    market: str = "jp"
    asset_class: str = "stock"

class JPNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: Union[int, str]
    publisher: Optional[str] = None
    summary: Optional[str] = None

class JPNews(BaseModel):
    symbol: str
    news: List[JPNewsEntry]
    provider: str
    market: str = "jp"
    asset_class: str = "stock"

class JPRatios(BaseModel):
    symbol: str
    ratios: Dict[str, Any]
    provider: str
    market: str = "jp"
    asset_class: str = "stock"
