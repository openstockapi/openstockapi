"""
CDK Test Mock Fixtures
=======================
Contains mock responses for standard testing of CDK provider classes.
"""

import pytest
from datetime import datetime
from openstockapi.core.models import OHLCVBar, FinancialItem, CompanyProfile

def cdk_mock_ohlcv():
    return [
        OHLCVBar(
            symbol="HPG",
            timestamp=datetime(2024, 1, 2),
            open=25000.0,
            high=26000.0,
            low=24800.0,
            close=25500.0,
            volume=5000000.0,
            provider="mock",
        ),
        OHLCVBar(
            symbol="HPG",
            timestamp=datetime(2024, 1, 3),
            open=25500.0,
            high=25800.0,
            low=25100.0,
            close=25300.0,
            volume=4200000.0,
            provider="mock",
        ),
    ]

def cdk_mock_financials():
    return [
        FinancialItem(
            symbol="HPG",
            year=2023,
            quarter=4,
            statement_type="income",
            items={"revenue": 30000000000.0, "net_profit": 2500000000.0},
            provider="mock",
        )
    ]

def cdk_mock_profile():
    return CompanyProfile(
        symbol="HPG",
        full_name="Hoa Phat Group Joint Stock Company",
        exchange="HOSE",
        sector="Basic Materials",
        industry="Steel",
        provider="mock",
    )
