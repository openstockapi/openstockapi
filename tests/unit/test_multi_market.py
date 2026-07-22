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
