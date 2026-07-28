import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import jp_stock
from openstockapi.providers.jp_stock.service import jp_stock_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_jp_symbols(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = ["7203", "6758"]
    monkeypatch.setattr(jp_stock_service, "get_symbols", mock_get)

    res = jp_stock.jp_symbols()
    assert "7203" in res
    assert "6758" in res

def test_jp_ohlcv(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "7203",
        "bars": [
            {"timestamp": 1784582400, "open": 2800.5, "high": 2850.0, "low": 2795.0, "close": 2820.0, "volume": 3200000}
        ],
        "provider": "yahoo"
    }
    monkeypatch.setattr(jp_stock_service, "get_ohlcv", mock_get)

    res = jp_stock.jp_ohlcv("7203")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["close"] == 2820.0
    else:
        assert res[0]["close"] == 2820.0

def test_jp_profile(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "7203",
        "company_name": "Toyota Motor Corporation",
        "sector": "Consumer Cyclical",
        "industry": "Auto Manufacturers",
        "website": "https://global.toyota",
        "logo_url": "https://www.google.com/s2/favicons?sz=128&domain=global.toyota",
        "provider": "yahoo"
    }
    monkeypatch.setattr(jp_stock_service, "get_profile", mock_get)

    res = jp_stock.jp_profile("7203")
    assert res["company_name"] == "Toyota Motor Corporation"
    assert res["sector"] == "Consumer Cyclical"
    assert res["logo_url"] == "https://www.google.com/s2/favicons?sz=128&domain=global.toyota"
    assert res["provider"] == "yahoo"

def test_jp_financials(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "7203",
        "period_type": "annual",
        "available_periods": ["2026-03-31"],
        "periods": [],
        "provider": "yahoo"
    }
    monkeypatch.setattr(jp_stock_service, "get_financials", mock_get)

    res = jp_stock.jp_financials("7203")
    assert res["period_type"] == "annual"
    assert res["provider"] == "yahoo"

def test_jp_balance_sheet(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "7203",
        "periods": [
            {
                "period": "2026-03-31",
                "financials": {
                    "balance_sheet": {
                        "total_assets": 105522331000000.0,
                        "total_liabilities": 64502263000000.0
                    }
                }
            }
        ],
        "provider": "yahoo"
    }
    monkeypatch.setattr(jp_stock_service, "get_financials", mock_get)

    res = jp_stock.jp_balance_sheet("7203")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["items"]["total_assets"] == 105522331000000.0
        assert res.iloc[0]["provider"] == "yahoo"
    else:
        assert res[0]["items"]["total_assets"] == 105522331000000.0
        assert res[0]["provider"] == "yahoo"

def test_jp_ratios(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "7203",
        "ratios": {
            "pe_trailing": 9.81,
            "pb": 0.94
        },
        "provider": "yahoo"
    }
    monkeypatch.setattr(jp_stock_service, "get_ratios", mock_get)

    res = jp_stock.jp_ratios("7203")
    assert res["ratios"]["pe_trailing"] == 9.81
    assert res["provider"] == "yahoo"

def test_jp_dividends(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"ex_date": "2025-03-27", "pay_date": None, "amount": 45.0, "type": "Dividend", "provider": "yahoo"}
    ]
    monkeypatch.setattr(jp_stock_service, "get_dividends", mock_get)

    res = jp_stock.jp_dividends("7203")
    assert res["dividends"][0]["amount"] == 45.0
    assert res["provider"] == "yahoo"

def test_jp_splits(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"date": "2021-09-28", "ratio": 5.0, "provider": "yahoo"}
    ]
    monkeypatch.setattr(jp_stock_service, "get_splits", mock_get)

    res = jp_stock.jp_splits("7203")
    assert res["splits"][0]["ratio"] == 5.0
    assert res["provider"] == "yahoo"

def test_jp_calendar(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {"Earnings Date": ["2026-05-08"], "provider": "yahoo"}
    monkeypatch.setattr(jp_stock_service, "get_calendar", mock_get)

    res = jp_stock.jp_calendar("7203")
    assert "2026-05-08" in res["calendar"]["Earnings Date"]
    assert res["provider"] == "yahoo"

def test_jp_news(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"id": "12345", "title": "Toyota Production", "url": "https://toyota.com", "published_at": 1784795096, "publisher": "Yahoo", "summary": "Toyota info", "provider": "yahoo"}
    ]
    monkeypatch.setattr(jp_stock_service, "get_news", mock_get)

    res = jp_stock.jp_news("7203")
    assert res["news"][0]["title"] == "Toyota Production"
    assert res["provider"] == "yahoo"

def test_jp_heatmap(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {
            "symbol": "8306",
            "name": "Mitsubishi UFJ Financial Group, Inc.",
            "change": 4.43,
            "market_cap": 41977228000000.0,
            "sector": "Finance",
            "industry": "Major Banks",
            "logo_url": "https://s3-symbol-logo.tradingview.com/mitsubishi-group.svg",
            "provider": "tradingview"
        }
    ]
    monkeypatch.setattr(jp_stock_service, "get_heatmap", mock_get)

    res = jp_stock.jp_heatmap(limit=1)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "8306"
        assert res.iloc[0]["market_cap"] == 41977228000000.0
    else:
        assert res[0]["symbol"] == "8306"
        assert res[0]["market_cap"] == 41977228000000.0
