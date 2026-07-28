import pytest
import httpx
from unittest.mock import patch, MagicMock
from openstockapi.core.exceptions import TierUpgradeRequiredError, RateLimitExceededError
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import stock


def _mock_validate_response(allowed: bool, tier: str = "pro", reason: str = None):
    """Helper to build a mocked httpx response from /v1/license/validate."""
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200
    body = {"allowed": allowed, "tier": tier}
    if reason:
        body["reason"] = reason
    mock_resp.json.return_value = body
    return mock_resp


def test_free_tier_blocked_by_server():
    """Server returns allowed=False with tier mismatch reason."""
    set_current_session(Session("free"))
    mock_resp = _mock_validate_response(
        allowed=False,
        tier="free",
        reason="This endpoint requires 'pro' tier. Your current tier is 'free'."
    )
    with patch("httpx.post", return_value=mock_resp):
        with pytest.raises(TierUpgradeRequiredError):
            stock.quote("VNM")


def test_pro_tier_allowed_by_server(monkeypatch):
    """Server returns allowed=True; broker call proceeds."""
    set_current_session(Session("pro"))
    mock_resp = _mock_validate_response(allowed=True, tier="pro")

    from openstockapi.providers.vn_stock.providers.dnse import DNSEProvider
    from openstockapi.core.models import RealtimeQuote
    from datetime import datetime

    def mock_quote(self, symbol):
        return RealtimeQuote(
            symbol=symbol,
            price=78000.0,
            change=500.0,
            pct_change=0.64,
            volume=1000000,
            timestamp=datetime.now(),
            provider="dnse"
        )

    monkeypatch.setattr(DNSEProvider, "get_vn_quote", mock_quote, raising=False)
    with patch("httpx.post", return_value=mock_resp):
        res = stock.quote("VNM")
        assert res["price"] == 78000.0
        assert res["provider"] == "dnse"


def test_rate_limit_exceeded_by_server():
    """Server returns allowed=False with rate limit reason."""
    set_current_session(Session("free"))
    mock_resp = _mock_validate_response(
        allowed=False,
        tier="free",
        reason="Rate limit exceeded for tier 'free'."
    )
    with patch("httpx.post", return_value=mock_resp):
        with pytest.raises((TierUpgradeRequiredError, RateLimitExceededError)):
            stock.quote("VNM")
