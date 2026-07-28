from datetime import datetime
from typing import List
from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models import OHLCVBar, FinancialItem, OrderBook, OrderBookEntry
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.core.utils import parse_date

class DNSEProvider(BaseStockProvider):
    name = "dnse"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.FREE
    supported_methods = [
        "get_ohlcv",
        "get_financial_statements",
        "get_order_book",
    ]

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        try:
            from_dt = parse_date(from_date)
            to_dt = parse_date(to_date)
            from_ts = int(from_dt.timestamp())
            to_ts = int(to_dt.timestamp())
        except Exception as e:
            raise ValueError(f"Invalid date format passed to DNSE get_ohlcv: {e}")

        # Map resolution to DNSE resolution values
        # e.g., "1D" -> "1D", "1m" -> "1", etc.
        res_map = {"1d": "1D", "1m": "1", "5m": "5", "15m": "15", "1h": "60", "1w": "1W"}
        dnse_res = res_map.get(resolution.lower(), resolution)

        url = f"https://services.entrade.com.vn/chart-api/v2/ohlc/history?resolution={dnse_res}&symbol={symbol}&from={from_ts}&to={to_ts}"
        
        try:
            res = http_client.request("GET", url)
            data = res.json()
            
            # Format: lists of t (timestamp), o, h, l, c, v
            t_list = data.get("t", [])
            o_list = data.get("o", [])
            h_list = data.get("h", [])
            l_list = data.get("l", [])
            c_list = data.get("c", [])
            v_list = data.get("v", [])

            results = []
            for i in range(len(t_list)):
                results.append(OHLCVBar(
                    symbol=symbol,
                    timestamp=datetime.fromtimestamp(t_list[i]),
                    open=float(o_list[i]),
                    high=float(h_list[i]),
                    low=float(l_list[i]),
                    close=float(c_list[i]),
                    volume=int(v_list[i]),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse OHLCV history from DNSE: {str(e)}")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        raise NotImplementedError("DNSE provider does not support financial statements. Use 'mas' instead.")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        try:
            from_dt = parse_date(from_date)
            to_dt = parse_date(to_date)
            from_ts = int(from_dt.timestamp())
            to_ts = int(to_dt.timestamp())
        except Exception as e:
            raise ValueError(f"Invalid date format passed to DNSE get_ohlcv: {e}")

        res_map = {"1d": "1D", "1m": "1", "5m": "5", "15m": "15", "1h": "60", "1w": "1W"}
        dnse_res = res_map.get(resolution.lower(), resolution)

        url = f"https://services.entrade.com.vn/chart-api/v2/ohlc/history?resolution={dnse_res}&symbol={symbol}&from={from_ts}&to={to_ts}"
        
        try:
            res = await http_client.async_request("GET", url)
            data = res.json()
            
            t_list = data.get("t", [])
            o_list = data.get("o", [])
            h_list = data.get("h", [])
            l_list = data.get("l", [])
            c_list = data.get("c", [])
            v_list = data.get("v", [])

            results = []
            for i in range(len(t_list)):
                results.append(OHLCVBar(
                    symbol=symbol,
                    timestamp=datetime.fromtimestamp(t_list[i]),
                    open=float(o_list[i]),
                    high=float(h_list[i]),
                    low=float(l_list[i]),
                    close=float(c_list[i]),
                    volume=int(v_list[i]),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse OHLCV history from DNSE: {str(e)}")

    def get_order_book(self, symbol: str) -> OrderBook:
        # Requires paid JWT token (stubbed here, in real implementation we fetch using token from session)
        raise NotImplementedError("Depth API is a premium feature. Authenticable tokens are handled in Control Plane integration.")
