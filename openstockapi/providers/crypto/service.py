from typing import List, Dict, Any, Optional
from openstockapi.providers.crypto.providers.binance import BinanceProvider
from openstockapi.providers.crypto.providers.bingx import BingXProvider
from openstockapi.providers.crypto.providers.hyperliquid import HyperliquidProvider
from openstockapi.providers.crypto.providers.bybit import BybitProvider
from openstockapi.providers.crypto.providers.okx import OKXProvider
from openstockapi.providers.crypto.providers.deribit import DeribitProvider
from openstockapi.providers.crypto.providers.news_compare import CryptoCompareNewsProvider
from openstockapi.providers.crypto.providers.news_rss import CryptoRSSNewsProvider
from openstockapi.providers.crypto.providers.events_coingecko import CoinGeckoEventsProvider
from openstockapi.providers.crypto.providers.profile_coingecko import CoinGeckoProfileProvider
from openstockapi.providers.crypto.providers.tradingview_heatmap import TradingViewHeatmapProvider

class CryptoService:
    def __init__(self):
        self.binance_provider = BinanceProvider()
        self.bingx_provider = BingXProvider()
        self.hyperliquid_provider = HyperliquidProvider()
        self.bybit_provider = BybitProvider()
        self.okx_provider = OKXProvider()
        self.deribit_provider = DeribitProvider()
        self.cryptocompare_news = CryptoCompareNewsProvider()
        self.coindesk_news = CryptoRSSNewsProvider("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/")
        self.cointelegraph_news = CryptoRSSNewsProvider("CoinTelegraph", "https://cointelegraph.com/rss")
        self.coingecko_events = CoinGeckoEventsProvider()
        self.coingecko_profile = CoinGeckoProfileProvider()
        self.coingecko_heatmap = TradingViewHeatmapProvider()
        self.tradfi_symbols = {"SPY", "QQQ", "GLD", "SLV", "USO"}

    def _select_provider(self, symbol: str, provider_override: Optional[str] = None):
        if provider_override:
            p_lower = provider_override.lower()
            if "binance" in p_lower:
                return self.binance_provider, "binance"
            elif "bingx" in p_lower:
                return self.bingx_provider, "bingx"
            elif "hyperliquid" in p_lower:
                return self.hyperliquid_provider, "hyperliquid"
            elif "bybit" in p_lower:
                return self.bybit_provider, "bybit"
            elif "okx" in p_lower:
                return self.okx_provider, "okx"
            elif "deribit" in p_lower:
                return self.deribit_provider, "deribit"
            return None, None
        symbol_upper = symbol.upper()
        if symbol_upper in self.tradfi_symbols:
            return self.bingx_provider, "bingx"
        return self.binance_provider, "binance"

    async def get_symbols(self, provider: Optional[str] = None) -> List[str]:
        # Return hardcoded symbol lists
        return [
            "BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT",
            "DOGEUSDT", "BNBUSDT", "LTCUSDT", "LINKUSDT", "DOTUSDT"
        ]

    async def get_tickers(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        p, name = self._select_provider("", provider)
        if not p:
            return []
        if hasattr(p, "get_tickers"):
            res = await p.get_tickers()
            for r in res:
                r["provider"] = name
            return res
        return []

    async def get_depth(self, symbol: str, limit: int = 20, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        p, name = self._select_provider(symbol, provider)
        if not p or not hasattr(p, "get_depth"):
            return None
        depth = await p.get_depth(symbol, limit)
        if depth:
            depth["provider"] = name
            if depth.get("bids") and depth.get("asks"):
                best_bid = depth["bids"][0][0]
                best_ask = depth["asks"][0][0]
                spread = round(best_ask - best_bid, 4)
                
                moderate_volume = sum(level[1] for level in depth["asks"][:5])
                if moderate_volume > 0:
                    weighted_sum = sum(level[0] * level[1] for level in depth["asks"][:5])
                    avg_price = weighted_sum / moderate_volume
                    slippage = round((avg_price - best_ask) / best_ask, 6)
                else:
                    slippage = 0.0
                    
                depth["spread"] = spread
                depth["estimated_slippage"] = slippage
        return depth

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        p, name = self._select_provider(symbol, provider)
        if not p or not hasattr(p, "get_footprint"):
            return None
        res = await p.get_footprint(symbol, timeframe, limit)
        if res:
            res["provider"] = name
        return res

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot", provider: Optional[str] = None) -> List[Dict[str, Any]]:
        from openstockapi.core.cooldown import is_cooling, set_cooldown
        if provider:
            p, name = self._select_provider(symbol, provider)
            if p and hasattr(p, "get_ohlcv"):
                res = await p.get_ohlcv(symbol, interval, limit, market_type)
                for r in res:
                    r["provider"] = name
                return res
            return []
            
        # Try sequentially (Auto-Switch)
        for name, p in [("binance", self.binance_provider), ("bybit", self.bybit_provider), ("okx", self.okx_provider)]:
            if is_cooling(name):
                continue
            try:
                res = await p.get_ohlcv(symbol, interval, limit, market_type)
                if res:
                    for r in res:
                        r["provider"] = name
                    return res
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    set_cooldown(name, 60.0)
                pass
        return []

    async def get_derivatives_indicators(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        from openstockapi.core.cooldown import is_cooling, set_cooldown
        if symbol.upper() in self.tradfi_symbols:
            return None
            
        if provider:
            p, name = self._select_provider(symbol, provider)
            if p and hasattr(p, "get_derivatives_indicators"):
                res = await p.get_derivatives_indicators(symbol)
                if res:
                    res["provider"] = name
                return res
            return None
            
        # Try sequentially
        for name, p in [("binance", self.binance_provider), ("bybit", self.bybit_provider), ("okx", self.okx_provider)]:
            if is_cooling(name):
                continue
            try:
                res = await p.get_derivatives_indicators(symbol)
                if res:
                    res["provider"] = name
                    return res
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    set_cooldown(name, 60.0)
                pass
        return None

    def simulate_leverage_margin(self, symbol: str, entry_price: float, leverage: float, position_size: float, direction: str = "long") -> Dict[str, Any]:
        mmr = 0.004
        initial_margin = (entry_price * position_size) / leverage
        
        if direction.lower() == "long":
            liq_price = entry_price * (1.0 - (1.0 / leverage) + mmr)
        else:
            liq_price = entry_price * (1.0 + (1.0 / leverage) - mmr)
            
        return {
            "symbol": symbol.upper(),
            "entry_price": entry_price,
            "leverage": leverage,
            "position_size": position_size,
            "direction": direction.lower(),
            "initial_margin": round(initial_margin, 4),
            "maintenance_margin": round(entry_price * position_size * mmr, 4),
            "liquidation_price": round(liq_price, 4)
        }

    async def get_orderbook_heatmap(self, symbol: str, timeframe: str = "15min", limit: int = 50) -> Optional[Dict[str, Any]]:
        res = await self.hyperliquid_provider.get_orderbook_heatmap(symbol, timeframe, limit)
        if res:
            res["provider"] = "hyperliquid"
        return res

    async def get_liq_heatmap(self, symbol: str, timeframe: str = "1h", limit: int = 720) -> Optional[Dict[str, Any]]:
        # Safe return for TradFi indexes
        if symbol.upper() in self.tradfi_symbols:
            return {
                "symbol": symbol.upper(),
                "timeframe": timeframe,
                "price_bins": [],
                "timestamps": [],
                "matrix": [],
                "provider": "hyperliquid"
            }
        res = await self.hyperliquid_provider.get_liq_heatmap(symbol, timeframe, limit)
        if res:
            res["provider"] = "hyperliquid"
        return res

    async def get_sim_liq_heatmap(self, symbol: str, timeframe: str = "1h", limit: int = 720) -> Optional[Dict[str, Any]]:
        res = await self.hyperliquid_provider.get_sim_liq_heatmap(symbol, timeframe, limit)
        if res:
            res["provider"] = "hyperliquid"
        return res

    # ─── Options Methods (Deribit + OKX Backup) ───────────────────────────────

    async def get_options_instruments(self, currency: str = "BTC", kind: str = "option", provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches all active option/future instruments with failover/override support."""
        if provider:
            p, name = self._select_provider("", provider)
            if p and hasattr(p, "get_options_instruments"):
                res = await p.get_options_instruments(currency, kind)
                for r in res:
                    r["provider"] = name
                return res
            if p == self.okx_provider:
                res = await self.okx_provider.get_options_instruments(currency, kind)
                for r in res:
                    r["provider"] = "okx"
                return res
            return []

        # Auto-switch: Deribit first, then OKX
        res = await self.deribit_provider.get_instruments(currency, kind)
        if res:
            for r in res:
                r["provider"] = "deribit"
            return res
        res = await self.okx_provider.get_options_instruments(currency, kind)
        if res:
            for r in res:
                r["provider"] = "okx"
            return res
        return []

    async def get_options_chain(self, currency: str = "BTC", provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetches the complete options chain summary including IV and pricing."""
        if provider:
            p, name = self._select_provider("", provider)
            if p and hasattr(p, "get_options_chain"):
                res = await p.get_options_chain(currency)
                for r in res:
                    r["provider"] = name
                return res
            if p == self.okx_provider:
                res = await self.okx_provider.get_options_chain(currency)
                for r in res:
                    r["provider"] = "okx"
                return res
            return []

        res = await self.deribit_provider.get_options_chain(currency)
        if res:
            for r in res:
                r["provider"] = "deribit"
            return res
        res = await self.okx_provider.get_options_chain(currency)
        if res:
            for r in res:
                r["provider"] = "okx"
            return res
        return []

    async def get_options_ticker(self, instrument_name: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetches detailed ticker with Greeks for a specific option instrument."""
        if provider:
            p, name = self._select_provider("", provider)
            if p == self.okx_provider:
                res = await self.okx_provider.get_options_ticker(instrument_name)
                if res:
                    res["provider"] = "okx"
                return res
            res = await self.deribit_provider.get_options_ticker(instrument_name)
            if res:
                res["provider"] = "deribit"
            return res

        if "USD-" in instrument_name.upper():
            res = await self.okx_provider.get_options_ticker(instrument_name)
            if res:
                res["provider"] = "okx"
            return res
        
        res = await self.deribit_provider.get_options_ticker(instrument_name)
        if res:
            res["provider"] = "deribit"
            return res
        res = await self.okx_provider.get_options_ticker(instrument_name)
        if res:
            res["provider"] = "okx"
        return res

    # ─── Crypto News & Events Methods ─────────────────────────────────────────

    async def get_news(self, limit: int = 20, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches crypto news with multi-provider backup failover support.
        Providers: cryptocompare, coindesk, cointelegraph
        """
        if provider:
            p_lower = provider.lower()
            if "compare" in p_lower:
                res = await self.cryptocompare_news.get_news(limit)
                for r in res:
                    r["provider"] = "cryptocompare"
                return res
            elif "coindesk" in p_lower:
                res = await self.coindesk_news.get_news(limit)
                for r in res:
                    r["provider"] = "coindesk"
                return res
            elif "telegraph" in p_lower:
                res = await self.cointelegraph_news.get_news(limit)
                for r in res:
                    r["provider"] = "cointelegraph"
                return res
            return []

        # Failover loop: CryptoCompare -> CoinDesk -> CoinTelegraph
        for name, p in [("cryptocompare", self.cryptocompare_news), ("coindesk", self.coindesk_news), ("cointelegraph", self.cointelegraph_news)]:
            try:
                res = await p.get_news(limit)
                if res:
                    for r in res:
                        r["provider"] = name
                    return res
            except Exception:
                pass
        return []

    async def get_events(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches crypto events/calendar with failover.
        """
        if provider:
            if "coingecko" in provider.lower():
                res = await self.coingecko_events.get_events()
                for r in res:
                    r["provider"] = "coingecko"
                return res
            return []
            
        res = await self.coingecko_events.get_events()
        for r in res:
            r["provider"] = "coingecko"
        return res

    async def get_profile(self, symbol: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Fetches crypto profile details.
        """
        if provider and "coingecko" not in provider.lower():
            return None
        return await self.coingecko_profile.get_profile(symbol)

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        if provider and "tradingview" not in provider.lower() and "tv" not in provider.lower():
            return []
        return await self.coingecko_heatmap.get_heatmap(limit=limit)

crypto_service = CryptoService()
