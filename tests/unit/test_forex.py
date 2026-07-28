import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.core.exceptions import TierUpgradeRequiredError
from openstockapi.api import forex
from openstockapi.providers.forex.service import forex_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_forex_rates_success(monkeypatch):
    mock_get_rates = AsyncMock()
    mock_get_rates.return_value = {
        "base": "USD",
        "rates": {"EUR": 0.88, "VND": 25400.0},
        "timestamp": 1625097600,
        "source": "yahoo",
        "provider": "yahoo"
    }
    monkeypatch.setattr(forex_service, "get_rates", mock_get_rates)

    res = forex.forex_rates("USD")
    assert res["base"] == "USD"
    assert res["rates"]["VND"] == 25400.0

def test_compare_rates_tier_validation():
    set_current_session(Session("free"))
    with pytest.raises(TierUpgradeRequiredError):
        forex.compare_rates("USD")

def test_forex_symbols_success():
    res = forex.forex_symbols()
    assert "forex" in res
    assert "EURUSD" in res["forex"]

def test_forex_profile_success():
    res = forex.forex_profile("EURUSD")
    assert res["symbol"] == "EURUSD"
    assert res["base_currency"] == "EUR"
    assert res["quote_currency"] == "USD"
    assert res["base_logo_url"] == "https://flagcdn.com/w160/eu.png"
    assert res["quote_logo_url"] == "https://flagcdn.com/w160/us.png"
    assert res["category"] == "Majors"
