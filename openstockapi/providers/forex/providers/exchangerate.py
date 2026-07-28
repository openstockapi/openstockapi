import httpx
from typing import Dict, Any, Optional
import time
from openstockapi.providers.forex.base import ForexBaseProvider

class ExchangeRateProvider(ForexBaseProvider):
    def __init__(self):
        # Free endpoint of ExchangeRate-API
        self.url_template = "https://open.er-api.com/v6/latest/{base}"

    async def fetch_rates(self, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        base = base_currency.upper()
        url = self.url_template.format(base=base)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("result") == "success":
                        # Standardize format
                        rates = {k: float(v) for k, v in data.get("rates", {}).items()}
                        return {
                            "base": base,
                            "rates": rates,
                            "timestamp": int(data.get("time_last_update_unix", time.time()) * 1000),
                            "source": "exchangerate_api"
                        }
            except Exception:
                pass
        return None
