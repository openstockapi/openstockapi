import httpx
import csv
from typing import List, Dict, Any, Optional

class ASXSiteProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def get_symbols(self) -> List[str]:
        # Try TradingView first as it is more reliable and doesn't block Python requests
        try:
            from openstockapi.providers.asx.providers.tradingview_heatmap import TradingViewHeatmapProvider
            tv = TradingViewHeatmapProvider()
            heatmap = await tv.get_heatmap(limit=5000)
            symbols = [item["symbol"] for item in heatmap if item.get("symbol")]
            if symbols:
                return symbols
        except Exception:
            pass

        # Fallback to fetching listed companies CSV directly from ASX
        url = "https://www.asx.com.au/asx/research/ASXListedCompanies.csv"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    lines = res.text.splitlines()
                    reader = csv.reader(lines)
                    symbols = []
                    # Skip header rows (ASX CSV typically has descriptive headers in first 3 lines)
                    for row in reader:
                        if len(row) > 1 and len(row[1]) >= 3 and row[1].isupper() and row[1].isalpha():
                            symbols.append(row[1])
                    if symbols:
                        return symbols
        except Exception:
            pass
            
        return ["BHP", "CBA", "TLS", "CSL", "WBC", "NAB", "ANZ", "FMG", "MQG", "RIO"]

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        # Query ASX directory API (internal Markit/ASX endpoint)
        url = f"https://www.asx.com.au/asx/1/share/{symbol.upper()}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    return {
                        "symbol": data.get("code"),
                        "company_name": data.get("name_short"),
                        "sector": None,
                        "industry": data.get("gics_industry"),
                        "website": "",
                        "logo_url": None,
                        "headcount": None,
                        "description": f"Listed on ASX, GICS Industry: {data.get('gics_industry')}"
                    }
        except Exception:
            pass
        return None

    async def get_announcements(self, symbol: str) -> List[Dict[str, Any]]:
        # ASX announcements API endpoint
        url = f"https://www.asx.com.au/asx/1/company/{symbol.upper()}/announcements"
        params = {"count": 20}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    return [
                        {
                            "id": item.get("id"),
                            "title": item.get("header"),
                            "url": f"https://www.asx.com.au/asxpdf/{item.get('document_release_date')[:8]}/pdf/{item.get('document_key')}.pdf",
                            "published_at": item.get("document_release_date"),
                            "size": item.get("size")
                        }
                        for item in data
                    ]
        except Exception:
            pass
        return []

    async def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        url = f"https://www.asx.com.au/asx/1/share/{symbol.upper()}/dividends"
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
                            "franking": item.get("franking_percent")
                        }
                        for item in data
                    ]
        except Exception:
            pass
        return []
