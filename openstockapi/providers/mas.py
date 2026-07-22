from datetime import datetime
import json
import urllib.parse
from typing import List, Any
from openstockapi.core.base_provider import BaseProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models import FinancialItem, OHLCVBar
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError

class MASProvider(BaseProvider):
    name = "mas"
    required_tier = DataTier.FREE

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        # MAS does not officially support clean OHLC history in free apis doc, DNSE is preferred.
        # But we implement a basic placeholder or pass.
        raise NotImplementedError("MAS provider does not support historical OHLCV. Use 'dnse' instead.")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        # Normalizes statement types (CDKT -> CDKT, KQKD -> KQKD, etc.)
        type_mapping = {
            "income": "KQKD",
            "balance": "CDKT",
            "cashflow": "LCTT",
            "ratios": "CSTC"
        }
        mas_type = type_mapping.get(stmt_type.lower(), "CDKT")
        term_type = "Q" if period.upper() == "Q" else "Y"

        gql_query = f'query{{vsFinancialReportList(StockCode:"{symbol}",Type:"{mas_type}",TermType:"{term_type}"){{YearPeriod,TermCode,Content{{Values{{Name,Value}}}}}}}}'
        encoded_query = urllib.parse.quote(gql_query)
        url = f"https://masboard.masvn.com/api/v2/vs/financialReport?query={encoded_query}"

        try:
            res = http_client.request("GET", url)
            data = res.json()
            
            # MAS returns a list directly or wraps it
            report_list = []
            if isinstance(data, list):
                report_list = data
            elif isinstance(data, dict):
                report_list = data.get("data", {}).get("vsFinancialReportList", [])

            results = []
            for report in report_list:
                year_period = report.get("YearPeriod", 0)
                term_code = report.get("TermCode") # e.g. "Q1", "Year"
                
                # Deduce quarter
                quarter = None
                if term_code and term_code.startswith("Q"):
                    try:
                        quarter = int(term_code[1])
                    except ValueError:
                        pass
                
                items = {}
                content = report.get("Content", [])
                if isinstance(content, list) and len(content) > 0:
                    values = content[0].get("Values", [])
                    for val in values:
                        name = val.get("Name")
                        value = val.get("Value")
                        if name:
                            try:
                                items[name] = float(value) if value is not None else None
                            except ValueError:
                                items[name] = None
                elif isinstance(content, dict):
                    values = content.get("Values", [])
                    for val in values:
                        name = val.get("Name")
                        value = val.get("Value")
                        if name:
                            try:
                                items[name] = float(value) if value is not None else None
                            except ValueError:
                                items[name] = None

                results.append(FinancialItem(
                    symbol=symbol,
                    year=int(year_period),
                    quarter=quarter,
                    statement_type=stmt_type,
                    items=items,
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse financial statements from MAS: {str(e)}")

    def get_intraday_ticks(self, symbol: str, limit: int = 100) -> List[Any]:
        from openstockapi.core.models import IntradayTick
        url = f"https://masboard.masvn.com/api/v1/market/{symbol.upper()}/quote"
        params = {"symbol": symbol.upper(), "fetchCount": limit}
        try:
            res = http_client.request("GET", url, params=params, timeout=15)
            raw = res.json()
            ticks = raw.get("data", [])
            
            results = []
            for t in ticks:
                ti_val = t.get("ti", 0) / 1000.0
                dt = datetime.fromtimestamp(ti_val)
                
                raw_price = float(t.get("c", 0))
                # MAS returns price multiplied by 1000 if not standard
                price = raw_price / 1000.0 if raw_price > 1000 else raw_price
                
                results.append(IntradayTick(
                    symbol=symbol.upper(),
                    timestamp=dt,
                    price=price,
                    volume=int(t.get("mv", 0)),
                    side=t.get("mb", "UNKNOWN").upper(),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse intraday ticks from MAS: {str(e)}")

