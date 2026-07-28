import pytest
import httpx
from unittest.mock import MagicMock, patch
from openstockapi.license.session import Session, set_current_session

@pytest.fixture(autouse=True)
def mock_license_validate():
    """Autouse fixture to mock the license validation endpoint and set up session tokens for unit tests.

    This ensures that all tests have a valid dummy session_token and intercepts
    validate calls to correctly simulate server-side tier restriction checks.
    """
    # Initialize a default pro session
    set_current_session(Session("pro"))

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200

    def validate_mock(url, json=None, **kwargs):
        # We only mock the validate endpoint
        if "/v1/license/validate" not in url:
            return httpx.Response(200, json={})

        action = json.get("action", "") if json else ""
        from openstockapi.license.session import get_current_session
        sess = get_current_session()

        allowed = True
        reason = None

        # Simulate the server-side ENDPOINT_TIER_MAP behavior for tests
        pro_actions = {
            "stock.vn.quote",
            "stock.vn.order_book",
            "crypto.global.depth",
            "crypto.global.derivatives",
            "crypto.global.tickers",
            "crypto.global.options",
            "forex.global.compare",
        }

        # If session is free tier and calls a pro action, block it
        if sess.api_key and "free" in sess.api_key.lower():
            if action in pro_actions:
                allowed = False
                reason = f"Endpoint '{action}' requires 'pro' tier. Your current tier is 'free'."

        mock_resp.json.return_value = {"allowed": allowed, "tier": sess.tier.value, "reason": reason}
        return mock_resp

    with patch("httpx.post", side_effect=validate_mock) as mock_post:
        yield mock_post
