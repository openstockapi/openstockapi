from openstockapi.core.utils import parse_market_symbol

def test_parse_market_symbol_default():
    sym, mkt = parse_market_symbol("VNM")
    assert sym == "VNM"
    assert mkt == "VN"

def test_parse_market_symbol_custom_market():
    sym, mkt = parse_market_symbol("AAPL", default_market="US")
    assert sym == "AAPL"
    assert mkt == "US"

def test_parse_market_symbol_dot_notation():
    sym, mkt = parse_market_symbol("AAPL.US")
    assert sym == "AAPL"
    assert mkt == "US"

    sym2, mkt2 = parse_market_symbol("vnm.vn")
    assert sym2 == "VNM"
    assert mkt2 == "VN"

def test_unified_api_functions(monkeypatch):
    import openstockapi as osapi
    from openstockapi.core.gateway import RequestGateway
    from unittest.mock import MagicMock

    mock_execute = MagicMock()
    monkeypatch.setattr(RequestGateway, "execute", mock_execute)

    # Test symbols
    mock_execute.return_value = ["AAPL", "MSFT"]
    syms = osapi.symbols(market="US")
    mock_execute.assert_called_with(
        action="stock.symbols",
        market="US",
        required_tier=osapi.core.types.DataTier.FREE,
        provider=None
    )
    assert syms == ["AAPL", "MSFT"]

    # Test heatmap
    mock_execute.return_value = []
    osapi.heatmap(market="US", limit=10)
    mock_execute.assert_called_with(
        action="stock.heatmap",
        market="US",
        required_tier=osapi.core.types.DataTier.FREE,
        limit=10,
        provider=None
    )

    # Test dividends
    mock_mock_model = MagicMock()
    mock_mock_model.model_dump.return_value = {"dividends": []}
    mock_execute.return_value = mock_mock_model
    osapi.dividends("AAPL", market="US")
    mock_execute.assert_called_with(
        action="stock.dividends",
        market="US",
        required_tier=osapi.core.types.DataTier.FREE,
        symbol="AAPL",
        provider=None
    )

    # Test splits
    osapi.splits("AAPL", market="US")
    mock_execute.assert_called_with(
        action="stock.splits",
        market="US",
        required_tier=osapi.core.types.DataTier.FREE,
        symbol="AAPL",
        provider=None
    )

    # Test calendar
    osapi.calendar("AAPL", market="US")
    mock_execute.assert_called_with(
        action="stock.calendar",
        market="US",
        required_tier=osapi.core.types.DataTier.FREE,
        symbol="AAPL",
        provider=None
    )

