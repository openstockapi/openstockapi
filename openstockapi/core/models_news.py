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

class CompanyEventEntry(BaseModel):
    symbol: str
    event_id: Optional[str] = None
    title: str
    event_date: Optional[datetime] = None
    details: Optional[str] = None
    provider: str
