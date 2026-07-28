import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import asx
from openstockapi.providers.asx.service import asx_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_asx_symbols(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = ["BHP", "CBA"]
    monkeypatch.setattr(asx_service, "get_symbols", mock_get)

    res = asx.asx_symbols()
    assert "BHP" in res
    assert "CBA" in res

def test_asx_ohlcv(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "BHP",
        "bars": [
            {"timestamp": 1784582400, "open": 40.5, "high": 42.0, "low": 39.8, "close": 41.2, "volume": 520000}
        ],
        "provider": "yahoo"
    }
    monkeypatch.setattr(asx_service, "get_ohlcv", mock_get)

    res = asx.asx_ohlcv("BHP")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["close"] == 41.2
    else:
        assert res[0]["close"] == 41.2

def test_asx_profile(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "BHP",
        "company_name": "BHP Group",
        "sector": "Basic Materials",
        "industry": "Mining",
        "website": "https://www.bhp.com",
        "logo_url": "https://www.google.com/s2/favicons?sz=128&domain=bhp.com",
        "provider": "yahoo"
    }
    monkeypatch.setattr(asx_service, "get_profile", mock_get)

    res = asx.asx_profile("BHP")
    assert res["company_name"] == "BHP Group"
    assert res["sector"] == "Basic Materials"
    assert res["logo_url"] == "https://www.google.com/s2/favicons?sz=128&domain=bhp.com"
    assert res["provider"] == "yahoo"

def test_asx_financials(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "BHP",
        "financials": {},
        "ratios": {"pe_trailing": 15.4},
        "provider": "marketindex"
    }
    monkeypatch.setattr(asx_service, "get_financials", mock_get)

    res = asx.asx_financials("BHP")
    assert res["provider"] == "marketindex"

def test_asx_statements(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "BHP",
        "periods": [
            {
                "period": "2025-06-30",
                "financials": {
                    "balance_sheet": {"total_assets": 359241000.0},
                    "income_statement": {"revenue": 391035000.0},
                    "cash_flow": {"operating_cash_flow": 1000000.0}
                }
            }
        ],
        "provider": "marketindex"
    }
    monkeypatch.setattr(asx_service, "get_financials", mock_get)

    bs = asx.asx_balance_sheet("BHP")
    inc = asx.asx_income_statement("BHP")
    cf = asx.asx_cashflow("BHP")

    if hasattr(bs, "iloc"):
        assert bs.iloc[0]["items"]["total_assets"] == 359241000.0
        assert inc.iloc[0]["items"]["revenue"] == 391035000.0
        assert cf.iloc[0]["items"]["operating_cash_flow"] == 1000000.0
        assert bs.iloc[0]["provider"] == "marketindex"
        assert inc.iloc[0]["provider"] == "marketindex"
        assert cf.iloc[0]["provider"] == "marketindex"
    else:
        assert bs[0]["items"]["total_assets"] == 359241000.0
        assert inc[0]["items"]["revenue"] == 391035000.0
        assert cf[0]["items"]["operating_cash_flow"] == 1000000.0
        assert bs[0]["provider"] == "marketindex"
        assert inc[0]["provider"] == "marketindex"
        assert cf[0]["provider"] == "marketindex"

def test_asx_dividends(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"ex_date": "2026-05-11", "pay_date": None, "amount": 0.27, "type": "Dividend", "franking": 100.0, "provider": "asx_site"}
    ]
    monkeypatch.setattr(asx_service, "get_dividends", mock_get)

    res = asx.asx_dividends("BHP")
    assert res["dividends"][0]["amount"] == 0.27
    assert res["provider"] == "asx_site"

def test_asx_announcements(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"id": "12345", "title": "ASX Announcement", "url": "http://example.com", "published_at": "2026-07-23", "size": "100KB", "provider": "asx_site"}
    ]
    monkeypatch.setattr(asx_service, "get_announcements", mock_get)

    res = asx.asx_announcements("BHP")
    assert res["announcements"][0]["title"] == "ASX Announcement"
    assert res["provider"] == "asx_site"

def test_asx_news(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"id": "12345", "title": "ASX News", "url": "http://example.com", "published_at": "2026-07-23", "publisher": "Yahoo Finance", "summary": "BHP updates", "provider": "yahoo"}
    ]
    monkeypatch.setattr(asx_service, "get_news", mock_get)

    res = asx.asx_news("BHP")
    assert res["news"][0]["title"] == "ASX News"
    assert res["provider"] == "yahoo"

def test_asx_heatmap(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {
            "symbol": "BHP",
            "name": "BHP Group Ltd",
            "change": -2.93,
            "market_cap": 298998595299.0,
            "sector": "Non-Energy Minerals",
            "industry": "Steel",
            "logo_url": "https://s3-symbol-logo.tradingview.com/bhp.svg",
            "provider": "tradingview"
        }
    ]
    monkeypatch.setattr(asx_service, "get_heatmap", mock_get)

    res = asx.asx_heatmap(limit=1)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "BHP"
        assert res.iloc[0]["market_cap"] == 298998595299.0
    else:
        assert res[0]["symbol"] == "BHP"
        assert res[0]["market_cap"] == 298998595299.0
