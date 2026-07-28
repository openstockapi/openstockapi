from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ForexBaseProvider(ABC):
    @abstractmethod
    async def fetch_rates(self, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        """
        Fetch current forex exchange rates for the base currency.
        Should return a standardized dictionary like:
        {
            "base": "USD",
            "rates": {"VND": 25450.0, "EUR": 0.92, ...},
            "timestamp": 1783630800000,
            "source": "provider_name"
        }
        """
        pass
