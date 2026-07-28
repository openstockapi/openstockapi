"""
OpenStock CDK (Connector Development Kit)
==========================================
A toolkit for building standardized data providers for OpenStockAPI.

Public API:
    - BaseStockProvider   : Abstract base class for stock market providers.
    - BaseCryptoProvider  : Abstract base class for crypto market providers.
    - BaseForexProvider   : Abstract base class for forex market providers.
    - ProviderCapabilityRegistry : Auto-resolves gateway dispatch without hard-coded if/elif.

Usage:
    from openstockapi.cdk import BaseStockProvider

    class MyProvider(BaseStockProvider):
        name = "my_provider"
        market = "VN"
        ...
"""

from openstockapi.cdk.base_contracts import (
    BaseStockProvider,
    BaseCryptoProvider,
    BaseForexProvider,
)
from openstockapi.cdk.registry import ProviderCapabilityRegistry

__all__ = [
    "BaseStockProvider",
    "BaseCryptoProvider",
    "BaseForexProvider",
    "ProviderCapabilityRegistry",
]

__cdk_version__ = "1.0.0"
