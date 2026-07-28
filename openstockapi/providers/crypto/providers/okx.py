import httpx
import redis
import json
import datetime
from typing import List, Dict, Any, Optional
from openstockapi.config import settings
from openstockapi.providers.crypto.base import CryptoBaseProvider

class OKXProvider(CryptoBaseProvider):
    def __init__(self):
        self.base_url = "https://www.okx.com/api/v5/market"
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
        cache_key = "crypto:okx:tickers"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/tickers"
        params = {"instType": "SPOT"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    list_data = data.get("data", [])
                    mapped = []
                    for t in list_data:
                        # OKX symbol format: BTC-USDT
                        inst_id = t["instId"]
                        # Convert to BTCUSDT standard
                        symbol_std = inst_id.replace("-", "")
                        if inst_id.endswith("-USDT"):
                            mapped.append({
                                "symbol": symbol_std,
                                "price": float(t["last"])
                            })
                    self._safe_setex(cache_key, 2, json.dumps(mapped))
                    return mapped
            except Exception:
                pass
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        # Convert BTCUSDT -> BTC-USDT
        if symbol_upper.endswith("USDT") and not symbol_upper.startswith("USDT") and "-" not in symbol_upper:
            inst_id = f"{symbol_upper[:-4]}-USDT"
        else:
            inst_id = symbol_upper

        cache_key = f"crypto:okx:depth:{symbol_upper}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/books"
        params = {"instId": inst_id, "sz": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    book = data.get("data", [{}])[0]
                    standardized = {
                        "symbol": symbol_upper,
                        "lastUpdateId": int(book.get("ts", 0)),
                        "bids": [[float(b[0]), float(b[1])] for b in book.get("bids", [])],
                        "asks": [[float(a[0]), float(a[1])] for a in book.get("asks", [])]
                    }
                    self._safe_setex(cache_key, 1, json.dumps(standardized))
                    return standardized
            except Exception:
                pass
        return None

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        # Convert BTCUSDT -> BTC-USDT
        if market_type.lower() == "futures":
            if symbol_upper.endswith("USDT") and not symbol_upper.startswith("USDT") and "-" not in symbol_upper:
                inst_id = f"{symbol_upper[:-4]}-USDT-SWAP"
            elif "-" in symbol_upper and not symbol_upper.endswith("-SWAP"):
                inst_id = f"{symbol_upper}-SWAP"
            elif not symbol_upper.endswith("-SWAP"):
                inst_id = f"{symbol_upper}-SWAP"
            else:
                inst_id = symbol_upper
        else:
            if symbol_upper.endswith("USDT") and not symbol_upper.startswith("USDT") and "-" not in symbol_upper:
                inst_id = f"{symbol_upper[:-4]}-USDT"
            elif "-" not in symbol_upper:
                inst_id = f"{symbol_upper}-USDT"
            else:
                inst_id = symbol_upper

        cache_key = f"crypto:okx:ohlcv:{symbol_upper}:{interval}:{limit}:{market_type}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        # Map interval
        interval_map = {
            "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m", "30m": "30m",
            "1h": "1H", "2h": "2H", "4h": "4H", "1d": "1D", "1D": "1D"
        }
        okx_interval = interval_map.get(interval, "1H")

        url = f"{self.base_url}/candles"
        params = {"instId": inst_id, "bar": okx_interval, "limit": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    candles = data.get("data", [])
                    mapped = []
                    for c in candles:
                        # OKX candle: [ts, open, high, low, close, vol, volCcy, volCcyQuote, confirm]
                        mapped.append({
                            "timestamp": int(c[0]),
                            "open": float(c[1]),
                            "high": float(c[2]),
                            "low": float(c[3]),
                            "close": float(c[4]),
                            "volume": float(c[5])
                        })
                    mapped.reverse()
                    self._safe_setex(cache_key, 5, json.dumps(mapped))
                    return mapped
            except Exception:
                pass
        return []

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        symbol_upper = symbol.upper()
        cache_key = f"crypto:okx:footprint:{symbol_upper}:{timeframe}:{limit}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

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
        if symbol_upper.endswith("USDT") and not symbol_upper.startswith("USDT") and "-" not in symbol_upper:
            inst_id = f"{symbol_upper[:-4]}-USDT-SWAP"
        elif "-" in symbol_upper and not symbol_upper.endswith("-SWAP"):
            inst_id = f"{symbol_upper}-SWAP"
        else:
            inst_id = symbol_upper

        cache_key = f"crypto:okx:derivatives:{symbol_upper}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        oi_url = "https://www.okx.com/api/v5/market/open-interest"
        funding_url = "https://www.okx.com/api/v5/public/funding-rate"
        
        async with httpx.AsyncClient() as client:
            try:
                oi_res = await client.get(oi_url, params={"instId": inst_id}, timeout=5.0)
                funding_res = await client.get(funding_url, params={"instId": inst_id}, timeout=5.0)
                
                oi_val = 0.0
                fr_val = 0.0
                next_funding_time = 0
                
                if oi_res.status_code == 200:
                    oi_data = oi_res.json().get("data", [])
                    if oi_data:
                        oi_val = float(oi_data[0].get("oi", 0.0))
                        
                if funding_res.status_code == 200:
                    f_data = funding_res.json().get("data", [])
                    if f_data:
                        fr_val = float(f_data[0].get("fundingRate", 0.0))
                        try:
                            next_funding_time = int(f_data[0].get("fundingTime", 0))
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

    # ─── OKX Options Methods (Deribit Backup) ───────────────────────────────

    async def get_options_instruments(self, currency: str = "BTC", kind: str = "option") -> List[Dict[str, Any]]:
        """
        Fetches option or future instruments for the given currency from OKX.
        Maps OKX format to the unified model.
        """
        # OKX uses BTC-USD or BTC-USDT as underlying index. Let's use currency.upper() + "-USD" as base uly
        uly = f"{currency.upper()}-USD"
        inst_type = "OPTION" if kind.lower() == "option" else "FUTURES"
        
        url = "https://www.okx.com/api/v5/public/instruments"
        params = {"instType": inst_type, "uly": uly}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    raw_insts = data.get("data", [])
                    return [
                        {
                            "instrument_name": inst.get("instId"),
                            "currency": inst.get("uly"),
                            "kind": inst.get("instType").lower(),
                            "strike": float(inst.get("stk")) if inst.get("stk") else None,
                            "expiration_timestamp": int(inst.get("expTime")) if inst.get("expTime") else None,
                            "option_type": "call" if inst.get("optType") == "C" else ("put" if inst.get("optType") == "P" else None),
                            "is_active": inst.get("state") == "live",
                        }
                        for inst in raw_insts
                    ]
        except Exception:
            pass
        return []

    async def get_options_chain(self, currency: str = "BTC") -> List[Dict[str, Any]]:
        """
        Fetches market ticker summaries for options under a currency to build options chain.
        """
        uly = f"{currency.upper()}-USD"
        url = "https://www.okx.com/api/v5/market/tickers"
        params = {"instType": "OPTION", "uly": uly}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    raw_tickers = data.get("data", [])
                    return [
                        {
                            "instrument_name": t.get("instId"),
                            "underlying_price": None, # OKX doesn't provide this directly in the list
                            "mark_price": float(t.get("sodPx")) if t.get("sodPx") else None, # Start of day / mark reference
                            "bid_price": float(t.get("bidPx")) if t.get("bidPx") else None,
                            "ask_price": float(t.get("askPx")) if t.get("askPx") else None,
                            "mark_iv": float(t.get("markVol")) if t.get("markVol") else None,
                            "bid_iv": None,
                            "ask_iv": None,
                            "volume": float(t.get("vol24h")) if t.get("vol24h") else None,
                            "open_interest": None,
                            "creation_timestamp": int(t.get("ts")) if t.get("ts") else None,
                        }
                        for t in raw_tickers
                    ]
        except Exception:
            pass
        return []

    async def get_options_ticker(self, instrument_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetches detailed ticker including option Greeks for a specific contract.
        """
        # First fetch standard ticker data
        url = "https://www.okx.com/api/v5/market/ticker"
        params = {"instId": instrument_name}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # OKX ticker contains option greeks and volatility if instType is OPTION
                res = await client.get(url, params=params)
                if res.status_code == 200:
                    t_data = res.json().get("data", [])
                    if t_data:
                        t = t_data[0]
                        # Fetch mark price / greeks details from public API
                        public_url = "https://www.okx.com/api/v5/public/mark-price"
                        pub_res = await client.get(public_url, params={"instId": instrument_name})
                        
                        greeks = {}
                        mark_price = None
                        iv = None
                        
                        if pub_res.status_code == 200:
                            pub_data = pub_res.json().get("data", [])
                            if pub_data:
                                p = pub_data[0]
                                mark_price = float(p.get("markPx")) if p.get("markPx") else None
                                
                        # Let's fallback or use ticker fields
                        # Note: OKX ticker fields for options do not have the complete Greeks, so public mark-price is queried.
                        return {
                            "instrument_name": instrument_name,
                            "underlying_index": t.get("uly"),
                            "underlying_price": None,
                            "mark_price": mark_price,
                            "mark_iv": float(t.get("markVol")) if t.get("markVol") else None,
                            "bid_price": float(t.get("bidPx")) if t.get("bidPx") else None,
                            "ask_price": float(t.get("askPx")) if t.get("askPx") else None,
                            "last_price": float(t.get("last")) if t.get("last") else None,
                            "volume": float(t.get("vol24h")) if t.get("vol24h") else None,
                            "open_interest": None,
                            "settlement_price": None,
                            "timestamp": int(t.get("ts")) if t.get("ts") else None,
                            "greeks": {
                                "delta": float(t.get("delta")) if t.get("delta") else None,
                                "gamma": float(t.get("gamma")) if t.get("gamma") else None,
                                "theta": float(t.get("theta")) if t.get("theta") else None,
                                "vega": float(t.get("vega")) if t.get("vega") else None,
                                "rho": None
                            }
                        }
        except Exception:
            pass
        return None

