import time
from openstockapi.core.types import DataTier
from openstockapi.core.exceptions import RateLimitError

# Max requests per minute
TIER_LIMITS = {
    DataTier.FREE: 10,
    DataTier.PRO: 200,
    DataTier.PREMIUM: 500,
}

class TokenBucketRateLimiter:
    def __init__(self) -> None:
        # Simplistic in-memory client state map: client_id -> (tokens, last_update_time)
        self.buckets = {}

    def check_limit(self, client_key: str, tier: DataTier) -> None:
        limit = TIER_LIMITS.get(tier, 10)
        now = time.time()
        
        if client_key not in self.buckets:
            self.buckets[client_key] = (limit - 1.0, now)
            return

        tokens, last_time = self.buckets[client_key]
        # Calculate refill
        elapsed = now - last_time
        refill = elapsed * (limit / 60.0)
        new_tokens = min(limit, tokens + refill)

        if new_tokens < 1.0:
            raise RateLimitError(f"Rate limit exceeded for tier '{tier.value}'. Limit: {limit} req/min.")

        self.buckets[client_key] = (new_tokens - 1.0, now)

rate_limiter = TokenBucketRateLimiter()
