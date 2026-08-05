import pytest
from unittest.mock import AsyncMock
from openstockapi.license.session import Session, set_current_session
from openstockapi.api import stock as stock_api
from openstockapi.providers.vn_stock.service import vn_stock_service


@pytest.fixture(autouse=True)
def setup_free_session():
    set_current_session(Session("free"))


def test_vn_symbols_default(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = ["AAA", "BBB", "CCC"]
    
    # Patch get_symbols on the service level
    monkeypatch.setattr(vn_stock_service, "get_symbols", mock_get)

    res = stock_api.symbols(market="VN")
    assert res == ["AAA", "BBB", "CCC"]
    mock_get.assert_called_once()


def test_vn_symbols_with_provider(monkeypatch):
    mock_get = AsyncMock()
    mock_get.return_value = ["XXX", "YYY"]
    monkeypatch.setattr(vn_stock_service, "get_symbols", mock_get)

    res = stock_api.symbols(market="VN", provider="vci")
    assert res == ["XXX", "YYY"]
    mock_get.assert_called_once_with(provider="vci")
