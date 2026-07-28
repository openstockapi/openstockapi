import httpx
import redis
import json
import datetime
import math
from typing import List, Dict, Any, Optional
from openstockapi.config import settings
from openstockapi.providers.crypto.base import CryptoBaseProvider

class BinanceProvider(CryptoBaseProvider):
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"
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
        # Check cache
        cache_key = "crypto:binance:tickers"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/ticker/price"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    # Keep only USDT pairs for simplicity
                    usdt_tickers = [t for t in data if t["symbol"].endswith("USDT")]
                    # Map format
                    mapped = [{"symbol": t["symbol"], "price": float(t["price"])} for t in usdt_tickers]
                    # Cache for 1 second
                    self._safe_setex(cache_key, 1, json.dumps(mapped))
                    return mapped
            except Exception as e:
                # Fallback to empty list or logs
                pass
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:binance:depth:{symbol_upper}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/depth"
        params = {"symbol": symbol_upper, "limit": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    # Standardize response
                    standardized = {
                        "symbol": symbol_upper,
                        "lastUpdateId": data.get("lastUpdateId"),
                        "bids": [[float(p), float(q)] for p, q in data.get("bids", [])],
                        "asks": [[float(p), float(q)] for p, q in data.get("asks", [])]
                    }
                    self._safe_setex(cache_key, 1, json.dumps(standardized))
                    return standardized
            except Exception:
                pass
        return None

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:binance:footprint:{symbol_upper}:{timeframe}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Map timeframe to Binance
        timeframe_map = {
            "1min": "1m", "1m": "1m",
            "3min": "3m", "3m": "3m",
            "5min": "5m", "5m": "5m",
            "15min": "15m", "15m": "15m",
            "30min": "30m", "30m": "30m",
            "1h": "1h", "2h": "2h", "4h": "4h", "1d": "1d"
        }
        interval = timeframe_map.get(timeframe, "5m")

        url = f"{self.base_url}/klines"
        params = {"symbol": symbol_upper, "interval": interval, "limit": limit}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    klines = response.json()
                    bars = []
                    
                    # Compute Footprint bars from klines
                    for k in klines:
                        # Binance Kline format:
                        # 0: Open time, 1: Open, 2: High, 3: Low, 4: Close, 5: Volume, 6: Close time, ...
                        open_time_ms = k[0]
                        o = float(k[1])
                        h = float(k[2])
                        l = float(k[3])
                        c = float(k[4])
                        v = float(k[5])
                        
                        dt = datetime.datetime.utcfromtimestamp(open_time_ms / 1000.0)
                        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Mock footprint metrics & profile based on high, low, open, close, volume
                        buy_vol = v * 0.52  # Simulated buy volume
                        sell_vol = v * 0.48  # Simulated sell volume
                        delta = buy_vol - sell_vol
                        vwap = (o + h + l + c) / 4.0
                        poc = c
                        
                        # Generate some price levels (e.g. 5 ticks between low and high)
                        price_levels = []
                        ticks = 5
                        step = (h - l) / ticks if h > l else 1.0
                        for idx in range(ticks):
                            lvl_price = round(l + idx * step, 4)
                            lvl_buy = buy_vol / ticks
                            lvl_sell = sell_vol / ticks
                            # Format matching Vietnam Stock levels
                            price_levels.append([lvl_price, lvl_buy, lvl_sell, 0.0, 0, 0, 0, 0, 0])
                        
                        bars.append({
                            "timestamp": timestamp_str,
                            "ohlc": {"open": o, "high": h, "low": l, "close": c},
                            "metrics": {
                                "delta": delta,
                                "cvd": delta,  # CVD equals delta in single bar context
                                "total_vol": v,
                                "poc": poc,
                                "vwap": vwap
                            },
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
                    
                    # Cache historical footprint bars for 60 seconds (1 minute)
                    self._safe_setex(cache_key, 60, json.dumps(standardized))
                    return standardized
            except Exception:
                pass
        return None

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:binance:ohlcv:{symbol_upper}:{interval}:{limit}:{market_type}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Base URL changes depending on spot or futures
        if market_type.lower() == "futures":
            base = "https://fapi.binance.com/fapi/v1"
        else:
            base = self.base_url

        url = f"{base}/klines"
        params = {"symbol": symbol_upper, "interval": interval, "limit": limit}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    # Map to unified OHLCV structure
                    mapped = []
                    for k in data:
                        mapped.append({
                            "timestamp": k[0],
                            "open": float(k[1]),
                            "high": float(k[2]),
                            "low": float(k[3]),
                            "close": float(k[4]),
                            "volume": float(k[5])
                        })
                    self._safe_setex(cache_key, 5, json.dumps(mapped))
                    return mapped
            except Exception:
                pass
        return []

    async def get_derivatives_indicators(self, symbol: str) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:binance:derivatives:{symbol_upper}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        base = "https://fapi.binance.com/fapi/v1"
        oi_url = f"{base}/openInterest"
        fr_url = f"{base}/premiumIndex"

        async with httpx.AsyncClient() as client:
            try:
                oi_res = await client.get(oi_url, params={"symbol": symbol_upper}, timeout=5.0)
                fr_res = await client.get(fr_url, params={"symbol": symbol_upper}, timeout=5.0)
                
                oi_val = 0.0
                fr_val = 0.0
                next_funding_time = 0
                
                if oi_res.status_code == 200:
                    oi_val = float(oi_res.json().get("openInterest", 0.0))
                if fr_res.status_code == 200:
                    fr_data = fr_res.json()
                    fr_val = float(fr_data.get("lastFundingRate", 0.0))
                    next_funding_time = int(fr_data.get("nextFundingTime", 0))
                    
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
