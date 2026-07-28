import httpx
import redis
import json
import datetime
from typing import List, Dict, Any, Optional
from openstockapi.config import settings
from openstockapi.providers.crypto.base import CryptoBaseProvider

class BybitProvider(CryptoBaseProvider):
    def __init__(self):
        self.base_url = "https://api.bybit.com/v5/market"
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

    async def get_tickers(self) -> List[Dict[str, Any]]:
        cache_key = "crypto:bybit:tickers"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/tickers"
        params = {"category": "spot"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    list_data = data.get("result", {}).get("list", [])
                    usdt_tickers = [t for t in list_data if t["symbol"].endswith("USDT")]
                    mapped = [{"symbol": t["symbol"], "price": float(t["lastPrice"])} for t in usdt_tickers]
                    self._safe_setex(cache_key, 2, json.dumps(mapped))
                    return mapped
            except Exception:
                pass
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:bybit:depth:{symbol_upper}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/orderbook"
        params = {"category": "spot", "symbol": symbol_upper, "limit": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("result", {})
                    standardized = {
                        "symbol": symbol_upper,
                        "lastUpdateId": int(result.get("ts", 0)),
                        "bids": [[float(p), float(q)] for p, q in result.get("b", [])],
                        "asks": [[float(p), float(q)] for p, q in result.get("a", [])]
                    }
                    self._safe_setex(cache_key, 1, json.dumps(standardized))
                    return standardized
            except Exception:
                pass
        return None

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:bybit:ohlcv:{symbol_upper}:{interval}:{limit}:{market_type}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        category = "linear" if market_type.lower() == "futures" else "spot"
        
        # Map intervals
        interval_map = {
            "1m": "1", "3m": "3", "5m": "5", "15m": "15", "30m": "30",
            "1h": "60", "2h": "120", "4h": "240", "1d": "D", "1D": "D"
        }
        bybit_interval = interval_map.get(interval, "60")

        url = f"{self.base_url}/kline"
        params = {"category": category, "symbol": symbol_upper, "interval": bybit_interval, "limit": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    list_data = data.get("result", {}).get("list", [])
                    mapped = []
                    for k in list_data:
                        # Bybit kline: [start_time, open, high, low, close, volume, turnover]
                        mapped.append({
                            "timestamp": int(k[0]),
                            "open": float(k[1]),
                            "high": float(k[2]),
                            "low": float(k[3]),
                            "close": float(k[4]),
                            "volume": float(k[5])
                        })
                    # Sort ascending by timestamp as standard
                    mapped.reverse()
                    self._safe_setex(cache_key, 5, json.dumps(mapped))
                    return mapped
            except Exception:
                pass
        return []

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:bybit:footprint:{symbol_upper}:{timeframe}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Retrieve OHLCV to simulate footprint
        klines = await self.get_ohlcv(symbol_upper, interval=timeframe, limit=limit)
        if not klines:
            return None

        bars = []
        for k in klines:
            dt = datetime.datetime.utcfromtimestamp(k["timestamp"] / 1000.0)
            timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            o, h, l, c, v = k["open"], k["high"], k["low"], k["close"], k["volume"]
            
            buy_vol = v * 0.51
            sell_vol = v * 0.49
            delta = buy_vol - sell_vol
            
            price_levels = []
            ticks = 5
            step = (h - l) / ticks if h > l else 1.0
            for idx in range(ticks):
                lvl_price = round(l + idx * step, 4)
                price_levels.append([lvl_price, buy_vol / ticks, sell_vol / ticks, 0.0, 0, 0, 0, 0, 0])

            bars.append({
                "timestamp": timestamp_str,
                "ohlc": {"open": o, "high": h, "low": l, "close": c},
                "metrics": {"delta": delta, "cvd": delta, "total_vol": v, "poc": c, "vwap": (o+h+l+c)/4.0},
                "price_levels": price_levels,
                "labels": ["AggBuyBar"] if delta > 0 else ["AggSellBar"],
                "patterns": []
            })

        standardized = {
            "symbol": symbol_upper,
            "timeframe": timeframe,
            "heatmap_resolution_mins": 5,
            "session_profile": {
                "poc": bars[-1]["metrics"]["poc"] if bars else 0,
                "vah": bars[-1]["ohlc"]["high"] if bars else 0,
                "val": bars[-1]["ohlc"]["low"] if bars else 0,
                "total_vol": sum(b["metrics"]["total_vol"] for b in bars),
                "profile": []
            },
            "imbalance_zones": [],
            "heatmap": [],
            "bars": bars
        }
        self._safe_setex(cache_key, 60, json.dumps(standardized))
        return standardized

    async def get_derivatives_indicators(self, symbol: str) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:bybit:derivatives:{symbol_upper}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Bybit open-interest & funding rate endpoints
        oi_url = "https://api.bybit.com/v5/market/open-interest"
        ticker_url = "https://api.bybit.com/v5/market/tickers"
        
        async with httpx.AsyncClient() as client:
            try:
                oi_res = await client.get(oi_url, params={"category": "linear", "symbol": symbol_upper, "intervalTime": "5min", "limit": 1}, timeout=5.0)
                ticker_res = await client.get(ticker_url, params={"category": "linear", "symbol": symbol_upper}, timeout=5.0)
                
                oi_val = 0.0
                fr_val = 0.0
                next_funding_time = 0
                
                if oi_res.status_code == 200:
                    oi_list = oi_res.json().get("result", {}).get("list", [])
                    if oi_list:
                        oi_val = float(oi_list[0].get("openInterest", 0.0))
                        
                if ticker_res.status_code == 200:
                    t_list = ticker_res.json().get("result", {}).get("list", [])
                    if t_list:
                        fr_val = float(t_list[0].get("fundingRate", 0.0))
                        try:
                            next_funding_time = int(t_list[0].get("nextFundingTime", 0))
                        except Exception:
                            pass
                            
                result = {
                    "symbol": symbol_upper,
                    "open_interest": oi_val,
                    "funding_rate": fr_val,
                    "next_funding_time": next_funding_time,
                    "timestamp": int(datetime.datetime.utcnow().timestamp() * 1000)
                }
                self._safe_setex(cache_key, 5, json.dumps(result))
                return result
            except Exception:
                pass
        return None
