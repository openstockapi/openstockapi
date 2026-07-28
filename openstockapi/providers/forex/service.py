import redis
import json
import datetime
from typing import Dict, Any, Optional, List
from openstockapi.config import settings
from openstockapi.providers.forex.providers.exchangerate import ExchangeRateProvider
from openstockapi.providers.forex.providers.openexchangerates import OpenExchangeRatesProvider
from openstockapi.providers.forex.providers.yahoo import YahooProvider
from openstockapi.providers.forex.providers.yahoo_finance import YahooFinanceProvider
from openstockapi.providers.forex.providers.frankfurter import FrankfurterOHLCVProvider
from openstockapi.providers.forex.providers.crypto_proxy import CryptoForexProxyProvider
from openstockapi.providers.forex.providers.calendar_forexfactory import ForexFactoryCalendarProvider
from openstockapi.providers.forex.providers.calendar_dailyfx import DailyFXCalendarProvider
from openstockapi.providers.forex.providers.news_yahoo import YahooForexNewsProvider
from openstockapi.providers.forex.providers.news_cnbc import CNBCForexNewsProvider
from openstockapi.providers.forex.providers.profile_forex import ForexProfileProvider

class ForexService:
    def __init__(self):
        self.providers = [
            ExchangeRateProvider(),
            OpenExchangeRatesProvider(),
            YahooProvider()
        ]
        self.yahoo_finance_provider = YahooFinanceProvider()
        self.frankfurter_ohlcv_provider = FrankfurterOHLCVProvider()
        self.bybit_ohlcv_provider = CryptoForexProxyProvider("bybit")
        self.okx_ohlcv_provider = CryptoForexProxyProvider("okx")
        self.bingx_ohlcv_provider = CryptoForexProxyProvider("bingx")
        self.forexfactory_calendar = ForexFactoryCalendarProvider()
        self.dailyfx_calendar = DailyFXCalendarProvider()
        self.yahoo_news = YahooForexNewsProvider("Yahoo Finance", "https://finance.yahoo.com/news/rssindex")
        self.dailyfx_news = YahooForexNewsProvider("DailyFX", "https://www.dailyfx.com/feeds/forex-market-news")
        self.marketwatch_news = YahooForexNewsProvider("MarketWatch", "https://rss.marketwatch.com/marketwatch/topstories/")
        self.cnbc_news = CNBCForexNewsProvider()
        self.profile_provider = ForexProfileProvider()
        self.r = redis.Redis(
            host=settings.OPENSTOCKAPI_REDIS_HOST,
            port=settings.OPENSTOCKAPI_REDIS_PORT,
            password=settings.OPENSTOCKAPI_REDIS_PASSWORD if settings.OPENSTOCKAPI_REDIS_PASSWORD else None,
            db=settings.OPENSTOCKAPI_REDIS_DB,
            decode_responses=True,
            socket_timeout=0.5,
            socket_connect_timeout=0.5,
            retry_on_timeout=False,
            retry=None
        )

    def _safe_get(self, key: str) -> Optional[str]:
        try:
            return self.r.get(key)
        except Exception:
            return None

    def _safe_setex(self, key: str, seconds: int, value: str):
        try:
            self.r.setex(key, seconds, value)
        except Exception:
            pass

    async def get_rates(self, base_currency: str = "USD", provider_override: Optional[str] = None) -> Optional[Dict[str, Any]]:
        base = base_currency.upper()
        cache_key = f"forex:rates:{base}"
        
        if provider_override:
            p_lower = provider_override.lower()
            for provider in self.providers:
                c_name = provider.__class__.__name__.lower()
                if p_lower in c_name:
                    res = await provider.fetch_rates(base)
                    if res:
                        res["provider"] = p_lower
                    return res
            return None

        # 1. Check Redis Cache
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        from openstockapi.core.cooldown import is_cooling, set_cooldown
        # 2. Try providers sequentially (Auto-Switch Fault Tolerance)
        for provider in self.providers:
            p_lower = provider.__class__.__name__.lower()
            if is_cooling(p_lower):
                continue
            try:
                rates_data = await provider.fetch_rates(base)
                if rates_data and rates_data.get("rates"):
                    rates_data["provider"] = p_lower
                    # Cache successfully fetched rates for 60 seconds
                    self._safe_setex(cache_key, 60, json.dumps(rates_data))
                    return rates_data
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    set_cooldown(p_lower, 60.0)
                pass

        return None

    async def convert(self, from_currency: str, to_currency: str, amount: float) -> Optional[Dict[str, Any]]:
        frm = from_currency.upper()
        to = to_currency.upper()
        
        rates_data = await self.get_rates("USD")
        if not rates_data or "rates" not in rates_data:
            return None
            
        rates = rates_data["rates"]
        if frm not in rates or to not in rates:
            return None
            
        usd_amount = amount / rates[frm]
        converted_amount = usd_amount * rates[to]
        
        return {
            "from": frm,
            "to": to,
            "amount": amount,
            "converted_amount": round(converted_amount, 4),
            "rate": round(rates[to] / rates[frm], 6),
            "timestamp": rates_data["timestamp"],
            "source": rates_data["source"],
            "provider": rates_data.get("provider")
        }

    async def get_forex_ohlcv(self, base: str = "USD", target: str = "VND", range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if base.upper() == target.upper():
            return None
        ticker = f"{base.upper()}{target.upper()}=X"
        
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo_finance_provider.fetch_chart(ticker, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "frankfurter" in p_lower:
                res = await self.frankfurter_ohlcv_provider.fetch_chart(ticker, range_str, interval_str)
                if res:
                    res["provider"] = "frankfurter"
                return res
            elif "bybit" in p_lower:
                res = await self.bybit_ohlcv_provider.fetch_chart(ticker, range_str, interval_str)
                if res:
                    res["provider"] = "bybit"
                return res
            elif "okx" in p_lower:
                res = await self.okx_ohlcv_provider.fetch_chart(ticker, range_str, interval_str)
                if res:
                    res["provider"] = "okx"
                return res
            return None

        # Auto-switch: Yahoo Finance -> Frankfurter -> Bybit -> OKX
        from openstockapi.core.cooldown import is_cooling, set_cooldown
        for name, p in [("yahoo", self.yahoo_finance_provider), ("frankfurter", self.frankfurter_ohlcv_provider), ("bybit", self.bybit_ohlcv_provider), ("okx", self.okx_ohlcv_provider)]:
            if is_cooling(name):
                continue
            try:
                res = await p.fetch_chart(ticker, range_str, interval_str)
                if res and res.get("bars"):
                    res["provider"] = name
                    return res
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    set_cooldown(name, 60.0)
                pass
        return None

    async def get_commodities(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo_finance_provider.fetch_chart(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "bybit" in p_lower:
                res = await self.bybit_ohlcv_provider.fetch_chart(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "bybit"
                return res
            elif "okx" in p_lower:
                res = await self.okx_ohlcv_provider.fetch_chart(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "okx"
                return res
            elif "bingx" in p_lower:
                res = await self.bingx_ohlcv_provider.fetch_chart(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "bingx"
                return res
            return None

        # Auto-switch: Yahoo Finance -> Bybit -> OKX -> BingX
        from openstockapi.core.cooldown import is_cooling, set_cooldown
        for name, p in [("yahoo", self.yahoo_finance_provider), ("bybit", self.bybit_ohlcv_provider), ("okx", self.okx_ohlcv_provider), ("bingx", self.bingx_ohlcv_provider)]:
            if is_cooling(name):
                continue
            try:
                res = await p.fetch_chart(symbol, range_str, interval_str)
                if res and res.get("bars"):
                    res["provider"] = name
                    return res
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    set_cooldown(name, 60.0)
                pass
        return None

    async def get_indices_etf(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo_finance_provider.fetch_chart(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "bingx" in p_lower:
                res = await self.bingx_ohlcv_provider.fetch_chart(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "bingx"
                return res
            return None

        # Auto-switch: Yahoo Finance -> BingX
        from openstockapi.core.cooldown import is_cooling, set_cooldown
        for name, p in [("yahoo", self.yahoo_finance_provider), ("bingx", self.bingx_ohlcv_provider)]:
            if is_cooling(name):
                continue
            try:
                res = await p.fetch_chart(symbol, range_str, interval_str)
                if res and res.get("bars"):
                    res["provider"] = name
                    return res
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    set_cooldown(name, 60.0)
                pass
        return None

    async def get_rate_comparison(self, base_currency: str = "USD") -> Dict[str, Any]:
        base = base_currency.upper()
        results = {}
        for provider in self.providers:
            try:
                rates_data = await provider.fetch_rates(base)
                if rates_data and rates_data.get("rates"):
                    results[rates_data["source"]] = rates_data["rates"]
            except Exception:
                pass
        return {
            "base": base,
            "comparison": results,
            "timestamp": int(datetime.datetime.utcnow().timestamp() * 1000)
        }

    # ─── Forex Events & News Methods ──────────────────────────────────────────

    async def get_events(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "factory" in p_lower:
                res = await self.forexfactory_calendar.get_events()
                for r in res:
                    r["provider"] = "forexfactory"
                return res
            elif "dailyfx" in p_lower:
                res = await self.dailyfx_calendar.get_events()
                for r in res:
                    r["provider"] = "dailyfx"
                return res
            return []

        # Failover: ForexFactory -> DailyFX
        for name, p in [("forexfactory", self.forexfactory_calendar), ("dailyfx", self.dailyfx_calendar)]:
            try:
                res = await p.get_events()
                if res:
                    for r in res:
                        r["provider"] = name
                    return res
            except Exception:
                pass
        return []

    async def get_news(self, limit: int = 20, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo_news.get_news(limit)
                for r in res:
                    r["provider"] = "yahoo"
                return res
            elif "dailyfx" in p_lower:
                res = await self.dailyfx_news.get_news(limit)
                for r in res:
                    r["provider"] = "dailyfx"
                return res
            elif "watch" in p_lower:
                res = await self.marketwatch_news.get_news(limit)
                for r in res:
                    r["provider"] = "marketwatch"
                return res
            elif "cnbc" in p_lower:
                res = await self.cnbc_news.get_news(limit)
                for r in res:
                    r["provider"] = "cnbc"
                return res
            return []

        # Failover: Yahoo -> DailyFX -> MarketWatch -> CNBC
        for name, p in [("yahoo", self.yahoo_news), ("dailyfx", self.dailyfx_news), ("marketwatch", self.marketwatch_news), ("cnbc", self.cnbc_news)]:
            try:
                res = await p.get_news(limit)
                if res:
                    for r in res:
                        r["provider"] = name
                    return res
            except Exception:
                pass
        return []

    def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self.profile_provider.get_profile(symbol)

forex_service = ForexService()
