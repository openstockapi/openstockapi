"""
Unit tests for VN Stock Heatmap — tests all 3 providers (tradingview, kbs, vci)
using monkeypatched async calls.
"""
import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import stock as vn_stock_api
from openstockapi.providers.vn_stock.heatmap_service import vn_heatmap_service


@pytest.fixture(autouse=True)
def setup_free_session():
    set_current_session(Session("free"))


def _mock_heatmap_item(symbol: str, provider: str, market_cap=None):
    return {
        "symbol": symbol,
        "name": f"Test Company {symbol}",
        "change": 1.23,
        "market_cap": market_cap,
        "sector": "Finance",
        "industry": "Banks",
        "logo_url": f"https://example.com/{symbol}.svg",
        "provider": provider,
    }


# -------------------------------------------------------
# TradingView provider (default)
# -------------------------------------------------------
def test_vn_heatmap_tradingview(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        _mock_heatmap_item("VIC", "tradingview", market_cap=1597981543945312.0),
        _mock_heatmap_item("VHM", "tradingview", market_cap=980000000000000.0),
    ]
    monkeypatch.setattr(vn_heatmap_service, "get_heatmap", mock_get)

    res = vn_stock_api.vn_heatmap(limit=2)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "VIC"
        assert res.iloc[0]["provider"] == "tradingview"
        assert res.iloc[0]["market_cap"] == 1597981543945312.0
    else:
        assert res[0]["symbol"] == "VIC"
        assert res[0]["provider"] == "tradingview"
        assert res[0]["market_cap"] == 1597981543945312.0


# -------------------------------------------------------
# KBS provider (change% only, no market_cap)
# -------------------------------------------------------
def test_vn_heatmap_kbs(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        _mock_heatmap_item("VNM", "kbs", market_cap=None),
        _mock_heatmap_item("FPT", "kbs", market_cap=None),
    ]
    monkeypatch.setattr(vn_heatmap_service, "get_heatmap", mock_get)

    res = vn_stock_api.vn_heatmap(limit=2, provider="kbs")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "VNM"
        assert res.iloc[0]["provider"] == "kbs"
        # market_cap is None/NaN for KBS
    else:
        assert res[0]["symbol"] == "VNM"
        assert res[0]["provider"] == "kbs"
        assert res[0]["market_cap"] is None


# -------------------------------------------------------
# VCI provider (sector/industry/logo, no change%)
# -------------------------------------------------------
def test_vn_heatmap_vci(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {
            "symbol": "ACB",
            "name": "Asia Commercial Bank",
            "change": 0.0,           # VCI doesn't have change% in batch
            "market_cap": None,       # VCI doesn't have market_cap in batch
            "sector": "Financials",
            "industry": "Banks",
            "logo_url": "https://vietcap-website.s3.ap-southeast-1.amazonaws.com/cms/logo/ACB.webp",
            "provider": "vci",
        }
    ]
    monkeypatch.setattr(vn_heatmap_service, "get_heatmap", mock_get)

    res = vn_stock_api.vn_heatmap(limit=1, provider="vci")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "ACB"
        assert res.iloc[0]["sector"] == "Financials"
        assert "logo_url" in res.columns
    else:
        assert res[0]["symbol"] == "ACB"
        assert res[0]["sector"] == "Financials"
        assert res[0]["logo_url"] is not None


# -------------------------------------------------------
# Empty result handling
# -------------------------------------------------------
def test_vn_heatmap_empty(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = []
    monkeypatch.setattr(vn_heatmap_service, "get_heatmap", mock_get)

    res = vn_stock_api.vn_heatmap(limit=10)
    if hasattr(res, "empty"):
        assert res.empty
    else:
        assert res == []
