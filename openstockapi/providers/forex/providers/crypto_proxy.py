import datetime
from typing import Dict, Any, Optional
from openstockapi.providers.crypto.providers.bybit import BybitProvider
from openstockapi.providers.crypto.providers.okx import OKXProvider
from openstockapi.providers.crypto.providers.bingx import BingXProvider
from openstockapi.providers.forex.normalizer import SymbolNormalizer

class CryptoForexProxyProvider:
    def __init__(self, source_name: str = "bybit"):
        self.source_name = source_name.lower()
        if self.source_name == "bybit":
            self.provider = BybitProvider()
        elif self.source_name == "okx":
            self.provider = OKXProvider()
        else:
            self.provider = BingXProvider()

    def _parse_ticker_to_crypto(self, ticker: str) -> Optional[str]:
        # Normalize symbol first (e.g. GOLD -> GC=F, EURUSD -> EURUSD=X)
        normalized = SymbolNormalizer.to_yahoo_ticker(ticker).upper()
        
        # Commodities mapping for each source
        commodities_map = {
            "GC=F": {
                "bybit": "XAUUSDT",
                "okx": "XAU-USDT",
                "bingx": "NCCOGOLD2USD-USDT"
            },
            "SI=F": {
                "bybit": "XAGUSDT",
                "okx": "XAG-USDT",
                "bingx": "NCCOXAG2USD-USDT"
            },
            "CL=F": {
                "bybit": "USOILUSDT",
                "okx": "USOIL-USDT",
                "bingx": "NCCO1OILWTI2USD-USDT"
            },
            "BZ=F": {
                "bybit": "OILUSDT",
                "okx": "OIL-USDT",
                "bingx": "NCCO1OILBRENT2USD-USDT"
            }
        }
        
        if normalized in commodities_map:
            return commodities_map[normalized].get(self.source_name)

        # Indices & ETF mapping for BingX
        indices_etf_map = {
            "SPY": "NCSKSPY2USD-USDT",
            "QQQ": "NCSKQQQ2USD-USDT"
        }
        if normalized in indices_etf_map and self.source_name == "bingx":
            return indices_etf_map[normalized]

        # Forex mapping: EURUSD=X to EURUSDT/USDTEUR
        if normalized.endswith("=X"):
            pair = normalized[:-2]
            if len(pair) == 6:
                base = pair[:3]
                target = pair[3:]
                # EUR/USD mapping
                if base == "EUR" and target == "USD":
                    if self.source_name == "bybit":
                        return "USDTEUR"
                    else:
                        return "USDT-EUR"
                # General USD proxy
                if target == "USD" or target == "USDT":
                    return f"{base}USDT"
        return None

    async def fetch_chart(self, ticker: str, range_str: str = "5d", interval_str: str = "1h") -> Optional[Dict[str, Any]]:
        normalized = SymbolNormalizer.to_yahoo_ticker(ticker).upper()
        crypto_symbol = self._parse_ticker_to_crypto(normalized)
        if not crypto_symbol:
            return None

        # Map interval
        interval = "1h"
        if interval_str in ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]:
            interval = interval_str

        # Get limit based on range
        limit = 100
        if range_str.endswith("d"):
            try:
                days = int(range_str[:-1])
                if interval == "1h":
                    limit = days * 24
                elif interval == "1d":
                    limit = days
            except Exception:
                pass

        # Query OHLCV
        is_futures_asset = normalized in ["GC=F", "SI=F", "CL=F", "BZ=F", "SPY", "QQQ"]
        m_type = "futures" if is_futures_asset else "spot"
        
        klines = await self.provider.get_ohlcv(crypto_symbol, interval, limit, market_type=m_type)
        if not klines:
            return None

        # Determine if we need to invert the rate (e.g. USDTEUR is 1 / EURUSD)
        is_inverted = crypto_symbol in ["USDTEUR", "USDT-EUR"]

        bars = []
        for k in klines:
            dt = datetime.datetime.utcfromtimestamp(k["timestamp"] / 1000.0)
            
            raw_o, raw_h, raw_l, raw_c = k["open"], k["high"], k["low"], k["close"]
            if is_inverted and raw_o > 0 and raw_h > 0 and raw_l > 0 and raw_c > 0:
                o = 1.0 / raw_o
                h = 1.0 / raw_l
                l = 1.0 / raw_h
                c = 1.0 / raw_c
            else:
                o, h, l, c = raw_o, raw_h, raw_l, raw_c

            bars.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "open": round(o, 6),
                "high": round(h, 6),
                "low": round(l, 6),
                "close": round(c, 6),
                "volume": k["volume"]
            })

        return {
            "ticker": ticker,
            "currency": ticker[-5:-2] if len(ticker) >= 5 else "USD",
            "regularMarketPrice": bars[-1]["close"] if bars else 0.0,
            "previousClose": bars[0]["close"] if bars else 0.0,
            "bars": bars
        }
