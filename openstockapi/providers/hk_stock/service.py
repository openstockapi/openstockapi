from typing import List, Dict, Any, Optional
from openstockapi.providers.hk_stock.providers.yahoo_hk import YahooHKProvider
from openstockapi.providers.hk_stock.providers.google_news_hk import GoogleNewsHKProvider
from openstockapi.providers.hk_stock.providers.tradingview_heatmap import TradingViewHeatmapProvider

class HKStockService:
    def __init__(self):
        self.yahoo = YahooHKProvider()
        self.google_news = GoogleNewsHKProvider()
        self.tradingview_heatmap = TradingViewHeatmapProvider()

    async def get_symbols(self, provider: Optional[str] = None) -> List[str]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                return ["0700", "9988", "3690", "9618", "1810"]
            return []
        return ["0700", "9988", "3690", "9618", "1810"]

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
        res = await self.yahoo.get_ohlcv(symbol, range_str, interval_str)
        if res:
            res["provider"] = "yahoo"
        return res

    async def get_profile(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_profile(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
        res = await self.yahoo.get_profile(symbol)
        if res:
            res["provider"] = "yahoo"
        return res

    async def get_financials(self, symbol: str, provider: Optional[str] = None, period: str = "annual") -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_financials(symbol, period)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
        res = await self.yahoo.get_financials(symbol, period)
        if res:
            res["provider"] = "yahoo"
        return res

    async def get_dividends(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_dividends(symbol)
                return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in (res or [])]
            return []
        res = await self.yahoo.get_dividends(symbol)
        return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in (res or [])]

    async def get_splits(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_splits(symbol)
                return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "yahoo"} for item in (res or [])]
            return []
        res = await self.yahoo.get_splits(symbol)
        return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "yahoo"} for item in (res or [])]

    async def get_calendar(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_calendar(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
        res = await self.yahoo.get_calendar(symbol)
        if res:
            res["provider"] = "yahoo"
        return res

    async def get_news(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "google" in p_lower or "news" in p_lower:
                res = await self.google_news.get_news(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": "google_news"} for item in (res or [])]
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_news(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": "yahoo"} for item in (res or [])]
            return []

        for name, p in [("yahoo", self.yahoo), ("google_news", self.google_news)]:
            try:
                res = await p.get_news(symbol)
                if res:
                    return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": name} for item in res]
            except Exception:
                pass
        return []

    async def get_ratios(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_ratios(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
        res = await self.yahoo.get_ratios(symbol)
        if res:
            res["provider"] = "yahoo"
        return res

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider and "tradingview" not in provider.lower() and "tv" not in provider.lower():
            return []
        return await self.tradingview_heatmap.get_heatmap(limit=limit)

hk_stock_service = HKStockService()
