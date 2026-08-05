from datetime import datetime
from typing import List, Any
from openstockapi.cdk import BaseStockProvider
from openstockapi.core.types import DataTier
from openstockapi.core.models_trading import ForeignTradingEntry, PropTradingEntry, InsiderTradingEntry
from openstockapi.core.models import OHLCVBar, FinancialItem, CompanyProfile, RealtimeQuote, OrderBook
from openstockapi.core.models_news import CompanyEventEntry

from openstockapi.core.http_client import http_client
from openstockapi.core.exceptions import DataParseError
from openstockapi.core.utils import parse_date, clean_html_text


class VCIProvider(BaseStockProvider):
    name = "vci"
    market = "VN"
    asset_class = "stock"
    required_tier = DataTier.PRO
    supported_methods = [
        "get_ohlcv",
        "get_financial_statements",
        "get_company_profile",
        "get_realtime_quote",
        "get_order_book",
        "get_foreign_trading",
        "get_prop_trading",
        "get_insider_trading",
        "get_company_events",
        "get_vn_symbols",
    ]

    def get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        url = "https://trading.vietcap.com.vn/api/chart/OHLCChart/gap-chart"
        from_dt = parse_date(from_date) if from_date else parse_date("2020-01-01")
        to_dt = parse_date(to_date) if to_date else datetime.now()
        
        # Map unified index symbols to VCI case-sensitive symbols
        vci_symbol = symbol
        if symbol.upper() == "HNXINDEX":
            vci_symbol = "HNXIndex"
        elif symbol.upper() == "UPCOMINDEX":
            vci_symbol = "HNXUpcomIndex"

        to_ts = int(to_dt.timestamp())
        tf_map = {"1D": "ONE_DAY", "1W": "ONE_WEEK", "1M": "ONE_MONTH"}
        tf = tf_map.get(resolution, "ONE_DAY")
        count = (to_dt - from_dt).days + 15
        
        payload = {
            "timeFrame": tf,
            "symbols": [vci_symbol],
            "to": to_ts,
            "countBack": max(10, count)
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Referer": "https://trading.vietcap.com.vn/"
        }
        
        try:
            res = http_client.request("POST", url, json=payload, headers=headers)
            vci_raw = res.json()
            
            results = []
            if isinstance(vci_raw, list) and len(vci_raw) > 0:
                item = vci_raw[0]
                times = item.get("t", [])
                opens = item.get("o", [])
                highs = item.get("h", [])
                lows = item.get("l", [])
                closes = item.get("c", [])
                vols = item.get("v", [])
                
                for i in range(len(times)):
                    trade_dt = parse_date(times[i])
                    results.append(OHLCVBar(
                        symbol=symbol,
                        timestamp=trade_dt,
                        open=float(opens[i]),
                        high=float(highs[i]),
                        low=float(lows[i]),
                        close=float(closes[i]),
                        volume=int(vols[i]),
                        provider=self.name
                    ))
            
            results.sort(key=lambda x: x.timestamp)
            filtered = [r for r in results if r.timestamp >= from_dt and r.timestamp <= to_dt]
            return filtered if filtered else results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse OHLCV history from VCI: {e}")

    async def async_get_ohlcv(self, symbol: str, resolution: str, from_date: str, to_date: str) -> List[OHLCVBar]:
        url = "https://trading.vietcap.com.vn/api/chart/OHLCChart/gap-chart"
        from_dt = parse_date(from_date) if from_date else parse_date("2020-01-01")
        to_dt = parse_date(to_date) if to_date else datetime.now()
        
        # Map unified index symbols to VCI case-sensitive symbols
        vci_symbol = symbol
        if symbol.upper() == "HNXINDEX":
            vci_symbol = "HNXIndex"
        elif symbol.upper() == "UPCOMINDEX":
            vci_symbol = "HNXUpcomIndex"

        to_ts = int(to_dt.timestamp())
        tf_map = {"1D": "ONE_DAY", "1W": "ONE_WEEK", "1M": "ONE_MONTH"}
        tf = tf_map.get(resolution, "ONE_DAY")
        count = (to_dt - from_dt).days + 15
        
        payload = {
            "timeFrame": tf,
            "symbols": [vci_symbol],
            "to": to_ts,
            "countBack": max(10, count)
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Referer": "https://trading.vietcap.com.vn/"
        }
        
        try:
            res = await http_client.async_request("POST", url, json=payload, headers=headers)
            vci_raw = res.json()
            
            results = []
            if isinstance(vci_raw, list) and len(vci_raw) > 0:
                item = vci_raw[0]
                times = item.get("t", [])
                opens = item.get("o", [])
                highs = item.get("h", [])
                lows = item.get("l", [])
                closes = item.get("c", [])
                vols = item.get("v", [])
                
                for i in range(len(times)):
                    trade_dt = parse_date(times[i])
                    results.append(OHLCVBar(
                        symbol=symbol,
                        timestamp=trade_dt,
                        open=float(opens[i]),
                        high=float(highs[i]),
                        low=float(lows[i]),
                        close=float(closes[i]),
                        volume=int(vols[i]),
                        provider=self.name
                    ))
            
            results.sort(key=lambda x: x.timestamp)
            filtered = [r for r in results if r.timestamp >= from_dt and r.timestamp <= to_dt]
            return filtered if filtered else results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async OHLCV history from VCI: {e}")


    def get_company_profile(self, symbol: str) -> CompanyProfile:
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol}"
        try:
            res = http_client.request("GET", url, headers=self._get_headers())
            raw = res.json()
            data = raw.get("data", raw) if isinstance(raw, dict) else raw

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
                full_name=data.get("viOrganName", data.get("enOrganName", symbol)),
                en_name=data.get("enOrganName"),
                exchange=data.get("comGroupCode", "HOSE"),
                sector=data.get("sector"),
                industry=data.get("sectorVn"),
                website=website,
                logo_url=logo_url,
                description=clean_html_text(data.get("profile")),

                provider=self.name
            )
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse company profile from VCI: {e}")



    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        if stmt_type != "ratios":
            raise NotImplementedError("Use MAS provider for balance, income and cashflow statements.")
        
        url = "https://trading.vietcap.com.vn/data-mt/graphql"
        payload = {
            "query": "query Query($ticker: String!, $lang: String!) {\n  TickerPriceInfo(ticker: $ticker) {\n    financialRatio {\n      yearReport\n      lengthReport\n      updateDate\n      roe\n      roic\n      roa\n      pe\n      pb\n      eps\n      currentRatio\n      quickRatio\n      netProfitMargin\n      grossMargin\n      ps\n      pcf\n      bvps\n      epsTTM\n      de\n    }\n    ticker\n  }\n}",
            "variables": {"ticker": symbol, "lang": "vi"}
        }
        
        try:
            # Note: Using verify=False because local tests might hit ssl certification issues
            res = http_client.request("POST", url, json=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0",
                "Referer": "https://trading.vietcap.com.vn/",
                "Content-Type": "application/json"
            })
            data = res.json()
            raw_info = data.get("data", {}).get("TickerPriceInfo", {})
            if not raw_info:
                return []
            ratios = raw_info.get("financialRatio") or {}
            
            items = {}
            for k, v in ratios.items():
                if k not in ("yearReport", "lengthReport", "updateDate", "__typename"):
                    try:
                        items[k] = float(v) if v is not None else None
                    except (ValueError, TypeError):
                        items[k] = None
                        
            year_val = ratios.get("yearReport")
            year = int(year_val) if year_val else datetime.now().year
            
            return [FinancialItem(
                symbol=symbol,
                year=year,
                quarter=None,
                statement_type="ratios",
                items=items,
                provider=self.name
            )]
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse financial ratios from VCI: {e}")



    def _get_headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://iq.vietcap.com.vn/",
            "Origin": "https://iq.vietcap.com.vn",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8"
        }

    def get_foreign_trading(self, symbol: str, limit: int = 10) -> List[ForeignTradingEntry]:
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol}/price-history"
        try:
            res = http_client.request("GET", url, headers=self._get_headers(), params={"timeFrame": "ONE_DAY", "size": limit})
            data = res.json()
            content = data.get("content", [])
            
            results = []
            for item in content:
                trade_date = parse_date(item.get("tradingDate"))
                results.append(ForeignTradingEntry(
                    symbol=symbol,
                    date=trade_date,
                    buy_volume=float(item.get("foreignBuyVolumeTotal", 0)),
                    buy_value=float(item.get("foreignBuyValueTotal", 0)),
                    sell_volume=float(item.get("foreignSellVolumeTotal", 0)),
                    sell_value=float(item.get("foreignSellValueTotal", 0)),
                    net_volume=float(item.get("foreignNetVolumeTotal", 0)),
                    net_value=float(item.get("foreignNetValueTotal", 0)),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse foreign trading from VCI: {e}")

    def get_prop_trading(self, symbol: str, limit: int = 10) -> List[PropTradingEntry]:
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol}/proprietary-history"
        try:
            res = http_client.request("GET", url, headers=self._get_headers(), params={"timeFrame": "ONE_DAY", "size": limit})
            data = res.json()
            content = data.get("content", [])
            
            results = []
            for item in content:
                trade_date = parse_date(item.get("tradingDate"))
                results.append(PropTradingEntry(
                    symbol=symbol,
                    date=trade_date,
                    buy_volume=float(item.get("totalBuyTradeVolume", 0)),
                    buy_value=float(item.get("totalBuyTradeValue", 0)),
                    sell_volume=float(item.get("totalSellTradeVolume", 0)),
                    sell_value=float(item.get("totalSellTradeValue", 0)),
                    net_volume=float(item.get("totalTradeNetVolume", 0)),
                    net_value=float(item.get("totalTradeNetValue", 0)),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse proprietary trading from VCI: {e}")

    def get_insider_trading(self, symbol: str, limit: int = 10) -> List[InsiderTradingEntry]:
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol}/insider-transaction"
        try:
            res = http_client.request("GET", url, headers=self._get_headers(), params={"size": limit})
            data = res.json()
            content = data.get("content", [])
            
            results = []
            for item in content:
                start_dt = parse_date(item.get("startDate")) if item.get("startDate") else None
                end_dt = parse_date(item.get("endDate")) if item.get("endDate") else None
                
                results.append(InsiderTradingEntry(
                    symbol=symbol,
                    trader_name=item.get("traderOrganNameVi", item.get("traderOrganNameEn", "")),
                    position=item.get("eventNameVi"),
                    relationship=item.get("eventNameEn"),
                    action_type=item.get("actionTypeVi", "Mua") if item.get("actionTypeCode") == "B" else "Bán",
                    registered_volume=float(item.get("shareRegister", 0)),
                    actual_volume=float(item.get("shareAcquire", 0)) if item.get("shareAcquire") is not None else None,
                    trade_status=item.get("tradeStatusVi", "Đăng ký"),
                    start_date=start_dt,
                    end_date=end_dt,
                    post_volume=float(item.get("shareAfterTrade", 0)),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse insider transactions from VCI: {e}")

    def get_financial_statements(self, symbol: str, stmt_type: str, period: str) -> List[FinancialItem]:
        # Handle ratios separately as it queries a different endpoint
        if stmt_type.lower() == "ratios":
            url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol.upper()}/statistics-financial"
            try:
                res = http_client.request("GET", url, headers=self._get_headers())
                data = res.json().get("data", [])
                
                ratio_mapping = {
                    "pe": "P/E",
                    "pb": "P/B",
                    "ps": "P/S",
                    "dividendYield": "Dividend Yield",
                    "marketCap": "Vốn hóa",
                    "roe": "ROE",
                    "roa": "ROA",
                    "roic": "ROIC",
                    "grossMargin": "Tỷ suất lợi nhuận gộp",
                    "afterTaxProfitMargin": "Tỷ suất lợi nhuận ròng",
                    "quickRatio": "Tỷ số thanh toán nhanh",
                    "currentRatio": "Tỷ số thanh toán hiện hành",
                    "debtToEquity": "Nợ/Vốn chủ sở hữu"
                }

                results = []
                requested_annual = period.upper() in ["Y", "YEAR", "ANNUAL"]
                for item in data:
                    year = item.get("yearReport", item.get("year"))
                    quarter = item.get("quarter")
                    ratio_type = item.get("ratioType")
                    
                    # Filter period type based on ratioType
                    if requested_annual:
                        if ratio_type != "RATIO_YEAR":
                            continue
                        q_val = None
                    else:
                        if ratio_type != "RATIO_TTM":
                            continue
                        q_val = quarter

                    # Safe convert year
                    try:
                        year_val = int(year) if year else 0
                    except ValueError:
                        year_val = 0

                    items_dict = {}
                    for k, v in item.items():
                        if k in ratio_mapping:
                            translated = ratio_mapping[k]
                            try:
                                items_dict[translated] = float(v) if v is not None else None
                            except ValueError:
                                items_dict[translated] = None

                    results.append(FinancialItem(
                        symbol=symbol,
                        year=year_val,
                        quarter=q_val,
                        statement_type=stmt_type,
                        items=items_dict,
                        provider=self.name
                    ))
                return results
            except Exception as e:
                raise DataParseError(f"Failed to fetch/parse financial ratios from VCI: {e}")

        # Standard statement types
        type_mapping = {
            "balance": "BALANCE_SHEET",
            "income": "INCOME_STATEMENT",
            "cashflow": "CASH_FLOW"
        }
        vci_section = type_mapping.get(stmt_type.lower())
        if not vci_section:
            raise NotImplementedError(f"Statement type '{stmt_type}' is not supported by VCI.")

        # Get metrics translations mapping
        metrics_url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol.upper()}/financial-statement/metrics"
        metrics_map = {}
        try:
            res = http_client.request("GET", metrics_url, headers=self._get_headers())
            metrics_data = res.json().get("data", {}).get(vci_section, [])
            for item in metrics_data:
                field = item.get("field")
                title_vi = item.get("titleVi")
                if field and title_vi:
                    metrics_map[field] = title_vi
        except Exception:
            pass

        # Get raw statement data
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{symbol.upper()}/financial-statement"
        params = {"section": vci_section}
        try:
            res = http_client.request("GET", url, params=params, headers=self._get_headers())
            raw_data = res.json().get("data", {})
            target_key = "years" if period.upper() in ["Y", "YEAR", "ANNUAL"] else "quarters"
            periods = raw_data.get(target_key, [])
            
            results = []
            for item in periods:
                year = item.get("yearReport", 0)
                length_report = item.get("lengthReport", 1)
                
                # Determine quarter
                quarter = None
                if target_key == "quarters":
                    quarter = length_report
                
                non_metric_keys = {"organCode", "ticker", "createDate", "updateDate", "yearReport", "lengthReport", "publicDate"}
                
                items_dict = {}
                for k, v in item.items():
                    if k not in non_metric_keys:
                        translated_name = metrics_map.get(k, k)
                        try:
                            items_dict[translated_name] = float(v) if v is not None else None
                        except ValueError:
                            items_dict[translated_name] = None
                
                results.append(FinancialItem(
                    symbol=symbol,
                    year=int(year),
                    quarter=quarter,
                    statement_type=stmt_type,
                    items=items_dict,
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse financial statements from VCI: {e}")

    def get_company_events(self, symbol: str, limit: int = 10) -> List[CompanyEventEntry]:
        url = "https://iq.vietcap.com.vn/api/iq-insight-service/v1/events"
        from_dt = "2020-01-01"
        to_dt = datetime.now().strftime("%Y-%m-%d")
        params = {
            "ticker": symbol.upper(),
            "fromDate": from_dt,
            "toDate": to_dt,
            "page": 1,
            "size": limit
        }
        try:
            res = http_client.request("GET", url, params=params, headers=self._get_headers())
            data = res.json().get("data", {})
            content = data.get("content", []) if isinstance(data, dict) else []
            
            results = []
            for item in content:
                event_date_str = item.get("publicDate") or item.get("startDate")
                event_date = parse_date(event_date_str) if event_date_str else None
                
                results.append(CompanyEventEntry(
                    symbol=symbol,
                    event_id=item.get("id"),
                    title=item.get("eventTitleVi") or item.get("eventNameVi") or "Event",
                    event_date=event_date,
                    details=item.get("eventTitleVi"),
                    provider=self.name
                ))
            return results
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse events from VCI: {e}")

    def _fetch_raw_board(self, symbol: str) -> dict:
        url = "https://trading.vietcap.com.vn/api/price/symbols/getList"
        payload = {"symbols": [symbol.upper()]}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "https://trading.vietcap.com.vn/"
        }
        res = http_client.request("POST", url, json=payload, headers=headers)
        data = res.json()
        if not isinstance(data, list) or len(data) == 0:
            raise DataParseError(f"No VCI price board items returned for {symbol}")
        return data[0]

    def get_realtime_quote(self, symbol: str) -> RealtimeQuote:
        from openstockapi.core.models import RealtimeQuote
        raw = self._fetch_raw_board(symbol)
        match_info = raw.get("matchPrice", {})
        lst_info = raw.get("listingInfo", {})
        
        ref = float(lst_info.get("refPrice", 0))
        price = float(match_info.get("matchPrice", ref))
        vol = int(match_info.get("accumulatedVolume", 0))
        
        # Calculate change and pct_change
        change = price - ref
        pct_change = (change / ref * 100) if ref > 0 else 0.0
        
        # Get raw timestamp, default to now
        time_str = match_info.get("time") or lst_info.get("receivedTime")
        timestamp = parse_date(time_str) if time_str else datetime.now()

        return RealtimeQuote(
            symbol=symbol.upper(),
            price=price,
            change=change,
            pct_change=pct_change,
            volume=vol,
            timestamp=timestamp,
            provider=self.name
        )

    def get_order_book(self, symbol: str) -> OrderBook:
        from openstockapi.core.models import OrderBook, OrderBookEntry
        raw = self._fetch_raw_board(symbol)
        bid_ask_info = raw.get("bidAsk", {})
        
        bid_entries = []
        for b in bid_ask_info.get("bidPrices", []):
            bid_entries.append(OrderBookEntry(price=float(b.get("price", 0)), volume=int(b.get("volume", 0))))
            
        ask_entries = []
        for a in bid_ask_info.get("askPrices", []):
            ask_entries.append(OrderBookEntry(price=float(a.get("price", 0)), volume=int(a.get("volume", 0))))
            
        time_str = bid_ask_info.get("time") or raw.get("listingInfo", {}).get("receivedTime")
        timestamp = parse_date(time_str) if time_str else datetime.now()

        return OrderBook(
            symbol=symbol.upper(),
            bids=bid_entries,
            asks=ask_entries,
            timestamp=timestamp,
            provider=self.name
        )

    def get_vn_symbols(self) -> List[str]:
        url = "https://iq.vietcap.com.vn/api/iq-insight-service/v2/company/search-bar"
        headers = self._get_headers()
        try:
            res = http_client.request("GET", url, params={"language": "2"}, headers=headers)
            if res.status_code == 200:
                data = res.json()
                items = data.get("data", []) if isinstance(data, dict) else data
                symbols = []
                for item in items:
                    if isinstance(item, dict) and item.get("code"):
                        symbols.append(item["code"].upper().strip())
                if symbols:
                    return sorted(list(set(symbols)))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse VN Symbols from VCI: {e}")
        return []

    async def async_get_vn_symbols(self) -> List[str]:
        url = "https://iq.vietcap.com.vn/api/iq-insight-service/v2/company/search-bar"
        headers = self._get_headers()
        try:
            res = await http_client.async_request("GET", url, params={"language": "2"}, headers=headers)
            if res.status_code == 200:
                data = res.json()
                items = data.get("data", []) if isinstance(data, dict) else data
                symbols = []
                for item in items:
                    if isinstance(item, dict) and item.get("code"):
                        symbols.append(item["code"].upper().strip())
                if symbols:
                    return sorted(list(set(symbols)))
        except Exception as e:
            raise DataParseError(f"Failed to fetch/parse async VN Symbols from VCI: {e}")
        return []

