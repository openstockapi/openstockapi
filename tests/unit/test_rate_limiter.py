import pytest
from openstockapi.core.types import DataTier
from openstockapi.core.exceptions import RateLimitError
from openstockapi.core.rate_limiter import TokenBucketRateLimiter
from unittest.mock import MagicMock, patch

def test_rate_limiter_anonymous_free():
    limiter = TokenBucketRateLimiter()
    # Free limit is now 5
    for _ in range(5):
        limiter.check_limit("anonymous", DataTier.FREE)
        
    with pytest.raises(RateLimitError) as exc_info:
        limiter.check_limit("anonymous", DataTier.FREE)

    assert exc_info.value.error_code == "RateLimitExceeded"
    assert "rate limit" in exc_info.value.message.lower()
    assert exc_info.value.retry_after_seconds >= 1

def test_rate_limiter_community():
    limiter = TokenBucketRateLimiter()
    # Community limit is 30
    for _ in range(30):
        limiter.check_limit("comm_key", DataTier.COMMUNITY)
        
    with pytest.raises(RateLimitError) as exc_info:
        limiter.check_limit("comm_key", DataTier.COMMUNITY)

    assert exc_info.value.error_code == "RateLimitExceeded"
    assert "rate limit" in exc_info.value.message.lower()
    assert exc_info.value.retry_after_seconds >= 1

def test_rate_limiter_pro_per_provider():
    limiter = TokenBucketRateLimiter()
    # Pro limit is 200 req/min but it is per-provider.
    # Call 150 times on provider "dnse" and 150 times on provider "vci" (both under 200).
    for _ in range(150):
        limiter.check_limit("pro_key", DataTier.PRO, provider="dnse")
        limiter.check_limit("pro_key", DataTier.PRO, provider="vci")

    # Exceeding on dnse specifically
    for _ in range(50):
        limiter.check_limit("pro_key", DataTier.PRO, provider="dnse")

    with pytest.raises(RateLimitError):
        limiter.check_limit("pro_key", DataTier.PRO, provider="dnse")

    # vci is still under limit (150 calls made, limit is 200)
    limiter.check_limit("pro_key", DataTier.PRO, provider="vci")

def test_rate_limiter_pro_custom_provider_limit():
    limiter = TokenBucketRateLimiter()
    
    # Mock a provider with a custom rate_limit attribute
    mock_provider = MagicMock()
    mock_provider.rate_limit = 10
    
    with patch("openstockapi.providers.get_provider", return_value=mock_provider):
        # We can only call 10 times for this provider
        for _ in range(10):
            limiter.check_limit("pro_key", DataTier.PRO, provider="custom_prov")
            
        with pytest.raises(RateLimitError):
            limiter.check_limit("pro_key", DataTier.PRO, provider="custom_prov")
