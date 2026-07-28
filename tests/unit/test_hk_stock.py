import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import hk_stock
from openstockapi.providers.hk_stock.service import hk_stock_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_hk_symbols(monkeypatch):
    mock_get = AsyncMock(return_value=["0700", "9988"])
    monkeypatch.setattr(hk_stock_service, "get_symbols", mock_get)

    res = hk_stock.hk_symbols()
    assert "0700" in res
    assert "9988" in res

def test_hk_ohlcv(monkeypatch):
    mock_get = AsyncMock(return_value={
        "symbol": "0700",
        "currency": "HKD",
        "bars": [
            {"timestamp": 1784795096000, "open": 465.6, "high": 481.8, "low": 465.0, "close": 478.2, "volume": 3250000}
        ]
    })
    monkeypatch.setattr(hk_stock_service, "get_ohlcv", mock_get)

    res = hk_stock.hk_ohlcv("0700")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["close"] == 478.2
    else:
        assert res[0]["close"] == 478.2

def test_hk_profile(monkeypatch):
    mock_get = AsyncMock(return_value={
        "symbol": "0700",
        "company_name": "Tencent Holdings Limited",
        "sector": "Technology",
        "industry": "Internet Content & Information",
        "website": "https://www.tencent.com",
        "logo_url": "https://www.google.com/s2/favicons?sz=128&domain=tencent.com"
    })
    monkeypatch.setattr(hk_stock_service, "get_profile", mock_get)

    res = hk_stock.hk_profile("0700")
    assert res["company_name"] == "Tencent Holdings Limited"
    assert res["sector"] == "Technology"
    assert res["logo_url"] == "https://www.google.com/s2/favicons?sz=128&domain=tencent.com"

def test_hk_financials(monkeypatch):
    mock_get = AsyncMock(return_value={
        "symbol": "0700",
        "period_type": "annual",
        "available_periods": ["2025-12-31"],
        "periods": []
    })
    monkeypatch.setattr(hk_stock_service, "get_financials", mock_get)

    res = hk_stock.hk_financials("0700")
    assert res["period_type"] == "annual"

def test_hk_balance_sheet(monkeypatch):
    mock_get = AsyncMock(return_value={
        "symbol": "0700",
        "period_type": "annual",
        "periods": [
            {
                "period": "2025-12-31",
                "financials": {
                    "balance_sheet": {
                        "total_assets": 1501230000000.0,
                        "total_liabilities": 650230000000.0
                    }
                }
            }
        ]
    })
    monkeypatch.setattr(hk_stock_service, "get_financials", mock_get)

    res = hk_stock.hk_balance_sheet("0700")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["items"]["total_assets"] == 1501230000000.0
    else:
        assert res[0]["items"]["total_assets"] == 1501230000000.0

def test_hk_ratios(monkeypatch):
    mock_get = AsyncMock(return_value={
        "symbol": "0700",
        "ratios": {
            "pe_trailing": 22.4,
            "pb": 4.1
        }
    })
    monkeypatch.setattr(hk_stock_service, "get_ratios", mock_get)

    res = hk_stock.hk_ratios("0700")
    assert res["ratios"]["pe_trailing"] == 22.4

def test_hk_dividends(monkeypatch):
    mock_get = AsyncMock(return_value=[
        {"ex_date": "2025-05-20", "amount": 3.4}
    ])
    monkeypatch.setattr(hk_stock_service, "get_dividends", mock_get)

    res = hk_stock.hk_dividends("0700")
    assert res["dividends"][0]["amount"] == 3.4

def test_hk_splits(monkeypatch):
    mock_get = AsyncMock(return_value=[
        {"date": "2014-05-15", "ratio": 5.0}
    ])
    monkeypatch.setattr(hk_stock_service, "get_splits", mock_get)

    res = hk_stock.hk_splits("0700")
    assert res["splits"][0]["ratio"] == 5.0

def test_hk_calendar(monkeypatch):
    mock_get = AsyncMock(return_value={
        "Earnings Date": ["2026-05-14"]
    })
    monkeypatch.setattr(hk_stock_service, "get_calendar", mock_get)

    res = hk_stock.hk_calendar("0700")
    assert "2026-05-14" in res["calendar"]["Earnings Date"]

def test_hk_news(monkeypatch):
    mock_get = AsyncMock(return_value=[
        {"id": "12345", "title": "Tencent Earnings", "url": "https://tencent.hk", "published_at": 1784795096}
    ])
    monkeypatch.setattr(hk_stock_service, "get_news", mock_get)

    res = hk_stock.hk_news("0700")
    assert res["news"][0]["title"] == "Tencent Earnings"

def test_hk_heatmap(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {
            "symbol": "0700",
            "name": "Tencent Holdings Ltd",
            "change": 1.70,
            "market_cap": 3915648864171.0,
            "sector": "Technology Services",
            "industry": "Packaged Software",
            "logo_url": "https://s3-symbol-logo.tradingview.com/tencent.svg",
            "provider": "tradingview"
        }
    ]
    from openstockapi.providers.hk_stock.service import hk_stock_service
    monkeypatch.setattr(hk_stock_service, "get_heatmap", mock_get)

    res = hk_stock.hk_heatmap(limit=1)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "0700"
        assert res.iloc[0]["market_cap"] == 3915648864171.0
    else:
        assert res[0]["symbol"] == "0700"
        assert res[0]["market_cap"] == 3915648864171.0

