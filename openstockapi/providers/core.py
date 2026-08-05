import httpx
import sys
import os
import asyncio
import threading
from typing import List, Dict, Any, Optional

from openstockapi.providers.us_stock.service import us_stock_service
from openstockapi.providers.asx.service import asx_service
from openstockapi.providers.jp_stock.service import jp_stock_service
from openstockapi.providers.cn_stock.service import cn_stock_service
from openstockapi.providers.hk_stock.service import hk_stock_service
from openstockapi.providers.crypto.service import crypto_service
from openstockapi.providers.forex.service import forex_service
from openstockapi.providers.vn_stock.service import vn_stock_service

from openstockapi.core.base_provider import BaseProvider
from openstockapi.core.types import DataTier
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.config.settings import BACKEND_URL
from openstockapi.core.models import OHLCVBar, FinancialItem, OrderBook, OrderBookEntry, OptionsInstrument, OptionsChainEntry, OptionsTicker, CryptoProfile, ForexProfile, HeatmapItem, CompanyProfile, RealtimeQuote, NewsItem, FundItem, IntradayTick, DerivativeProfile
from openstockapi.core.models_news import CryptoNewsEntry, CryptoEventEntry, ForexNewsEntry, ForexEventEntry, CompanyEventEntry
from openstockapi.core.models_asx import ASXCompanyProfile, ASXFinancials, ASXDividendEntry, ASXDividends, ASXAnnouncementEntry, ASXAnnouncements, ASXNewsEntry, ASXNews
from openstockapi.core.models_us import USCompanyProfile, USFinancials, USDividendEntry, USDividends, USSplitEntry, USSplits, USCalendar, USNewsEntry, USNews
from openstockapi.core.models_jp import JPCompanyProfile, JPFinancials, JPDividendEntry, JPDividends, JPSplitEntry, JPSplits, JPCalendar, JPNewsEntry, JPNews, JPRatios
from openstockapi.core.models_cn import CNCompanyProfile, CNFinancials, CNDividendEntry, CNDividends, CNSplitEntry, CNSplits, CNCalendar, CNNewsEntry, CNNews, CNRatios, CNRealtimeQuote, CNIntradayTick, CNOrderBook, CNOrderBookEntry
from openstockapi.core.models_hk import HKCompanyProfile, HKFinancials, HKDividendEntry, HKDividends, HKSplitEntry, HKSplits, HKCalendar, HKNewsEntry, HKNews, HKRatios
from openstockapi.core.utils import parse_date
from datetime import datetime

def _run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        result = [None]
        exception = [None]

        def target():
            try:
                result[0] = asyncio.run(coro)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()
        if exception[0]:
            raise exception[0]
        return result[0]
    else:
        return asyncio.run(coro)


class CoreProvider(BaseProvider):
    """
    Multi-market aggregator provider that delegates to specialized service modules
    (us_stock_service, asx_service, crypto_service, forex_service, etc.).

    Note: CoreProvider is intentionally NOT a subclass of BaseStockProvider /
    BaseCryptoProvider / BaseForexProvider because it handles all asset classes.
    It follows the same CDK metadata conventions for registry compatibility.
    """
    name = "core"
    market = "MULTI"   # Serves US, JP, CN, HK, AU, GLOBAL (crypto/forex)
    asset_class = "multi"
    required_tier = DataTier.PRO  # Some endpoints are PRO/PREMIUM, checked in API layer
    # supported_methods is intentionally not set here — CoreProvider exposes
    # market-specific methods (get_us_ohlcv, get_jp_ohlcv, etc.) that the
    # ProviderCapabilityRegistry resolves via the MARKET_PREFIX_MAP.

    def _get_headers(self) -> Dict[str, str]:
        from openstockapi.license.session import get_current_session
        api_key = None
        session_token = None
        try:
            session = get_current_session()
            api_key = session.api_key
            session_token = session.session_token
        except Exception:
            pass

        headers = {
            "Accept": "application/json",
        }
        if session_token and not session_token.startswith("mock_"):
            headers["Authorization"] = f"Bearer {session_token}"
        elif api_key and api_key != "free" and not api_key.startswith("free"):
            headers["X-API-Key"] = api_key
        return headers

    # --- BaseProvider abstract methods stubs ---
    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[Any]:
        # For global stocks/US stocks fallback if implemented in backend later
        raise NotImplementedError("CoreProvider does not support standard get_ohlcv. Use specific crypto/forex methods instead.")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str, market: Optional[str] = None) -> List[OHLCVBar]:
        if not market:
            from openstockapi.core.utils import parse_market_symbol
            _, market = parse_market_symbol(symbol, default_market="VN")
        
        market_lower = market.lower()
        
        # Translate resolution & from_date for non-VN markets
        range_str = "max"
        interval_str = "1d"
        if market_lower != "vn":
            res_lower = resolution.lower() if resolution else ""
            if res_lower in ("d", "1d"):
                interval_str = "1d"
            elif res_lower in ("w", "1w"):
                interval_str = "1wk"
            elif res_lower in ("m", "1m"):
                interval_str = "1mo"
            else:
                interval_str = resolution

            if from_date:
                from datetime import datetime
                try:
                    start_dt = datetime.strptime(from_date, "%Y-%m-%d")
                    days = (datetime.now() - start_dt).days
                    if days <= 5:
                        range_str = "5d"
                    elif days <= 30:
                        range_str = "1mo"
                    elif days <= 90:
                        range_str = "3mo"
                    elif days <= 180:
                        range_str = "6mo"
                    elif days <= 365:
                        range_str = "1y"
                    elif days <= 365 * 2:
                        range_str = "2y"
                    elif days <= 365 * 5:
                        range_str = "5y"
                    elif days <= 365 * 10:
                        range_str = "10y"
                    else:
                        range_str = "max"
                except Exception:
                    range_str = "max"

        try:
            if market_lower == "vn":
                res = await vn_stock_service.get_ohlcv(symbol, resolution, from_date, to_date)
                return res if res else []
            elif market_lower == "us":
                res = await us_stock_service.get_ohlcv(symbol, range_str=range_str, interval_str=interval_str)
            elif market_lower == "jp":
                res = await jp_stock_service.get_ohlcv(symbol, range_str=range_str, interval_str=interval_str)
            elif market_lower == "cn":
                res = await cn_stock_service.get_ohlcv(symbol, range_str=range_str, interval_str=interval_str)
            elif market_lower == "hk":
                res = await hk_stock_service.get_ohlcv(symbol, range_str=range_str, interval_str=interval_str)
            elif market_lower in ("au", "asx"):
                res = await asx_service.get_ohlcv(symbol, range_str=range_str, interval_str=interval_str)
            elif market_lower == "crypto":
                res = await crypto_service.get_ohlcv(symbol, interval=interval_str, limit=100)
            elif market_lower == "forex":
                from openstockapi.providers.forex.normalizer import parse_forex_pair
                base, target = parse_forex_pair(symbol)
                res = await forex_service.get_ohlcv(symbol=symbol, base=base, target=target, range_str=range_str, interval_str=interval_str)
            else:
                raise NotImplementedError(f"Market '{market}' not supported for async OHLCV in CoreProvider")

            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async {market.upper()} OHLCV: {e}")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[Any]:
        raise NotImplementedError("CoreProvider does not support standard get_financial_statements.")

    def _parse_crypto_ohlcv_response(self, raw_data: List[Dict[str, Any]], symbol: str) -> List[OHLCVBar]:
        return [
            OHLCVBar(
                symbol=symbol.upper(),
                timestamp=parse_date(item["timestamp"]),
                open=float(item["open"]),
                high=float(item["high"]),
                low=float(item["low"]),
                close=float(item["close"]),
                volume=float(item["volume"]) if item.get("volume") is not None else 0.0,
                provider=self.name
            )
            for item in raw_data
        ]

    def _parse_core_ohlcv_response(self, raw_json: Dict[str, Any], default_symbol: str) -> List[OHLCVBar]:
        actual_symbol = raw_json.get("ticker", default_symbol) or raw_json.get("symbol", default_symbol)
        raw_bars = raw_json.get("bars", [])
        provider_name = raw_json.get("provider", self.name)
        return [
            OHLCVBar(
                symbol=actual_symbol.upper(),
                timestamp=parse_date(item["timestamp"]),
                open=float(item["open"]),
                high=float(item["high"]),
                low=float(item["low"]),
                close=float(item["close"]),
                volume=float(item["volume"]) if item.get("volume") is not None else 0.0,
                provider=provider_name
            )
            for item in raw_bars
        ]

    # --- Crypto Endpoints ---
    def get_crypto_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            raw_bars = _run_async(crypto_service.get_ohlcv(symbol, interval=interval, limit=limit, market_type=market_type, provider=provider))
            return [
                OHLCVBar(
                    symbol=symbol.upper(),
                    timestamp=parse_date(item["timestamp"]),
                    open=float(item["open"]),
                    high=float(item["high"]),
                    low=float(item["low"]),
                    close=float(item["close"]),
                    volume=float(item["volume"]) if item.get("volume") is not None else 0.0,
                    provider=item.get("provider", provider or self.name),
                    market="global"
                )
                for item in raw_bars
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto OHLCV from Core Engine: {e}")

    async def async_get_crypto_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            raw_bars = await crypto_service.get_ohlcv(symbol, interval=interval, limit=limit, market_type=market_type, provider=provider)
            return [
                OHLCVBar(
                    symbol=symbol.upper(),
                    timestamp=parse_date(item["timestamp"]),
                    open=float(item["open"]),
                    high=float(item["high"]),
                    low=float(item["low"]),
                    close=float(item["close"]),
                    volume=float(item["volume"]) if item.get("volume") is not None else 0.0,
                    provider=item.get("provider", provider or self.name),
                    market="global"
                )
                for item in raw_bars
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async Crypto OHLCV from Core Engine: {e}")

    def get_crypto_depth(self, symbol: str, limit: int = 100, provider: Optional[str] = None) -> OrderBook:
        try:
            data = _run_async(crypto_service.get_depth(symbol, limit=limit, provider=provider))
            if not data:
                raise ValueError("No depth data returned")
            provider_name = data.get("provider", provider or self.name)
            bids = [OrderBookEntry(price=float(b[0]), volume=float(b[1])) for b in data.get("bids", [])]
            asks = [OrderBookEntry(price=float(a[0]), volume=float(a[1])) for a in data.get("asks", [])]
            return OrderBook(
                symbol=symbol.upper(),
                bids=bids,
                asks=asks,
                timestamp=datetime.now(),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Depth from Core Engine: {e}")

    def get_crypto_derivatives(self, symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
        try:
            data = _run_async(crypto_service.get_derivatives_indicators(symbol, provider=provider))
            if not data:
                return {}
            data["provider"] = data.get("provider", provider or self.name)
            return data
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Derivatives from Core Engine: {e}")

    def get_crypto_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 10, provider: Optional[str] = None) -> Dict[str, Any]:
        try:
            data = _run_async(crypto_service.get_footprint(symbol, timeframe=timeframe, limit=limit, provider=provider))
            if not data:
                return {}
            data["provider"] = data.get("provider", provider or self.name)
            return data
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Footprint from Core Engine: {e}")

    def simulate_crypto_leverage(self, symbol: str, entry_price: float, leverage: float, position_size: float, direction: str) -> Dict[str, Any]:
        try:
            # Note: simulate doesn't use provider parameter, computed locally in service.py
            return crypto_service.simulate_leverage_margin(
                symbol=symbol,
                entry_price=entry_price,
                leverage=leverage,
                position_size=position_size,
                direction=direction
            )
        except Exception as e:
            raise DataParseError(f"Failed to perform leverage simulation from Core Engine: {e}")

    def get_crypto_profile(self, symbol: str, provider: Optional[str] = None) -> CryptoProfile:
        try:
            data = _run_async(crypto_service.get_profile(symbol, provider=provider))
            if not data:
                raise ValueError(f"No profile data returned for symbol '{symbol}'")
            return CryptoProfile(
                symbol=data["symbol"],
                name=data["name"],
                id=data["id"],
                categories=data["categories"],
                website=data.get("website"),
                logo_url=data.get("logo_url"),
                description=data.get("description"),
                market_cap_rank=data.get("market_cap_rank"),
                provider=data["provider"],
                market="global",
                asset_class="crypto"
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Profile from Core Engine: {e}")

    def get_crypto_news(self, limit: int = 20, provider: Optional[str] = None) -> List[CryptoNewsEntry]:
        try:
            raw_news = _run_async(crypto_service.get_news(limit=limit, provider=provider))
            results = []
            for item in raw_news:
                pub_date = parse_date(item.get("published_at"))
                results.append(CryptoNewsEntry(
                    id=item.get("id"),
                    title=item.get("title"),
                    url=item.get("url"),
                    published_at=pub_date,
                    source=item.get("publisher") or item.get("source"),
                    summary=item.get("summary"),
                    provider=item.get("provider", provider or self.name)
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto News from Core Engine: {e}")

    def get_crypto_events(self, provider: Optional[str] = None) -> List[CryptoEventEntry]:
        try:
            raw_events = _run_async(crypto_service.get_events(provider=provider))
            results = []
            for item in raw_events:
                results.append(CryptoEventEntry(
                    title=item.get("title"),
                    description=item.get("description"),
                    organizer=item.get("organizer"),
                    start_date=item.get("start_date"),
                    end_date=item.get("end_date"),
                    website=item.get("website"),
                    venue=item.get("venue"),
                    country=item.get("country"),
                    provider=item.get("provider", provider or self.name)
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Events from Core Engine: {e}")

    def get_crypto_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(crypto_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item["market_cap"],
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="global",
                    asset_class="crypto"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Heatmap from Core Engine: {e}")

    # --- Forex & Commodities Endpoints ---
    def get_forex_rates(self, base: str = "USD", provider: Optional[str] = None) -> Dict[str, Any]:
        try:
            res = _run_async(forex_service.get_rates(base, provider_override=provider))
            if not res:
                raise ValueError("No rates returned")
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Forex Rates: {e}")

    def get_forex_profile(self, symbol: str, provider: Optional[str] = None) -> ForexProfile:
        try:
            data = forex_service.get_profile(symbol)
            if not data:
                raise ValueError(f"No profile data returned for symbol '{symbol}'")
            return ForexProfile(
                symbol=data["symbol"],
                base_currency=data["base_currency"],
                quote_currency=data["quote_currency"],
                base_logo_url=data.get("base_logo_url"),
                quote_logo_url=data.get("quote_logo_url"),
                category=data["category"],
                provider=data["provider"],
                market="global",
                asset_class="forex"
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Forex Profile: {e}")

    def get_forex_ohlcv(self, symbol: Optional[str] = None, base: Optional[str] = None, target: Optional[str] = None, range_val: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        if symbol:
            from openstockapi.providers.forex.normalizer import SymbolNormalizer
            parsed = SymbolNormalizer.parse_forex_pair(symbol)
            if parsed:
                base, target = parsed
        base = base or "USD"
        target = target or "VND"
        try:
            res = _run_async(forex_service.get_forex_ohlcv(base, target, range_str=range_val, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol or f"{base}{target}")
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Forex OHLCV: {e}")

    def get_commodities_prices(self, symbol: str, range_val: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(forex_service.get_commodities(symbol, range_str=range_val, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Commodities Prices: {e}")

    def get_global_indices_etf(self, symbol: str, range_val: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(forex_service.get_indices_etf(symbol, range_str=range_val, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Global Indices & ETF: {e}")

    def compare_forex_rates(self, base: str = "USD") -> Dict[str, Any]:
        try:
            return _run_async(forex_service.get_rate_comparison(base))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Forex Rate Comparison: {e}")

    # --- Symbols/Tickers List Endpoints ---
    def get_crypto_symbols(self, provider: Optional[str] = None) -> Dict[str, Any]:
        try:
            symbols = _run_async(crypto_service.get_symbols(provider=provider))
            return {"symbols": symbols}
        except Exception as e:
            raise DataParseError(f"Failed to fetch Crypto Symbols list: {e}")

    def get_crypto_tickers(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            return _run_async(crypto_service.get_tickers(provider=provider))
        except Exception as e:
            raise DataParseError(f"Failed to fetch Crypto Tickers list: {e}")

    def get_forex_symbols(self, provider: Optional[str] = None) -> Dict[str, Any]:
        try:
            return {
                "forex": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "USDVND", "EURGBP"],
                "commodities": ["GOLD", "SILVER", "CRUDE_OIL", "BRENT_OIL"],
                "indices_etf": ["SPY", "QQQ"]
            }
        except Exception as e:
            raise DataParseError(f"Failed to fetch Forex Symbols list: {e}")

    # --- Options Endpoints ---
    def get_crypto_options_instruments(self, currency: str = "BTC", kind: str = "option", provider: Optional[str] = None) -> List[OptionsInstrument]:
        try:
            inst_list = _run_async(crypto_service.get_options_instruments(currency, kind, provider))
            return [
                OptionsInstrument(
                    instrument_name=item["instrument_name"],
                    currency=item["currency"],
                    kind=item["kind"],
                    strike=float(item["strike"]),
                    expiration_timestamp=int(item["expiration_timestamp"]),
                    option_type=item["option_type"],
                    is_active=bool(item["is_active"]),
                    provider=item.get("provider", provider or self.name)
                )
                for item in inst_list
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Options Instruments: {e}")

    def get_crypto_options_chain(self, currency: str = "BTC", provider: Optional[str] = None) -> List[OptionsChainEntry]:
        try:
            chain_list = _run_async(crypto_service.get_options_chain(currency, provider))
            return [
                OptionsChainEntry(
                    instrument_name=item["instrument_name"],
                    underlying_price=float(item["underlying_price"]) if item.get("underlying_price") is not None else None,
                    mark_price=float(item["mark_price"]) if item.get("mark_price") is not None else None,
                    bid_price=float(item["bid_price"]) if item.get("bid_price") is not None else None,
                    ask_price=float(item["ask_price"]) if item.get("ask_price") is not None else None,
                    mark_iv=float(item["mark_iv"]) if item.get("mark_iv") is not None else None,
                    bid_iv=float(item["bid_iv"]) if item.get("bid_iv") is not None else None,
                    ask_iv=float(item["ask_iv"]) if item.get("ask_iv") is not None else None,
                    volume=float(item["volume"]) if item.get("volume") is not None else 0.0,
                    open_interest=float(item["open_interest"]) if item.get("open_interest") is not None else None,
                    creation_timestamp=int(item["creation_timestamp"]),
                    provider=item.get("provider", provider or self.name)
                )
                for item in chain_list
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Options Chain: {e}")

    def get_crypto_options_ticker(self, instrument_name: str, provider: Optional[str] = None) -> OptionsTicker:
        try:
            item = _run_async(crypto_service.get_options_ticker(instrument_name, provider))
            if not item:
                raise ValueError("No option ticker returned")
            from openstockapi.core.models import OptionsGreeks
            g = item.get("greeks", {})
            greeks = OptionsGreeks(
                delta=float(g["delta"]) if g.get("delta") is not None else 0.0,
                gamma=float(g["gamma"]) if g.get("gamma") is not None else 0.0,
                theta=float(g["theta"]) if g.get("theta") is not None else 0.0,
                vega=float(g["vega"]) if g.get("vega") is not None else 0.0,
                rho=float(g["rho"]) if g.get("rho") is not None else None
            )
            return OptionsTicker(
                instrument_name=item["instrument_name"],
                underlying_index=item.get("underlying_index") or item["instrument_name"].split("-")[0],
                underlying_price=float(item["underlying_price"]) if item.get("underlying_price") is not None else None,
                mark_price=float(item["mark_price"]) if item.get("mark_price") is not None else None,
                mark_iv=float(item["mark_iv"]) if item.get("mark_iv") is not None else None,
                bid_price=float(item["bid_price"]) if item.get("bid_price") is not None else None,
                ask_price=float(item["ask_price"]) if item.get("ask_price") is not None else None,
                last_price=float(item["last_price"]) if item.get("last_price") is not None else None,
                volume=float(item["volume"]) if item.get("volume") is not None else 0.0,
                open_interest=float(item["open_interest"]) if item.get("open_interest") is not None else None,
                settlement_price=float(item["settlement_price"]) if item.get("settlement_price") is not None else None,
                timestamp=int(item["timestamp"]),
                greeks=greeks,
                provider=item.get("provider", provider or self.name)
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Crypto Options Ticker: {e}")

    def get_forex_news(self, limit: int = 20, provider: Optional[str] = None) -> List[ForexNewsEntry]:
        try:
            raw_news = _run_async(forex_service.get_news(limit=limit, provider=provider))
            results = []
            for item in raw_news:
                pub_date = parse_date(item.get("published_at"))
                results.append(ForexNewsEntry(
                    id=item.get("id"),
                    title=item.get("title"),
                    url=item.get("url"),
                    published_at=pub_date,
                    source=item.get("source"),
                    summary=item.get("summary"),
                    provider=item.get("provider", provider or self.name)
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Forex News: {e}")

    def get_forex_events(self, provider: Optional[str] = None) -> List[ForexEventEntry]:
        try:
            raw_events = _run_async(forex_service.get_events(provider=provider))
            results = []
            for item in raw_events:
                results.append(ForexEventEntry(
                    title=item.get("title"),
                    currency=item.get("currency"),
                    date=item.get("date"),
                    time=item.get("time"),
                    impact=item.get("impact"),
                    forecast=item.get("forecast"),
                    previous=item.get("previous"),
                    provider=item.get("provider", provider or self.name)
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Forex Events: {e}")

    # --- ASX Endpoints ---
    # --- ASX Endpoints ---
    def get_au_symbols(self, provider: Optional[str] = None) -> List[str]:
        try:
            return _run_async(asx_service.get_symbols(provider=provider))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX Symbols from Core Engine: {e}")

    def get_au_ohlcv(self, symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(asx_service.get_ohlcv(symbol, range_str=range, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX OHLCV from Core Engine: {e}")

    def get_au_profile(self, symbol: str, provider: Optional[str] = None) -> ASXCompanyProfile:
        try:
            data = _run_async(asx_service.get_profile(symbol, provider=provider))
            if not data:
                raise ValueError("No profile data returned")
            provider_name = data.get("provider", self.name)
            return ASXCompanyProfile(
                symbol=data.get("symbol", symbol.upper()),
                company_name=data.get("company_name", ""),
                sector=data.get("sector"),
                industry=data.get("industry"),
                website=data.get("website"),
                logo_url=data.get("logo_url"),
                headcount=data.get("headcount"),
                description=data.get("description"),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX Company Profile: {e}")

    def get_au_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(asx_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item["market_cap"],
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="au",
                    asset_class="stock"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX Stock Heatmap: {e}")

    def get_vn_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(vn_stock_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item.get("market_cap"),
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="vn",
                    asset_class="stock"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Stock Heatmap: {e}")

    def get_au_financials(self, symbol: str, provider: Optional[str] = None) -> ASXFinancials:
        try:
            data = _run_async(asx_service.get_financials(symbol, provider=provider))
            if not data:
                raise ValueError("No financials data returned")
            provider_name = data.get("provider", self.name)
            return ASXFinancials(
                symbol=data.get("symbol", symbol.upper()),
                financials=data.get("financials", {}),
                ratios=data.get("ratios", {}),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX Financials: {e}")

    def get_au_income_statement(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(asx_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                inc = p.get("financials", {}).get("income_statement", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="income",
                    items={k: float(v) if v is not None else None for k, v in inc.items()},
                    provider=provider_name,
                    market="au",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX income statement: {e}")

    def get_au_balance_sheet(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(asx_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                bs = p.get("financials", {}).get("balance_sheet", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="balance",
                    items={k: float(v) if v is not None else None for k, v in bs.items()},
                    provider=provider_name,
                    market="au",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX balance sheet: {e}")

    def get_au_balance_sheet(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(asx_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                bs = p.get("financials", {}).get("balance_sheet", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="balance",
                    items={k: float(v) if v is not None else None for k, v in bs.items()},
                    provider=provider_name,
                    market="au",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX balance sheet: {e}")

    def get_au_cashflow(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(asx_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                cf = p.get("financials", {}).get("cash_flow", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="cashflow",
                    items={k: float(v) if v is not None else None for k, v in cf.items()},
                    provider=provider_name,
                    market="au",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX cashflow statement: {e}")

    def get_au_ratios(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(asx_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            ratios_dict = data.get("ratios", {})
            year = datetime.now().year
            return [FinancialItem(
                symbol=symbol.upper(),
                year=year,
                quarter=None,
                statement_type="ratios",
                items={k: float(v) if v is not None and isinstance(v, (int, float)) else v for k, v in ratios_dict.items()},
                provider=provider_name,
                market="au",
                asset_class="stock"
            )]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX financial ratios: {e}")

    def get_au_dividends(self, symbol: str, provider: Optional[str] = None) -> ASXDividends:
        try:
            raw_divs = _run_async(asx_service.get_dividends(symbol, provider=provider))
            provider_name = raw_divs[0].get("provider", self.name) if raw_divs else self.name
            divs = [
                ASXDividendEntry(
                    ex_date=item.get("ex_date"),
                    pay_date=item.get("pay_date"),
                    amount=float(item.get("amount", 0.0)),
                    type=item.get("type"),
                    franking=float(item.get("franking")) if item.get("franking") is not None else None
                )
                for item in raw_divs
            ]
            return ASXDividends(
                symbol=symbol.upper(),
                dividends=divs,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX Dividends: {e}")

    def get_au_announcements(self, symbol: str, provider: Optional[str] = None) -> ASXAnnouncements:
        try:
            raw_announcements = _run_async(asx_service.get_announcements(symbol, provider=provider))
            provider_name = raw_announcements[0].get("provider", self.name) if raw_announcements else self.name
            announcements = [
                ASXAnnouncementEntry(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    published_at=item.get("published_at", ""),
                    size=item.get("size")
                )
                for item in raw_announcements
            ]
            return ASXAnnouncements(
                symbol=symbol.upper(),
                announcements=announcements,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX Announcements: {e}")

    def get_au_news(self, symbol: str, provider: Optional[str] = None) -> ASXNews:
        try:
            raw_news = _run_async(asx_service.get_news(symbol, provider=provider))
            provider_name = raw_news[0].get("provider", self.name) if raw_news else self.name
            news_list = [
                ASXNewsEntry(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    published_at=item.get("published_at", ""),
                    publisher=item.get("publisher"),
                    summary=item.get("summary")
                )
                for item in raw_news
            ]
            return ASXNews(
                symbol=symbol.upper(),
                news=news_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse ASX News: {e}")

    # --- VN Endpoints ---
    def get_vn_symbols(self, provider: Optional[str] = None) -> List[str]:
        try:
            return _run_async(vn_stock_service.get_symbols(provider=provider))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Symbols: {e}")

    def get_vn_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str, provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(vn_stock_service.get_ohlcv(symbol, resolution, from_date, to_date, provider))
            if not res:
                return []
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN OHLCV: {e}")

    def get_vn_profile(self, symbol: str, provider: Optional[str] = None) -> CompanyProfile:
        try:
            res = _run_async(vn_stock_service.get_profile(symbol, provider))
            if not res:
                raise ValueError(f"No profile data returned for symbol '{symbol}'")
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Profile: {e}")

    def get_vn_financials(self, symbol: str, period: str = "quarter", provider: Optional[str] = None) -> List[FinancialItem]:
        try:
            res = _run_async(vn_stock_service.get_financials(symbol, "financials", period, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Financials: {e}")

    def get_vn_balance_sheet(self, symbol: str, period: str = "quarter", provider: Optional[str] = None) -> List[FinancialItem]:
        try:
            res = _run_async(vn_stock_service.get_financials(symbol, "balance", period, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Balance Sheet: {e}")

    def get_vn_income_statement(self, symbol: str, period: str = "quarter", provider: Optional[str] = None) -> List[FinancialItem]:
        try:
            res = _run_async(vn_stock_service.get_financials(symbol, "income", period, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Income Statement: {e}")

    def get_vn_cashflow(self, symbol: str, period: str = "quarter", provider: Optional[str] = None) -> List[FinancialItem]:
        try:
            res = _run_async(vn_stock_service.get_financials(symbol, "cashflow", period, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Cashflow: {e}")

    def get_vn_ratios(self, symbol: str, period: str = "quarter", provider: Optional[str] = None) -> List[FinancialItem]:
        try:
            res = _run_async(vn_stock_service.get_financials(symbol, "ratios", period, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Ratios: {e}")

    def get_vn_derivative_profile(self, symbol: str, provider: Optional[str] = None) -> DerivativeProfile:
        try:
            res = _run_async(vn_stock_service.get_derivative_profile(symbol, provider))
            if not res:
                raise ValueError(f"No derivative profile returned for symbol '{symbol}'")
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Derivative Profile: {e}")

    def get_vn_quote(self, symbol: str, provider: Optional[str] = None) -> RealtimeQuote:
        try:
            res = _run_async(vn_stock_service.get_quote(symbol, provider))
            if not res:
                raise ValueError(f"No quote returned for symbol '{symbol}'")
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Quote: {e}")

    def get_vn_order_book(self, symbol: str, provider: Optional[str] = None) -> OrderBook:
        try:
            res = _run_async(vn_stock_service.get_order_book(symbol, provider))
            if not res:
                raise ValueError(f"No order book returned for symbol '{symbol}'")
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Order Book: {e}")

    def get_vn_macro_indicators(self, provider: Optional[str] = None) -> List[Any]:
        try:
            res = _run_async(vn_stock_service.get_macro_indicators(provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Macro Indicators: {e}")

    def get_vn_fund_details(self, fund_id: int, provider: Optional[str] = None) -> FundItem:
        try:
            res = _run_async(vn_stock_service.get_fund_details(fund_id, provider))
            if not res:
                raise ValueError(f"No fund details returned for fund_id '{fund_id}'")
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Fund Details: {e}")

    def get_vn_company_news(self, symbol: str, provider: Optional[str] = None) -> List[NewsItem]:
        try:
            res = _run_async(vn_stock_service.get_news(symbol, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN News: {e}")

    def get_vn_company_events(self, symbol: str, provider: Optional[str] = None) -> List[CompanyEventEntry]:
        try:
            res = _run_async(vn_stock_service.get_events(symbol, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Events: {e}")

    def get_vn_foreign_trading(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        try:
            res = _run_async(vn_stock_service.get_foreign_trading(symbol, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Foreign Trading: {e}")

    def get_vn_prop_trading(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        try:
            res = _run_async(vn_stock_service.get_prop_trading(symbol, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Prop Trading: {e}")

    def get_vn_insider_trading(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        try:
            res = _run_async(vn_stock_service.get_insider_trading(symbol, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Insider Trading: {e}")

    def get_vn_ticks(self, symbol: str, provider: Optional[str] = None) -> List[IntradayTick]:
        try:
            res = _run_async(vn_stock_service.get_intraday_ticks(symbol, provider))
            return res
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Ticks: {e}")

    # --- US Endpoints ---
    def get_us_ohlcv(self, symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(us_stock_service.get_ohlcv(symbol, range_str=range, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US OHLCV from Core Engine: {e}")

    def get_us_profile(self, symbol: str, provider: Optional[str] = None) -> USCompanyProfile:
        try:
            data = _run_async(us_stock_service.get_profile(symbol, provider=provider))
            if not data:
                raise ValueError("No profile data returned")
            provider_name = data.get("provider", self.name)
            return USCompanyProfile(
                symbol=data.get("symbol", symbol.upper()),
                company_name=data.get("company_name", ""),
                sector=data.get("sector"),
                industry=data.get("industry"),
                website=data.get("website"),
                logo_url=data.get("logo_url"),
                headcount=data.get("headcount"),
                description=data.get("description"),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Company Profile: {e}")

    def get_us_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(us_stock_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item["market_cap"],
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="us",
                    asset_class="stock"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Stock Heatmap: {e}")

    def get_us_financials(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> USFinancials:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(us_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                raise ValueError("No financials data returned")
            provider_name = data.get("provider", self.name)
            return USFinancials(
                symbol=data.get("symbol", symbol.upper()),
                period_type=data.get("period_type", backend_period),
                available_periods=data.get("available_periods", []),
                periods=data.get("periods", []),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Financials: {e}")

    def get_us_income_statement(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(us_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                inc = p.get("financials", {}).get("income_statement", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="income",
                    items={k: float(v) if v is not None else None for k, v in inc.items()},
                    provider=provider_name,
                    market="us",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US income statement: {e}")

    def get_us_balance_sheet(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(us_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                bs = p.get("financials", {}).get("balance_sheet", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="balance",
                    items={k: float(v) if v is not None else None for k, v in bs.items()},
                    provider=provider_name,
                    market="us",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US balance sheet: {e}")

    def get_us_cashflow(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(us_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                cf = p.get("financials", {}).get("cash_flow", {}) or p.get("financials", {}).get("cashflow", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="cashflow",
                    items={k: float(v) if v is not None else None for k, v in cf.items()},
                    provider=provider_name,
                    market="us",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US cashflow statement: {e}")

    def get_us_ratios(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(us_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            ratios_dict = data.get("ratios", {})
            year = datetime.now().year
            return [FinancialItem(
                symbol=symbol.upper(),
                year=year,
                quarter=None,
                statement_type="ratios",
                items={k: float(v) if v is not None and isinstance(v, (int, float)) else v for k, v in ratios_dict.items()},
                provider=provider_name,
                market="us",
                asset_class="stock"
            )]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US financial ratios: {e}")

    def get_us_dividends(self, symbol: str, provider: Optional[str] = None) -> USDividends:
        try:
            data = _run_async(us_stock_service.get_dividends(symbol, provider=provider))
            raw_divs = data.get("dividends", [])
            provider_name = data.get("provider", self.name)
            divs = [
                USDividendEntry(
                    ex_date=item.get("ex_date"),
                    pay_date=item.get("pay_date"),
                    amount=float(item.get("amount", 0.0)),
                    type=item.get("type")
                )
                for item in raw_divs
            ]
            return USDividends(
                symbol=symbol.upper(),
                dividends=divs,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Dividends: {e}")

    def get_us_splits(self, symbol: str, provider: Optional[str] = None) -> USSplits:
        try:
            data = _run_async(us_stock_service.get_splits(symbol, provider=provider))
            raw_splits = data.get("splits", [])
            provider_name = data.get("provider", self.name)
            splits = [
                USSplitEntry(
                    date=item.get("date"),
                    ratio=float(item.get("ratio", 1.0))
                )
                for item in raw_splits
            ]
            return USSplits(
                symbol=symbol.upper(),
                splits=splits,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Splits: {e}")

    def get_us_calendar(self, symbol: str, provider: Optional[str] = None) -> USCalendar:
        try:
            data = _run_async(us_stock_service.get_calendar(symbol))
            provider_name = data.get("provider", self.name) if data else self.name
            calendar_data = {k: v for k, v in data.items() if k != "provider"} if data else {}
            return USCalendar(
                symbol=symbol.upper(),
                calendar=calendar_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Calendar: {e}")

    def get_us_news(self, symbol: str, provider: Optional[str] = None) -> USNews:
        try:
            data = _run_async(us_stock_service.get_news(symbol, provider=provider))
            raw_news = data.get("news", [])
            provider_name = data.get("provider", self.name)
            news_list = [
                USNewsEntry(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    published_at=item.get("published_at", 0) if isinstance(item.get("published_at"), (int, str)) else "",
                    publisher=item.get("publisher"),
                    summary=item.get("summary")
                )
                for item in raw_news
            ]
            return USNews(
                symbol=symbol.upper(),
                news=news_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US News: {e}")

    def get_us_symbols(self, provider: Optional[str] = None) -> List[str]:
        try:
            data = _run_async(us_stock_service.get_symbols())
            return data.get("symbols", [])
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse US Symbols from Core Engine: {e}")


    def get_jp_symbols(self, provider: Optional[str] = None) -> List[str]:
        try:
            return _run_async(jp_stock_service.get_symbols(provider=provider))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Symbols from Core Engine: {e}")

    def get_jp_ohlcv(self, symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(jp_stock_service.get_ohlcv(symbol, range_str=range, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP OHLCV: {e}")

    def get_jp_profile(self, symbol: str, provider: Optional[str] = None) -> JPCompanyProfile:
        try:
            data = _run_async(jp_stock_service.get_profile(symbol, provider=provider))
            if not data:
                raise ValueError("No profile data returned")
            provider_name = data.get("provider", self.name)
            return JPCompanyProfile(
                symbol=data.get("symbol", symbol.upper()),
                company_name=data.get("company_name", ""),
                sector=data.get("sector"),
                industry=data.get("industry"),
                website=data.get("website"),
                logo_url=data.get("logo_url"),
                headcount=data.get("headcount"),
                description=data.get("description"),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Company Profile: {e}")

    def get_jp_financials(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> JPFinancials:
        try:
            data = _run_async(jp_stock_service.get_financials(symbol, provider=provider, period=period))
            if not data:
                raise ValueError("No financials data returned")
            provider_name = data.get("provider", self.name)
            return JPFinancials(
                symbol=data.get("symbol", symbol.upper()),
                period_type=data.get("period_type", period),
                available_periods=data.get("available_periods", []),
                periods=data.get("periods", []),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Financials: {e}")

    def get_jp_dividends(self, symbol: str, provider: Optional[str] = None) -> JPDividends:
        try:
            raw_divs = _run_async(jp_stock_service.get_dividends(symbol, provider=provider))
            provider_name = raw_divs[0].get("provider", self.name) if raw_divs else self.name
            div_list = [
                JPDividendEntry(
                    ex_date=item.get("ex_date"),
                    pay_date=item.get("pay_date"),
                    amount=float(item.get("amount", 0.0)),
                    type=item.get("type")
                )
                for item in raw_divs
            ]
            return JPDividends(
                symbol=symbol.upper(),
                dividends=div_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Dividends: {e}")

    def get_jp_splits(self, symbol: str, provider: Optional[str] = None) -> JPSplits:
        try:
            raw_splits = _run_async(jp_stock_service.get_splits(symbol, provider=provider))
            provider_name = raw_splits[0].get("provider", self.name) if raw_splits else self.name
            split_list = [
                JPSplitEntry(
                    date=item.get("date", ""),
                    ratio=float(item.get("ratio", 1.0))
                )
                for item in raw_splits
            ]
            return JPSplits(
                symbol=symbol.upper(),
                splits=split_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Splits: {e}")

    def get_jp_calendar(self, symbol: str, provider: Optional[str] = None) -> JPCalendar:
        try:
            data = _run_async(jp_stock_service.get_calendar(symbol, provider=provider))
            provider_name = data.get("provider", self.name) if data else self.name
            calendar_data = {k: v for k, v in data.items() if k != "provider"} if data else {}
            return JPCalendar(
                symbol=symbol.upper(),
                calendar=calendar_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Calendar: {e}")

    def get_jp_news(self, symbol: str, provider: Optional[str] = None) -> JPNews:
        try:
            raw_news = _run_async(jp_stock_service.get_news(symbol, provider=provider))
            provider_name = raw_news[0].get("provider", self.name) if raw_news else self.name
            news_list = [
                JPNewsEntry(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    published_at=item.get("published_at", 0),
                    publisher=item.get("publisher"),
                    summary=item.get("summary")
                )
                for item in raw_news
            ]
            return JPNews(
                symbol=symbol.upper(),
                news=news_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP News: {e}")

    def get_jp_ratios(self, symbol: str, provider: Optional[str] = None) -> JPRatios:
        try:
            data = _run_async(jp_stock_service.get_ratios(symbol, provider=provider))
            provider_name = data.get("provider", self.name) if data else self.name
            if data:
                if "ratios" in data:
                    ratios_data = data["ratios"]
                else:
                    ratios_data = {k: v for k, v in data.items() if k not in ("provider", "symbol")}
            else:
                ratios_data = {}
            return JPRatios(
                symbol=symbol.upper(),
                ratios=ratios_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Ratios: {e}")

    def get_jp_income_statement(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(jp_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                inc = p.get("financials", {}).get("income_statement", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="income",
                    items={k: float(v) if v is not None else None for k, v in inc.items()},
                    provider=provider_name,
                    market="jp",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP income statement: {e}")

    def get_jp_balance_sheet(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(jp_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                bs = p.get("financials", {}).get("balance_sheet", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="balance",
                    items={k: float(v) if v is not None else None for k, v in bs.items()},
                    provider=provider_name,
                    market="jp",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP balance sheet: {e}")

    def get_jp_cashflow(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(jp_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                cf = p.get("financials", {}).get("cash_flow", {}) or p.get("financials", {}).get("cashflow", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="cashflow",
                    items={k: float(v) if v is not None else None for k, v in cf.items()},
                    provider=provider_name,
                    market="jp",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP cashflow statement: {e}")

    def get_jp_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(jp_stock_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item["market_cap"],
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="jp",
                    asset_class="stock"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse JP Stock Heatmap: {e}")

    # CHINA (CN) MARKET DATA
    def get_cn_symbols(self, provider: Optional[str] = None) -> List[str]:
        try:
            return _run_async(cn_stock_service.get_symbols(provider=provider))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Symbols: {e}")

    def get_cn_ohlcv(self, symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(cn_stock_service.get_ohlcv(symbol, range_str=range, interval_str=interval, provider=provider))
            if not res:
                return []
            return self._parse_core_ohlcv_response(res, symbol)
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN OHLCV: {e}")

    def get_cn_profile(self, symbol: str, provider: Optional[str] = None) -> CNCompanyProfile:
        try:
            data = _run_async(cn_stock_service.get_profile(symbol, provider=provider))
            if not data:
                raise ValueError("No profile data returned")
            provider_name = data.get("provider", self.name)
            return CNCompanyProfile(
                symbol=data.get("symbol", symbol.upper()),
                company_name=data.get("company_name", ""),
                sector=data.get("sector"),
                industry=data.get("industry"),
                website=data.get("website"),
                logo_url=data.get("logo_url"),
                headcount=data.get("headcount"),
                description=data.get("description"),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Profile: {e}")

    def get_cn_financials(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> CNFinancials:
        try:
            data = _run_async(cn_stock_service.get_financials(symbol, provider=provider, period=period))
            if not data:
                raise ValueError("No financials data returned")
            provider_name = data.get("provider", self.name)
            return CNFinancials(
                symbol=data.get("symbol", symbol.upper()),
                period_type=data.get("period_type", period),
                available_periods=data.get("available_periods", []),
                periods=data.get("periods", []),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Financials: {e}")

    def get_cn_income_statement(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(cn_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                inc = p.get("financials", {}).get("income_statement", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="income",
                    items={k: float(v) if v is not None else None for k, v in inc.items()},
                    provider=provider_name,
                    market="cn",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN income statement: {e}")

    def get_cn_balance_sheet(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(cn_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                bs = p.get("financials", {}).get("balance_sheet", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="balance",
                    items={k: float(v) if v is not None else None for k, v in bs.items()},
                    provider=provider_name,
                    market="cn",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN balance sheet: {e}")

    def get_cn_cashflow(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(cn_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                cf = p.get("financials", {}).get("cash_flow", {}) or p.get("financials", {}).get("cashflow", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="cashflow",
                    items={k: float(v) if v is not None else None for k, v in cf.items()},
                    provider=provider_name,
                    market="cn",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN cashflow statement: {e}")

    def get_cn_dividends(self, symbol: str, provider: Optional[str] = None) -> CNDividends:
        try:
            raw_divs = _run_async(cn_stock_service.get_dividends(symbol, provider=provider))
            provider_name = raw_divs[0].get("provider", self.name) if raw_divs else self.name
            div_list = [
                CNDividendEntry(
                    ex_date=item.get("ex_date"),
                    pay_date=item.get("pay_date"),
                    amount=float(item.get("amount", 0.0)),
                    type=item.get("type")
                )
                for item in raw_divs
            ]
            return CNDividends(
                symbol=symbol.upper(),
                dividends=div_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Dividends: {e}")

    def get_cn_splits(self, symbol: str, provider: Optional[str] = None) -> CNSplits:
        try:
            raw_splits = _run_async(cn_stock_service.get_splits(symbol, provider=provider))
            provider_name = raw_splits[0].get("provider", self.name) if raw_splits else self.name
            split_list = [
                CNSplitEntry(
                    date=item.get("date", ""),
                    ratio=float(item.get("ratio", 1.0))
                )
                for item in raw_splits
            ]
            return CNSplits(
                symbol=symbol.upper(),
                splits=split_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Splits: {e}")

    def get_cn_calendar(self, symbol: str, provider: Optional[str] = None) -> CNCalendar:
        try:
            data = _run_async(cn_stock_service.get_calendar(symbol, provider=provider))
            provider_name = data.get("provider", self.name) if data else self.name
            calendar_data = {k: v for k, v in data.items() if k != "provider"} if data else {}
            return CNCalendar(
                symbol=symbol.upper(),
                calendar=calendar_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Calendar: {e}")

    def get_cn_news(self, symbol: str, provider: Optional[str] = None) -> CNNews:
        try:
            raw_news = _run_async(cn_stock_service.get_news(symbol, provider=provider))
            provider_name = raw_news[0].get("provider", self.name) if raw_news else self.name
            news_list = [
                CNNewsEntry(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    published_at=item.get("published_at", 0),
                    publisher=item.get("publisher"),
                    summary=item.get("summary")
                )
                for item in raw_news
            ]
            return CNNews(
                symbol=symbol.upper(),
                news=news_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN News: {e}")

    def get_cn_ratios(self, symbol: str, provider: Optional[str] = None) -> CNRatios:
        try:
            data = _run_async(cn_stock_service.get_ratios(symbol, provider=provider))
            provider_name = data.get("provider", self.name) if data else self.name
            if data:
                if "ratios" in data:
                    ratios_data = data["ratios"]
                else:
                    ratios_data = {k: v for k, v in data.items() if k not in ("provider", "symbol")}
            else:
                ratios_data = {}
            return CNRatios(
                symbol=symbol.upper(),
                ratios=ratios_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Ratios: {e}")

    def get_cn_quote(self, symbol: str, provider: Optional[str] = None) -> CNRealtimeQuote:
        try:
            data = _run_async(cn_stock_service.get_quote(symbol, provider=provider))
            if not data:
                raise ValueError("No quote data returned")
            provider_name = data.get("provider", self.name)
            return CNRealtimeQuote(
                symbol=symbol.upper(),
                price=float(data.get("price", 0.0)),
                open=float(data.get("open")) if data.get("open") is not None else None,
                high=float(data.get("high")) if data.get("high") is not None else None,
                low=float(data.get("low")) if data.get("low") is not None else None,
                volume=float(data.get("volume")) if data.get("volume") is not None else None,
                timestamp=data.get("timestamp", 0),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Quote: {e}")

    def get_cn_ticks(self, symbol: str, provider: Optional[str] = None) -> List[CNIntradayTick]:
        try:
            data = _run_async(cn_stock_service.get_tick(symbol, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            raw_ticks = data.get("ticks", []) if "ticks" in data else ([data] if "price" in data else [])
            results = []
            for item in raw_ticks:
                results.append(CNIntradayTick(
                    symbol=item.get("symbol", symbol.upper()),
                    time=item.get("time", ""),
                    price=float(item.get("price", 0.0)),
                    volume=float(item.get("volume", 0.0)),
                    provider=provider_name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Ticks: {e}")

    def get_cn_order_book(self, symbol: str, provider: Optional[str] = None) -> CNOrderBook:
        try:
            data = _run_async(cn_stock_service.get_book_order(symbol, provider=provider))
            if not data:
                raise ValueError("No order book data returned")
            provider_name = data.get("provider", self.name)
            bids = [CNOrderBookEntry(price=float(b.get("price")), volume=float(b.get("volume"))) for b in data.get("bids", [])]
            asks = [CNOrderBookEntry(price=float(a.get("price")), volume=float(a.get("volume"))) for a in data.get("asks", [])]
            return CNOrderBook(
                symbol=symbol.upper(),
                bids=bids,
                asks=asks,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Order Book: {e}")

    def get_cn_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(cn_stock_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item["market_cap"],
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="cn",
                    asset_class="stock"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse CN Stock Heatmap: {e}")

    # HONG KONG (HK) MARKET DATA
    def get_hk_symbols(self, provider: Optional[str] = None) -> List[str]:
        try:
            return _run_async(hk_stock_service.get_symbols(provider=provider))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Symbols: {e}")

    def get_hk_ohlcv(self, symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None) -> List[OHLCVBar]:
        try:
            res = _run_async(hk_stock_service.get_ohlcv(symbol, range_str=range, interval_str=interval, provider=provider))
            if not res:
                return []
            bars_list = res.get("bars", [])
            provider_name = res.get("provider", self.name)
            return [
                OHLCVBar(
                    symbol=res.get("symbol", symbol.upper()),
                    timestamp=parse_date(bar.get("timestamp")),
                    open=float(bar.get("open", 0.0)),
                    high=float(bar.get("high", 0.0)),
                    low=float(bar.get("low", 0.0)),
                    close=float(bar.get("close", 0.0)),
                    volume=float(bar.get("volume", 0.0)),
                    provider=provider_name,
                    market="hk"
                )
                for bar in bars_list
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK OHLCV: {e}")

    def get_hk_profile(self, symbol: str, provider: Optional[str] = None) -> HKCompanyProfile:
        try:
            data = _run_async(hk_stock_service.get_profile(symbol, provider=provider))
            if not data:
                raise ValueError("No profile data returned")
            provider_name = data.get("provider", self.name)
            return HKCompanyProfile(
                symbol=data.get("symbol", symbol.upper()),
                company_name=data.get("company_name", ""),
                sector=data.get("sector"),
                industry=data.get("industry"),
                website=data.get("website"),
                logo_url=data.get("logo_url"),
                headcount=data.get("headcount"),
                description=data.get("description"),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Profile: {e}")

    def get_hk_financials(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> HKFinancials:
        try:
            data = _run_async(hk_stock_service.get_financials(symbol, provider=provider, period=period))
            if not data:
                raise ValueError("No financials data returned")
            provider_name = data.get("provider", self.name)
            return HKFinancials(
                symbol=data.get("symbol", symbol.upper()),
                period_type=data.get("period_type", period),
                available_periods=data.get("available_periods", []),
                periods=data.get("periods", []),
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Financials: {e}")

    def get_hk_income_statement(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(hk_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                inc = p.get("financials", {}).get("income_statement", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="income",
                    items={k: float(v) if v is not None else None for k, v in inc.items()},
                    provider=provider_name,
                    market="hk",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK income statement: {e}")

    def get_hk_balance_sheet(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(hk_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                bs = p.get("financials", {}).get("balance_sheet", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="balance",
                    items={k: float(v) if v is not None else None for k, v in bs.items()},
                    provider=provider_name,
                    market="hk",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK balance sheet: {e}")

    def get_hk_cashflow(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> List[FinancialItem]:
        backend_period = "quarterly" if period.upper().startswith("Q") else "annual"
        try:
            data = _run_async(hk_stock_service.get_financials(symbol, period=backend_period, provider=provider))
            if not data:
                return []
            provider_name = data.get("provider", self.name)
            periods = data.get("periods", [])
            results = []
            for p in periods:
                period_str = p.get("period", "")
                year = int(period_str[:4]) if period_str else datetime.now().year
                quarter = None
                if period_str and "-" in period_str:
                    parts = period_str.split("-")
                    if len(parts) >= 2 and parts[1].isdigit():
                        quarter = (int(parts[1]) - 1) // 3 + 1
                cf = p.get("financials", {}).get("cash_flow", {}) or p.get("financials", {}).get("cashflow", {})
                results.append(FinancialItem(
                    symbol=symbol.upper(),
                    year=year,
                    quarter=quarter,
                    statement_type="cashflow",
                    items={k: float(v) if v is not None else None for k, v in cf.items()},
                    provider=provider_name,
                    market="hk",
                    asset_class="stock"
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK cashflow statement: {e}")

    def get_hk_dividends(self, symbol: str, provider: Optional[str] = None) -> HKDividends:
        try:
            raw_divs = _run_async(hk_stock_service.get_dividends(symbol, provider=provider))
            provider_name = raw_divs[0].get("provider", self.name) if raw_divs else self.name
            div_list = [
                HKDividendEntry(
                    ex_date=item.get("ex_date"),
                    pay_date=item.get("pay_date"),
                    amount=float(item.get("amount", 0.0)),
                    type=item.get("type")
                )
                for item in raw_divs
            ]
            return HKDividends(
                symbol=symbol.upper(),
                dividends=div_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Dividends: {e}")

    def get_hk_splits(self, symbol: str, provider: Optional[str] = None) -> HKSplits:
        try:
            raw_splits = _run_async(hk_stock_service.get_splits(symbol, provider=provider))
            provider_name = raw_splits[0].get("provider", self.name) if raw_splits else self.name
            split_list = [
                HKSplitEntry(
                    date=item.get("date", ""),
                    ratio=float(item.get("ratio", 1.0))
                )
                for item in raw_splits
            ]
            return HKSplits(
                symbol=symbol.upper(),
                splits=split_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Splits: {e}")

    def get_hk_calendar(self, symbol: str, provider: Optional[str] = None) -> HKCalendar:
        try:
            data = _run_async(hk_stock_service.get_calendar(symbol, provider=provider))
            provider_name = data.get("provider", self.name) if data else self.name
            calendar_data = {k: v for k, v in data.items() if k != "provider"} if data else {}
            return HKCalendar(
                symbol=symbol.upper(),
                calendar=calendar_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Calendar: {e}")

    def get_hk_news(self, symbol: str, provider: Optional[str] = None) -> HKNews:
        try:
            raw_news = _run_async(hk_stock_service.get_news(symbol, provider=provider))
            provider_name = raw_news[0].get("provider", self.name) if raw_news else self.name
            news_list = [
                HKNewsEntry(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    published_at=item.get("published_at", 0),
                    publisher=item.get("publisher"),
                    summary=item.get("summary")
                )
                for item in raw_news
            ]
            return HKNews(
                symbol=symbol.upper(),
                news=news_list,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK News: {e}")

    def get_hk_ratios(self, symbol: str, provider: Optional[str] = None) -> HKRatios:
        try:
            data = _run_async(hk_stock_service.get_ratios(symbol, provider=provider))
            provider_name = data.get("provider", self.name) if data else self.name
            if data:
                if "ratios" in data:
                    ratios_data = data["ratios"]
                else:
                    ratios_data = {k: v for k, v in data.items() if k not in ("provider", "symbol")}
            else:
                ratios_data = {}
            return HKRatios(
                symbol=symbol.upper(),
                ratios=ratios_data,
                provider=provider_name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Ratios: {e}")

    def get_hk_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[HeatmapItem]:
        try:
            raw_data = _run_async(hk_stock_service.get_heatmap(limit=limit, provider=provider))
            if not raw_data:
                return []
            return [
                HeatmapItem(
                    symbol=item["symbol"],
                    name=item["name"],
                    change=item["change"],
                    price=item.get("price"),
                    change_pct=item.get("change_pct"),
                    market_cap=item["market_cap"],
                    sector=item["sector"],
                    industry=item["industry"],
                    logo_url=item.get("logo_url"),
                    provider=item.get("provider", provider or self.name),
                    market="hk",
                    asset_class="stock"
                )
                for item in raw_data
            ]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse HK Stock Heatmap: {e}")



