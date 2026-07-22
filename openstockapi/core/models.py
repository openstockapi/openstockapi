from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class OHLCVBar(BaseModel):
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    provider: str

class FinancialItem(BaseModel):
    symbol: str
    year: int
    quarter: Optional[int] = None
    statement_type: str  # "income", "balance", "cashflow", "ratios"
    items: Dict[str, Optional[float]]
    provider: str

class CompanyProfile(BaseModel):
    symbol: str
    full_name: str
    en_name: Optional[str] = None
    exchange: str
    industry: Optional[str] = None
    website: Optional[str] = None
    employees: Optional[int] = None
    tax_code: Optional[str] = None
    ceo: Optional[str] = None
    charter_capital: Optional[float] = None
    shares_outstanding: Optional[int] = None
    address: Optional[str] = None
    shareholders: Optional[List[Dict[str, Any]]] = None
    leaders: Optional[List[Dict[str, Any]]] = None
    subsidiaries: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = None
    provider: str


class RealtimeQuote(BaseModel):
    symbol: str
    price: float
    change: float
    pct_change: float
    volume: int
    timestamp: datetime
    provider: str

class OrderBookEntry(BaseModel):
    price: float
    volume: int

class OrderBook(BaseModel):
    symbol: str
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]
    timestamp: datetime
    provider: str

class NewsItem(BaseModel):
    symbol: str
    title: str
    url: Optional[str] = None
    source: Optional[str] = None
    publish_date: datetime
    summary: Optional[str] = None
    provider: str

class FundItem(BaseModel):
    fund_code: str
    name: str
    nav: float
    provider: str

class IntradayTick(BaseModel):
    symbol: str
    timestamp: datetime
    price: float
    volume: int
    side: str  # "BUY", "SELL", or "UNKNOWN"
    provider: str

