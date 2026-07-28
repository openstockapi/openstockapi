from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ASXCompanyProfile(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    headcount: Optional[int] = None
    description: Optional[str] = None
    provider: str
    market: str = "asx"
    asset_class: str = "stock"

class ASXFinancials(BaseModel):
    symbol: str
    financials: Dict[str, Any]
    ratios: Dict[str, Any]
    provider: str
    market: str = "asx"
    asset_class: str = "stock"

class ASXDividendEntry(BaseModel):
    ex_date: Optional[str] = None
    pay_date: Optional[str] = None
    amount: float
    type: Optional[str] = None
    franking: Optional[float] = None

class ASXDividends(BaseModel):
    symbol: str
    dividends: List[ASXDividendEntry]
    provider: str
    market: str = "asx"
    asset_class: str = "stock"

class ASXAnnouncementEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: str
    size: Optional[str] = None

class ASXAnnouncements(BaseModel):
    symbol: str
    announcements: List[ASXAnnouncementEntry]
    provider: str
    market: str = "asx"
    asset_class: str = "stock"

class ASXNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: str
    publisher: Optional[str] = None
    summary: Optional[str] = None

class ASXNews(BaseModel):
    symbol: str
    news: List[ASXNewsEntry]
    provider: str
    market: str = "asx"
    asset_class: str = "stock"
