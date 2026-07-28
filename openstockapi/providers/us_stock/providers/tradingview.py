import httpx
from typing import Dict, Any, Optional

class TradingViewUSProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.tradingview.com/"
        }

    async def _resolve_exchange(self, symbol: str) -> str:
        sym_upper = symbol.upper().strip()
        search_url = "https://symbol-search.tradingview.com/symbol_search/"
        params = {"text": sym_upper, "type": "stock"}
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(search_url, params=params, headers=self.headers)
                if res.status_code == 200:
                    results = res.json()
                    for item in results:
                        if item.get("symbol") == sym_upper and item.get("country") == "US":
                            exchange = item.get("exchange")
                            if exchange:
                                return exchange.upper()
        except Exception:
            pass
        return "NASDAQ"

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1D") -> Optional[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
        exchange = await self._resolve_exchange(sym_norm)
        
        tv_interval = "1D"
        if "1h" in interval_str:
            tv_interval = "60"
        elif "5m" in interval_str:
            tv_interval = "5"
        elif "15m" in interval_str:
            tv_interval = "15"
        elif "1d" in interval_str.lower():
            tv_interval = "1D"
            
        url = "https://webcharts.tradingview.com/chartex/"
        params = {
            "symbol": f"{exchange}:{sym_norm}",
            "interval": tv_interval
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, dict) and data.get("s") == "ok":
                        t = data.get("t", [])
                        o = data.get("o", [])
                        h = data.get("h", [])
                        l = data.get("l", [])
                        c = data.get("c", [])
                        v = data.get("v", [])
                        
                        bars = []
                        for i in range(len(t)):
                            bars.append({
                                "timestamp": t[i] * 1000,
                                "open": float(o[i]),
                                "high": float(h[i]),
                                "low": float(l[i]),
                                "close": float(c[i]),
                                "volume": int(v[i]) if v else 0
                            })
                        if bars:
                            return {
                                "symbol": sym_norm,
                                "currency": "USD",
                                "bars": bars[-100:]
                            }
        except Exception:
            pass
        return None
