import httpx
import json
import datetime
from typing import List, Dict, Any, Optional

class TencentCNProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://gu.qq.com/"
        }

    def _format_symbol(self, symbol: str) -> str:
        sym = symbol.upper().strip()
        if sym.startswith(("SH", "SZ", "BJ")):
            return sym.lower()
        if sym.startswith(("60", "68", "90", "73", "5", "7")):
            return f"sh{sym.lower()}"
        if sym.startswith(("8", "4")):
            return f"bj{sym.lower()}"
        return f"sz{sym.lower()}"

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1d") -> Optional[Dict[str, Any]]:
        # Map range to number of bars
        days_map = {
            "1d": 1, "5d": 5, "1mo": 22, "3mo": 66, "6mo": 132, 
            "1y": 250, "2y": 500, "5y": 1250, "10y": 2500, "max": 5000
        }
        num_bars = days_map.get(range_str.lower(), 5)
        
        sym_formatted = self._format_symbol(symbol)
        url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        params = {
            "_var": "kline_dayqfq",
            "param": f"{sym_formatted},day,,,{num_bars},qfq"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    text = res.text.strip()
                    if "=" in text:
                        json_str = text.split("=", 1)[1]
                        data = json.loads(json_str)
                        if data.get("code") == 0 and "data" in data:
                            stock_data = data["data"].get(sym_formatted, {})
                            k_data = stock_data.get("qfqday", stock_data.get("day", []))
                            bars = []
                            for row in k_data:
                                dt = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                                ts = int(dt.timestamp() * 1000)
                                bars.append({
                                    "timestamp": ts,
                                    "open": float(row[1]),
                                    "high": float(row[3]),
                                    "low": float(row[4]),
                                    "close": float(row[2]),
                                    "volume": int(float(row[5]) * 100)
                                })
                            return {
                                "symbol": symbol.upper().strip(),
                                "currency": "CNY",
                                "bars": bars
                            }
        except Exception:
            pass
        return None

    async def _fetch_raw_fields(self, symbol: str) -> Optional[List[str]]:
        sym_formatted = self._format_symbol(symbol)
        url = f"http://qt.gtimg.cn/q={sym_formatted}"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    parts = res.text.strip().split("=")
                    if len(parts) == 2:
                        content = parts[1].strip('"').strip(';\n')
                        fields = content.split("~")
                        if len(fields) > 30:
                            return fields
        except Exception:
            pass
        return None

    async def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        fields = await self._fetch_raw_fields(symbol)
        if fields:
            ts_str = fields[30]
            try:
                dt = datetime.datetime.strptime(ts_str, "%Y%m%d%H%M%S")
                ts = int(dt.timestamp() * 1000)
            except Exception:
                ts = int(datetime.datetime.now().timestamp() * 1000)
            return {
                "symbol": symbol.upper().strip(),
                "price": float(fields[3]),
                "open": float(fields[5]),
                "high": float(fields[33]),
                "low": float(fields[34]),
                "volume": int(float(fields[6]) * 100),
                "timestamp": ts
            }
        return None

    async def get_tick(self, symbol: str) -> Optional[Dict[str, Any]]:
        fields = await self._fetch_raw_fields(symbol)
        if fields:
            ts_str = fields[30]
            formatted_time = f"{ts_str[8:10]}:{ts_str[10:12]}:{ts_str[12:14]}" if len(ts_str) >= 14 else ts_str
            return {
                "symbol": symbol.upper().strip(),
                "time": formatted_time,
                "price": float(fields[3]),
                "volume": int(float(fields[6]) * 100)
            }
        return None

    async def get_book_order(self, symbol: str) -> Optional[Dict[str, Any]]:
        fields = await self._fetch_raw_fields(symbol)
        if fields:
            bids = []
            asks = []
            for i in range(5):
                price = float(fields[9 + i * 2])
                vol = int(float(fields[10 + i * 2]) * 100)
                bids.append({"price": price, "volume": vol})
            for i in range(5):
                price = float(fields[19 + i * 2])
                vol = int(float(fields[20 + i * 2]) * 100)
                asks.append({"price": price, "volume": vol})
            return {
                "symbol": symbol.upper().strip(),
                "bids": bids,
                "asks": asks
            }
        return None
