from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class CryptoBaseProvider(ABC):
    @abstractmethod
    async def get_tickers(self) -> List[Dict[str, Any]]:
        """
        Fetch all ticker symbols with their current price.
        """
        pass

    @abstractmethod
    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        """
        Fetch order book depth for a given symbol.
        """
        pass

    @abstractmethod
    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        """
        Fetch order flow footprint data for a given symbol.
        """
        pass

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, Any]]:
        return []

    async def get_derivatives_indicators(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None
