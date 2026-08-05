import httpx
from typing import List, Dict, Any, Optional
from openstockapi.providers.crypto.base import CryptoBaseProvider

class CoinGeckoProfileProvider(CryptoBaseProvider):
    # Mapping for main crypto symbols to CoinGecko IDs
    _SYMBOL_TO_ID = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "ADA": "cardano",
        "XRP": "ripple",
        "DOGE": "dogecoin",
        "BNB": "binancecoin",
        "LTC": "litecoin",
        "LINK": "chainlink",
        "DOT": "polkadot",
    }

    async def get_tickers(self) -> List[Dict[str, Any]]:
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        return None

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        return None

    async def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        sym_upper = symbol.upper().strip()
        
        # Clean symbol to get the base asset (e.g. BTCUSDT -> BTC, BTC-USD -> BTC)
        clean_sym = sym_upper
        for delimiter in ("-", "/", "_"):
            if delimiter in clean_sym:
                clean_sym = clean_sym.split(delimiter)[0]
                break
                
        suffixes = ("USDT", "USDC", "BUSD", "TUSD", "USD", "EUR")
        for suffix in suffixes:
            if clean_sym.endswith(suffix) and len(clean_sym) > len(suffix):
                clean_sym = clean_sym[:-len(suffix)]
                break
                
        cg_id = self._SYMBOL_TO_ID.get(clean_sym, clean_sym.lower())
        url = f"https://api.coingecko.com/api/v3/coins/{cg_id}"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    
                    homepage = data.get("links", {}).get("homepage", [])
                    website = homepage[0] if homepage else None
                    
                    return {
                        "symbol": sym_upper,
                        "name": data.get("name"),
                        "id": data.get("id"),
                        "categories": data.get("categories", []),
                        "website": website,
                        "logo_url": data.get("image", {}).get("large"),
                        "description": data.get("description", {}).get("en"),
                        "market_cap_rank": data.get("market_cap_rank"),
                        "provider": "coingecko"
                    }
        except Exception:
            pass
        return None
