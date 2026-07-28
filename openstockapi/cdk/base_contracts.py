"""
CDK Base Contracts
==================
Defines the Abstract Base Classes (ABCs) that all OpenStockAPI providers must inherit.

These contracts enforce:
  - Required method signatures with correct return types.
  - Mandatory class-level metadata (name, market, asset_class, required_tier, supported_methods).
  - Separation of concerns: stock / crypto / forex providers are distinct hierarchies.

Design principles:
  - FAIL FAST: Python raises TypeError at instantiation if @abstractmethod not implemented.
  - BACKWARD COMPATIBLE: Existing providers (KBSProvider, VCIProvider, etc.) can migrate
    with a one-line change — just swap `BaseProvider` for `BaseStockProvider`.
  - NON-INTRUSIVE: No changes to core/gateway.py or existing logic.
"""

from abc import abstractmethod
from typing import List, Optional, Any

from openstockapi.core.base_provider import BaseProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models import (
    OHLCVBar,
    FinancialItem,
    CompanyProfile,
    RealtimeQuote,
    OrderBook,
    IntradayTick,
    CryptoProfile,
    ForexProfile,
)
from openstockapi.core.models_trading import (
    ForeignTradingEntry,
    PropTradingEntry,
    InsiderTradingEntry,
)
from openstockapi.core.models_news import (
    CompanyNewsEntry,
    CompanyEventEntry,
    CryptoNewsEntry,
    CryptoEventEntry,
    ForexNewsEntry,
    ForexEventEntry,
)


# ──────────────────────────────────────────────────────────────────────────────
# BaseStockProvider
# ──────────────────────────────────────────────────────────────────────────────

class BaseStockProvider(BaseProvider):
    """
    Abstract base class for all Stock Market data providers.

    Subclasses MUST implement:
        - get_ohlcv()
        - get_financial_statements()

    Subclasses SHOULD override (if the data source supports it):
        - get_company_profile()
        - get_realtime_quote()
        - get_order_book()
        - get_intraday_ticks()
        - get_foreign_trading()
        - get_prop_trading()
        - get_insider_trading()
        - get_company_news()
        - get_company_events()

    Required class attributes:
        name (str):
            Unique lowercase identifier used as the key in the PROVIDERS registry.
            Example: "kbs", "vci", "ssi"

        market (str):
            Market code this provider serves.
            Example: "VN", "US", "JP", "CN", "HK", "AU"

        asset_class (str):
            Always "stock" for stock providers. Do not override.

        required_tier (DataTier):
            The minimum subscription tier needed to access this provider.
            Defaults to DataTier.FREE.

        supported_methods (List[str]):
            Explicit list of method names this provider implements beyond the
            two abstract ones. Used by CDK test suite to know which contract
            tests to run automatically.
            Example: ["get_company_profile", "get_company_news"]

    Example:
        class SSIProvider(BaseStockProvider):
            name = "ssi"
            market = "VN"
            required_tier = DataTier.FREE
            supported_methods = [
                "get_company_profile",
                "get_company_news",
            ]

            def get_ohlcv(self, symbol, resolution, from_date, to_date):
                ...

            def get_financial_statements(self, symbol, stmt_type, period):
                ...
    """

    asset_class: str = "stock"
    supported_methods: List[str] = []

    # ── Abstract Methods (MUST implement) ─────────────────────────────────────

    @abstractmethod
    def get_ohlcv(
        self,
        symbol: str,
        resolution: str,
        from_date: str,
        to_date: str,
    ) -> List[OHLCVBar]:
        """
        Fetch OHLCV historical price data for a given symbol.

        Args:
            symbol:     Stock ticker (e.g. "HPG", "AAPL").
            resolution: Time resolution — "1D" (daily), "1W" (weekly), "1M" (monthly).
            from_date:  Start date string in any format supported by parse_date().
            to_date:    End date string in any format supported by parse_date().

        Returns:
            List[OHLCVBar]: Validated Pydantic models, sorted ascending by timestamp.

        Raises:
            DataParseError:         If the provider response cannot be parsed.
            ProviderUnavailableError: If the upstream API is unreachable.

        CDK Contract (enforced by CDK-101 to CDK-109):
            - All price fields (open, high, low, close) must be float and > 0.
            - volume must be float and >= 0.
            - timestamp must be a valid datetime object.
            - Results must be sorted ascending by timestamp.
            - high >= open, close, low (OHLCV integrity).
            - low  <= open, close, high (OHLCV integrity).
            - symbol field in each bar must match the input symbol.
            - provider field must match the class attribute `name`.
        """
        pass

    @abstractmethod
    def get_financial_statements(
        self,
        symbol: str,
        stmt_type: str,
        period: str,
    ) -> List[FinancialItem]:
        """
        Fetch financial statements for a given symbol.

        Args:
            symbol:    Stock ticker.
            stmt_type: Statement type — "income" | "balance" | "cashflow" | "ratios".
            period:    Reporting period — "annual" | "quarterly".

        Returns:
            List[FinancialItem]: Validated Pydantic models, one per reporting period.

        CDK Contract (enforced by CDK-201 to CDK-205):
            - statement_type must be one of: "income", "balance", "cashflow", "ratios".
            - year must be an integer in range 2000–2040.
            - items values must be float or None — never strings or raw objects.
            - symbol field must match the input symbol.
        """
        pass

    # ── Optional Methods (override if supported) ───────────────────────────────

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise NotImplementedError(f"{self.__class__.__name__} does not support company profiles.")

    def get_realtime_quote(self, symbol: str) -> RealtimeQuote:
        raise NotImplementedError(f"{self.__class__.__name__} does not support realtime quotes.")

    def get_order_book(self, symbol: str) -> OrderBook:
        raise NotImplementedError(f"{self.__class__.__name__} does not support order book depth.")

    def get_intraday_ticks(self, symbol: str, limit: int = 100) -> List[IntradayTick]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support intraday ticks.")

    def get_foreign_trading(self, symbol: str, limit: int = 10) -> List[ForeignTradingEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support foreign trading data.")

    def get_prop_trading(self, symbol: str, limit: int = 10) -> List[PropTradingEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support proprietary trading data.")

    def get_insider_trading(self, symbol: str, limit: int = 10) -> List[InsiderTradingEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support insider trading data.")

    def get_company_news(self, symbol: str, limit: int = 10) -> List[CompanyNewsEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support company news.")

    def get_company_events(self, symbol: str, limit: int = 10) -> List[CompanyEventEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support company events.")

    async def async_get_ohlcv(
        self,
        symbol: str,
        resolution: str,
        from_date: str,
        to_date: str,
    ) -> List[OHLCVBar]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support async OHLCV.")

    async def async_get_financial_statements(
        self,
        symbol: str,
        stmt_type: str,
        period: str,
    ) -> List[FinancialItem]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support async financial statements.")


# ──────────────────────────────────────────────────────────────────────────────
# BaseCryptoProvider
# ──────────────────────────────────────────────────────────────────────────────

class BaseCryptoProvider(BaseProvider):
    """
    Abstract base class for all Cryptocurrency data providers.

    Subclasses MUST implement:
        - get_crypto_ohlcv()
        - get_crypto_profile()

    Required class attributes:
        name (str):           Unique lowercase identifier (e.g. "binance", "coinbase").
        market (str):         Always "GLOBAL" for crypto providers.
        asset_class (str):    Always "crypto". Do not override.
        required_tier:        Minimum DataTier required.
        supported_methods:    List of optional method names this provider implements.

    Example:
        class BinanceProvider(BaseCryptoProvider):
            name = "binance"
            market = "GLOBAL"
            required_tier = DataTier.FREE
            supported_methods = ["get_crypto_news", "get_crypto_events"]

            def get_crypto_ohlcv(self, symbol, resolution, from_date, to_date):
                ...

            def get_crypto_profile(self, symbol):
                ...
    """

    asset_class: str = "crypto"
    supported_methods: List[str] = []

    @abstractmethod
    def get_crypto_ohlcv(
        self,
        symbol: str,
        resolution: str,
        from_date: str,
        to_date: str,
    ) -> List[OHLCVBar]:
        """
        Fetch OHLCV historical price data for a crypto symbol.

        Returns:
            List[OHLCVBar]: Sorted ascending by timestamp.
        """
        pass

    @abstractmethod
    def get_crypto_profile(self, symbol: str) -> CryptoProfile:
        """
        Fetch profile/metadata for a crypto asset.

        Returns:
            CryptoProfile: Validated Pydantic model.
        """
        pass

    # ── Optional Methods ───────────────────────────────────────────────────────

    def get_crypto_news(self, limit: int = 20) -> List[CryptoNewsEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto news.")

    def get_crypto_events(self) -> List[CryptoEventEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto events.")

    def get_crypto_symbols(self) -> List[Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto symbol listing.")

    def get_crypto_depth(self, symbol: str) -> Any:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto order book depth.")

    def get_crypto_options_instruments(
        self,
        currency: str = "BTC",
        kind: str = "option",
        provider: Optional[str] = None,
    ) -> List[Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto options instruments.")

    def get_crypto_options_chain(
        self,
        currency: str = "BTC",
        provider: Optional[str] = None,
    ) -> List[Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto options chain.")

    def get_crypto_options_ticker(
        self,
        instrument_name: str,
        provider: Optional[str] = None,
    ) -> Any:
        raise NotImplementedError(f"{self.__class__.__name__} does not support crypto options ticker.")


# ──────────────────────────────────────────────────────────────────────────────
# BaseForexProvider
# ──────────────────────────────────────────────────────────────────────────────

class BaseForexProvider(BaseProvider):
    """
    Abstract base class for all Forex / FX data providers.

    Subclasses MUST implement:
        - get_forex_ohlcv()
        - get_forex_rates()

    Required class attributes:
        name (str):           Unique lowercase identifier (e.g. "oanda", "fxcm").
        market (str):         Always "GLOBAL" for forex providers.
        asset_class (str):    Always "forex". Do not override.
        required_tier:        Minimum DataTier required.
        supported_methods:    List of optional method names this provider implements.

    Example:
        class OandaProvider(BaseForexProvider):
            name = "oanda"
            market = "GLOBAL"
            required_tier = DataTier.PRO
            supported_methods = ["get_forex_news", "get_commodities_prices"]

            def get_forex_ohlcv(self, symbol, resolution, from_date, to_date):
                ...

            def get_forex_rates(self, base, quote):
                ...
    """

    asset_class: str = "forex"
    supported_methods: List[str] = []

    @abstractmethod
    def get_forex_ohlcv(
        self,
        symbol: str,
        resolution: str,
        from_date: str,
        to_date: str,
    ) -> List[OHLCVBar]:
        """
        Fetch OHLCV historical price data for a forex pair.

        Returns:
            List[OHLCVBar]: Sorted ascending by timestamp.
        """
        pass

    @abstractmethod
    def get_forex_rates(self, base: str, quote: str) -> Any:
        """
        Fetch current exchange rates.

        Args:
            base:  Base currency code (e.g. "USD").
            quote: Quote currency code (e.g. "VND").

        Returns:
            Exchange rate data (structure depends on provider).
        """
        pass

    # ── Optional Methods ───────────────────────────────────────────────────────

    def get_forex_profile(self, symbol: str) -> ForexProfile:
        raise NotImplementedError(f"{self.__class__.__name__} does not support forex profile.")

    def get_forex_symbols(self) -> List[Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support forex symbol listing.")

    def get_forex_news(self, limit: int = 20) -> List[ForexNewsEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support forex news.")

    def get_forex_events(self) -> List[ForexEventEntry]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support forex events.")

    def get_commodities_prices(self) -> List[Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support commodities prices.")

    def get_global_indices_etf(self) -> List[Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support global indices/ETF data.")

    def compare_forex_rates(self, base: str, targets: List[str]) -> Any:
        raise NotImplementedError(f"{self.__class__.__name__} does not support forex rate comparison.")
