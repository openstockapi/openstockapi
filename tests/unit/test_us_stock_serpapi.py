import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx
from openstockapi.license.session import Session, set_current_session
from openstockapi.providers.us_stock.service import us_stock_service
from openstockapi.api import us_stock

@pytest.fixture(autouse=True)
def setup_pro_session():
    set_current_session(Session("pro"))

@pytest.mark.asyncio
async def test_serpapi_provider_ohlcv(monkeypatch):
    # Mock response from SerpApi for Google Finance
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "graph": [
            {
                "price": 150.0,
                "currency": "USD",
                "date": "May 22 2026, 09:30 AM UTC-04:00",
                "volume": 5000
            },
            {
                "price": 151.5,
                "currency": "USD",
                "date": "May 22 2026, 09:31 AM UTC-04:00",
                "volume": 6000
            }
        ]
    }
    
    mock_client = MagicMock()
    mock_client.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: mock_client)

    # Test get_ohlcv directly on provider/service
    res = await us_stock_service.get_ohlcv("AAPL", provider="serpapi")
    assert res is not None
    assert res["symbol"] == "AAPL"
    assert res["provider"] == "serpapi"
    assert len(res["bars"]) == 2
    assert res["bars"][0]["close"] == 150.0
    assert res["bars"][1]["close"] == 151.5

@pytest.mark.asyncio
async def test_serpapi_provider_news(monkeypatch):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "news_results": [
            {
                "title": "SerpApi integration successful",
                "link": "https://example.com/news1",
                "source": "OpenStockNews",
                "snippet": "Test snippet 1"
            }
        ]
    }
    
    mock_client = MagicMock()
    mock_client.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: mock_client)

    res = await us_stock_service.get_news("AAPL", provider="serpapi")
    assert res is not None
    assert res["provider"] == "serpapi"
    assert len(res["news"]) == 1
    assert res["news"][0]["title"] == "SerpApi integration successful"
    assert res["news"][0]["url"] == "https://example.com/news1"
