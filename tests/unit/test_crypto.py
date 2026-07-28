import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.core.exceptions import TierUpgradeRequiredError
from openstockapi.api import crypto
from openstockapi.providers.crypto.service import crypto_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_crypto_ohlcv_success(monkeypatch):
    mock_get = AsyncMock(return_value=[
        {"timestamp": 1625097600000, "open": 35000.0, "high": 35500.0, "low": 34800.0, "close": 35200.0, "volume": 120.5}
    ])
    monkeypatch.setattr(crypto_service, "get_ohlcv", mock_get)

    res = crypto.crypto_ohlcv("BTCUSDT", limit=1)
    assert len(res) == 1
    if hasattr(res, "iloc"):
        assert res.iloc[0]["close"] == 35200.0
    else:
        assert res[0]["close"] == 35200.0

def test_crypto_depth_tier_validation():
    set_current_session(Session("free"))
    with pytest.raises(TierUpgradeRequiredError):
        crypto.crypto_depth("BTCUSDT")

def test_crypto_symbols_success(monkeypatch):
    mock_get = AsyncMock(return_value=["BTCUSDT", "ETHUSDT"])
    monkeypatch.setattr(crypto_service, "get_symbols", mock_get)

    res = crypto.crypto_symbols()
    assert "symbols" in res
    assert "BTCUSDT" in res["symbols"]

def test_crypto_profile_success(monkeypatch):
    mock_get = AsyncMock(return_value={
        "symbol": "BTC",
        "name": "Bitcoin",
        "id": "bitcoin",
        "categories": ["Smart Contract Platform", "Layer 1"],
        "website": "https://bitcoin.org",
        "logo_url": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        "description": "Bitcoin is a decentralized digital currency...",
        "market_cap_rank": 1,
        "provider": "coingecko"
    })
    monkeypatch.setattr(crypto_service.coingecko_profile, "get_profile", mock_get)

    res = crypto.crypto_profile("BTC")
    assert res["symbol"] == "BTC"
    assert res["name"] == "Bitcoin"
    assert "Layer 1" in res["categories"]
    assert res["website"] == "https://bitcoin.org"
    assert res["logo_url"] == "https://assets.coingecko.com/coins/images/1/large/bitcoin.png"
    assert res["market_cap_rank"] == 1

def test_crypto_heatmap_success(monkeypatch):
    mock_get = AsyncMock(return_value=[
        {
            "symbol": "BTC",
            "name": "Bitcoin",
            "change": 1.20,
            "market_cap": 1310814128010.0,
            "sector": "Cryptocurrency",
            "industry": "Digital Asset",
            "logo_url": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png",
            "provider": "tradingview"
        }
    ])
    monkeypatch.setattr(crypto_service, "get_heatmap", mock_get)

    res = crypto.crypto_heatmap(limit=1)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "BTC"
        assert res.iloc[0]["market_cap"] == 1310814128010.0
    else:
        assert res[0]["symbol"] == "BTC"
        assert res[0]["market_cap"] == 1310814128010.0

