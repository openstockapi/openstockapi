import httpx
import yfinance as yf
import asyncio
import math
from typing import List, Dict, Any, Optional

class YahooUSProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def get_ohlcv(self, symbol: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
        url = f"https://query1.finance.yahoo.com/v7/finance/chart/{sym_norm}"
        params = {
            "range": range_str,
            "interval": interval_str,
            "indicators": "quote",
            "includeTimestamps": "true"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    data = res.json().get("chart", {}).get("result", [])
                    if data:
                        result = data[0]
                        meta = result.get("meta", {})
                        timestamps = result.get("timestamp", [])
                        quotes = result.get("indicators", {}).get("quote", [{}])[0]
                        
                        bars = []
                        for i in range(len(timestamps)):
                            if quotes.get("close") and quotes.get("close")[i] is not None:
                                bars.append({
                                    "timestamp": timestamps[i] * 1000,
                                    "open": quotes.get("open")[i],
                                    "high": quotes.get("high")[i],
                                    "low": quotes.get("low")[i],
                                    "close": quotes.get("close")[i],
                                    "volume": quotes.get("volume")[i]
                                })
                        return {
                            "symbol": symbol.upper(),
                            "currency": meta.get("currency"),
                            "bars": bars
                        }
        except Exception:
            pass
        return None

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
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
                    "symbol": symbol.upper(),
                    "company_name": info.get("longName") or info.get("shortName") or symbol.upper(),
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
        sym_norm = symbol.upper().strip()
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

            def gv(df, keys, col):
                for k in keys:
                    for idx in df.index:
                        if k.lower() == str(idx).lower():
                            val = df.loc[idx][col]
                            if val is not None and not (isinstance(val, float) and math.isnan(val)):
                                return float(val)
                return None

            def iv(key):
                val = info.get(key)
                if val is not None and not (isinstance(val, float) and math.isnan(val)):
                    return val
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

            def build_balance_sheet(col):
                return build_statement(bs, col)

            def build_income_statement(col):
                return build_statement(fin, col)

            def build_cash_flow(col):
                return build_statement(cf, col)

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
                "earnings_growth":           round(iv("earningsGrowth") * 100, 4) if iv("earningsGrowth") else None,
                "revenue_growth":            round(iv("revenueGrowth") * 100, 4) if iv("revenueGrowth") else None,
                "earnings_quarterly_growth": round(iv("earningsQuarterlyGrowth") * 100, 4) if iv("earningsQuarterlyGrowth") else None,
                "dividend_rate":             iv("dividendRate"),
                "dividend_yield":            iv("dividendYield"),
                "payout_ratio":              round(iv("payoutRatio") * 100, 4) if iv("payoutRatio") else None,
                "five_year_avg_dividend_yield": iv("fiveYearAvgDividendYield"),
                "beta":                      iv("beta"),
                "ebitda":                    iv("ebitda"),
                "total_revenue":             iv("totalRevenue"),
                "free_cashflow":             iv("freeCashflow"),
                "operating_cashflow":        iv("operatingCashflow"),
                "shares_outstanding":        iv("sharesOutstanding"),
                "held_percent_institutions": iv("heldPercentInstitutions"),
            }

            periods_out = []
            for col in bs.columns:
                period_label = str(col.date()) if hasattr(col, "date") else str(col)[:10]
                fin_col = col if (not fin.empty and col in fin.columns) else (fin.columns[0] if not fin.empty else None)
                cf_col  = col if (not cf.empty  and col in cf.columns)  else (cf.columns[0]  if not cf.empty  else None)

                entry = {
                    "period": period_label,
                    "financials": {
                        "balance_sheet":    build_balance_sheet(col),
                        "income_statement": build_income_statement(fin_col) if fin_col else {},
                        "cash_flow":        build_cash_flow(cf_col) if cf_col else {},
                    }
                }
                periods_out.append(entry)

            return {
                "symbol": symbol.upper(),
                "period_type": "quarterly" if is_quarterly else "annual",
                "available_periods": [p["period"] for p in periods_out],
                "periods": periods_out,
                "ratios": {k: v for k, v in ratios.items() if v is not None}
            }
        except Exception:
            pass
        return None

    async def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
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
        sym_norm = symbol.upper().strip()
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
        sym_norm = symbol.upper().strip()
        try:
            def _fetch():
                ticker = yf.Ticker(sym_norm)
                return ticker.calendar
            cal = await asyncio.to_thread(_fetch)
            if cal:
                res = {}
                if isinstance(cal, dict):
                    for k, v in cal.items():
                        if hasattr(v, "date"):
                            res[k] = str(v.date())
                        elif isinstance(v, list):
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
        sym_norm = symbol.upper().strip()
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
        sym_norm = symbol.upper().strip()
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
                    "earnings_growth":           round(iv("earningsGrowth") * 100, 4) if iv("earningsGrowth") else None,
                    "revenue_growth":            round(iv("revenueGrowth") * 100, 4) if iv("revenueGrowth") else None,
                    "earnings_quarterly_growth": round(iv("earningsQuarterlyGrowth") * 100, 4) if iv("earningsQuarterlyGrowth") else None,
                    "dividend_rate":             iv("dividendRate"),
                    "dividend_yield":            iv("dividendYield"),
                    "payout_ratio":              round(iv("payoutRatio") * 100, 4) if iv("payoutRatio") else None,
                    "five_year_avg_dividend_yield": iv("fiveYearAvgDividendYield"),
                    "beta":                      iv("beta"),
                    "ebitda":                    iv("ebitda"),
                    "total_revenue":             iv("totalRevenue"),
                    "free_cashflow":             iv("freeCashflow"),
                    "operating_cashflow":        iv("operatingCashflow"),
                    "shares_outstanding":        iv("sharesOutstanding"),
                    "held_percent_institutions": iv("heldPercentInstitutions"),
                }
                return {k: v for k, v in ratios.items() if v is not None}
        except Exception:
            pass
        return None
