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
    volume: float
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class FinancialItem(BaseModel):
    symbol: str
    year: int
    quarter: Optional[int] = None
    statement_type: str  # "income", "balance", "cashflow", "ratios"
    items: Dict[str, Optional[float]]
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class CompanyProfile(BaseModel):
    symbol: str
    full_name: str
    en_name: Optional[str] = None
    exchange: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
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
    market: str = "vn"
    asset_class: str = "stock"


class RealtimeQuote(BaseModel):
    symbol: str
    price: float
    change: float
    pct_change: float
    volume: float
    timestamp: datetime
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class OrderBookEntry(BaseModel):
    price: float
    volume: float

class OrderBook(BaseModel):
    symbol: str
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]
    timestamp: datetime
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class NewsItem(BaseModel):
    symbol: str
    title: str
    url: Optional[str] = None
    source: Optional[str] = None
    publish_date: datetime
    summary: Optional[str] = None
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class FundItem(BaseModel):
    fund_code: str
    name: str
    nav: float
    provider: str

class IntradayTick(BaseModel):
    symbol: str
    timestamp: datetime
    price: float
    volume: float
    side: str  # "BUY", "SELL", or "UNKNOWN"
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class OptionsInstrument(BaseModel):
    instrument_name: str
    currency: str
    kind: str
    strike: float
    expiration_timestamp: int
    option_type: str
    is_active: bool
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class OptionsChainEntry(BaseModel):
    instrument_name: str
    underlying_price: Optional[float] = None
    mark_price: Optional[float] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    mark_iv: Optional[float] = None
    bid_iv: Optional[float] = None
    ask_iv: Optional[float] = None
    volume: float
    open_interest: Optional[float] = None
    creation_timestamp: int
    provider: str
    market: str = "vn"
    asset_class: str = "stock"

class OptionsGreeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: Optional[float] = None

class OptionsTicker(BaseModel):
    instrument_name: str
    underlying_index: str
    underlying_price: Optional[float] = None
    mark_price: Optional[float] = None
    mark_iv: Optional[float] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    last_price: Optional[float] = None
    volume: float
    open_interest: Optional[float] = None
    settlement_price: Optional[float] = None
    timestamp: int
    greeks: OptionsGreeks
    provider: str
    market: str = "vn"
    asset_class: str = "stock"


class DerivativeProfile(BaseModel):
    symbol: str
    full_name: str
    underlying_symbol: str
    exchange: str
    first_trading_date: Optional[datetime] = None
    last_trading_date: Optional[datetime] = None
    reference_price: float
    ceiling_price: float
    floor_price: float
    open_interest: Optional[int] = None
    # Warrant specific fields
    warrant_type: Optional[str] = None  # e.g., "Call" or "Put"
    exercise_price: Optional[float] = None
    conversion_ratio: Optional[float] = None
    provider: str
    market: str = "vn"
    asset_class: str = "derivative"


class CryptoProfile(BaseModel):
    symbol: str
    name: str
    id: str
    categories: List[str]
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    market_cap_rank: Optional[int] = None
    provider: str
    market: str = "global"
    asset_class: str = "crypto"


class ForexProfile(BaseModel):
    symbol: str
    base_currency: str
    quote_currency: str
    base_logo_url: Optional[str] = None
    quote_logo_url: Optional[str] = None
    category: str
    provider: str
    market: str = "global"
    asset_class: str = "forex"


class HeatmapItem(BaseModel):
    symbol: str
    name: str
    change: float
    price: Optional[float] = None
    change_pct: Optional[float] = None
    market_cap: Optional[float] = None
    sector: str
    industry: str
    logo_url: Optional[str] = None
    provider: str
    market: str = "us"
    asset_class: str = "stock"





