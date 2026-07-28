from typing import List, Dict, Any

class OpenInsiderProvider:
    async def get_insider_trading(self, symbol: str) -> List[Dict[str, Any]]:
        return []
