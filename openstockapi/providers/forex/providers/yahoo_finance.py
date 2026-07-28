import httpx
import redis
import json
import datetime
from typing import Dict, Any, Optional
from openstockapi.config import settings
from openstockapi.providers.forex.normalizer import SymbolNormalizer

class YahooFinanceProvider:
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
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

    async def fetch_chart(self, ticker: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        normalized = SymbolNormalizer.to_yahoo_ticker(ticker)
        cache_key = f"forex:yahoo_finance:chart:{normalized}:{range_str}:{interval_str}"
        cached = self._safe_get(cache_key)
        if cached:
            return json.loads(cached)

        url = f"{self.base_url}/{normalized}"
        params = {"range": range_str, "interval": interval_str}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    chart = data.get("chart", {})
                    result = chart.get("result", [])
                    if not result:
                        return None
                        
                    res_data = result[0]
                    meta = res_data.get("meta", {})
                    indicators = res_data.get("indicators", {})
                    quote = indicators.get("quote", [{}])[0]
                    timestamps = res_data.get("timestamp", [])
                    
                    # Map to standardized bars
                    bars = []
                    opens = quote.get("open", [])
                    highs = quote.get("high", [])
                    lows = quote.get("low", [])
                    closes = quote.get("close", [])
                    volumes = quote.get("volume", [])
                    
                    for i in range(len(timestamps)):
                        if i >= len(opens) or opens[i] is None or closes[i] is None:
                            continue
                        dt = datetime.datetime.utcfromtimestamp(timestamps[i])
                        bars.append({
                            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                            "open": round(float(opens[i]), 4),
                            "high": round(float(highs[i]), 4),
                            "low": round(float(lows[i]), 4),
                            "close": round(float(closes[i]), 4),
                            "volume": float(volumes[i]) if (volumes and i < len(volumes) and volumes[i] is not None) else 0.0
                        })
                        
                    standardized = {
                        "ticker": ticker,
                        "currency": meta.get("currency"),
                        "regularMarketPrice": meta.get("regularMarketPrice"),
                        "previousClose": meta.get("previousClose"),
                        "bars": bars
                    }
                    self._safe_setex(cache_key, 60, json.dumps(standardized))
                    return standardized
            except Exception:
                pass
        return None
