from typing import List, Dict, Any, Optional
from openstockapi.providers.jp_stock.providers.yahoo_jp import YahooJPProvider
from openstockapi.providers.jp_stock.providers.google_news_jp import GoogleNewsJPProvider
from openstockapi.providers.jp_stock.providers.tradingview_heatmap import TradingViewHeatmapProvider

class JPStockService:
    def __init__(self):
        self.yahoo = YahooJPProvider()
        self.google_news = GoogleNewsJPProvider()
        self.tradingview_heatmap = TradingViewHeatmapProvider()
        # Top 50 major TSE-listed companies (Nikkei 225 & TOPIX 100 components)
        self.tse_symbols = [
            "7203", "6758", "9984", "6861", "8306", "8035", "9983", "7974", "7267", "6501",
            "4063", "6098", "8031", "8001", "8316", "8058", "9433", "7751", "4502", "6902",
            "6954", "6981", "6752", "7741", "9434", "6702", "6594", "2914", "5108", "9022",
            "9020", "3382", "6301", "9531", "9503", "8604", "8411", "4568", "4503", "4523",
            "7270", "7269", "7261", "6326", "2502", "2503", "4911", "4452", "4901", "9021"
        ]

    async def get_symbols(self, provider: Optional[str] = None) -> List[str]:
        """Fetches list of active listed symbols on TSE."""
        return sorted(self.tse_symbols)

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches historical OHLCV chart."""
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
        """Fetches company profile details."""
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
        """Fetches financial statements (annual/quarterly)."""
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
        """Fetches dividend history."""
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_dividends(symbol)
                return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in (res or [])]
            return []
        res = await self.yahoo.get_dividends(symbol)
        return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in (res or [])]

    async def get_splits(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches stock split history."""
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_splits(symbol)
                return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "yahoo"} for item in (res or [])]
            return []
        res = await self.yahoo.get_splits(symbol)
        return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "yahoo"} for item in (res or [])]

    async def get_calendar(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches corporate actions calendar."""
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
        """Fetches recent news articles."""
        if provider:
            p_lower = provider.lower()
            if "google" in p_lower or "news" in p_lower:
                res = await self.google_news.get_news(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": "google_news"} for item in (res or [])]
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_news(symbol)
                return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": "yahoo"} for item in (res or [])]
            return []

        # Fallback: Yahoo -> Google News
        for name, p in [("yahoo", self.yahoo), ("google_news", self.google_news)]:
            try:
                res = await p.get_news(symbol)
                if res:
                    return [{"id": item.get("id"), "title": item.get("title"), "url": item.get("url"), "published_at": item.get("published_at"), "publisher": item.get("publisher"), "summary": item.get("summary"), "provider": name} for item in res]
            except Exception:
                pass
        return []

    async def get_ratios(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches valuation and financial ratios."""
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

jp_stock_service = JPStockService()
