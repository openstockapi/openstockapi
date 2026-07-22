from openstockapi.core.exceptions import TierUpgradeRequiredError
from openstockapi.license.session import get_current_session
from openstockapi.core.types import DataTier
from openstockapi.core.rate_limiter import rate_limiter

def enforce_tier_and_rate_limit(required_tier: DataTier, endpoint_name: str) -> None:
    session = get_current_session()
    current_tier = session.tier

    # 1. Enforce data classification tier
    # Hierarchical checks: FREE = 0, PRO = 1, PREMIUM = 2
    tier_levels = {DataTier.FREE: 0, DataTier.PRO: 1, DataTier.PREMIUM: 2}
    
    if tier_levels[current_tier] < tier_levels[required_tier]:
        raise TierUpgradeRequiredError(required_tier.value, endpoint_name)

    # 2. Local client-side rate limit enforcement
    client_key = session.api_key or "anonymous"
    rate_limiter.check_limit(client_key, current_tier)
