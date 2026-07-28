import pytest
from openstockapi.providers.vn_stock.providers.kbs import KBSProvider
from openstockapi.providers.vn_stock.providers.vci import VCIProvider
from openstockapi.core.models import CompanyProfile

def test_kbs_provider_maps_extended_profile_fields(monkeypatch):
    kbs = KBSProvider()
    
    # Mock network request response
    class MockResponse:
        def json(self):
            return {
                "SB": "HPG",
                "EX": "HOSE",
                "IS": "Thép",
                "URL": "https://hoaphat.com.vn",
                "HS": "Tập đoàn Hòa Phát...",
                "TC": "0900189284",
                "CTP": "Nguyễn Việt Thắng",
                "CC": 58147.0,
                "KLCPLH": 5814785700,
                "ADD": "Hưng Yên",
                "Shareholders": [{"NM": "Trần Đình Long", "OR": 26.08, "V": 1516320000}],
                "Leaders": [{"NM": "Trần Đình Long", "PO": "Chủ tịch HĐQT", "FD": 1992}],
                "Ownership": [{"NM": "Nước ngoài", "OR": 22.4}],
                "Subsidiaries": [{"NM": "Thép Hòa Phát Dung Quất", "OR": 99.9}]
            }
            
    monkeypatch.setattr("openstockapi.providers.vn_stock.providers.kbs.http_client.request", lambda *args, **kwargs: MockResponse())
    
    prof = kbs.get_company_profile("HPG")
    assert prof.symbol == "HPG"
    assert prof.logo_url == "https://www.google.com/s2/favicons?sz=128&domain=hoaphat.com.vn"
    assert prof.tax_code == "0900189284"
    assert prof.ceo == "Nguyễn Việt Thắng"
    assert prof.charter_capital == 58147.0
    assert prof.shares_outstanding == 5814785700
    assert prof.address == "Hưng Yên"
    assert len(prof.shareholders) == 1
    assert len(prof.leaders) == 1
    assert len(prof.subsidiaries) == 1

def test_vci_provider_maps_profile_fields(monkeypatch):
    vci = VCIProvider()
    
    class MockResponse:
        def json(self):
            return {
                "data": {
                    "viOrganName": "Tập đoàn Hòa Phát",
                    "comGroupCode": "HOSE",
                    "sector": "Basic Materials",
                    "sectorVn": "Thép",
                    "website": "https://hoaphat.com",
                    "profile": "Mô tả..."
                }
            }
            
    monkeypatch.setattr("openstockapi.providers.vn_stock.providers.vci.http_client.request", lambda *args, **kwargs: MockResponse())

    
    prof = vci.get_company_profile("HPG")
    assert prof.symbol == "HPG"
    assert prof.full_name == "Tập đoàn Hòa Phát"
    assert prof.sector == "Basic Materials"
    assert prof.logo_url == "https://www.google.com/s2/favicons?sz=128&domain=hoaphat.com"
    assert prof.tax_code is None
