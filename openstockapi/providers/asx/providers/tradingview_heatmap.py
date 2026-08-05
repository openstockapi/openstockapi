import httpx
from typing import List, Dict, Any, Optional

class TradingViewHeatmapProvider:
    def __init__(self) -> None:
        self.name = "tradingview"

    async def get_heatmap(self, limit: int = 500) -> List[Dict[str, Any]]:
        url = "https://scanner.tradingview.com/australia/scan"
        payload = {
            "markets": ["australia"],
            "symbols": {
                "query": {"types": []},
                "tickers": []
            },
            "options": {"lang": "en"},
            "columns": [
                "name",
                "description",
                "change",
                "market_cap_basic",
                "sector",
                "industry",
                "logoid",
                "close"
            ],
            "sort": {
                "sortBy": "market_cap_basic",
                "sortOrder": "desc"
            },
            "range": [0, limit]
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    results = []
                    for item in data:
                        d = item.get("d", [])
                        if len(d) >= 8:
                            logo_id = d[6]
                            logo_url = f"https://s3-symbol-logo.tradingview.com/{logo_id}.svg" if logo_id else None
                            results.append({
                                "symbol": d[0],
                                "name": d[1],
                                "change": float(d[2]) if d[2] is not None else 0.0,
                                "change_pct": float(d[2]) if d[2] is not None else 0.0,
                                "price": float(d[7]) if d[7] is not None else 0.0,
                                "market_cap": float(d[3]) if d[3] is not None else 0.0,
                                "sector": d[4] or "Unknown",
                                "industry": d[5] or "Unknown",
                                "logo_url": logo_url,
                                "provider": self.name
                            })
                    return results
        except Exception:
            pass
        return []
