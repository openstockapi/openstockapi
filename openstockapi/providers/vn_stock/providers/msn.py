import json
from datetime import datetime
from typing import List
from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models import OHLCVBar, FinancialItem
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.core.utils import parse_date

class MSNProvider(BaseStockProvider):
    name = "msn"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.FREE
    supported_methods = [
        "get_ohlcv",
        "get_financial_statements",
    ]

    # Static map of ticker to MSN internal base-36 IDs
    SYMBOL_MAP = {
        "VNM": "aqk1a2",
        "FPT": "aqji2w",
        "VIC": "aqjzgh",
        "HPG": "aqjkim",
        "MSN": "aqjolh",
        "TCB": "b15bar",
        "VCB": "aqjysm",
        "ACB": "bx1soc",
        "MBB": "aqjo77",
        "SSB": "c13rim",
        "SHB": "c3oe1h",
        "EIB": "aqjh6h",
        "VHM": "azztvh",
        "MWG": "aqjooc",
        "GAS": "aqjibh",
    }

    def _get_apikey(self) -> str:
        scope_dict = {
            "audienceMode": "adult",
            "browser": {"browserType": "chrome", "version": "0", "ismobile": "false"},
            "deviceFormFactor": "desktop",
            "domain": "www.msn.com",
            "locale": {"content": {"language": "vi", "market": "vn"}, "display": {"language": "vi", "market": "vn"}},
            "ocid": "hpmsn",
            "os": "macos",
            "platform": "web",
            "pageType": "financestockdetails"
        }
        scope = json.dumps(scope_dict)
        url = f"https://assets.msn.com/resolver/api/resolve/v3/config/?expType=AppConfig&expInstance=default&apptype=finance&v=20240430.168&targetScope={scope}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.msn.com/",
            "Origin": "https://www.msn.com"
        }
        try:
            resp = http_client.request("GET", url, headers=headers)
            data = resp.json()
            return data['configs']["shared/msn-ns/HoroscopeAnswerCardWC/default"]["properties"]["horoscopeAnswerServiceClientSettings"]["apikey"]
        except Exception as e:
            raise DataParseError(f"Failed to acquire dynamic MSN API Key: {e}")

    async def _async_get_apikey(self) -> str:
        scope_dict = {
            "audienceMode": "adult",
            "browser": {"browserType": "chrome", "version": "0", "ismobile": "false"},
            "deviceFormFactor": "desktop",
            "domain": "www.msn.com",
            "locale": {"content": {"language": "vi", "market": "vn"}, "display": {"language": "vi", "market": "vn"}},
            "ocid": "hpmsn",
            "os": "macos",
            "platform": "web",
            "pageType": "financestockdetails"
        }
        scope = json.dumps(scope_dict)
        url = f"https://assets.msn.com/resolver/api/resolve/v3/config/?expType=AppConfig&expInstance=default&apptype=finance&v=20240430.168&targetScope={scope}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.msn.com/",
            "Origin": "https://www.msn.com"
        }
        try:
            resp = await http_client.async_request("GET", url, headers=headers)
            data = resp.json()
            return data['configs']["shared/msn-ns/HoroscopeAnswerCardWC/default"]["properties"]["horoscopeAnswerServiceClientSettings"]["apikey"]
        except Exception as e:
            raise DataParseError(f"Failed to acquire dynamic MSN API Key asynchronously: {e}")

    def _resolve_symbol_id(self, symbol: str) -> str:
        sym_upper = symbol.upper()
        sym_id = self.SYMBOL_MAP.get(sym_upper)
        if sym_id:
            return sym_id

        # Query dynamic Bing suggestions API
        url = "https://services.bingapis.com/contentservices-finance.csautosuggest/api/v1/Query"
        params = {"query": sym_upper, "market": "vi-vn", "count": 10}
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            res = http_client.request("GET", url, params=params, headers=headers)
            stocks = res.json().get("data", {}).get("stocks", [])
            for s in stocks:
                item = json.loads(s)
                if item.get("OS001", "").upper() == sym_upper:
                    sec_id = item.get("SecId")
                    if sec_id:
                        self.SYMBOL_MAP[sym_upper] = sec_id
                        return sec_id
        except Exception:
            pass

        raise NotImplementedError(f"Symbol '{symbol}' is not mapped for MSN provider and could not be resolved dynamically.")

    async def _async_resolve_symbol_id(self, symbol: str) -> str:
        sym_upper = symbol.upper()
        sym_id = self.SYMBOL_MAP.get(sym_upper)
        if sym_id:
            return sym_id

        # Query dynamic Bing suggestions API asynchronously
        url = "https://services.bingapis.com/contentservices-finance.csautosuggest/api/v1/Query"
        params = {"query": sym_upper, "market": "vi-vn", "count": 10}
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            res = await http_client.async_request("GET", url, params=params, headers=headers)
            stocks = res.json().get("data", {}).get("stocks", [])
            for s in stocks:
                item = json.loads(s)
                if item.get("OS001", "").upper() == sym_upper:
                    sec_id = item.get("SecId")
                    if sec_id:
                        self.SYMBOL_MAP[sym_upper] = sec_id
                        return sec_id
        except Exception:
            pass

        raise NotImplementedError(f"Symbol '{symbol}' is not mapped for MSN provider and could not be resolved dynamically.")

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        sym_id = self._resolve_symbol_id(symbol)

        apikey = self._get_apikey()
        url = "https://assets.msn.com/service/Finance/Charts/TimeRange"
        
        from_dt = parse_date(from_date) if from_date else datetime.now()
        to_dt = parse_date(to_date) if to_date else datetime.now()

        params = {
            "apikey": apikey,
            "StartTime": f"{from_dt.strftime('%Y-%m-%d')}T17:00:00.000Z",
            "EndTime": f"{to_dt.strftime('%Y-%m-%d')}T16:59:59.000Z",
            "timeframe": 1,
            "ocid": "finance-utils-peregrine",
            "cm": "vi-vn",
            "it": "web",
            "scn": "ANON",
            "ids": sym_id,
            "type": "All",
            "wrapodata": "false",
            "disableSymbol": "false"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.msn.com/"
        }

        try:
            res = http_client.request("GET", url, params=params, headers=headers)
            data = res.json()
            
            results = []
            if isinstance(data, list) and len(data) > 0:
                series = data[0].get("series", {})
                timestamps = series.get("timeStamps", [])
                opens = series.get("openPrices", [])
                highs = series.get("pricesHigh", [])
                lows = series.get("pricesLow", [])
                closes = series.get("prices", [])
                vols = series.get("volumes", [])
                
                for i in range(len(timestamps)):
                    t_str = timestamps[i]
                    dt = parse_date(t_str)
                    
                    results.append(OHLCVBar(
                        symbol=symbol,
                        timestamp=dt,
                        open=float(opens[i]) if opens else 0.0,
                        high=float(highs[i]) if highs else 0.0,
                        low=float(lows[i]) if lows else 0.0,
                        close=float(closes[i]) if closes else 0.0,
                        volume=int(vols[i]) if vols else 0,
                        provider=self.name
                    ))
            results.sort(key=lambda x: x.timestamp)
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse OHLCV history from MSN: {e}")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        sym_id = await self._async_resolve_symbol_id(symbol)

        apikey = await self._async_get_apikey()
        url = "https://assets.msn.com/service/Finance/Charts/TimeRange"
        
        from_dt = parse_date(from_date) if from_date else datetime.now()
        to_dt = parse_date(to_date) if to_date else datetime.now()

        params = {
            "apikey": apikey,
            "StartTime": f"{from_dt.strftime('%Y-%m-%d')}T17:00:00.000Z",
            "EndTime": f"{to_dt.strftime('%Y-%m-%d')}T16:59:59.000Z",
            "timeframe": 1,
            "ocid": "finance-utils-peregrine",
            "cm": "vi-vn",
            "it": "web",
            "scn": "ANON",
            "ids": sym_id,
            "type": "All",
            "wrapodata": "false",
            "disableSymbol": "false"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.msn.com/"
        }

        try:
            res = await http_client.async_request("GET", url, params=params, headers=headers)
            data = res.json()
            
            results = []
            if isinstance(data, list) and len(data) > 0:
                series = data[0].get("series", {})
                timestamps = series.get("timeStamps", [])
                opens = series.get("openPrices", [])
                highs = series.get("pricesHigh", [])
                lows = series.get("pricesLow", [])
                closes = series.get("prices", [])
                vols = series.get("volumes", [])
                
                for i in range(len(timestamps)):
                    t_str = timestamps[i]
                    dt = parse_date(t_str)
                    results.append(OHLCVBar(
                        symbol=symbol,
                        timestamp=dt,
                        open=float(opens[i]) if opens else 0.0,
                        high=float(highs[i]) if highs else 0.0,
                        low=float(lows[i]) if lows else 0.0,
                        close=float(closes[i]) if closes else 0.0,
                        volume=int(vols[i]) if vols else 0,
                        provider=self.name
                    ))
            results.sort(key=lambda x: x.timestamp)
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async OHLCV history from MSN: {e}")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        raise NotImplementedError("MSN provider does not support financial statements. Use 'mas' instead.")
