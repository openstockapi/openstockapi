"""
VN Stock Heatmap Service — aggregates data from 3 providers:
- tradingview (default): full data (change, market_cap, sector, industry, logo)
- kbs: change%, price, name (no market_cap, no sector)
- vci: sector, industry, logo, currentPrice (no change%, no market_cap in batch)
"""
from typing import List, Dict, Any, Optional
from openstockapi.providers.vn_stock.providers.tradingview_heatmap import TradingViewHeatmapProvider
from openstockapi.providers.vn_stock.providers.kbs_heatmap import KBSHeatmapProvider
from openstockapi.providers.vn_stock.providers.vci_heatmap import VCIHeatmapProvider


class VNStockHeatmapService:
    def __init__(self):
        self.tradingview = TradingViewHeatmapProvider()
        self.kbs = KBSHeatmapProvider()
        self.vci = VCIHeatmapProvider()

    async def get_heatmap(self, limit: int = 500, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches heatmap data from one or all providers.

        Provider selection:
        - provider=None or "tradingview" → TradingView (full data, default)
        - provider="kbs" → KBS rtranking (change%, no market_cap)
        - provider="vci" → VCI IQ search-bar (sector/industry/logo, no change%)
        """
        if provider:
            p_lower = provider.lower()
            if "kbs" in p_lower:
                return await self.kbs.get_heatmap(limit=limit)
            elif "vci" in p_lower:
                return await self.vci.get_heatmap(limit=limit)
            # tradingview / tv / default
        return await self.tradingview.get_heatmap(limit=limit)


vn_heatmap_service = VNStockHeatmapService()
