from typing import List, Dict, Any, Optional
from openstockapi.providers.us_stock.providers.yfinance import YahooUSProvider
from openstockapi.providers.us_stock.providers.sec_edgar import SecEdgarProvider
from openstockapi.providers.us_stock.providers.tradingview import TradingViewUSProvider
from openstockapi.providers.us_stock.providers.nasdaq import NasdaqUSProvider
from openstockapi.providers.us_stock.providers.google_news import GoogleNewsUSProvider
from openstockapi.providers.us_stock.providers.tradingview_heatmap import TradingViewHeatmapProvider
from openstockapi.providers.us_stock.providers.serpapi import SerpApiUSProvider

class USStockService:
    def __init__(self):
        self.yahoo = YahooUSProvider()
        self.sec_edgar = SecEdgarProvider()
        self.tradingview = TradingViewUSProvider()
        self.nasdaq = NasdaqUSProvider()
        self.google_news = GoogleNewsUSProvider()
        self.tradingview_heatmap = TradingViewHeatmapProvider()
        self.serpapi = SerpApiUSProvider()

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "yahoo" in p_lower:
                res = await self.yahoo.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "tradingview" in p_lower or "tv" in p_lower:
                res = await self.tradingview.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "tradingview"
                return res
            elif "serpapi" in p_lower:
                res = await self.serpapi.get_ohlcv(symbol, range_str, interval_str)
                if res:
                    res["provider"] = "serpapi"
                return res
            return None

        # Fallback loop if no provider specified
        for name, p in [("yahoo", self.yahoo), ("tradingview", self.tradingview), ("serpapi", self.serpapi)]:
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
            if "sec" in p_lower or "edgar" in p_lower:
                res = await self.sec_edgar.get_profile(symbol)
                if res:
                    res["provider"] = "sec_edgar"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_profile(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            elif "serpapi" in p_lower:
                res = await self.serpapi.get_quote(symbol)
                if res:
                    # Map minimal quote data to profile format
                    return {
                        "symbol": symbol.upper(),
                        "company_name": symbol.upper(),
                        "provider": "serpapi"
                    }
                return res
            return None

        # Fallback loop if no provider specified
        for name, p in [("yahoo", self.yahoo), ("sec_edgar", self.sec_edgar)]:
            try:
                res = await p.get_profile(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_financials(self, symbol: str, period: str = "annual", provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sec" in p_lower or "edgar" in p_lower:
                res = await self.sec_edgar.get_financials(symbol, period)
                if res:
                    res["provider"] = "sec_edgar"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_financials(symbol, period)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None

        # Fallback loop if no provider specified
        for name, p in [("yahoo", self.yahoo), ("sec_edgar", self.sec_edgar)]:
            try:
                res = await p.get_financials(symbol, period)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_dividends(self, symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
        if provider:
            p_lower = provider.lower()
            if "nasdaq" in p_lower:
                res = await self.nasdaq.get_dividends(symbol)
                return {"dividends": res or [], "provider": "nasdaq"}
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_dividends(symbol)
                return {"dividends": res or [], "provider": "yahoo"}
            return {"dividends": [], "provider": provider}

        # Fallback loop if no provider specified
        for name, p in [("yahoo", self.yahoo), ("nasdaq", self.nasdaq)]:
            try:
                res = await p.get_dividends(symbol)
                if res:
                    return {"dividends": res, "provider": name}
            except Exception:
                pass
        return {"dividends": [], "provider": "yahoo"}

    async def get_splits(self, symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
        res = await self.yahoo.get_splits(symbol)
        return {"splits": res or [], "provider": "yahoo"}

    async def get_calendar(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        res = await self.yahoo.get_calendar(symbol)
        if res is not None:
            res["provider"] = "yahoo"
        return res

    async def get_insider_trading(self, symbol: str) -> List[Dict[str, Any]]:
        return []

    async def get_news(self, symbol: str, provider: Optional[str] = None) -> Dict[str, Any]:
        if provider:
            p_lower = provider.lower()
            if "google" in p_lower or "news" in p_lower:
                res = await self.google_news.get_news(symbol)
                return {"news": res or [], "provider": "google_news"}
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_news(symbol)
                return {"news": res or [], "provider": "yahoo"}
            elif "serpapi" in p_lower:
                res = await self.serpapi.get_news(symbol)
                return {"news": res or [], "provider": "serpapi"}
            return {"news": [], "provider": provider}

        # Fallback loop if no provider specified
        for name, p in [("yahoo", self.yahoo), ("google_news", self.google_news), ("serpapi", self.serpapi)]:
            try:
                res = await p.get_news(symbol)
                if res:
                    return {"news": res, "provider": name}
            except Exception:
                pass
        return {"news": [], "provider": "yahoo"}

    async def get_ratios(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if provider:
            p_lower = provider.lower()
            if "sec" in p_lower or "edgar" in p_lower:
                res = await self.sec_edgar.get_ratios(symbol)
                if res:
                    res["provider"] = "sec_edgar"
                return res
            elif "yahoo" in p_lower:
                res = await self.yahoo.get_ratios(symbol)
                if res:
                    res["provider"] = "yahoo"
                return res
            return None

        # Fallback loop if no provider specified
        for name, p in [("yahoo", self.yahoo), ("sec_edgar", self.sec_edgar)]:
            try:
                res = await p.get_ratios(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception:
                pass
        return None

    async def get_symbols(self, provider: Optional[str] = None) -> Dict[str, Any]:
        if provider:
            p_lower = provider.lower()
            if "nasdaq" in p_lower:
                res = await self.nasdaq.get_symbols()
                return {"symbols": res or [], "provider": "nasdaq"}
            elif "sec" in p_lower or "edgar" in p_lower:
                res = await self.sec_edgar.get_symbols()
                return {"symbols": res or [], "provider": "sec_edgar"}
            return {"symbols": [], "provider": provider}

        for name, p in [("nasdaq", self.nasdaq), ("sec_edgar", self.sec_edgar)]:
            try:
                symbols = await p.get_symbols()
                if symbols:
                    return {"symbols": symbols, "provider": name}
            except Exception:
                pass
        
        default_symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA", "TSLA", "META", "NFLX", "AMD", "INTC", "BRK.B", "JNJ", "V", "PG"]
        return {"symbols": default_symbols, "provider": "nasdaq"}

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider and "tradingview" not in provider.lower() and "tv" not in provider.lower():
            return []
        return await self.tradingview_heatmap.get_heatmap(limit=limit)

us_stock_service = USStockService()
