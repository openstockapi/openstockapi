import httpx
import redis
import json
import datetime
from typing import List, Dict, Any, Optional
from openstockapi.config import settings
from openstockapi.providers.crypto.base import CryptoBaseProvider

class BingXProvider(CryptoBaseProvider):
    def __init__(self):
        self.base_url = "https://open-api.bingx.com/openApi/swap/v3/quote/klines"
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
        # BingX is mainly used for custom Index footprint data. Return empty or basic placeholder.
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        # Not implemented for TradFi indexes on BingX
        return None

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:bingx:footprint:{symbol_upper}:{timeframe}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Map timeframe to BingX
        timeframe_map = {
            "1min": "1m", "1m": "1m",
            "3min": "3m", "3m": "3m",
            "5min": "5m", "5m": "5m",
            "15min": "15m", "15m": "15m",
            "30min": "30m", "30m": "30m",
            "1h": "1h", "2h": "2h", "4h": "4h", "1d": "1d"
        }
        interval = timeframe_map.get(timeframe, "5m")

        if symbol_upper.endswith("USDT") and not symbol_upper.startswith("USDT"):
            base_coin = symbol_upper[:-4]
            bingx_symbol = f"{base_coin}-USDT"
        elif "-" not in symbol_upper:
            bingx_symbol = f"{symbol_upper}-USDT"
        else:
            bingx_symbol = symbol_upper
        params = {
            "symbol": bingx_symbol,
            "interval": interval,
            "limit": limit
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=10.0)
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data.get("code") == 0:
                        data = res_data.get("data", [])
                        # Reverse to chronological order (oldest first)
                        data.reverse()
                        
                        bars = []
                        for k in data:
                            # BingX kline keys: open, close, high, low, volume, time
                            o = float(k.get("open", 0))
                            h = float(k.get("high", 0))
                            l = float(k.get("low", 0))
                            c = float(k.get("close", 0))
                            v = float(k.get("volume", 0))
                            time_ms = int(k.get("time", 0))
                            
                            dt = datetime.datetime.utcfromtimestamp(time_ms / 1000.0)
                            timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                            
                            buy_vol = v * 0.51
                            sell_vol = v * 0.49
                            delta = buy_vol - sell_vol
                            vwap = (o + h + l + c) / 4.0
                            poc = c
                            
                            # Price levels splitting
                            price_levels = []
                            ticks = 5
                            step = (h - l) / ticks if h > l else 1.0
                            for idx in range(ticks):
                                lvl_price = round(l + idx * step, 4)
                                lvl_buy = buy_vol / ticks
                                lvl_sell = sell_vol / ticks
                                price_levels.append([lvl_price, lvl_buy, lvl_sell, 0.0, 0, 0, 0, 0, 0])
                            
                            bars.append({
                                "timestamp": timestamp_str,
                                "ohlc": {"open": o, "high": h, "low": l, "close": c},
                                "metrics": {
                                    "delta": delta,
                                    "cvd": delta,
                                    "total_vol": v,
                                    "poc": poc,
                                    "vwap": vwap
                                },
                                "price_levels": price_levels,
                                "labels": ["VolumeSplitBar"],
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
                        
                        # Cache for 60 seconds
                        self._safe_setex(cache_key, 60, json.dumps(standardized))
                        return standardized
            except Exception:
                pass
        return None

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:bingx:ohlcv:{symbol_upper}:{interval}:{limit}:{market_type}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        timeframe_map = {
            "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m", "30m": "30m",
            "1h": "1h", "2h": "2h", "4h": "4h", "1d": "1d", "1D": "1d"
        }
        bingx_interval = timeframe_map.get(interval, "1h")

        if symbol_upper.endswith("USDT") and not symbol_upper.startswith("USDT") and "-" not in symbol_upper:
            bingx_symbol = f"{symbol_upper[:-4]}-USDT"
        elif "-" not in symbol_upper:
            bingx_symbol = f"{symbol_upper}-USDT"
        else:
            bingx_symbol = symbol_upper

        params = {
            "symbol": bingx_symbol,
            "interval": bingx_interval,
            "limit": limit
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=10.0)
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data.get("code") == 0:
                        data = res_data.get("data", [])
                        data.reverse()
                        mapped = []
                        for k in data:
                            mapped.append({
                                "timestamp": int(k.get("time", 0)),
                                "open": float(k.get("open", 0)),
                                "high": float(k.get("high", 0)),
                                "low": float(k.get("low", 0)),
                                "close": float(k.get("close", 0)),
                                "volume": float(k.get("volume", 0))
                            })
                        self._safe_setex(cache_key, 5, json.dumps(mapped))
                        return mapped
            except Exception:
                pass
        return []
