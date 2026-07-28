from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from openstockapi.core.types import DataTier
from openstockapi.core.models import OHLCVBar, FinancialItem, CompanyProfile, RealtimeQuote, OrderBook

from openstockapi.core.models_trading import ForeignTradingEntry, PropTradingEntry, InsiderTradingEntry

from openstockapi.core.models_news import CryptoNewsEntry, CryptoEventEntry, ForexNewsEntry, ForexEventEntry

class BaseProvider(ABC):
    name: str = "base"
    required_tier: DataTier = DataTier.FREE

    @abstractmethod
    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        pass

    @abstractmethod
    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        pass

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise NotImplementedError("This provider does not support company profiles")

    def get_realtime_quote(self, symbol: str) -> RealtimeQuote:
        raise NotImplementedError("This provider does not support realtime quotes")

    def get_order_book(self, symbol: str) -> OrderBook:
        raise NotImplementedError("This provider does not support order book depth")

    def get_foreign_trading(self, symbol: str, limit: int = 10) -> List[ForeignTradingEntry]:
        raise NotImplementedError("This provider does not support foreign trading data")

    def get_prop_trading(self, symbol: str, limit: int = 10) -> List[PropTradingEntry]:
        raise NotImplementedError("This provider does not support proprietary trading data")

    def get_insider_trading(self, symbol: str, limit: int = 10) -> List[InsiderTradingEntry]:
        raise NotImplementedError("This provider does not support insider trading transactions")

    def get_macro_indicators(self) -> List[Any]:
        raise NotImplementedError("This provider does not support macro indicators")

    def get_fund_details(self, fund_id: int) -> Any:
        raise NotImplementedError("This provider does not support fund details data")

    def get_company_news(self, symbol: str, limit: int = 10) -> List[Any]:
        raise NotImplementedError("This provider does not support company news data")

    def get_company_events(self, symbol: str, limit: int = 10) -> List[Any]:
        raise NotImplementedError("This provider does not support company events data")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        raise NotImplementedError("This provider does not support async OHLCV")

    async def async_get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        raise NotImplementedError("This provider does not support async financial statements")

    def get_intraday_ticks(self, symbol: str, limit: int = 100) -> List[Any]:
        raise NotImplementedError("This provider does not support intraday matching ticks")

    def get_crypto_options_instruments(self, currency: str = "BTC", kind: str = "option", provider: Optional[str] = None) -> List[Any]:
        raise NotImplementedError("This provider does not support crypto options instruments")

    def get_crypto_options_chain(self, currency: str = "BTC", provider: Optional[str] = None) -> List[Any]:
        raise NotImplementedError("This provider does not support crypto options chain")

    def get_crypto_options_ticker(self, instrument_name: str, provider: Optional[str] = None) -> Any:
        raise NotImplementedError("This provider does not support crypto options ticker")

    def get_crypto_news(self, limit: int = 20) -> List[CryptoNewsEntry]:
        raise NotImplementedError("This provider does not support crypto news")

    def get_crypto_events(self) -> List[CryptoEventEntry]:
        raise NotImplementedError("This provider does not support crypto events")

    def get_forex_news(self, limit: int = 20) -> List[ForexNewsEntry]:
        raise NotImplementedError("This provider does not support forex news")

    def get_forex_events(self) -> List[ForexEventEntry]:
        raise NotImplementedError("This provider does not support forex events")

