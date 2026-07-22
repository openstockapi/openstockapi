import os
from typing import Optional, Union

from openstockapi.core.types import DataTier
from openstockapi.core.exceptions import ApiKeyRequiredError

class Session:
    """Manages API key authentication and resolves the current tier."""
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENSTOCKAPI_KEY")
        self.tier = self._resolve_tier()

    def _resolve_tier(self) -> DataTier:
        if not self.api_key:
            raise ApiKeyRequiredError()

        # Resolve tier from key prefix
        # Accepted formats: free_xxx, pro_xxx, prem_xxx, premium_xxx
        # Shortcut bare strings (free, pro, premium) reserved for internal/UAT use
        key = self.api_key.strip().lower()
        if key.startswith("pro_") or key == "pro":
            return DataTier.PRO
        elif key.startswith("prem_") or key.startswith("premium_") or key == "premium":
            return DataTier.PREMIUM
        elif key.startswith("free_") or key == "free":
            return DataTier.FREE
        else:
            # Unknown key format — treat as free but warn
            raise ApiKeyRequiredError()


# Default global session singleton — requires init() or OPENSTOCKAPI_KEY env var
_current_session: Optional["Session"] = None

def get_current_session() -> "Session":
    global _current_session
    if _current_session is None:
        raise ApiKeyRequiredError()
    return _current_session

def set_current_session(session: Union["Session", str]) -> None:
    global _current_session
    if isinstance(session, str):
        _current_session = Session(session)
    else:
        _current_session = session


def init(api_key: str) -> None:
    """Initialize OpenStockAPI with your API key.
    
    Args:
        api_key: Your API key. Format: 'free_xxx', 'pro_xxx', or 'premium_xxx'.
                 Register at: https://openstockapi.com/register
    """
    set_current_session(Session(api_key))
