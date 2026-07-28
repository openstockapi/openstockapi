import httpx
from typing import Dict, Any, Optional
import time
from openstockapi.providers.forex.base import ForexBaseProvider

class YahooProvider(ForexBaseProvider):
    def __init__(self):
        # We use Frankfurter API as the Yahoo Provider fallback for public exchange rates
        self.url_template = "https://api.frankfurter.dev/v1/latest?from={base}"

    async def fetch_rates(self, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        base = base_currency.upper()
        # Frankfurter doesn't support USD to USD conversion or some direct bases, but handles most
        url = self.url_template.format(base=base)
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    rates = {k: float(v) for k, v in data.get("rates", {}).items()}
                    # Add base currency = 1.0 to rates dict
                    rates[base] = 1.0
                    
                    # Convert Frankfurter timestamp (YYYY-MM-DD) to epoch ms
                    date_str = data.get("date", "")
                    try:
                        epoch_s = time.mktime(time.strptime(date_str, "%Y-%m-%d"))
                    except Exception:
                        epoch_s = time.time()
                        
                    return {
                        "base": base,
                        "rates": rates,
                        "timestamp": int(epoch_s * 1000),
                        "source": "yahoo_frankfurter_api"
                    }
            except Exception:
                pass
        return None
