import pytest
from datetime import datetime
from openstockapi.core.utils import get_asset_type, safe_convert_derivative_symbol
from openstockapi.providers.vn_stock.providers.kbs import KBSProvider

def test_derivative_symbol_parsing_and_conversion():
    # Test asset types
    assert get_asset_type("VN30F1M") == "derivative"
    assert get_asset_type("VN30F2506") == "derivative"
    assert get_asset_type("CHPG2301") == "coveredWarr"
    
    # Test safe conversion
    # For explicit suffixes: VN30F2506 -> 41I1F7000 (effective May 2025 cycle index conversion)
    krx_explicit = safe_convert_derivative_symbol("VN30F2506")
    assert krx_explicit == "41I1F6000"

def test_kbs_provider_warrant_profile(monkeypatch):
    kbs = KBSProvider()
    
    class MockResponse:
        def json(self):
            return [
                {
                    "ULS": "HPG",
                    "EX": "HOSE",
                    "RE": 1200,
                    "CL": 1300,
                    "FL": 1100,
                    "CWT": "Call",
                    "EP": 26000,
                    "ER": "4:1"
                }
            ]
            
    monkeypatch.setattr("openstockapi.providers.vn_stock.providers.kbs.http_client.request", lambda *args, **kwargs: MockResponse())
    
    prof = kbs.get_derivative_profile("CHPG2301")
    assert prof.symbol == "CHPG2301"
    assert prof.underlying_symbol == "HPG"
    assert prof.exchange == "HOSE"
    assert prof.reference_price == 1.2
    assert prof.warrant_type == "Call"
    assert prof.exercise_price == 26.0
    assert prof.conversion_ratio == 4.0

def test_kbs_provider_future_profile(monkeypatch):
    kbs = KBSProvider()
    
    class MockResponse:
        def json(self):
            return {
                "data": [
                    {
                        "FN": "HĐTL Chỉ số VN30F1M",
                        "ULS": "VN30",
                        "EX": "HNX",
                        "FTD": "20260701",
                        "LTD": "20260716",
                        "RE": 1250.0,
                        "CL": 1330.0,
                        "FL": 1170.0,
                        "OI": 45000
                    }
                ]
            }
            
    monkeypatch.setattr("openstockapi.providers.vn_stock.providers.kbs.http_client.request", lambda *args, **kwargs: MockResponse())
    
    prof = kbs.get_derivative_profile("VN30F1M")
    assert prof.symbol == "VN30F1M"
    assert prof.full_name == "HĐTL Chỉ số VN30F1M"
    assert prof.underlying_symbol == "VN30"
    assert prof.exchange == "HNX"
    assert prof.reference_price == 1250.0
    assert prof.open_interest == 45000
