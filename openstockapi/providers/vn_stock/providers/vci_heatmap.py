import httpx
from typing import List, Dict, Any, Optional


class VCIHeatmapProvider:
    """
    Vietcap (VCI) provider for Vietnam market heatmap.

    Uses the IQ search-bar endpoint which returns all listed companies
    with sector, industry ICB classification, logo URL (WebP) and current price.

    Note: change% and market_cap are NOT available in batch from this endpoint.
    change will be set to 0.0 and market_cap to None.
    Logo URL uses Vietcap S3 WebP format: https://vietcap-website.s3.ap-southeast-1.amazonaws.com/cms/logo/{symbol}.webp
    """

    def __init__(self) -> None:
        self.name = "vci"
        self._url = "https://iq.vietcap.com.vn/api/iq-insight-service/v2/company/search-bar"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0",
            "Accept": "application/json",
            "Referer": "https://iq.vietcap.com.vn/",
        }

    async def get_heatmap(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Fetches company listing with ICB sector/industry and logo from VCI IQ.

        Data available: symbol, name, floor (exchange), current_price,
                        sector (icbLv1), industry (icbLv4), logo_url.
        NOT available: change%, market_cap (set to 0.0 and None respectively).
        """
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(
                    self._url,
                    params={"language": "2"},  # English
                    headers=self._headers
                )
                if res.status_code == 200:
                    data = res.json()
                    items = data.get("data", []) if isinstance(data, dict) else data
                    results = []
                    for item in items:
                        if not isinstance(item, dict):
                            continue
                        symbol = item.get("code", "")
                        if not symbol:
                            continue

                        icb1 = item.get("icbLv1") or {}
                        icb4 = item.get("icbLv4") or {}
                        sector = icb1.get("name") or "Unknown"
                        industry = icb4.get("name") or "Unknown"

                        logo_url = item.get("logoUrl")

                        try:
                            current_price = float(item.get("currentPrice") or 0.0)
                        except (ValueError, TypeError):
                            current_price = 0.0

                        results.append({
                            "symbol": symbol,
                            "name": item.get("shortName") or item.get("name") or symbol,
                            "change": 0.0,          # Not available in batch from VCI IQ
                            "market_cap": None,     # Not available in batch from VCI IQ
                            "sector": sector,
                            "industry": industry,
                            "logo_url": logo_url,
                            "provider": self.name
                        })

                    return results[:limit]
        except Exception:
            pass
        return []
