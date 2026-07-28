import httpx
from typing import List, Dict, Any, Optional
from openstockapi.providers.crypto.base import CryptoBaseProvider

class CoinGeckoEventsProvider(CryptoBaseProvider):
    async def get_tickers(self) -> List[Dict[str, Any]]:
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        return None

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        return None

    async def get_events(self) -> List[Dict[str, Any]]:
        url = "https://api.coingecko.com/api/v3/events"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    return [
                        {
                            "title": item.get("title"),
                            "description": item.get("description"),
                            "organizer": item.get("organizer"),
                            "start_date": item.get("start_date"),
                            "end_date": item.get("end_date"),
                            "website": item.get("website"),
                            "venue": item.get("venue"),
                            "country": item.get("country")
                        }
                        for item in data
                    ]
        except Exception:
            pass
        
        # Return empty list on failure
        return []
