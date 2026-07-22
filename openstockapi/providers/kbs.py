from datetime import datetime
from typing import List, Any

from openstockapi.core.base_provider import BaseProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models_news import CompanyNewsEntry, CompanyEventEntry
from openstockapi.core.models import CompanyProfile, OHLCVBar, FinancialItem
from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.core.utils import parse_date, clean_html_text


class KBSProvider(BaseProvider):

    name = "kbs"
    required_tier = DataTier.FREE

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
            return CompanyProfile(
                symbol=symbol,
                full_name=data.get("SB", symbol),
                en_name=data.get("SB"),
                exchange=data.get("EX", "HOSE"),
                industry=data.get("IS"),
                website=data.get("URL"),
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

