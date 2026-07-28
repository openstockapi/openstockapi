from typing import List
from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models_macro import MacroIndicatorEntry
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError

class MBKProvider(BaseStockProvider):
    name = "mbk"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.FREE
    supported_methods = [
        "get_macro_indicators",
    ]

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[any]:
        raise NotImplementedError()

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[any]:
        raise NotImplementedError()

    def get_macro_indicators(self) -> List[MacroIndicatorEntry]:
        url = "https://data.maybanktrade.com.vn/data/reportdatatopbynormtype"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://data.maybanktrade.com.vn/"
        }
        
        # Fetch Money Supply (M2) & Credit data (type=2, normTypeID=51)
        payload = "type=2&fromYear=2024&toYear=2026&from=1&to=12&normTypeID=51"
        
        try:
            res = http_client.request("POST", url, headers=headers, content=payload)
            data = res.json()
            
            results = []
            for item in data:
                val = item.get("NormValue")
                results.append(MacroIndicatorEntry(
                    name=item.get("NormName", "M2"),
                    year=int(item.get("TermYear", 2026)),
                    period=item.get("ReportTime", ""),
                    value=float(val) if val is not None else None,
                    unit=item.get("UnitCode", "Tỷ VNĐ"),
                    source=item.get("FromSource"),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse Maybank Macro M2 indicators: {e}")
