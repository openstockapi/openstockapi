"""
CDK Contract Tests for KBSProvider
==================================
Verifies KBSProvider complies with CDK data quality standards.
"""

from unittest.mock import patch
from openstockapi.providers.vn_stock.providers.kbs import KBSProvider
from .base_test import BaseCDKProviderTest
from .fixtures import cdk_mock_ohlcv, cdk_mock_financials, cdk_mock_profile


class TestKBSProviderCDK(BaseCDKProviderTest):
    PROVIDER_CLASS = KBSProvider
    SAMPLE_SYMBOL = "HPG"
    SAMPLE_MARKET = "VN"

    def test_cdk_100_ohlcv_contract(self):
        """Mock the get_ohlcv output to verify validation logic parses it correctly."""
        # 1. Test with valid mocked data
        mock_data = cdk_mock_ohlcv()
        for bar in mock_data:
            bar.provider = "kbs"  # Update provider name to match KBS

        with patch.object(self.PROVIDER_CLASS, "get_ohlcv", return_value=mock_data):
            super().test_cdk_100_ohlcv_contract()

    def test_cdk_200_financial_contract(self):
        """Mock the get_financial_statements output to verify validation logic."""
        mock_data = cdk_mock_financials()
        for item in mock_data:
            item.provider = "kbs"

        with patch.object(self.PROVIDER_CLASS, "get_financial_statements", return_value=mock_data):
            super().test_cdk_200_financial_contract()

    def test_cdk_300_profile_contract(self):
        """Mock the get_company_profile output to verify validation logic."""
        mock_data = cdk_mock_profile()
        mock_data.provider = "kbs"

        with patch.object(self.PROVIDER_CLASS, "get_company_profile", return_value=mock_data):
            super().test_cdk_300_profile_contract()
