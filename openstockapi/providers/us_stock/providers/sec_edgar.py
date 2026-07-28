import httpx
import asyncio
from typing import List, Dict, Any, Optional

class SecEdgarProvider:
    def __init__(self):
        # SEC EDGAR requires a specific User-Agent format: CompanyName contact@email.com
        self.headers = {
            "User-Agent": "OpenStockAPI Admin info@openstockapi.com",
            "Accept-Encoding": "gzip, deflate"
        }
        self.ticker_to_cik: Dict[str, str] = {}
        self._lock = asyncio.Lock()

    async def _ensure_ticker_map(self):
        if self.ticker_to_cik:
            return
        async with self._lock:
            if self.ticker_to_cik:
                return
            try:
                url = "https://www.sec.gov/files/company_tickers.json"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    res = await client.get(url, headers=self.headers)
                    if res.status_code == 200:
                        data = res.json()
                        for item in data.values():
                            ticker = str(item["ticker"]).upper().strip()
                            cik = str(item["cik_str"]).zfill(10)
                            self.ticker_to_cik[ticker] = cik
            except Exception:
                pass

    async def get_cik(self, symbol: str) -> Optional[str]:
        await self._ensure_ticker_map()
        return self.ticker_to_cik.get(symbol.upper().strip())

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        cik = await self.get_cik(symbol)
        if not cik:
            return None
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    website = data.get("website")
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
                        "company_name": data.get("name") or symbol.upper(),
                        "sector": data.get("sicDescription"),
                        "industry": data.get("sicDescription"),
                        "website": website,
                        "logo_url": logo_url,
                        "headcount": None,
                        "description": data.get("description")
                    }
        except Exception:
            pass
        return None

    async def get_company_facts(self, symbol: str) -> Optional[Dict[str, Any]]:
        cik = await self.get_cik(symbol)
        if not cik:
            return None
        
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    return res.json()
        except Exception:
            pass
        return None

    async def get_financials(self, symbol: str, period: str = "annual") -> Optional[Dict[str, Any]]:
        facts = await self.get_company_facts(symbol)
        if not facts:
            return None

        us_gaap = facts.get("facts", {}).get("us-gaap", {})
        
        def extract_concept(concept_name: str) -> List[Dict[str, Any]]:
            concept_data = us_gaap.get(concept_name, {})
            units = concept_data.get("units", {})
            for unit_key, unit_values in units.items():
                return unit_values
            return []

        assets_raw = extract_concept("Assets") or extract_concept("AssetsCurrent")
        liabilities_raw = extract_concept("Liabilities") or extract_concept("LiabilitiesCurrent")
        revenue_raw = extract_concept("Revenues") or extract_concept("SalesRevenueNet") or extract_concept("RevenueFromContractWithCustomerExcludingAssessedTax")
        net_income_raw = extract_concept("NetIncomeLoss")

        form_filter = "10-K" if period.lower() == "annual" else "10-Q"
        periods_dict = {}

        def process_raw_values(raw_list, key_name):
            for item in raw_list:
                if item.get("form") == form_filter:
                    end_date = item.get("end") or item.get("filed")
                    if not end_date:
                        continue
                    val = item.get("val")
                    if end_date not in periods_dict:
                        periods_dict[end_date] = {}
                    periods_dict[end_date][key_name] = val

        process_raw_values(assets_raw, "total_assets")
        process_raw_values(liabilities_raw, "total_liabilities")
        process_raw_values(revenue_raw, "revenue")
        process_raw_values(net_income_raw, "net_income")

        periods_out = []
        for dt, metrics in sorted(periods_dict.items(), reverse=True):
            if not metrics:
                continue
            periods_out.append({
                "period": dt,
                "financials": {
                    "balance_sheet": {
                        "total_assets": metrics.get("total_assets"),
                        "total_liabilities": metrics.get("total_liabilities")
                    },
                    "income_statement": {
                        "revenue": metrics.get("revenue"),
                        "net_income": metrics.get("net_income")
                    },
                    "cash_flow": {}
                }
            })

        return {
            "symbol": symbol.upper(),
            "period_type": period.lower(),
            "available_periods": [p["period"] for p in periods_out],
            "periods": periods_out
        }

    async def get_ratios(self, symbol: str) -> Optional[Dict[str, Any]]:
        financials = await self.get_financials(symbol, period="annual")
        if not financials or not financials.get("periods"):
            return None
        latest = financials["periods"][0]
        bs = latest.get("financials", {}).get("balance_sheet", {})
        is_ = latest.get("financials", {}).get("income_statement", {})

        total_assets = bs.get("total_assets")
        total_liabilities = bs.get("total_liabilities")
        revenue = is_.get("revenue")
        net_income = is_.get("net_income")

        ratios = {}
        if total_assets and total_liabilities:
            equity = total_assets - total_liabilities
            if equity != 0 and net_income is not None:
                ratios["roe"] = round((net_income / equity) * 100, 4)
            if total_assets != 0 and net_income is not None:
                ratios["roa"] = round((net_income / total_assets) * 100, 4)
            if equity != 0 and total_liabilities is not None:
                ratios["debt_to_equity"] = round(total_liabilities / equity, 4)
        return ratios

    async def get_symbols(self) -> List[str]:
        url = "https://www.sec.gov/files/company_tickers.json"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = res.json()
                    return sorted(list(set([
                        v["ticker"].strip().upper() 
                        for v in data.values() 
                        if isinstance(v, dict) and v.get("ticker")
                    ])))
        except Exception:
            pass
        return []
