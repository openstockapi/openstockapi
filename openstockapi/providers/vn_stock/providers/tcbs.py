from datetime import datetime
from typing import List
from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models import OHLCVBar, CompanyProfile, FinancialItem
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.core.utils import parse_date

class TCBSProvider(BaseStockProvider):
    name = "tcbs"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.FREE
    supported_methods = [
        "get_ohlcv",
        "get_financial_statements",
        "get_company_profile",
    ]

    def _get_headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        url = f"https://apipub.tcbs.com.vn/tcanalysis/v1/ticker/{symbol}/historical-quotes?page=0&size=1000"
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
            data = res.json()
            
            # Data is returned under "data" key or as direct list
            items = data.get("data", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            if not items:
                raise DataParseError(f"No TCBS historical quote items found for symbol '{symbol}'.")

            from_dt = parse_date(from_date) if from_date else None
            to_dt = parse_date(to_date) if to_date else None

            results = []
            for item in items:
                raw_date = item.get("tradingDate") or item.get("date")
                if not raw_date:
                    continue
                trade_dt = parse_date(raw_date)

                # Filter by date range if provided
                if from_dt and trade_dt < from_dt:
                    continue
                if to_dt and trade_dt > to_dt:
                    continue

                open_p = float(item.get("open", item.get("openPrice", 0)))
                high_p = float(item.get("high", item.get("highPrice", 0)))
                low_p = float(item.get("low", item.get("lowPrice", 0)))
                close_p = float(item.get("close", item.get("closePrice", 0)))
                vol = int(item.get("volume", item.get("totalVolume", 0)))

                results.append(OHLCVBar(
                    symbol=symbol,
                    timestamp=trade_dt,
                    open=open_p,
                    high=high_p,
                    low=low_p,
                    close=close_p,
                    volume=vol,
                    provider=self.name
                ))
            
            results.sort(key=lambda x: x.timestamp)
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse OHLCV history from TCBS: {str(e)}")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        url = f"https://apipub.tcbs.com.vn/tcanalysis/v1/ticker/{symbol}/historical-quotes?page=0&size=1000"
        try:
            res = await http_client.async_request("GET", url, headers=self._get_headers())
            data = res.json()
            
            items = data.get("data", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            if not items:
                raise DataParseError(f"No TCBS historical quote items found for symbol '{symbol}'.")

            from_dt = parse_date(from_date) if from_date else None
            to_dt = parse_date(to_date) if to_date else None

            results = []
            for item in items:
                raw_date = item.get("tradingDate") or item.get("date")
                if not raw_date:
                    continue
                trade_dt = parse_date(raw_date)

                if from_dt and trade_dt < from_dt:
                    continue
                if to_dt and trade_dt > to_dt:
                    continue

                open_p = float(item.get("open", item.get("openPrice", 0)))
                high_p = float(item.get("high", item.get("highPrice", 0)))
                low_p = float(item.get("low", item.get("lowPrice", 0)))
                close_p = float(item.get("close", item.get("closePrice", 0)))
                vol = int(item.get("volume", item.get("totalVolume", 0)))

                results.append(OHLCVBar(
                    symbol=symbol,
                    timestamp=trade_dt,
                    open=open_p,
                    high=high_p,
                    low=low_p,
                    close=close_p,
                    volume=vol,
                    provider=self.name
                ))
            
            results.sort(key=lambda x: x.timestamp)
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async OHLCV history from TCBS: {str(e)}")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        url = f"https://apipub.tcbs.com.vn/tcanalysis/v1/ticker/{symbol}/overview"
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
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
            
            return CompanyProfile(
                symbol=symbol,
                full_name=data.get("companyName", symbol),
                en_name=data.get("shortName"),
                exchange=data.get("exchange", "HOSE"),
                sector=data.get("sector"),
                industry=data.get("industry"),
                website=website,
                logo_url=logo_url,
                description=data.get("summary"),
                provider=self.name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse company profile from TCBS: {str(e)}")


    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        raise NotImplementedError("TCBS provider does not support financial statements. Use 'mas' instead.")
