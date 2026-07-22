from typing import Dict, List

DEFAULT_PROVIDER_PRIORITY: Dict[str, Dict[str, List[str]]] = {
    "VN": {
        "ohlcv": ["dnse", "kbs", "vci", "msn"],
        "financials": ["mas", "vci"],

        "profile": ["vndirect", "vci", "kbs"],



        "quote": ["dnse", "vci"],
        "orderbook": ["vci", "dnse"],
        "trading": ["vci"],
        "macro": ["mbk"],
        "fund": ["fmarket"],
        "news": ["kbs"],
        "events": ["vci", "kbs"],
    },



    "US": {
        "ohlcv": [],
        "financials": [],
        "profile": [],
        "quote": [],
        "orderbook": [],
        "trading": [],
        "macro": [],
        "fund": [],
        "news": [],
    }
}

def get_default_providers(endpoint_category: str, market: str = "VN") -> List[str]:
    market_upper = market.upper()
    market_config = DEFAULT_PROVIDER_PRIORITY.get(market_upper, DEFAULT_PROVIDER_PRIORITY.get("VN", {}))
    return market_config.get(endpoint_category, [])

