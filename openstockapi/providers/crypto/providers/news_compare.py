import httpx
from typing import List, Dict, Any, Optional
from openstockapi.providers.crypto.base import CryptoBaseProvider

class CryptoCompareNewsProvider(CryptoBaseProvider):
    async def get_tickers(self) -> List[Dict[str, Any]]:
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        return None

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        return None

    async def get_news(self, limit: int = 20) -> List[Dict[str, Any]]:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json().get("Data", [])
                    # Normalize
                    return [
                        {
                            "id": item.get("id"),
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "published_at": int(item.get("published_on", 0)) * 1000,
                            "source": item.get("source_info", {}).get("name") or item.get("source"),
                            "summary": item.get("body")
                        }
                        for item in data[:limit]
                    ]
        except Exception:
            pass
        return []
