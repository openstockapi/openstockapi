import httpx
from typing import List, Dict, Any, Optional

class MarketIndexProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def get_financials(self, symbol: str) -> Optional[Dict[str, Any]]:
        # Query MarketIndex REST pages or endpoints
        url = f"https://www.marketindex.com.au/api/v1/companies/{symbol.lower()}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    # Map to standard financials schema
                    return {
                        "symbol": symbol.upper(),
                        "financials": data.get("financials", {}),
                        "ratios": data.get("ratios", {})
                    }
        except Exception:
            pass
            
        return None

    async def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        # Fetch dividend events
        url = f"https://www.marketindex.com.au/api/v1/companies/{symbol.lower()}/dividends"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    return [
                        {
                            "ex_date": item.get("ex_date"),
                            "pay_date": item.get("payment_date"),
                            "amount": item.get("amount"),
                            "type": item.get("type"),
                            "franking": item.get("franking")
                        }
                        for item in data
                    ]
        except Exception:
            pass
        return []

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        url = f"https://www.marketindex.com.au/api/v1/chart/prices/{symbol.lower()}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    prices = data if isinstance(data, list) else data.get("prices", [])
                    bars = []
                    for item in prices:
                        if isinstance(item, list) and len(item) >= 5:
                            bars.append({
                                "timestamp": item[0] if item[0] > 10000000000 else item[0] * 1000,
                                "open": float(item[1]),
                                "high": float(item[2]),
                                "low": float(item[3]),
                                "close": float(item[4]),
                                "volume": int(item[5]) if len(item) > 5 else 0
                            })
                        elif isinstance(item, dict):
                            bars.append({
                                "timestamp": item.get("t") or item.get("timestamp"),
                                "open": float(item.get("o") or item.get("open", 0)),
                                "high": float(item.get("h") or item.get("high", 0)),
                                "low": float(item.get("l") or item.get("low", 0)),
                                "close": float(item.get("c") or item.get("close", 0)),
                                "volume": int(item.get("v") or item.get("volume", 0))
                            })
                    if bars:
                        return {
                            "symbol": symbol.upper(),
                            "currency": "AUD",
                            "bars": bars[:100]
                        }
        except Exception:
            pass
        return None

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        url = f"https://www.marketindex.com.au/api/v1/companies/{symbol.lower()}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    website = data.get("website", "")
                    logo_url = None
                    if website:
                        from urllib.parse import urlparse
                        try:
                            parsed = urlparse(website)
                            domain = parsed.netloc or parsed.path
                            if domain.startswith("www."):
                                domain = domain[4:]
                            domain = domain.split("/")[0]
                            if domain:
                                logo_url = f"https://www.google.com/s2/favicons?sz=128&domain={domain}"
                        except Exception:
                            pass
                    return {
                        "symbol": symbol.upper(),
                        "company_name": data.get("name") or data.get("short_name"),
                        "sector": data.get("sector"),
                        "industry": data.get("industry"),
                        "website": website,
                        "logo_url": logo_url,
                        "headcount": data.get("employees") or data.get("headcount"),
                        "description": data.get("description") or data.get("summary")
                    }
        except Exception:
            pass
        return None

    async def get_announcements(self, symbol: str) -> List[Dict[str, Any]]:
        url = f"https://www.marketindex.com.au/api/v1/companies/{symbol.lower()}/announcements"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json().get("data", []) if isinstance(res.json(), dict) else res.json()
                    if not isinstance(data, list):
                        data = []
                    return [
                        {
                            "id": str(item.get("id") or item.get("document_key") or idx),
                            "title": item.get("title") or item.get("header") or item.get("description") or "Announcement",
                            "url": item.get("url") or item.get("pdf_url") or "",
                            "published_at": item.get("published_at") or item.get("date") or "",
                            "size": item.get("size") or ""
                        }
                        for idx, item in enumerate(data)
                    ]
        except Exception:
            pass
        return []
