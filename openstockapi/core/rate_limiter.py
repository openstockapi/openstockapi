import time
from typing import Optional
from openstockapi.core.types import DataTier
from openstockapi.core.exceptions import RateLimitError

# Max requests per minute
TIER_LIMITS = {
    DataTier.FREE: 5,
    DataTier.COMMUNITY: 30,
    DataTier.PRO: 200,
    DataTier.PREMIUM: 500,
}

class TokenBucketRateLimiter:
    def __init__(self) -> None:
        # Simplistic in-memory client state map: bucket_key -> (tokens, last_update_time)
        self.buckets = {}

    def check_limit(self, client_key: str, tier: DataTier, provider: Optional[str] = None) -> None:
        limit = TIER_LIMITS.get(tier, 10)
        
        # Pro/Premium: rate limit based on provider but capped at tier limit
        if tier in (DataTier.PRO, DataTier.PREMIUM):
            if provider:
                # If provider is passed, let's see if we can check if it has a custom rate limit
                try:
                    from openstockapi.providers import get_provider
                    p_inst = get_provider(provider)
                    if p_inst and hasattr(p_inst, "rate_limit"):
                        custom_limit = getattr(p_inst, "rate_limit")
                        if isinstance(custom_limit, (int, float)):
                            limit = min(limit, custom_limit)
                except Exception:
                    pass
                bucket_key = (client_key, provider)
            else:
                bucket_key = client_key
        else:
            bucket_key = client_key

        now = time.time()
        
        if bucket_key not in self.buckets:
            self.buckets[bucket_key] = (limit - 1.0, now)
            return

        tokens, last_time = self.buckets[bucket_key]
        # Calculate refill
        elapsed = now - last_time
        refill = elapsed * (limit / 60.0)
        new_tokens = min(limit, tokens + refill)

        if new_tokens < 1.0:
            refill_rate = limit / 60.0
            retry_after = int(max(1.0, (1.0 - new_tokens) / refill_rate))
            raise RateLimitError(
                error_code="RateLimitExceeded",
                tier=tier.value,
                limit=limit,
                retry_after_seconds=retry_after
            )

        self.buckets[bucket_key] = (new_tokens - 1.0, now)

rate_limiter = TokenBucketRateLimiter()
