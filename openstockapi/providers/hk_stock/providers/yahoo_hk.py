import yfinance as yf
import asyncio
import math
from typing import List, Dict, Any, Optional

class YahooHKProvider:
    def __init__(self):
        pass

    def _format_symbol(self, symbol: str) -> str:
        sym = symbol.upper().strip()
        if sym.endswith(".HK"):
            return sym
        digits = ''.join(c for c in sym if c.isdigit())
        padded = digits.zfill(4)
        return f"{padded}.HK"

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                valid_intervals = {
                    "1m": "1m", "2m": "2m", "5m": "5m", "15m": "15m", "30m": "30m",
                    "60m": "60m", "90m": "90m", "1h": "1h", "1d": "1d", "5d": "5d",
                    "1wk": "1wk", "1mo": "1mo", "3mo": "3mo"
                }
                inv = valid_intervals.get(interval_str, "1h")
                return ticker.history(period=range_str, interval=inv)
            
            df = await asyncio.to_thread(_fetch)
            if not df.empty:
                bars = []
                for index, row in df.iterrows():
                    ts = int(index.timestamp() * 1000)
                    bars.append({
                        "timestamp": ts,
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"])
                    })
                return {
                    "symbol": symbol.upper().strip(),
                    "currency": "HKD",
                    "bars": bars
                }
        except Exception:
            pass
        return None

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.info
            info = await asyncio.to_thread(_fetch)
            if info:
                website = info.get("website")
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
                    "symbol": symbol.upper().strip(),
                    "company_name": info.get("longName") or info.get("shortName"),
                    "sector": info.get("sector"),
                    "industry": info.get("industry"),
                    "website": website,
                    "logo_url": logo_url,
                    "headcount": info.get("fullTimeEmployees"),
                    "description": info.get("longBusinessSummary")
                }
        except Exception:
            pass
        return None

    async def get_financials(self, symbol: str, period: str = "annual") -> Optional[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        is_quarterly = (period.lower() == "quarterly")
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                if is_quarterly:
                    return (
                        ticker.quarterly_balance_sheet,
                        ticker.quarterly_financials,
                        ticker.quarterly_cashflow,
                        ticker.info
                    )
                return ticker.balance_sheet, ticker.financials, ticker.cashflow, ticker.info
            bs, fin, cf, info = await asyncio.to_thread(_fetch)

            if bs.empty:
                return None

            def build_statement(df, col):
                if df.empty or col not in df.columns:
                    return {}
                import re
                d = {}
                for idx in df.index:
                    key = re.sub(r'[^a-z0-9_]', '', str(idx).lower().strip().replace(' ', '_').replace('-', '_').replace('/', '_'))
                    val = df.loc[idx][col]
                    if val is not None and not (isinstance(val, float) and math.isnan(val)):
                        d[key] = float(val) if isinstance(val, (int, float)) else val
                return d

            def iv(key):
                val = info.get(key)
                if val is not None and not (isinstance(val, float) and math.isnan(val)):
                    return val
                return None

            ratios = {
                "pe_trailing":               iv("trailingPE"),
                "pe_forward":                iv("forwardPE"),
                "pb":                        iv("priceToBook"),
                "ps":                        iv("enterpriseToRevenue"),
                "ev_ebitda":                 iv("enterpriseToEbitda"),
                "peg":                       iv("pegRatio"),
                "enterprise_value":          iv("enterpriseValue"),
                "market_cap":                iv("marketCap"),
                "roe":                       round(iv("returnOnEquity") * 100, 4) if iv("returnOnEquity") else None,
                "roa":                       round(iv("returnOnAssets") * 100, 4) if iv("returnOnAssets") else None,
                "profit_margin":             round(iv("profitMargins") * 100, 4) if iv("profitMargins") else None,
                "gross_margin":              round(iv("grossMargins") * 100, 4) if iv("grossMargins") else None,
                "operating_margin":          round(iv("operatingMargins") * 100, 4) if iv("operatingMargins") else None,
                "ebitda_margin":             round(iv("ebitdaMargins") * 100, 4) if iv("ebitdaMargins") else None,
                "current_ratio":             iv("currentRatio"),
                "quick_ratio":               iv("quickRatio"),
                "debt_to_equity":            iv("debtToEquity"),
                "eps_trailing":              iv("trailingEps"),
                "eps_forward":               iv("forwardEps"),
                "book_value_per_share":      iv("bookValue"),
                "revenue_per_share":         iv("revenuePerShare"),
                "total_cash_per_share":      iv("totalCashPerShare"),
                "shares_outstanding":        iv("sharesOutstanding"),
            }

            all_cols = []
            for df in [bs, fin, cf]:
                if not df.empty:
                    for col in df.columns:
                        if col not in all_cols:
                            all_cols.append(col)

            periods_out = []
            for col in all_cols:
                period_label = str(col.date()) if hasattr(col, "date") else str(col)[:10]
                entry = {
                    "period": period_label,
                    "financials": {
                        "balance_sheet":    build_statement(bs, col),
                        "income_statement": build_statement(fin, col),
                        "cash_flow":        build_statement(cf, col),
                    }
                }
                periods_out.append(entry)

            return {
                "symbol": symbol.upper().strip(),
                "period_type": "quarterly" if is_quarterly else "annual",
                "available_periods": [p["period"] for p in periods_out],
                "periods": periods_out,
                "ratios": {k: v for k, v in ratios.items() if v is not None}
            }
        except Exception:
            pass
        return None

    async def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.dividends
            divs = await asyncio.to_thread(_fetch)
            if not divs.empty:
                divs = divs.sort_index(ascending=False)
                res = []
                for dt, amount in divs.items():
                    res.append({
                        "ex_date": str(dt.date()) if hasattr(dt, "date") else str(dt)[:10],
                        "pay_date": None,
                        "amount": float(amount),
                        "type": "Dividend"
                    })
                return res
        except Exception:
            pass
        return []

    async def get_splits(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.splits
            splits = await asyncio.to_thread(_fetch)
            if not splits.empty:
                splits = splits.sort_index(ascending=False)
                res = []
                for dt, ratio in splits.items():
                    res.append({
                        "date": str(dt.date()) if hasattr(dt, "date") else str(dt)[:10],
                        "ratio": float(ratio)
                    })
                return res
        except Exception:
            pass
        return []

    async def get_calendar(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.calendar
            cal = await asyncio.to_thread(_fetch)
            if cal:
                res = {}
                if isinstance(cal, dict):
                    for k, v in cal.items():
                        if isinstance(v, list):
                            res[k] = [str(x.date()) if hasattr(x, "date") else str(x) for x in v]
                        else:
                            res[k] = str(v)
                else:
                    res["raw"] = str(cal)
                return res
        except Exception:
            pass
        return None

    async def get_news(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.news
            news_items = await asyncio.to_thread(_fetch)
            if news_items:
                res = []
                for item in news_items:
                    content = item.get("content") or item
                    title = content.get("title") or ""
                    url = (content.get("canonicalUrl") or {}).get("url") or content.get("link") or ""
                    summary = content.get("summary") or content.get("description") or ""
                    provider = content.get("provider") or {}
                    publisher = provider.get("displayName") or content.get("publisher") or "Yahoo Finance"
                    pub_date = content.get("pubDate") or content.get("providerPublishTime") or ""
                    res.append({
                        "id": item.get("id") or url,
                        "title": title,
                        "url": url,
                        "published_at": pub_date,
                        "publisher": publisher,
                        "summary": summary
                    })
                return res
        except Exception:
            pass
        return []

    async def get_ratios(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_norm = self._format_symbol(symbol)
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.info
            info = await asyncio.to_thread(_fetch)
            if info:
                def iv(key):
                    val = info.get(key)
                    if val is not None and not (isinstance(val, float) and math.isnan(val)):
                        return val
                    return None

                ratios = {
                    "pe_trailing":               iv("trailingPE"),
                    "pe_forward":                iv("forwardPE"),
                    "pb":                        iv("priceToBook"),
                    "ps":                        iv("enterpriseToRevenue"),
                    "ev_ebitda":                 iv("enterpriseToEbitda"),
                    "peg":                       iv("pegRatio"),
                    "enterprise_value":          iv("enterpriseValue"),
                    "market_cap":                iv("marketCap"),
                    "roe":                       round(iv("returnOnEquity") * 100, 4) if iv("returnOnEquity") else None,
                    "roa":                       round(iv("returnOnAssets") * 100, 4) if iv("returnOnAssets") else None,
                    "profit_margin":             round(iv("profitMargins") * 100, 4) if iv("profitMargins") else None,
                    "gross_margin":              round(iv("grossMargins") * 100, 4) if iv("grossMargins") else None,
                    "operating_margin":          round(iv("operatingMargins") * 100, 4) if iv("operatingMargins") else None,
                    "ebitda_margin":             round(iv("ebitdaMargins") * 100, 4) if iv("ebitdaMargins") else None,
                    "current_ratio":             iv("currentRatio"),
                    "quick_ratio":               iv("quickRatio"),
                    "debt_to_equity":            iv("debtToEquity"),
                    "eps_trailing":              iv("trailingEps"),
                    "eps_forward":               iv("forwardEps"),
                    "book_value_per_share":      iv("bookValue"),
                    "revenue_per_share":         iv("revenuePerShare"),
                    "total_cash_per_share":      iv("totalCashPerShare"),
                    "shares_outstanding":        iv("sharesOutstanding"),
                }
                return {k: v for k, v in ratios.items() if v is not None}
        except Exception:
            pass
        return None
