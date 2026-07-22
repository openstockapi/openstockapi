import pytest
from openstockapi.core.types import DataTier
from openstockapi.license.session import Session, set_current_session
from openstockapi.core.exceptions import RateLimitError
from openstockapi.core.rate_limiter import TokenBucketRateLimiter

def test_rate_limiter_anonymous_free():
    limiter = TokenBucketRateLimiter()
    # Call within limit
    for _ in range(10):
        limiter.check_limit("anonymous", DataTier.FREE)
        
    with pytest.raises(RateLimitError):
        limiter.check_limit("anonymous", DataTier.FREE)

def test_rate_limiter_pro():
    limiter = TokenBucketRateLimiter()
    # Call within Pro limit (200)
    for _ in range(100):
        limiter.check_limit("pro_key", DataTier.PRO)
