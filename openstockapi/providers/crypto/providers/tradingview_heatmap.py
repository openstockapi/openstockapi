import httpx
from typing import List, Dict, Any, Optional

class TradingViewHeatmapProvider:
    # Static mapping for the top cryptocurrencies to CoinGecko's hosted logo URLs
    _STATIC_LOGOS = {
        'BTC': 'https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png',
        'ETH': 'https://coin-images.coingecko.com/coins/images/279/large/ethereum.png',
        'USDT': 'https://coin-images.coingecko.com/coins/images/325/large/Tether.png',
        'BNB': 'https://coin-images.coingecko.com/coins/images/825/large/bnb-icon2_2x.png',
        'USDC': 'https://coin-images.coingecko.com/coins/images/6319/large/USDC.png',
        'XRP': 'https://coin-images.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png',
        'SOL': 'https://coin-images.coingecko.com/coins/images/4128/large/solana.png',
        'TRX': 'https://coin-images.coingecko.com/coins/images/1094/large/photo_2026-04-13_09-59-16.png',
        'HYPE': 'https://coin-images.coingecko.com/coins/images/50882/large/hyperliquid.jpg',
        'DOGE': 'https://coin-images.coingecko.com/coins/images/5/large/dogecoin.png',
        'USDS': 'https://coin-images.coingecko.com/coins/images/39926/large/usds.webp',
        'LEO': 'https://coin-images.coingecko.com/coins/images/8418/large/leo-token.png',
        'ZEC': 'https://coin-images.coingecko.com/coins/images/486/large/circle-zcash-color.png',
        'LINK': 'https://coin-images.coingecko.com/coins/images/877/large/Chainlink_Logo_500.png',
        'XMR': 'https://coin-images.coingecko.com/coins/images/69/large/monero_logo.png',
        'XLM': 'https://coin-images.coingecko.com/coins/images/100/large/fmpFRHHQ_400x400.jpg',
        'ADA': 'https://coin-images.coingecko.com/coins/images/975/large/cardano.png',
        'DAI': 'https://coin-images.coingecko.com/coins/images/9956/large/Badge_Dai.png',
        'BCH': 'https://coin-images.coingecko.com/coins/images/780/large/bitcoin-cash-circle.png',
        'USDE': 'https://coin-images.coingecko.com/coins/images/33613/large/usde.png',
        'LTC': 'https://coin-images.coingecko.com/coins/images/2/large/litecoin.png',
        'HBAR': 'https://coin-images.coingecko.com/coins/images/3688/large/hbar.png',
        'SHIB': 'https://coin-images.coingecko.com/coins/images/11939/large/shiba.png',
        'SUI': 'https://coin-images.coingecko.com/coins/images/26375/large/sui-ocean-square.png',
        'AVAX': 'https://coin-images.coingecko.com/coins/images/12559/large/Avalanche_Circle_RedWhite_Trans.png',
        'CRO': 'https://coin-images.coingecko.com/coins/images/7310/large/cro_token_logo.png',
        'PYUSD': 'https://coin-images.coingecko.com/coins/images/31212/large/PYUSD_Token_Logo_2x.png',
        'UNI': 'https://coin-images.coingecko.com/coins/images/12504/large/uniswap-logo.png',
        'NEAR': 'https://coin-images.coingecko.com/coins/images/10365/large/near.jpg',
        'ONDO': 'https://coin-images.coingecko.com/coins/images/26580/large/ONDO.png',
        'TAO': 'https://coin-images.coingecko.com/coins/images/28452/large/ARUsPeNQ_400x400.jpeg',
        'PAXG': 'https://coin-images.coingecko.com/coins/images/9519/large/paxgold.png',
        'OKB': 'https://coin-images.coingecko.com/coins/images/4463/large/WeChat_Image_20220118095654.png',
        'USDD': 'https://coin-images.coingecko.com/coins/images/25380/large/UUSD.jpg'
    }

    def __init__(self) -> None:
        self.name = "tradingview"

    async def get_heatmap(self, limit: int = 500) -> List[Dict[str, Any]]:
        # Fetch a larger range first to allow for deduplication of coins across exchanges
        fetch_limit = min(limit * 10, 1000)
        url = "https://scanner.tradingview.com/crypto/scan"
        payload = {
            "markets": ["crypto"],
            "columns": ["name", "description", "change", "market_cap_calc", "logoid", "exchange"],
            "sort": {"sortBy": "market_cap_calc", "sortOrder": "desc"},
            "range": [0, fetch_limit]
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    seen = set()
                    results = []
                    for item in data:
                        d = item.get("d", [])
                        if len(d) >= 6:
                            symbol = d[0]
                            # Clean quote currency to find the base coin (e.g. BTCUSD -> BTC)
                            base = symbol
                            for quote in ["USDT", "USD"]:
                                if symbol.endswith(quote) and symbol != quote:
                                    base = symbol[:-len(quote)]
                                    break
                            
                            # Filter out derivative/Gemini regulated tokens or invalid caps
                            if len(base) > 6 or base.endswith("RL") or not d[3]:
                                continue
                                
                            if base not in seen:
                                seen.add(base)
                                # Try static CoinGecko logo mapping first, fallback to TV logo if present
                                logo_url = self._STATIC_LOGOS.get(base)
                                if not logo_url and d[4]:
                                    logo_url = f"https://s3-symbol-logo.tradingview.com/{d[4]}.svg"
                                
                                results.append({
                                    "symbol": base,
                                    "name": d[1],
                                    "change": float(d[2]) if d[2] is not None else 0.0,
                                    "market_cap": float(d[3]) if d[3] is not None else 0.0,
                                    "sector": "Cryptocurrency",
                                    "industry": "Digital Asset",
                                    "logo_url": logo_url,
                                    "provider": self.name
                                })
                                if len(results) >= limit:
                                    break
                    return results
        except Exception:
            pass
        return []
