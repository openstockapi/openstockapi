from typing import List, Dict, Any, Optional
from openstockapi.providers.cn_stock.providers.sina_cn import SinaCNProvider
from openstockapi.providers.cn_stock.providers.tencent_cn import TencentCNProvider
from openstockapi.providers.cn_stock.providers.yahoo_cn import YahooCNProvider
from openstockapi.providers.cn_stock.providers.google_news_cn import GoogleNewsCNProvider
from openstockapi.providers.cn_stock.providers.tradingview_heatmap import TradingViewHeatmapProvider

class CNStockService:
    def __init__(self):
        self.sina_cn = SinaCNProvider()
        self.tencent_cn = TencentCNProvider()
        self.yahoo = YahooCNProvider()
        self.google_news = GoogleNewsCNProvider()
        self.tradingview_heatmap = TradingViewHeatmapProvider()

    async def get_symbols(self, provider: Optional[str] = None) -> List[str]:
        return ["600519", "002594", "000001", "600036", "601318"]

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sina" in p_lower:
                res = await self.sina_cn.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "sina"
                return res
            elif "tencent" in p_lower:
                res = await self.tencent_cn.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "tencent"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
        
        for name, p in [("sina", self.sina_cn), ("tencent", self.tencent_cn), ("yahoo", self.yahoo)]:
            try:
                res = await p.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_profile(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sina" in p_lower:
                res = await self.sina_cn.get_profile(symbol)
                if res:
                    res["provider"] = "sina"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_profile(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
                
        for name, p in [("yahoo", self.yahoo), ("sina", self.sina_cn)]:
            try:
                res = await p.get_profile(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_financials(self, symbol: str, provider: Optional[str] = None, period: str = "annual") -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sina" in p_lower:
                res = await self.sina_cn.get_financials(symbol, period)
                if res:
                    res["provider"] = "sina"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_financials(symbol, period)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
                
        for name, p in [("yahoo", self.yahoo), ("sina", self.sina_cn)]:
            try:
                res = await p.get_financials(symbol, period)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_dividends(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sina" in p_lower:
                res = await self.sina_cn.get_dividends(symbol)
                return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "sina"} for item in (res or [])]
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_dividends(symbol)
                return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in (res or [])]
            return []
                
        try:
            res = await self.sina_cn.get_dividends(symbol)
            if res:
                return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "sina"} for item in res]
        except Exception:
            pass

        try:
            res = await self.yahoo.get_dividends(symbol)
            if res:
                return [{"ex_date": item.get("ex_date"), "pay_date": item.get("pay_date"), "amount": item.get("amount"), "type": item.get("type"), "provider": "yahoo"} for item in res]
        except Exception:
            pass

        return []

    async def get_splits(self, symbol: str, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sina" in p_lower:
                res = await self.sina_cn.get_splits(symbol)
                return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "sina"} for item in (res or [])]
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_splits(symbol)
                return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "yahoo"} for item in (res or [])]
            return []
                
        try:
            res = await self.sina_cn.get_splits(symbol)
            if res:
                return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "sina"} for item in res]
        except Exception:
            pass

        try:
            res = await self.yahoo.get_splits(symbol)
            if res:
                return [{"date": item.get("date"), "ratio": item.get("ratio"), "provider": "yahoo"} for item in res]
        except Exception:
            pass

        return []

    async def get_calendar(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sina" in p_lower:
                res = await self.sina_cn.get_calendar(symbol)
                if res:
                    res["provider"] = "sina"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_calendar(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
                
        try:
            res = await self.sina_cn.get_calendar(symbol)
            if res:
                res["provider"] = "sina"
                return res
        except Exception:
            pass

        try:
            res = await self.yahoo.get_calendar(symbol)
            if res:
                res["provider"] = "yahoo"
                return res
        except Exception:
            pass

        return None

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
            if "sina" in p_lower:
                res = await self.sina_cn.get_ratios(symbol)
                if res:
                    res["provider"] = "sina"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_ratios(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None
                
        try:
            res = await self.yahoo.get_ratios(symbol)
            if res:
                res["provider"] = "yahoo"
                return res
        except Exception:
            pass

        try:
            res = await self.sina_cn.get_ratios(symbol)
            if res:
                res["provider"] = "sina"
                return res
        except Exception:
            pass

        return None

    async def get_quote(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "tencent" in p_lower:
                res = await self.tencent_cn.get_quote(symbol)
                if res:
                    res["provider"] = "tencent"
                return res
            elif "sina" in p_lower:
                res = await self.sina_cn.get_quote(symbol)
                if res:
                    res["provider"] = "sina"
                return res
            return None

        for name, p in [("sina", self.sina_cn), ("tencent", self.tencent_cn)]:
            try:
                res = await p.get_quote(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_tick(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "tencent" in p_lower:
                res = await self.tencent_cn.get_tick(symbol)
                if res:
                    res["provider"] = "tencent"
                return res
            elif "sina" in p_lower:
                res = await self.sina_cn.get_tick(symbol)
                if res:
                    res["provider"] = "sina"
                return res
            return None

        for name, p in [("sina", self.sina_cn), ("tencent", self.tencent_cn)]:
            try:
                res = await p.get_tick(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_book_order(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "tencent" in p_lower:
                res = await self.tencent_cn.get_book_order(symbol)
                if res:
                    res["provider"] = "tencent"
                return res
            elif "sina" in p_lower:
                res = await self.sina_cn.get_book_order(symbol)
                if res:
                    res["provider"] = "sina"
                return res
            return None

        for name, p in [("sina", self.sina_cn), ("tencent", self.tencent_cn)]:
            try:
                res = await p.get_book_order(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider and "tradingview" not in provider.lower() and "tv" not in provider.lower():
            return []
        return await self.tradingview_heatmap.get_heatmap(limit=limit)

cn_stock_service = CNStockService()
