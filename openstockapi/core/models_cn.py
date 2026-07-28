from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

class CNCompanyProfile(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    headcount: Optional[int] = None
    description: Optional[str] = None
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNFinancials(BaseModel):
    symbol: str
    period_type: str
    available_periods: List[str]
    periods: List[Dict[str, Any]]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNDividendEntry(BaseModel):
    ex_date: Optional[str] = None
    pay_date: Optional[str] = None
    amount: float
    type: Optional[str] = None

class CNDividends(BaseModel):
    symbol: str
    dividends: List[CNDividendEntry]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNSplitEntry(BaseModel):
    date: str
    ratio: float

class CNSplits(BaseModel):
    symbol: str
    splits: List[CNSplitEntry]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNCalendar(BaseModel):
    symbol: str
    calendar: Dict[str, Any]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: Union[int, str]
    publisher: Optional[str] = None
    summary: Optional[str] = None

class CNNews(BaseModel):
    symbol: str
    news: List[CNNewsEntry]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNRatios(BaseModel):
    symbol: str
    ratios: Dict[str, Any]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNRealtimeQuote(BaseModel):
    symbol: str
    price: float
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    timestamp: Union[int, str]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNIntradayTick(BaseModel):
    symbol: str
    time: str
    price: float
    volume: float
    provider: str
    market: str = "cn"
    asset_class: str = "stock"

class CNOrderBookEntry(BaseModel):
    price: float
    volume: float

class CNOrderBook(BaseModel):
    symbol: str
    bids: List[CNOrderBookEntry]
    asks: List[CNOrderBookEntry]
    provider: str
    market: str = "cn"
    asset_class: str = "stock"
