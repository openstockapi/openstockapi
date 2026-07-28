from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CompanyNewsEntry(BaseModel):
    symbol: str
    news_id: int
    title: str
    publish_date: datetime
    url: Optional[str] = None
    summary: Optional[str] = None
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class CompanyEventEntry(BaseModel):
    symbol: str
    event_id: Optional[str] = None
    title: str
    event_date: Optional[datetime] = None
    details: Optional[str] = None
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class CryptoNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: datetime
    source: str
    summary: Optional[str] = None
    provider: str = "core"
    market: str = "global"
    asset_class: str = "crypto"

class CryptoEventEntry(BaseModel):
    title: str
    description: Optional[str] = None
    organizer: Optional[str] = None
    start_date: str
    end_date: str
    website: Optional[str] = None
    venue: Optional[str] = None
    country: Optional[str] = None
    provider: str = "core"
    market: str = "global"
    asset_class: str = "crypto"

class ForexNewsEntry(BaseModel):
    id: str
    title: str
    url: str
    published_at: datetime
    source: str
    summary: Optional[str] = None
    provider: str = "core"
    market: str = "global"
    asset_class: str = "forex"

class ForexEventEntry(BaseModel):
    title: str
    currency: str
    date: str
    time: Optional[str] = None
    impact: Optional[str] = None
    forecast: Optional[str] = None
    previous: Optional[str] = None
    provider: str = "core"
    market: str = "global"
    asset_class: str = "forex"
