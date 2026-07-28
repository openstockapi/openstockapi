import httpx
from typing import List, Dict, Any

class NasdaqUSProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.nasdaq.com",
            "Referer": "https://www.nasdaq.com/"
        }

    async def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
        url = f"https://api.nasdaq.com/api/quote/{sym_norm}/dividends"
        params = {"assetclass": "stocks"}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    rows = data.get("data", {}).get("dividends", {}).get("rows", [])
                    if not rows:
                        return []
                    
                    dividends = []
                    for row in rows:
                        def parse_date(date_str: str) -> str:
                            if not date_str or date_str == "N/A":
                                return None
                            parts = date_str.split("/")
                            if len(parts) == 3:
                                return f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
                            return date_str

                        raw_amount = row.get("amount") or ""
                        clean_amount = raw_amount.replace("$", "").strip()
                        
                        try:
                            amount_val = float(clean_amount)
                        except ValueError:
                            amount_val = 0.0

                        dividends.append({
                            "ex_date": parse_date(row.get("exOrEffDate")),
                            "pay_date": parse_date(row.get("paymentDate")),
                            "amount": amount_val,
                            "type": "Dividend"
                        })
                    return dividends
        except Exception:
            pass
        return []

    async def get_splits(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
        url = f"https://api.nasdaq.com/api/quote/{sym_norm}/splits"
        params = {"assetclass": "stocks"}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    rows = data.get("data", {}).get("splits", {}).get("rows", [])
                    if not rows:
                        return []
                    
                    splits = []
                    for row in rows:
                        def parse_date(date_str: str) -> str:
                            if not date_str or date_str == "N/A":
                                return None
                            parts = date_str.split("/")
                            if len(parts) == 3:
                                return f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
                            return date_str

                        raw_ratio = row.get("ratio") or "1 : 1"
                        ratio_val = 1.0
                        try:
                            parts = [float(x.strip()) for x in raw_ratio.replace("/", ":").split(":") if x.strip()]
                            if len(parts) == 2 and parts[1] != 0:
                                ratio_val = parts[0] / parts[1]
                        except Exception:
                            pass

                        splits.append({
                            "date": parse_date(row.get("splitDate")),
                            "ratio": ratio_val
                        })
                    return splits
        except Exception:
            pass
        return []

    async def get_symbols(self) -> List[str]:
        url = "https://api.nasdaq.com/api/screener/stocks"
        params = {"tableonly": "true", "limit": "8000"}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    rows = data.get("data", {}).get("table", {}).get("rows", [])
                    if rows:
                        return sorted(list(set([r["symbol"].strip().upper() for r in rows if r.get("symbol")])))
        except Exception:
            pass
        
        return ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA", "TSLA", "META", "NFLX", "AMD", "INTC", "BRK.B", "JNJ", "V", "PG"]
