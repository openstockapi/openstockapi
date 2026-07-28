import httpx
from typing import List, Dict, Any, Optional


class KBSHeatmapProvider:
    """
    KB Securities (KBS) provider for Vietnam market heatmap.

    Uses the rtranking/volume endpoint which returns realtime ranked stocks
    by trading volume, including price change% and exchange info.

    Note: market_cap is not available from KBS endpoints; it will be set to None.
    """

    def __init__(self) -> None:
        self.name = "kbs"
        self._base = "https://kbbuddywts.kbsec.com.vn/iis-server/investment"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0",
            "Accept": "application/json",
        }

    async def get_heatmap(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Fetches heatmap data from KBS rtranking/volume for HOSE, HNX, UPCOM.
        Combines all 3 exchanges and deduplicates by symbol.

        Fields available: symbol, name, change%, price, exchange.
        Fields NOT available: market_cap, sector, industry, logo_url (set to None).
        """
        results: Dict[str, Dict[str, Any]] = {}
        count_per_exchange = max(limit, 500)

        exchanges = ["HOSE", "HNX", "UPCOM"]
        async with httpx.AsyncClient(timeout=15.0) as client:
            for exchange in exchanges:
                try:
                    url = f"{self._base}/rtranking/volume?group={exchange}&count={count_per_exchange}"
                    res = await client.get(url, headers=self._headers)
                    if res.status_code == 200:
                        items = res.json()
                        if not isinstance(items, list):
                            items = items.get("data", [])
                        for item in items:
                            symbol = item.get("SB") or item.get("sb", "")
                            if not symbol or symbol in results:
                                continue
                            try:
                                change_pct = float(item.get("CHPE", 0.0) or 0.0)
                            except (ValueError, TypeError):
                                change_pct = 0.0
                            name = item.get("NAME_EN") or item.get("NAME") or symbol
                            results[symbol] = {
                                "symbol": symbol,
                                "name": name,
                                "change": change_pct,
                                "market_cap": None,        # Not available from KBS
                                "sector": "Unknown",       # Not available from KBS
                                "industry": "Unknown",     # Not available from KBS
                                "logo_url": None,          # Not available from KBS
                                "provider": self.name
                            }
                except Exception:
                    continue

        # Sort by abs(change) descending, then return up to limit
        sorted_items = sorted(results.values(), key=lambda x: abs(x["change"]), reverse=True)
        return sorted_items[:limit]
