import redis
import json
import httpx
import datetime
from typing import List, Dict, Any, Optional
from openstockapi.config import settings

class HyperliquidProvider:
    def __init__(self):
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

    async def get_orderbook_heatmap(self, symbol: str, timeframe: str = "15min", limit: int = 50) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:hyperliquid:ob_heatmap:{symbol_upper}:{timeframe}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Generate timestamps for limit bars
        now = datetime.datetime.utcnow()
        minutes_map = {
            "1min": 1, "5min": 5, "15min": 15, "30min": 30,
            "1h": 60, "4h": 240, "1d": 1440
        }
        step_mins = minutes_map.get(timeframe, 15)
        
        timestamps = []
        for i in range(limit):
            dt = now - datetime.timedelta(minutes=(limit - i) * step_mins)
            timestamps.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

        # Fetch current price as reference
        current_price = 60000.0
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol_upper}USDT", timeout=3.0)
                if res.status_code == 200:
                    current_price = float(res.json().get("price", 60000.0))
        except Exception:
            pass

        # Generate price levels around current price
        price_step = round(current_price * 0.001, 2)  # 0.1% steps
        price_levels = [round(current_price - (5 - j) * price_step, 2) for j in range(11)]

        # Generate mock matrices (bid and ask distribution)
        bid_matrix = []
        ask_matrix = []
        
        # Matrix dimensions: len(price_levels) x len(timestamps)
        for p_idx in range(len(price_levels)):
            bid_row = []
            ask_row = []
            for t_idx in range(len(timestamps)):
                # Higher bids below current price, higher asks above current price
                dist_factor = abs(p_idx - 5)
                val = max(0.0, 5.0 - dist_factor) + (t_idx % 3) * 0.5
                if p_idx < 5:
                    bid_row.append(round(val, 3))
                    ask_row.append(0.0)
                elif p_idx > 5:
                    bid_row.append(0.0)
                    ask_row.append(round(val, 3))
                else:
                    bid_row.append(0.0)
                    ask_row.append(0.0)
            bid_matrix.append(bid_row)
            ask_matrix.append(ask_row)

        last_price_series = [current_price] * len(timestamps)

        result = {
            "symbol": symbol_upper,
            "timeframe": timeframe,
            "price_levels": price_levels,
            "bar_timestamps": timestamps,
            "bid_matrix": bid_matrix,
            "ask_matrix": ask_matrix,
            "last_price_series": last_price_series
        }

        # Cache for 5 seconds
        self._safe_setex(cache_key, 5, json.dumps(result))
        return result

    async def get_liq_heatmap(self, symbol: str, timeframe: str = "1h", limit: int = 720) -> Optional[Dict[str, Any]]:
        # Alias/wrapper for simulated model to provide data stably without complex Hyperliquid credentials
        return await self.get_sim_liq_heatmap(symbol, timeframe, limit)

    async def get_sim_liq_heatmap(self, symbol: str, timeframe: str = "1h", limit: int = 720) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:hyperliquid:sim_liq_heatmap:{symbol_upper}:{timeframe}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Get Klines to base simulation on real price action
        timeframe_map = {"1min": "1m", "5min": "5m", "15min": "15m", "30min": "30m", "1h": "1h", "4h": "4h", "1d": "1d"}
        interval = timeframe_map.get(timeframe, "1h")
        
        klines = []
        try:
            # We look at symbol + USDT for Binance perpetual price tracking
            binance_symbol = f"{symbol_upper}USDT"
            url = f"https://api.binance.com/api/v3/klines"
            async with httpx.AsyncClient() as client:
                res = await client.get(url, params={"symbol": binance_symbol, "interval": interval, "limit": min(limit, 100)}, timeout=5.0)
                if res.status_code == 200:
                    klines = res.json()
        except Exception:
            pass

        if not klines:
            # Fallback mock data if api call fails
            return {
                "symbol": symbol_upper,
                "timeframe": timeframe,
                "price_bins": [],
                "timestamps": [],
                "matrix": []
            }

        timestamps = []
        prices = []
        for k in klines:
            dt = datetime.datetime.utcfromtimestamp(k[0] / 1000.0)
            timestamps.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
            prices.append(float(k[4]))  # Close price

        # Generate bins around the min/max prices
        min_p = min(prices)
        max_p = max(prices)
        spread = max_p - min_p if max_p > min_p else min_p * 0.05
        price_bins = [round(min_p + i * (spread / 10), 2) for i in range(11)]

        # Build simulated liquidation intensity matrix (11 price levels x N timestamps)
        matrix = []
        for p_bin in price_bins:
            row = []
            for p in prices:
                # Simulate liquidation points: if close price is close to the price bin, 
                # there's higher liquidation activity/simulation intensity
                dist = abs(p - p_bin) / p
                intensity = max(0.0, 100.0 - dist * 5000.0)  # Peak intensity near the price
                row.append(round(intensity, 2))
            matrix.append(row)

        result = {
            "symbol": symbol_upper,
            "timeframe": timeframe,
            "price_bins": price_bins,
            "timestamps": timestamps,
            "matrix": matrix
        }

        # Cache for 10 seconds
        self._safe_setex(cache_key, 10, json.dumps(result))
        return result
