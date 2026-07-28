import httpx
from typing import Dict, Any, Optional
import time
from openstockapi.providers.forex.base import ForexBaseProvider

class OpenExchangeRatesProvider(ForexBaseProvider):
    def __init__(self):
        # We use public fallback endpoint for Open Exchange Rates or a key if provided
        self.url_template = "https://api.exchangerate-api.com/v4/latest/{base}"

    async def fetch_rates(self, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        base = base_currency.upper()
        url = self.url_template.format(base=base)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    rates = {k: float(v) for k, v in data.get("rates", {}).items()}
                    return {
                        "base": base,
                        "rates": rates,
                        "timestamp": int(data.get("time_last_update", time.time()) * 1000),
                        "source": "openexchangerates_api"
                    }
            except Exception:
                pass
        return None
