from typing import List, Dict, Any, Optional
from openstockapi.providers.asx.providers.asx_site import ASXSiteProvider
from openstockapi.providers.asx.providers.marketindex import MarketIndexProvider
from openstockapi.providers.asx.providers.yahoo import YahooASXProvider
from openstockapi.providers.asx.providers.tradingview import TradingViewASXProvider
from openstockapi.providers.asx.providers.tradingview_heatmap import TradingViewHeatmapProvider

class ASXService:
    def __init__(self):
        self.asx_site = ASXSiteProvider()
        self.marketindex = MarketIndexProvider()
        self.yahoo = YahooASXProvider()
        self.tradingview = TradingViewASXProvider()
        self.tradingview_heatmap = TradingViewHeatmapProvider()

    async def get_symbols(self, provider: Optional[str] = None) -> List[str]:
        """Fetches list of active listed symbols on ASX."""
        if provider:
            p_lower = provider.lower()
            if "asx" in p_lower:
                return await self.asx_site.get_symbols()
            elif "index" in p_lower:
                return await self.marketindex.get_symbols()
            return []
        return await self.asx_site.get_symbols()

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches OHLCV chart."""
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "index" in p_lower:
                res = await self.marketindex.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "marketindex"
                return res
            elif "tradingview" in p_lower or "tv" in p_lower:
                res = await self.tradingview.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "tradingview"
                return res
            return None

        # Fallback loop if no provider specified: Yahoo -> TradingView -> MarketIndex
        for name, p in [("yahoo", self.yahoo), ("tradingview", self.tradingview), ("marketindex", self.marketindex)]:
            try:
                res = await p.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_profile(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches company profile metadata."""
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_profile(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "asx" in p_lower:
                res = await self.asx_site.get_profile(symbol)
                if res:
                    res["provider"] = "asx"
                return res
            elif "index" in p_lower:
                res = await self.marketindex.get_profile(symbol)
                if res:
                    res["provider"] = "marketindex"
                return res
            return None

        # Fallback: Yahoo -> ASXSite -> MarketIndex
        for name, p in [("yahoo", self.yahoo), ("asx", self.asx_site), ("marketindex", self.marketindex)]:
            try:
                res = await p.get_profile(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_financials(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches financial statements."""
        if provider:
            p_lower = provider.lower()
            if "index" in p_lower:
                res = await self.marketindex.get_financials(symbol)
                if res:
                    res["provider"] = "marketindex"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_financials(symbol, period)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None

        # Fallback: Yahoo first for quarterly; else MarketIndex -> Yahoo
        if period == "quarterly":
            providers = [("yahoo", self.yahoo), ("marketindex", self.marketindex)]
        else:
            providers = [("marketindex", self.marketindex), ("yahoo", self.yahoo)]
        
        for name, p in providers:
            try:
                kwargs = {"period": period} if hasattr(p.get_financials, "__code__") and "period" in p.get_financials.__code__.co_varnames else {}
                res = await p.get_financials(symbol, **kwargs)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_dividends(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches dividend history details."""
        if provider:
            p_lower = provider.lower()
            if "asx" in p_lower:
                res = await self.asx_site.get_dividends(symbol)
                return [{"franking": item.get("franking"), "ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "asx"} for item in (res or [])]
            elif "index" in p_lower:
                res = await self.marketindex.get_dividends(symbol)
                return [{"franking": item.get("franking"), "ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "marketindex"} for item in (res or [])]
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_dividends(symbol)
                return [{"franking": item.get("franking"), "ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in (res or [])]
            return []

        # Failover: ASXSite -> MarketIndex -> Yahoo
        for name, p in [("asx", self.asx_site), ("marketindex", self.marketindex), ("yahoo", self.yahoo)]:
            try:
                res = await p.get_dividends(symbol)
                if res:
                    return [{"franking": item.get("franking"), "ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": name} for item in res]
            except Exception:
                pass
        return []

    async def get_announcements(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches PDF file announcements feed."""
        if provider:
            p_lower = provider.lower()
            if "asx" in p_lower:
                res = await self.asx_site.get_announcements(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "size": item.get("size"), "provider": "asx"} for item in (res or [])]
            elif "index" in p_lower:
                res = await self.marketindex.get_announcements(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "size": item.get("size"), "provider": "marketindex"} for item in (res or [])]
            return []

        # Failover: ASXSite -> MarketIndex
        for name, p in [("asx", self.asx_site), ("marketindex", self.marketindex)]:
            try:
                res = await p.get_announcements(symbol)
                if res:
                    return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "size": item.get("size"), "provider": name} for item in res]
            except Exception:
                pass
        return []

    async def get_news(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches news updates for an ASX stock symbol."""
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_news(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": "yahoo"} for item in (res or [])]
            return []

        # Failover: Yahoo
        for name, p in [("yahoo", self.yahoo)]:
            try:
                res = await p.get_news(symbol)
                if res:
                    return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": name} for item in res]
            except Exception:
                pass
        return []

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider and "tradingview" not in provider.lower() and "tv" not in provider.lower():
            return []
        return await self.tradingview_heatmap.get_heatmap(limit=limit)

asx_service = ASXService()
