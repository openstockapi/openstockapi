from datetime import datetime
from typing import List, Any

from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models_news import CompanyNewsEntry, CompanyEventEntry
from openstockapi.core.models import CompanyProfile, OHLCVBar, FinancialItem, DerivativeProfile
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.core.utils import parse_date, clean_html_text


class KBSProvider(BaseStockProvider):

    name = "kbs"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.FREE
    supported_methods = [
        "get_ohlcv",
        "get_financial_statements",
        "get_company_profile",
        "get_company_news",
        "get_company_events",
    ]

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        f_dt = parse_date(from_date) if from_date else None
        t_dt = parse_date(to_date) if to_date else None
        
        sdate = f_dt.strftime("%d/%m/%Y") if f_dt else "01/01/2020"
        edate = t_dt.strftime("%d/%m/%Y") if t_dt else datetime.now().strftime("%d/%m/%Y")
        
        url = f"https://kbbuddywts.kbsec.com.vn/iis-server/investment/stocks/{symbol}/data_day?sdate={sdate}&edate={edate}"
        
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
            data = res.json()
            raw_list = data.get("data_day", [])
            
            results = []
            for item in raw_list:
                raw_date = item.get("t")
                if not raw_date:
                    continue
                trade_dt = parse_date(raw_date)
                results.append(OHLCVBar(
                    symbol=symbol,
                    timestamp=trade_dt,
                    open=float(item.get("o", 0)),
                    high=float(item.get("h", 0)),
                    low=float(item.get("l", 0)),
                    close=float(item.get("c", 0)),
                    volume=int(item.get("v", 0)),
                    provider=self.name
                ))
            results.sort(key=lambda x: x.timestamp)
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse OHLCV history from KBS: {e}")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        f_dt = parse_date(from_date) if from_date else None
        t_dt = parse_date(to_date) if to_date else None
        
        sdate = f_dt.strftime("%d/%m/%Y") if f_dt else "01/01/2020"
        edate = t_dt.strftime("%d/%m/%Y") if t_dt else datetime.now().strftime("%d/%m/%Y")
        
        url = f"https://kbbuddywts.kbsec.com.vn/iis-server/investment/stocks/{symbol}/data_day?sdate={sdate}&edate={edate}"
        
        try:
            res = await http_client.async_request("GET", url, headers=self._get_headers())
            data = res.json()
            raw_list = data.get("data_day", [])
            
            results = []
            for item in raw_list:
                raw_date = item.get("t")
                if not raw_date:
                    continue
                trade_dt = parse_date(raw_date)
                results.append(OHLCVBar(
                    symbol=symbol,
                    timestamp=trade_dt,
                    open=float(item.get("o", 0)),
                    high=float(item.get("h", 0)),
                    low=float(item.get("l", 0)),
                    close=float(item.get("c", 0)),
                    volume=int(item.get("v", 0)),
                    provider=self.name
                ))
            results.sort(key=lambda x: x.timestamp)
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async OHLCV history from KBS: {e}")




    def get_company_profile(self, symbol: str) -> CompanyProfile:
        url = f"https://kbbuddywts.kbsec.com.vn/iis-server/investment/stockinfo/profile/{symbol}"
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
            data = res.json()
            website = data.get("URL")
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
                full_name=data.get("SB", symbol),
                en_name=data.get("SB"),
                exchange=data.get("EX", "HOSE"),
                industry=None,
                website=website,
                logo_url=logo_url,
                description=clean_html_text(data.get("HS")),
                tax_code=data.get("TC"),
                ceo=data.get("CTP"),
                charter_capital=data.get("CC"),
                shares_outstanding=data.get("KLCPLH"),
                address=data.get("ADD"),
                shareholders=data.get("Shareholders"),
                leaders=data.get("Leaders"),
                subsidiaries=data.get("Subsidiaries"),
                provider=self.name
            )

        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse company profile from KBS: {e}")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        raise NotImplementedError()


    def _get_headers(self) -> dict:
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

    def get_company_news(self, symbol: str, limit: int = 10) -> List[CompanyNewsEntry]:
        url = f"https://kbbuddywts.kbsec.com.vn/iis-server/investment/stockinfo/news/{symbol}?l=1&p=1&s={limit}"
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
            data = res.json()
            
            results = []
            for item in data:
                results.append(CompanyNewsEntry(
                    symbol=symbol,
                    news_id=int(item.get("ArticleID", 0)),
                    title=item.get("Title", ""),
                    publish_date=parse_date(item.get("PublishTime")),
                    url=item.get("URL"),
                    summary=item.get("Head"),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse news from KBS: {e}")

    def get_company_events(self, symbol: str, limit: int = 10) -> List[CompanyEventEntry]:
        url = f"https://kbbuddywts.kbsec.com.vn/iis-server/investment/stockinfo/event/{symbol}?l=1&p=1&s={limit}"
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
            data = res.json()
            
            results = []
            for item in data:
                # Structure may contain EventTitle, EventDate etc depending on response. 
                # KBS event schema varies, but we parse gracefully.
                results.append(CompanyEventEntry(
                    symbol=symbol,
                    event_id=str(item.get("EventID", "")),
                    title=item.get("EventTitle", item.get("Title", "Event")),
                    event_date=parse_date(item.get("EventDate")) if item.get("EventDate") else None,
                    details=item.get("EventContent", item.get("Content")),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse events from KBS: {e}")

    def get_intraday_ticks(self, symbol: str, limit: int = 100) -> List[Any]:
        from openstockapi.core.models import IntradayTick
        url = f"https://kbbuddywts.kbsec.com.vn/iis-server/investment/trade/history/{symbol.upper()}"
        params = {"page": 1, "limit": limit}
        try:
            res = http_client.request("GET", url, params=params, headers=self._get_headers())
            data = res.json()
            ticks = data.get("data", [])
            
            results = []
            for t in ticks:
                raw_time = t.get("t")
                dt = parse_date(raw_time) if raw_time else datetime.now()
                
                raw_price = float(t.get("FMP", 0))
                # KBS returns price in standard unit (e.g. 59000 instead of 59.0)
                price = raw_price / 1000.0 if raw_price > 1000 else raw_price
                
                # LC has side e.g. "S", "B", ""
                side_map = {"B": "BUY", "S": "SELL"}
                side = side_map.get(t.get("LC", "").upper(), "UNKNOWN")
                
                results.append(IntradayTick(
                    symbol=symbol.upper(),
                    timestamp=dt,
                    price=price,
                    volume=int(t.get("FV", 0)),
                    side=side,
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse intraday ticks from KBS: {e}")

    def get_derivative_profile(self, symbol: str) -> DerivativeProfile:
        from openstockapi.core.utils import get_asset_type, safe_convert_derivative_symbol
        
        symbol_upper = symbol.upper()
        try:
            asset_type = get_asset_type(symbol_upper)
        except Exception:
            if len(symbol_upper) == 8:
                asset_type = 'coveredWarr'
            else:
                asset_type = 'derivative'

        if asset_type == 'coveredWarr':
            url = "https://kbbuddywts.kbsec.com.vn/iis-server/investment/stock/iss"
            payload = {"code": symbol_upper}
            try:
                res = http_client.request("POST", url, json=payload, headers=self._get_headers())
                data_list = res.json()
                if not data_list:
                    raise DataParseError(f"No warrant data returned for {symbol_upper}")
                item = data_list[0]
                
                ref_price = float(item.get("RE", 0)) / 1000.0 if "RE" in item else 0.0
                ceil_price = float(item.get("CL", 0)) / 1000.0 if "CL" in item else 0.0
                floor_price = float(item.get("FL", 0)) / 1000.0 if "FL" in item else 0.0
                
                w_type_raw = str(item.get("CWT", "Call")).upper()
                w_type = "Call" if "C" in w_type_raw else ("Put" if "P" in w_type_raw else "Call")
                
                ex_price = float(item.get("EP", 0)) / 1000.0 if "EP" in item else 0.0
                
                er = item.get("ER", "1:1")
                conv_ratio = 1.0
                if ":" in er:
                    try:
                        parts = er.split(":")
                        conv_ratio = float(parts[0]) / float(parts[1])
                    except Exception:
                        pass
                
                return DerivativeProfile(
                    symbol=symbol_upper,
                    full_name=f"Warrant {symbol_upper} (Underlying: {item.get('ULS')})",
                    underlying_symbol=item.get("ULS", ""),
                    exchange=item.get("EX", "HOSE"),
                    reference_price=ref_price,
                    ceiling_price=ceil_price,
                    floor_price=floor_price,
                    warrant_type=w_type,
                    exercise_price=ex_price,
                    conversion_ratio=conv_ratio,
                    provider=self.name,
                    asset_class="derivative"
                )
            except Exception as e:
                raise DataParseError(f"Failed to fetch/parse Covered Warrant profile from KBS: {e}")
        else:
            krx_symbol = safe_convert_derivative_symbol(symbol_upper)
            url = "https://kbbuddywts.kbsec.com.vn/iis-server/investment/derivative/iss"
            payload = {"code": krx_symbol}
            try:
                headers = self._get_headers()
                headers.update({
                    "x-lang": "vi",
                    "Referer": "https://kbbuddywts.kbsec.com.vn/DER"
                })
                res = http_client.request("POST", url, json=payload, headers=headers)
                response_json = res.json()
                
                raw_list = response_json.get("data", []) if isinstance(response_json, dict) else []
                if not raw_list:
                    raise DataParseError(f"No derivative data returned for {symbol_upper} ({krx_symbol})")
                item = raw_list[0]
                
                ftd_raw = item.get("FTD")
                ltd_raw = item.get("LTD")
                
                ftd = parse_date(ftd_raw) if ftd_raw else None
                ltd = parse_date(ltd_raw) if ltd_raw else None
                
                return DerivativeProfile(
                    symbol=symbol_upper,
                    full_name=item.get("FN", f"Future {symbol_upper}"),
                    underlying_symbol=item.get("ULS", "VN30"),
                    exchange=item.get("EX", "HNX"),
                    first_trading_date=ftd,
                    last_trading_date=ltd,
                    reference_price=float(item.get("RE", 0)),
                    ceiling_price=float(item.get("CL", 0)),
                    floor_price=float(item.get("FL", 0)),
                    open_interest=int(item.get("OI", 0)) if item.get("OI") else None,
                    provider=self.name,
                    asset_class="derivative"
                )
            except Exception as e:
                raise DataParseError(f"Failed to fetch/parse Derivative profile from KBS: {e}")


