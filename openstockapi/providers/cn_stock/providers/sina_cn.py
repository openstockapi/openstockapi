import httpx
import asyncio
from typing import List, Dict, Any, Optional

class SinaCNProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://finance.sina.com.cn/"
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

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        # Map range_str to datalen (approximate number of days)
        days_map = {
            "1d": 1, "5d": 5, "1mo": 22, "3mo": 66, "6mo": 132, 
            "1y": 250, "2y": 500, "5y": 1250, "10y": 2500, "max": 5000
        }
        datalen = days_map.get(range_str.lower(), 5)
        
        sym_formatted = self._format_symbol(symbol)
        url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
        params = {
            "symbol": sym_formatted,
            "scale": "240", # 240 minutes = 1 day
            "ma": "no",
            "datalen": str(datalen)
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and data:
                        bars = []
                        import datetime
                        for row in data:
                            dt_str = row.get("day")
                            dt = datetime.datetime.strptime(dt_str.split()[0], "%Y-%m-%d")
                            ts = int(dt.timestamp() * 1000)
                            bars.append({
                                "timestamp": ts,
                                "open": float(row["open"]),
                                "high": float(row["high"]),
                                "low": float(row["low"]),
                                "close": float(row["close"]),
                                "volume": int(row["volume"])
                            })
                        return {
                            "symbol": symbol.upper().strip(),
                            "currency": "CNY",
                            "bars": bars
                        }
        except Exception:
            pass
        return None

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_formatted = self._format_symbol(symbol)
        url = f"https://hq.sinajs.cn/list={sym_formatted}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    parts = res.text.strip().split("=")
                    if len(parts) == 2:
                        content = parts[1].strip('"').strip(';\n')
                        fields = content.split(",")
                        if len(fields) > 1:
                            company_name = fields[0]
                            return {
                                "symbol": symbol.upper().strip(),
                                "company_name": company_name,
                                "sector": None,
                                "industry": "CN Equity",
                                "website": "https://finance.sina.com.cn",
                                "logo_url": None,
                                "headcount": None,
                                "description": f"CN listed stock {company_name} traded on Shanghai/Shenzhen exchanges."
                            }
        except Exception:
            pass
        return None

    async def get_financials(self, symbol: str, period: str = "annual") -> Optional[Dict[str, Any]]:
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        clean_symbol = symbol.upper().strip().replace(".SS", "").replace(".SZ", "")
        params = {
            "reportName": "RPT_LICO_FN_CPD",
            "filter": f'(SECURITY_CODE="{clean_symbol}")',
            "pageSize": "10",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success") and "result" in data and "data" in data["result"]:
                        rows = data["result"]["data"]
                        periods = []
                        available_periods = []
                        for row in rows:
                            rep_date_full = row.get("REPORTDATE", "")
                            if not rep_date_full:
                                continue
                            rep_date = rep_date_full.split()[0]
                            
                            if period == "annual" and not rep_date.endswith("-12-31"):
                                continue
                                
                            available_periods.append(rep_date)
                            periods.append({
                                "period": rep_date,
                                "financials": {
                                    "balance_sheet": {
                                        "total_assets": row.get("TOTAL_ASSETS"),
                                        "total_liabilities": row.get("TOTAL_LIABILITIES")
                                    },
                                    "income_statement": {
                                        "revenue": row.get("TOTAL_OPERATE_INCOME"),
                                        "net_income": row.get("PARENT_NETPROFIT")
                                    },
                                    **{k.lower(): v for k, v in row.items() if v is not None}
                                }
                            })
                            
                        return {
                            "symbol": symbol.upper().strip(),
                            "period_type": period,
                            "available_periods": available_periods,
                            "periods": periods
                        }
        except Exception:
            pass
        return None

    async def get_ratios(self, symbol: str) -> Optional[Dict[str, Any]]:
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        clean_symbol = symbol.upper().strip().replace(".SS", "").replace(".SZ", "")
        params = {
            "reportName": "RPT_LICO_FN_CPD",
            "filter": f'(SECURITY_CODE="{clean_symbol}")',
            "pageSize": "1",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success") and "result" in data and "data" in data["result"]:
                        rows = data["result"]["data"]
                        if rows:
                            row = rows[0]
                            return {
                                "symbol": symbol.upper().strip(),
                                "ratios": {
                                    "pe_trailing": None,
                                    "pe_forward": None,
                                    "pb": None,
                                    "roe": row.get("WEIGHTAVG_ROE"),
                                    "roa": None,
                                    "debt_to_equity": None
                                }
                            }
        except Exception:
            pass
        return None

    async def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        clean_symbol = symbol.upper().strip().replace(".SS", "").replace(".SZ", "")
        params = {
            "reportName": "RPT_SHAREBONUS_DET",
            "filter": f'(SECURITY_CODE="{clean_symbol}")',
            "pageSize": "50",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        res_list = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success") and "result" in data and "data" in data["result"]:
                        rows = data["result"]["data"]
                        for row in rows:
                            ex_div_date_full = row.get("EX_DIVIDEND_DATE")
                            if not ex_div_date_full:
                                continue
                            ex_div_date = ex_div_date_full.split()[0]
                            pretax_rmb = row.get("PRETAX_BONUS_RMB")
                            amount = float(pretax_rmb) / 10.0 if pretax_rmb is not None else 0.0
                            res_list.append({
                                "ex_date": ex_div_date,
                                "pay_date": None,
                                "amount": amount,
                                "type": "Dividend"
                            })
        except Exception:
            pass
        return res_list

    async def get_splits(self, symbol: str) -> List[Dict[str, Any]]:
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        clean_symbol = symbol.upper().strip().replace(".SS", "").replace(".SZ", "")
        params = {
            "reportName": "RPT_SHAREBONUS_DET",
            "filter": f'(SECURITY_CODE="{clean_symbol}")',
            "pageSize": "50",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        res_list = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success") and "result" in data and "data" in data["result"]:
                        rows = data["result"]["data"]
                        for row in rows:
                            ex_div_date_full = row.get("EX_DIVIDEND_DATE")
                            if not ex_div_date_full:
                                continue
                            ex_div_date = ex_div_date_full.split()[0]
                            
                            bonus_ratio = row.get("BONUS_RATIO") or 0.0
                            it_ratio = row.get("IT_RATIO") or 0.0
                            
                            if bonus_ratio > 0 or it_ratio > 0:
                                ratio = 1.0 + (float(bonus_ratio) + float(it_ratio)) / 10.0
                                res_list.append({
                                    "date": ex_div_date,
                                    "ratio": ratio
                                })
        except Exception:
            pass
        return res_list

    async def get_calendar(self, symbol: str) -> Optional[Dict[str, Any]]:
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        clean_symbol = symbol.upper().strip().replace(".SS", "").replace(".SZ", "")
        params = {
            "reportName": "RPT_PUBLIC_BS_APPOIN",
            "filter": f'(SECURITY_CODE="{clean_symbol}")',
            "pageSize": "5",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success") and "result" in data and "data" in data["result"]:
                        rows = data["result"]["data"]
                        earnings_dates = []
                        for row in rows:
                            pub_date_full = row.get("APPOINT_PUBLISH_DATE")
                            if pub_date_full:
                                pub_date = pub_date_full.split()[0]
                                earnings_dates.append(pub_date)
                        if earnings_dates:
                            return {
                                "symbol": symbol.upper().strip(),
                                "calendar": {
                                    "Earnings Date": earnings_dates[:2]
                                }
                            }
        except Exception:
            pass
        return None

    async def _fetch_raw_fields(self, symbol: str) -> Optional[List[str]]:
        sym_formatted = self._format_symbol(symbol)
        url = f"https://hq.sinajs.cn/list={sym_formatted}"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    parts = res.text.strip().split("=")
                    if len(parts) == 2:
                        content = parts[1].strip('"').strip(';\n')
                        fields = content.split(",")
                        if len(fields) > 30:
                            return fields
        except Exception:
            pass
        return None

    async def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        fields = await self._fetch_raw_fields(symbol)
        if fields:
            import datetime
            try:
                dt_str = f"{fields[30]} {fields[31]}"
                dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                ts = int(dt.timestamp() * 1000)
            except Exception:
                ts = int(datetime.datetime.now().timestamp() * 1000)
            return {
                "symbol": symbol.upper().strip(),
                "price": float(fields[3]),
                "open": float(fields[1]),
                "high": float(fields[4]),
                "low": float(fields[5]),
                "volume": int(fields[8]),
                "timestamp": ts
            }
        return None

    async def get_tick(self, symbol: str) -> Optional[Dict[str, Any]]:
        fields = await self._fetch_raw_fields(symbol)
        if fields:
            return {
                "symbol": symbol.upper().strip(),
                "time": fields[31],
                "price": float(fields[3]),
                "volume": int(fields[8])
            }
        return None

    async def get_book_order(self, symbol: str) -> Optional[Dict[str, Any]]:
        fields = await self._fetch_raw_fields(symbol)
        if fields:
            bids = []
            asks = []
            for i in range(5):
                vol = int(fields[10 + i * 2])
                price = float(fields[11 + i * 2])
                bids.append({"price": price, "volume": vol})
            for i in range(5):
                vol = int(fields[20 + i * 2])
                price = float(fields[21 + i * 2])
                asks.append({"price": price, "volume": vol})
            return {
                "symbol": symbol.upper().strip(),
                "bids": bids,
                "asks": asks
            }
        return None
