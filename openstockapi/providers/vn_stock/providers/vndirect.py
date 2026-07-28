import re
from datetime import datetime
from typing import List
from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models import CompanyProfile, OHLCVBar, FinancialItem
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError

class VNDIRECTProvider(BaseStockProvider):
    name = "vndirect"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.FREE
    supported_methods = [
        "get_company_profile",
    ]

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        raise NotImplementedError("VNDIRECT provider does not support historical OHLCV. Use 'dnse' instead.")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        raise NotImplementedError("VNDIRECT provider does not support financial statements. Use 'mas' instead.")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        url = f"https://finfo-api.vndirect.com.vn/v4/company_profiles?q=code:{symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }
        try:
            res = http_client.request("GET", url, headers=headers)
            data = res.json()
            
            # VNDIRECT profile output format contains array of records in "data" field
            records = data.get("data", [])
            if not records:
                raise DataParseError(f"No profile records found for symbol '{symbol}' from VNDIRECT.")
            
            rec = records[0]
            website = rec.get("website")
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
            # Map standard fields
            return CompanyProfile(
                symbol=symbol,
                full_name=rec.get("companyName", ""),
                en_name=rec.get("companyNameEng"),
                exchange=rec.get("floor", "HOSE"),
                sector=rec.get("sectorName"),
                industry=rec.get("industryName"),
                website=website,
                logo_url=logo_url,
                employees=rec.get("employees"),
                tax_code=rec.get("taxCode"),
                address=rec.get("address"),
                description=rec.get("summary"),
                provider=self.name
            )

        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse company profile from VNDIRECT: {str(e)}")
