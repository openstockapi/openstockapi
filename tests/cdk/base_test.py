"""
Base CDK Provider Test
======================
Automatically tests any provider against CDK quality contracts (CDK-101 to CDK-304)
using standard mocks.
"""

import pytest
from typing import Type
from openstockapi.core.base_provider import BaseProvider
from openstockapi.cdk.validator import (
    validate_ohlcv,
    validate_financial,
    validate_company_profile,
)


class BaseCDKProviderTest:
    """
    Subclass this class to test your provider against the CDK contract.
    You must override PROVIDER_CLASS, SAMPLE_SYMBOL, and optional config fields.
    """

    PROVIDER_CLASS: Type[BaseProvider] = None
    SAMPLE_SYMBOL: str = "HPG"
    SAMPLE_MARKET: str = "VN"

    @pytest.fixture(autouse=True)
    def setup_provider(self):
        """Instantiates the provider before every test."""
        if self.PROVIDER_CLASS is None:
            pytest.skip("PROVIDER_CLASS is not defined")
        self.provider = self.PROVIDER_CLASS()

    # ── Contract Metadata Checks ──────────────────────────────────────────────

    def test_cdk_001_provider_has_name(self):
        assert hasattr(self.PROVIDER_CLASS, "name")
        assert self.PROVIDER_CLASS.name != ""
        assert self.PROVIDER_CLASS.name != "base"

    def test_cdk_002_provider_has_market_and_asset_class(self):
        assert hasattr(self.PROVIDER_CLASS, "market")
        assert hasattr(self.PROVIDER_CLASS, "asset_class")
        assert self.PROVIDER_CLASS.market != ""
        assert self.PROVIDER_CLASS.asset_class != ""

    def test_cdk_003_supported_methods_is_list(self):
        assert hasattr(self.PROVIDER_CLASS, "supported_methods")
        assert isinstance(self.PROVIDER_CLASS.supported_methods, list)

    # ── OHLCV Data Contract Checks ────────────────────────────────────────────

    def test_cdk_100_ohlcv_contract(self):
        """Runs the validation logic for OHLCV data."""
        if "get_ohlcv" not in self.PROVIDER_CLASS.supported_methods:
            pytest.skip("get_ohlcv is not supported/implemented by this provider")

        try:
            # We call the provider with a standard request (will hit the actual provider
            # or its mock inside the provider's unit tests, but here we test the class contract).
            # To run contract tests without hitting real APIs in normal test suites,
            # subclasses can mock the http_client or specific raw responses.
            data = self.provider.get_ohlcv(
                symbol=self.SAMPLE_SYMBOL,
                resolution="1D",
                from_date="2024-01-01",
                to_date="2024-01-10",
            )
            result = validate_ohlcv(data, symbol=self.SAMPLE_SYMBOL, provider_name=self.provider.name)
            assert result.passed, f"OHLCV Validation failed:\n{result}"
        except NotImplementedError:
            pytest.skip("get_ohlcv raised NotImplementedError")
        except Exception as e:
            # Let other unexpected errors fail the test, except connection errors if we are offline
            if "connection" in str(e).lower() or "unreachable" in str(e).lower():
                pytest.skip(f"Skipping contract test due to network: {e}")
            raise

    # ── Financial Statements Data Contract Checks ─────────────────────────────

    def test_cdk_200_financial_contract(self):
        """Runs the validation logic for Financial statements."""
        if "get_financial_statements" not in self.PROVIDER_CLASS.supported_methods:
            pytest.skip("get_financial_statements is not supported/implemented by this provider")

        try:
            data = self.provider.get_financial_statements(
                symbol=self.SAMPLE_SYMBOL,
                stmt_type="income",
                period="quarterly",
            )
            result = validate_financial(data, symbol=self.SAMPLE_SYMBOL, stmt_type="income")
            assert result.passed, f"Financial Statements Validation failed:\n{result}"
        except NotImplementedError:
            pytest.skip("get_financial_statements raised NotImplementedError")
        except Exception as e:
            if "connection" in str(e).lower() or "unreachable" in str(e).lower():
                pytest.skip(f"Skipping contract test due to network: {e}")
            raise

    # ── Company Profile Data Contract Checks ──────────────────────────────────

    def test_cdk_300_profile_contract(self):
        """Runs the validation logic for Company Profiles."""
        if "get_company_profile" not in self.PROVIDER_CLASS.supported_methods:
            pytest.skip("get_company_profile is not supported/implemented by this provider")

        try:
            data = self.provider.get_company_profile(symbol=self.SAMPLE_SYMBOL)
            result = validate_company_profile(data, symbol=self.SAMPLE_SYMBOL)
            assert result.passed, f"Company Profile Validation failed:\n{result}"
        except NotImplementedError:
            pytest.skip("get_company_profile raised NotImplementedError")
        except Exception as e:
            if "connection" in str(e).lower() or "unreachable" in str(e).lower():
                pytest.skip(f"Skipping contract test due to network: {e}")
            raise
