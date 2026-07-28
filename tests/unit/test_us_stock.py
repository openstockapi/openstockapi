import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import us_stock
from openstockapi.providers.us_stock.service import us_stock_service

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

def test_us_symbols(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {"symbols": ["AAPL", "MSFT"], "provider": "nasdaq"}
    monkeypatch.setattr(us_stock_service, "get_symbols", mock_get)

    res = us_stock.us_symbols()
    assert "AAPL" in res
    assert "MSFT" in res

def test_us_ohlcv(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "AAPL",
        "currency": "USD",
        "bars": [
            {"timestamp": 1784582400, "open": 180.5, "high": 182.0, "low": 179.8, "close": 181.2, "volume": 52000000}
        ],
        "provider": "yahoo"
    }
    monkeypatch.setattr(us_stock_service, "get_ohlcv", mock_get)

    res = us_stock.us_ohlcv("AAPL")
    if hasattr(res, "iloc"):
        assert res.iloc[0]["close"] == 181.2
    else:
        assert res[0]["close"] == 181.2

def test_us_profile(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "website": "https://www.apple.com",
        "logo_url": "https://www.google.com/s2/favicons?sz=128&domain=apple.com",
        "provider": "yahoo"
    }
    monkeypatch.setattr(us_stock_service, "get_profile", mock_get)

    res = us_stock.us_profile("AAPL")
    assert res["company_name"] == "Apple Inc."
    assert res["sector"] == "Technology"
    assert res["logo_url"] == "https://www.google.com/s2/favicons?sz=128&domain=apple.com"
    assert res["provider"] == "yahoo"

def test_us_financials(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "AAPL",
        "period_type": "annual",
        "available_periods": ["2025-09-30"],
        "periods": [],
        "provider": "sec_edgar"
    }
    monkeypatch.setattr(us_stock_service, "get_financials", mock_get)

    res = us_stock.us_financials("AAPL")
    assert res["period_type"] == "annual"
    assert res["provider"] == "sec_edgar"

def test_us_statements(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "symbol": "AAPL",
        "periods": [
            {
                "period": "2025-09-30",
                "financials": {
                    "balance_sheet": {"total_assets": 359241000000.0},
                    "income_statement": {"revenue": 391035000000.0},
                    "cash_flow": {"operating_cash_flow": 1000000000.0}
                }
            }
        ],
        "provider": "sec_edgar"
    }
    monkeypatch.setattr(us_stock_service, "get_financials", mock_get)

    bs = us_stock.us_balance_sheet("AAPL")
    inc = us_stock.us_income_statement("AAPL")
    cf = us_stock.us_cashflow("AAPL")

    if hasattr(bs, "iloc"):
        assert bs.iloc[0]["items"]["total_assets"] == 359241000000.0
        assert inc.iloc[0]["items"]["revenue"] == 391035000000.0
        assert cf.iloc[0]["items"]["operating_cash_flow"] == 1000000000.0
        assert bs.iloc[0]["provider"] == "sec_edgar"
        assert inc.iloc[0]["provider"] == "sec_edgar"
        assert cf.iloc[0]["provider"] == "sec_edgar"
    else:
        assert bs[0]["items"]["total_assets"] == 359241000000.0
        assert inc[0]["items"]["revenue"] == 391035000000.0
        assert cf[0]["items"]["operating_cash_flow"] == 1000000000.0
        assert bs[0]["provider"] == "sec_edgar"
        assert inc[0]["provider"] == "sec_edgar"
        assert cf[0]["provider"] == "sec_edgar"

def test_us_dividends(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "dividends": [
            {"ex_date": "2026-05-11", "pay_date": None, "amount": 0.27, "type": "Dividend"}
        ],
        "provider": "nasdaq"
    }
    monkeypatch.setattr(us_stock_service, "get_dividends", mock_get)

    res = us_stock.us_dividends("AAPL")
    assert res["dividends"][0]["amount"] == 0.27
    assert res["provider"] == "nasdaq"

def test_us_splits(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "splits": [
            {"date": "2020-08-31", "ratio": 4.0}
        ],
        "provider": "yahoo"
    }
    monkeypatch.setattr(us_stock_service, "get_splits", mock_get)

    res = us_stock.us_splits("AAPL")
    assert res["splits"][0]["ratio"] == 4.0
    assert res["provider"] == "yahoo"

def test_us_calendar(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {"Dividend Date": "2026-05-14", "provider": "yahoo"}
    monkeypatch.setattr(us_stock_service, "get_calendar", mock_get)

    res = us_stock.us_calendar("AAPL")
    assert res["calendar"]["Dividend Date"] == "2026-05-14"
    assert res["provider"] == "yahoo"

def test_us_news(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = {
        "news": [
            {"id": "12345", "title": "Apple Q3 Results", "url": "http://example.com", "published_at": 1784795096}
        ],
        "provider": "google_news"
    }
    monkeypatch.setattr(us_stock_service, "get_news", mock_get)

    res = us_stock.us_news("AAPL")
    assert res["news"][0]["title"] == "Apple Q3 Results"
    assert res["provider"] == "google_news"

def test_us_heatmap(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "change": 1.25,
            "market_cap": 3000000000000.0,
            "sector": "Electronic Technology",
            "industry": "Telecommunications Equipment",
            "provider": "tradingview"
        }
    ]
    monkeypatch.setattr(us_stock_service, "get_heatmap", mock_get)

    res = us_stock.us_heatmap(limit=1)
    if hasattr(res, "iloc"):
        assert res.iloc[0]["symbol"] == "AAPL"
        assert res.iloc[0]["market_cap"] == 3000000000000.0
    else:
        assert res[0]["symbol"] == "AAPL"
        assert res[0]["market_cap"] == 3000000000000.0
