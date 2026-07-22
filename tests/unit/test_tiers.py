import pytest
from openstockapi.core.exceptions import TierUpgradeRequiredError
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import stock, trading

def test_free_tier_cannot_access_quote():
    set_current_session(Session()) # default to Free
    with pytest.raises(TierUpgradeRequiredError):
        stock.quote("VNM")

def test_pro_tier_can_access_quote_under_limit(monkeypatch):
    set_current_session(Session("pro_mykey"))
    
    # Mock DNSE's get_realtime_quote method to bypass HTTP network calls during unit testing
    from openstockapi.providers.dnse import DNSEProvider
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
    
    monkeypatch.setattr(DNSEProvider, "get_realtime_quote", mock_quote)
    
    res = stock.quote("VNM")
    assert res["price"] == 78000.0
    assert res["provider"] == "dnse"
