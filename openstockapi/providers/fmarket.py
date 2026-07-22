from typing import List
from openstockapi.core.base_provider import BaseProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models_fund import FundDetails, FundHolding
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError

class FmarketProvider(BaseProvider):
    name = "fmarket"
    required_tier = DataTier.FREE

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[any]:
        raise NotImplementedError()

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[any]:
        raise NotImplementedError()

    def get_fund_details(self, fund_id: int) -> FundDetails:
        url = f"https://api.fmarket.vn/res/products/{fund_id}"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            res = http_client.request("GET", url, headers=headers)
            data = res.json()
            
            p_data = data.get("data", {})
            if not p_data:
                raise DataParseError(f"No fund details data returned by Fmarket for fund_id: {fund_id}")

            raw_holdings = p_data.get("productTopHoldingList", [])
            holdings = []
            for h in raw_holdings:
                holdings.append(FundHolding(
                    ticker=h.get("stockCode") or h.get("name", ""),
                    name=h.get("name"),
                    net_asset_percent=float(h.get("netAssetPercent", 0)),
                    asset_value=float(h.get("assetValue")) if h.get("assetValue") is not None else None,
                    volume=float(h.get("volume")) if h.get("volume") is not None else None
                ))

            return FundDetails(
                fund_id=int(p_data.get("id")),
                name=p_data.get("name", ""),
                short_name=p_data.get("shortName", ""),
                code=p_data.get("code", ""),
                price=float(p_data.get("price", 0)),
                nav=float(p_data.get("nav", 0)),
                expected_return=p_data.get("expectedReturn"),
                management_fee=p_data.get("managementFee"),
                description=p_data.get("description"),
                holdings=holdings,
                provider=self.name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse fund details from Fmarket: {e}")
