import time
import httpx
from openstockapi.core.exceptions import TierUpgradeRequiredError, RateLimitExceededError
from openstockapi.license.session import get_current_session
from openstockapi.core.types import DataTier
from openstockapi.config.settings import BACKEND_URL

# Local in-memory validation cache: endpoint_name -> expiry_timestamp
_validation_cache = {}

def enforce_tier_and_rate_limit(required_tier: DataTier, endpoint_name: str) -> None:
    """Validate tier access and rate limit via server-side handshake.

    Sends only (session_token, action) to the Core Engine. The server determines
    the required tier from its own authoritative ENDPOINT_TIER_MAP — the client
    never sends nor controls what tier is required, eliminating client-side bypass.

    Args:
        required_tier: Used ONLY as a fallback when Core Engine is unreachable.
        endpoint_name: The action name, e.g. "stock.quote" or "crypto.depth".
    """
    session = get_current_session()

    if not session.session_token:
        raise TierUpgradeRequiredError(required_tier.value, endpoint_name)

    if session.session_token.startswith("mock_"):
        _local_tier_check(session, required_tier, endpoint_name)
        session.increment_usage()
        return

    # Check local validation cache
    now = time.time()
    if endpoint_name in _validation_cache and _validation_cache[endpoint_name] > now:
        session.increment_usage()
        return

    try:
        response = httpx.post(
            f"{BACKEND_URL}/v1/license/validate",
            json={
                "session_token": session.session_token,
                "action": endpoint_name,
            },
            timeout=5.0,
        )

        if response.status_code == 200:
            data = response.json()
            if not data.get("allowed", False):
                reason = data.get("reason", "")
                if "rate limit" in reason.lower():
                    raise RateLimitExceededError(session.tier.value, endpoint_name)
                raise TierUpgradeRequiredError(required_tier.value, endpoint_name)
            
            # Cache the successful validation for 10 minutes (600 seconds)
            _validation_cache[endpoint_name] = now + 600
            session.increment_usage()
            return

        # Unexpected server error — fail open to avoid blocking legitimate users
        import logging
        logging.getLogger("openstockapi.security").warning(
            f"Validate endpoint returned {response.status_code} for '{endpoint_name}'. Failing open."
        )
        session.increment_usage()

    except (httpx.ConnectError, httpx.TimeoutException):
        # Network unreachable — fall back to local session tier check
        import logging
        logging.getLogger("openstockapi.security").warning(
            f"Core Engine unreachable for '{endpoint_name}'. Falling back to local session check."
        )
        _local_tier_check(session, required_tier, endpoint_name)
        session.increment_usage()


def _local_tier_check(session, required_tier: DataTier, endpoint_name: str) -> None:
    """Fallback: local tier check used only when Core Engine is unreachable."""
    tier_levels = {DataTier.FREE: 0, DataTier.COMMUNITY: 1, DataTier.PRO: 2, DataTier.PREMIUM: 3}
    if tier_levels[session.tier] < tier_levels[required_tier]:
        raise TierUpgradeRequiredError(required_tier.value, endpoint_name)

    # Local token rate limiting fallback
    from openstockapi.core.rate_limiter import rate_limiter
    # Resolve provider from endpoint name if possible (e.g. stock.vn.ohlcv -> resolved through priority config if needed, or default None)
    rate_limiter.check_limit(session.api_key, session.tier)
