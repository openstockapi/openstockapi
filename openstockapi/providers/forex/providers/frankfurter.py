import httpx
import redis
import json
import datetime
from typing import Dict, Any, Optional
from openstockapi.config import settings

class FrankfurterOHLCVProvider:
    def __init__(self):
        self.base_url = "https://api.frankfurter.dev/v1"
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

    def _parse_ticker(self, ticker: str) -> Optional[tuple]:
        from openstockapi.providers.forex.normalizer import SymbolNormalizer
        ticker_upper = SymbolNormalizer.to_yahoo_ticker(ticker).upper()
        if ticker_upper.endswith("=X"):
            pair = ticker_upper[:-2]
            if len(pair) == 6:
                return pair[:3], pair[3:]
        return None

    def _parse_range(self, range_str: str) -> tuple:
        end_date = datetime.date.today()
        # Parse range (e.g. 5d, 1mo, 1y)
        days = 5
        if range_str.endswith("d"):
            try:
                days = int(range_str[:-1])
            except Exception:
                pass
        elif range_str.endswith("mo"):
            try:
                days = int(range_str[:-2]) * 30
            except Exception:
                pass
        elif range_str.endswith("y"):
            try:
                days = int(range_str[:-1]) * 365
            except Exception:
                pass
        
        start_date = end_date - datetime.timedelta(days=days)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    async def fetch_chart(self, ticker: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        parsed = self._parse_ticker(ticker)
        if not parsed:
            return None
        base, target = parsed

        cache_key = f"forex:frankfurter:chart:{ticker}:{range_str}:{interval_str}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        start_date, end_date = self._parse_range(range_str)
        url = f"{self.base_url}/{start_date}..{end_date}"
        params = {"from": base, "to": target}
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    rates_data = data.get("rates", {})
                    
                    bars = []
                    # Frankfurter returns: { "2026-07-20": { "VND": 25000 } }
                    for date_str, rates in sorted(rates_data.items()):
                        val = rates.get(target)
                        if val is not None:
                            rate = float(val)
                            # Convert YYYY-MM-DD to YYYY-MM-DD HH:MM:SS
                            dt_str = f"{date_str} 00:00:00"
                            bars.append({
                                "timestamp": dt_str,
                                "open": rate,
                                "high": rate,
                                "low": rate,
                                "close": rate,
                                "volume": 0.0
                            })
                            
                    if not bars:
                        return None
                        
                    standardized = {
                        "ticker": ticker,
                        "currency": target,
                        "regularMarketPrice": bars[-1]["close"],
                        "previousClose": bars[0]["close"],
                        "bars": bars
                    }
                    self._safe_setex(cache_key, 60, json.dumps(standardized))
                    return standardized
            except Exception:
                pass
        return None
