import httpx
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SerpApiUSProvider:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY", "")
        self.base_url = "https://serpapi.com/search"

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        # SerpApi Google Finance API uses engine=google_finance
        # and search query 'q' as SYMBOL:EXCHANGE (e.g., GOOGL:NASDAQ)
        # For simplicity, we assume exchange is NASDAQ or NYSE. 
        # Usually symbols like AAPL are GOOGL:NASDAQ or AAPL:NASDAQ
        # In real case, we might need a mapping or search first, but here we assume NASDAQ as default.
        sym_upper = symbol.upper().strip()
        q = f"{sym_upper}:NASDAQ"
        
        params = {
            "engine": "google_finance",
            "q": q,
            "api_key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.base_url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    graph = data.get("graph", [])
                    
                    bars = []
                    for item in graph:
                        # Map graph data to ohlcv bar format
                        # Date example: "May 22 2026, 09:30 AM UTC-04:00"
                        date_str = item.get("date")
                        ts = int(datetime.now().timestamp() * 1000) # Fallback timestamp
                        if date_str:
                            try:
                                # Quick parse for standard google finance date format
                                # Removing timezone offset suffix (e.g., UTC-04:00) for standard python datetime parsing
                                clean_date_str = date_str.split("UTC")[0].strip()
                                dt = datetime.strptime(clean_date_str, "%b %d %Y, %I:%M %p")
                                ts = int(dt.timestamp() * 1000)
                            except Exception:
                                pass
                        
                        price = float(item.get("price", 0))
                        volume = float(item.get("volume", 0))
                        
                        # Google Finance graph doesn't always have open, high, low, close separately.
                        # We use price for all of them if not available.
                        bars.append({
                            "timestamp": ts,
                            "open": price,
                            "high": price,
                            "low": price,
                            "close": price,
                            "volume": volume
                        })
                    
                    return {
                        "symbol": sym_upper,
                        "currency": graph[0].get("currency", "USD") if graph else "USD",
                        "bars": bars
                    }
        except Exception as e:
            logger.error(f"SerpApiUSProvider get_ohlcv error: {str(e)}")
        return None

    async def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_upper = symbol.upper().strip()
        q = f"{sym_upper}:NASDAQ"
        
        params = {
            "engine": "google_finance",
            "q": q,
            "api_key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.base_url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    summary = data.get("summary", {})
                    # Standard quote structure
                    price = float(summary.get("price", 0))
                    change = float(summary.get("price_movement", {}).get("value", 0))
                    pct_change = float(summary.get("price_movement", {}).get("percentage", 0))
                    
                    # Determine sign of change based on movement direction
                    movement = summary.get("price_movement", {}).get("movement", "").lower()
                    if movement == "down" and change > 0:
                        change = -change
                        pct_change = -pct_change
                        
                    return {
                        "symbol": sym_upper,
                        "price": price,
                        "change": change,
                        "pct_change": pct_change,
                        "volume": 0.0, # Google Finance summary doesn't always have current volume directly in summary
                        "timestamp": int(datetime.now().timestamp() * 1000)
                    }
        except Exception as e:
            logger.error(f"SerpApiUSProvider get_quote error: {str(e)}")
        return None

    async def get_news(self, symbol: str) -> List[Dict[str, Any]]:
        sym_upper = symbol.upper().strip()
        q = f"{sym_upper}:NASDAQ"
        
        params = {
            "engine": "google_finance",
            "q": q,
            "api_key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(self.base_url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    news_results = data.get("news_results", [])
                    
                    news_list = []
                    for item in news_results:
                        date_str = item.get("date")
                        ts = int(datetime.now().timestamp() * 1000)
                        if date_str:
                            try:
                                # Example: "3 hours ago" or "May 22, 2026"
                                # For quick demo, we use simple timestamp or current
                                pass
                            except Exception:
                                pass
                                
                        news_list.append({
                            "id": item.get("link", ""),
                            "title": item.get("title", ""),
                            "url": item.get("link", ""),
                            "published_at": ts,
                            "source": item.get("source", ""),
                            "summary": item.get("snippet", "")
                        })
                    return news_list
        except Exception as e:
            logger.error(f"SerpApiUSProvider get_news error: {str(e)}")
        return []
