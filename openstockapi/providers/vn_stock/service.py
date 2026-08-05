from typing import List, Dict, Any, Optional
from openstockapi.providers.vn_stock.providers.mas import MASProvider
from openstockapi.providers.vn_stock.providers.dnse import DNSEProvider
from openstockapi.providers.vn_stock.providers.vndirect import VNDIRECTProvider
from openstockapi.providers.vn_stock.providers.vci import VCIProvider
from openstockapi.providers.vn_stock.providers.mbk import MBKProvider
from openstockapi.providers.vn_stock.providers.fmarket import FmarketProvider
from openstockapi.providers.vn_stock.providers.kbs import KBSProvider
from openstockapi.providers.vn_stock.providers.tcbs import TCBSProvider
from openstockapi.providers.vn_stock.providers.msn import MSNProvider
from openstockapi.providers.vn_stock.heatmap_service import vn_heatmap_service

class VNStockService:
    def __init__(self):
        self.providers = {
            "mas": MASProvider(),
            "dnse": DNSEProvider(),
            "vndirect": VNDIRECTProvider(),
            "vci": VCIProvider(),
            "mbk": MBKProvider(),
            "fmarket": FmarketProvider(),
            "kbs": KBSProvider(),
            "tcbs": TCBSProvider(),
            "msn": MSNProvider(),
        }
        self.priorities = {
            "ohlcv": ["kbs", "vci", "msn", "dnse"],
            "financials": ["mas", "vci"],
            "profile": ["vndirect", "vci", "kbs"],
            "derivative_profile": ["kbs"],
            "quote": ["vci", "dnse"],
            "orderbook": ["vci", "dnse"],
            "trading": ["mas", "kbs", "vci"],
            "macro": ["mbk"],
            "fund": ["fmarket"],
            "news": ["kbs"],
            "events": ["vci", "kbs"],
        }

    def _get_providers_to_try(self, category: str, explicit_provider: Optional[str] = None) -> List[Any]:
        if explicit_provider:
            p_name = explicit_provider.lower()
            if p_name in self.providers:
                return [self.providers[p_name]]
            return []
        names = self.priorities.get(category, [])
        return [self.providers[name] for name in names if name in self.providers]

    async def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str, provider: Optional[str] = None) -> List[Any]:
        # Standardize index symbols input to SDK-unified uppercase codes
        symbol_upper = symbol.upper()
        index_normalization = {
            "VNINDEX": "VNINDEX",
            "VN30": "VN30",
            "HNX30": "HNX30",
            "HNX": "HNXINDEX",
            "HNXINDEX": "HNXINDEX",
            "HNX-INDEX": "HNXINDEX",
            "UPCOM": "UPCOMINDEX",
            "UPCOMINDEX": "UPCOMINDEX",
            "UPCOM-INDEX": "UPCOMINDEX",
            "HNXUPCOMINDEX": "UPCOMINDEX"
        }
        
        is_index = symbol_upper in index_normalization
        if is_index:
            symbol = index_normalization[symbol_upper]
            if not provider:
                provider = "vci"

        providers = self._get_providers_to_try("ohlcv", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_ohlcv(symbol, resolution, from_date, to_date)
                except (NotImplementedError, AttributeError):
                    res = p.get_ohlcv(symbol, resolution, from_date, to_date)
                if res is not None:
                    for bar in res:
                        if hasattr(bar, "provider"):
                            bar.provider = p.name
                        if is_index and hasattr(bar, "symbol"):
                            bar.symbol = symbol
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_profile(self, symbol: str, provider: Optional[str] = None) -> Any:
        providers = self._get_providers_to_try("profile", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_company_profile(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_company_profile(symbol)
                if res is not None:
                    if hasattr(res, "provider"):
                        res.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return None

    async def get_financials(self, symbol: str, stmt_type: str, period: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("financials", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_financial_statements(symbol, stmt_type, period)
                except (NotImplementedError, AttributeError):
                    res = p.get_financial_statements(symbol, stmt_type, period)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_derivative_profile(self, symbol: str, provider: Optional[str] = None) -> Any:
        providers = self._get_providers_to_try("derivative_profile", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_derivative_profile(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_derivative_profile(symbol)
                if res is not None:
                    if hasattr(res, "provider"):
                        res.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return None

    async def get_quote(self, symbol: str, provider: Optional[str] = None) -> Any:
        providers = self._get_providers_to_try("quote", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_realtime_quote(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_realtime_quote(symbol)
                if res is not None:
                    if hasattr(res, "provider"):
                        res.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return None

    async def get_order_book(self, symbol: str, provider: Optional[str] = None) -> Any:
        providers = self._get_providers_to_try("orderbook", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_order_book(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_order_book(symbol)
                if res is not None:
                    if hasattr(res, "provider"):
                        res.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return None

    async def get_macro_indicators(self, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("macro", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_macro_indicators()
                except (NotImplementedError, AttributeError):
                    res = p.get_macro_indicators()
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_fund_details(self, fund_id: int, provider: Optional[str] = None) -> Any:
        providers = self._get_providers_to_try("fund", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_fund_details(fund_id)
                except (NotImplementedError, AttributeError):
                    res = p.get_fund_details(fund_id)
                if res is not None:
                    if hasattr(res, "provider"):
                        res.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return None

    async def get_news(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("news", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_company_news(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_company_news(symbol)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_events(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("events", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_company_events(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_company_events(symbol)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_foreign_trading(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("trading", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_foreign_trading(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_foreign_trading(symbol)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_prop_trading(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("trading", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_prop_trading(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_prop_trading(symbol)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_insider_trading(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("trading", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_insider_trading(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_insider_trading(symbol)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_intraday_ticks(self, symbol: str, provider: Optional[str] = None) -> List[Any]:
        providers = self._get_providers_to_try("trading", provider)
        last_err = None
        for p in providers:
            try:
                try:
                    res = await p.async_get_intraday_ticks(symbol)
                except (NotImplementedError, AttributeError):
                    res = p.get_intraday_ticks(symbol)
                if res is not None:
                    for item in res:
                        if hasattr(item, "provider"):
                            item.provider = p.name
                    return res
            except Exception as e:
                last_err = e
        if last_err:
            raise last_err
        return []

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        return await vn_heatmap_service.get_heatmap(limit=limit, provider=provider)

    async def get_symbols(self, provider: Optional[str] = None) -> List[str]:
        fallback = ["VCB", "VIC", "VHM", "HPG", "FPT", "VNM", "MSN", "TCB", "ACB", "GAS"]
        
        # Set VCI as default provider if none specified
        if not provider:
            provider = "vci"
            
        # If a specific provider is requested
        if provider:
            p_lower = provider.lower()
            if "vci" in p_lower:
                p = self.providers.get("vci")
                if p:
                    try:
                        return await p.async_get_vn_symbols()
                    except Exception:
                        try:
                            return p.get_vn_symbols()
                        except Exception:
                            pass
            elif "tradingview" in p_lower or "tv" in p_lower:
                try:
                    heatmap = await vn_heatmap_service.tradingview.get_heatmap(limit=2000)
                    return sorted(list(set([item["symbol"] for item in heatmap if item.get("symbol")])))
                except Exception:
                    pass
            elif "kbs" in p_lower:
                try:
                    heatmap = await vn_heatmap_service.kbs.get_heatmap(limit=2000)
                    return sorted(list(set([item["symbol"] for item in heatmap if item.get("symbol")])))
                except Exception:
                    pass
            return []

        # Fallback sequence: try VCI first, then TradingView
        try:
            p = self.providers.get("vci")
            if p:
                res = await p.async_get_vn_symbols()
                if res:
                    return res
        except Exception:
            pass

        try:
            heatmap = await vn_heatmap_service.tradingview.get_heatmap(limit=2000)
            if heatmap:
                return sorted(list(set([item["symbol"] for item in heatmap if item.get("symbol")])))
        except Exception:
            pass

        return fallback

vn_stock_service = VNStockService()
