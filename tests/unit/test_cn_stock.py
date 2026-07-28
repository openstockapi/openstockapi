import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import cn_stock
from openstockapi.providers.cn_stock.service import cn_stock_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_cn_symbols(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = ["600519", "002594"]
    monkeypatch.setattr(cn_stock_service, "get_symbols", mock_get)

    res = cn_stock.cn_symbols()
    assert "600519" in res
    assert "002594" in res

def test_cn_ohlcv(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "bars": [
            {"timestamp": 1784582400, "open": 1300.0, "high": 1310.0, "low": 1290.0, "close": 1305.0, "volume": 120000}
        ],
        "provider": "sina"
    }
    monkeypatch.setattr(cn_stock_service, "get_ohlcv", mock_get)

    res = cn_stock.cn_ohlcv("600519")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["close"] == 1305.0
    else:
        assert res[0]["close"] == 1305.0

def test_cn_profile(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "company_name": "Kweichow Moutai Co., Ltd.",
        "sector": "Consumer Defensive",
        "industry": "Beverages—Brewers",
        "website": "https://www.moutaichina.com",
        "logo_url": "https://www.google.com/s2/favicons?sz=128&domain=moutaichina.com",
        "provider": "yahoo"
    }
    monkeypatch.setattr(cn_stock_service, "get_profile", mock_get)

    res = cn_stock.cn_profile("600519")
    assert res["company_name"] == "Kweichow Moutai Co., Ltd."
    assert res["sector"] == "Consumer Defensive"
    assert res["logo_url"] == "https://www.google.com/s2/favicons?sz=128&domain=moutaichina.com"
    assert res["provider"] == "yahoo"

def test_cn_financials(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "period_type": "annual",
        "available_periods": ["2025-12-31"],
        "periods": [],
        "provider": "yahoo"
    }
    monkeypatch.setattr(cn_stock_service, "get_financials", mock_get)

    res = cn_stock.cn_financials("600519")
    assert res["period_type"] == "annual"
    assert res["provider"] == "yahoo"

def test_cn_balance_sheet(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "periods": [
            {
                "period": "2025-12-31",
                "financials": {
                    "balance_sheet": {
                        "total_assets": 280123000000.0,
                        "total_liabilities": 45012000000.0
                    }
                }
            }
        ],
        "provider": "yahoo"
    }
    monkeypatch.setattr(cn_stock_service, "get_financials", mock_get)

    res = cn_stock.cn_balance_sheet("600519")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["items"]["total_assets"] == 280123000000.0
        assert res.iloc[0]["provider"] == "yahoo"
    else:
        assert res[0]["items"]["total_assets"] == 280123000000.0
        assert res[0]["provider"] == "yahoo"

def test_cn_ratios(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "ratios": {
            "pe_trailing": 28.5,
            "pb": 8.2
        },
        "provider": "yahoo"
    }
    monkeypatch.setattr(cn_stock_service, "get_ratios", mock_get)

    res = cn_stock.cn_ratios("600519")
    assert res["ratios"]["pe_trailing"] == 28.5
    assert res["provider"] == "yahoo"

def test_cn_dividends(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"ex_date": "2025-06-15", "pay_date": None, "amount": 30.85, "type": "Dividend", "provider": "sina"}
    ]
    monkeypatch.setattr(cn_stock_service, "get_dividends", mock_get)

    res = cn_stock.cn_dividends("600519")
    assert res["dividends"][0]["amount"] == 30.85
    assert res["provider"] == "sina"

def test_cn_splits(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = []
    monkeypatch.setattr(cn_stock_service, "get_splits", mock_get)

    res = cn_stock.cn_splits("600519")
    assert len(res["splits"]) == 0

def test_cn_calendar(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {"Earnings Date": ["2026-04-18"], "provider": "sina"}
    monkeypatch.setattr(cn_stock_service, "get_calendar", mock_get)

    res = cn_stock.cn_calendar("600519")
    assert "2026-04-18" in res["calendar"]["Earnings Date"]
    assert res["provider"] == "sina"

def test_cn_news(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {"id": "12345", "title": "Moutai Earnings", "url": "https://moutai.cn", "published_at": 1784795096, "publisher": "Sina", "summary": "Moutai info", "provider": "sina"}
    ]
    monkeypatch.setattr(cn_stock_service, "get_news", mock_get)

    res = cn_stock.cn_news("600519")
    assert res["news"][0]["title"] == "Moutai Earnings"
    assert res["provider"] == "sina"

def test_cn_quote(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "price": 1297.41,
        "open": 1300.0,
        "high": 1310.0,
        "low": 1290.0,
        "volume": 3569900.0,
        "timestamp": 1784795096000,
        "provider": "sina"
    }
    monkeypatch.setattr(cn_stock_service, "get_quote", mock_get)

    res = cn_stock.cn_quote("600519")
    assert res["price"] == 1297.41
    assert res["provider"] == "sina"

def test_cn_tick(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "ticks": [
            {"symbol": "600519", "time": "15:00:00", "price": 1297.41, "volume": 3569900.0}
        ],
        "provider": "sina"
    }
    monkeypatch.setattr(cn_stock_service, "get_tick", mock_get)

    res = cn_stock.cn_tick("600519")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["price"] == 1297.41
        assert res.iloc[0]["provider"] == "sina"
    else:
        assert res[0]["price"] == 1297.41
        assert res[0]["provider"] == "sina"

def test_cn_order_book(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "600519",
        "bids": [{"price": 1297.41, "volume": 2100.0}],
        "asks": [{"price": 1297.57, "volume": 100.0}],
        "provider": "sina"
    }
    monkeypatch.setattr(cn_stock_service, "get_book_order", mock_get)

    res = cn_stock.cn_order_book("600519")
    assert res["bids"][0]["price"] == 1297.41
    assert res["provider"] == "sina"

def test_cn_heatmap(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {
            "symbol": "600519",
            "name": "Kweichow Moutai Co., Ltd.",
            "change": 1.25,
            "market_cap": 2500000000000.0,
            "sector": "Consumer Non-Durables",
            "industry": "Beverages: Alcoholic",
            "logo_url": "https://s3-symbol-logo.tradingview.com/kweichow-moutai.svg",
            "provider": "tradingview"
        }
    ]
    monkeypatch.setattr(cn_stock_service, "get_heatmap", mock_get)

    res = cn_stock.cn_heatmap(limit=1)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "600519"
        assert res.iloc[0]["market_cap"] == 2500000000000.0
    else:
        assert res[0]["symbol"] == "600519"
        assert res[0]["market_cap"] == 2500000000000.0

