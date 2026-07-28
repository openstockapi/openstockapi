import httpx
from typing import Dict, Any, Optional

class TradingViewASXProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.tradingview.com/"
        }

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1D") -> Optional[Dict[str, Any]]:
        # Map interval to TradingView format (e.g. 1h -> 60, 1d -> 1D)
        tv_interval = "1D"
        if "1h" in interval_str:
            tv_interval = "60"
        elif "5m" in interval_str:
            tv_interval = "5"
            
        url = "https://webcharts.tradingview.com/chartex/"
        params = {
            "symbol": f"ASX:{symbol.upper()}",
            "interval": tv_interval
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    # Handle TradingView's typical UDF chart format: {"s": "ok", "t": [...], "o": [...], "h": [...], "l": [...], "c": [...], "v": [...]}
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
                                "symbol": symbol.upper(),
                                "currency": "AUD",
                                "bars": bars[-100:]  # get last 100 bars
                            }
                    # Alternative candles list format
                    elif isinstance(data, dict) and "candles" in data:
                        candles = data["candles"]
                        bars = [
                            {
                                "timestamp": item[0] if isinstance(item, list) else item.get("time"),
                                "open": float(item[1] if isinstance(item, list) else item.get("open")),
                                "high": float(item[2] if isinstance(item, list) else item.get("high")),
                                "low": float(item[3] if isinstance(item, list) else item.get("low")),
                                "close": float(item[4] if isinstance(item, list) else item.get("close")),
                                "volume": int(item[5] if isinstance(item, list) else item.get("volume", 0))
                            }
                            for item in candles
                        ]
                        return {
                            "symbol": symbol.upper(),
                            "currency": "AUD",
                            "bars": bars[-100:]
                        }
        except Exception:
            pass
        return None
