from typing import Optional, Dict

class SymbolNormalizer:
    # Maps unified symbol to Yahoo ticker format
    YAHOO_COMMODITIES = {
        "GOLD": "GC=F",
        "SILVER": "SI=F",
        "CRUDE_OIL": "CL=F",
        "BRENT_OIL": "BZ=F"
    }

    YAHOO_INDICES_ETF = {
        "SPY": "SPY",
        "QQQ": "QQQ",
        "DIA": "DIA",
        "IWM": "IWM"
    }

    @classmethod
    def to_yahoo_ticker(cls, symbol: str) -> str:
        sym_upper = symbol.upper()
        # 1. Check if commodity
        if sym_upper in cls.YAHOO_COMMODITIES:
            return cls.YAHOO_COMMODITIES[sym_upper]
        # 2. Check if index/etf
        if sym_upper in cls.YAHOO_INDICES_ETF:
            return cls.YAHOO_INDICES_ETF[sym_upper]
        # 3. Check if standard Forex symbol like EURUSD (6 chars)
        if len(sym_upper) == 6 and not sym_upper.startswith("^"):
            return f"{sym_upper}=X"
        return sym_upper

    @classmethod
    def parse_forex_pair(cls, symbol: str) -> Optional[tuple]:
        sym_upper = symbol.upper()
        # Remove suffix if any
        if sym_upper.endswith("=X"):
            sym_upper = sym_upper[:-2]
        if len(sym_upper) == 6:
            return sym_upper[:3], sym_upper[3:]
        return None
