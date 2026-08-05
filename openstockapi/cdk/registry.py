"""
CDK Provider Capability Registry
==================================
Resolves the gateway action-to-method dispatch without requiring hard-coded
if/elif chains in gateway._dispatch_to_provider().

This registry centralizes the mapping logic so that:
  - New markets do NOT require changes to gateway.py.
  - Method resolution is transparent and testable.
  - The same map is used by both the gateway and the CDK test suite.

Usage (in gateway.py):
    from openstockapi.cdk.registry import registry

    method_name = registry.resolve_method(
        provider=provider_instance,
        function="ohlcv",
        asset_class="stock",
        market="vn",
    )
    result = getattr(provider_instance, method_name)(**params)
"""

from typing import Optional, Any
import logging

logger = logging.getLogger("openstockapi.cdk.registry")


class ProviderCapabilityRegistry:
    """
    Centralizes and automates the resolution of provider method names
    from an incoming gateway action string.

    Resolution order:
        1. Market-specific override  (e.g. stock + us + ohlcv -> get_us_ohlcv)
        2. Universal method map      (e.g. ohlcv -> get_ohlcv)
        3. Dynamic hasattr fallback  (last resort, for legacy providers)

    The registry does NOT instantiate providers; it only resolves method names.
    """

    # ── Market-specific method prefix map ─────────────────────────────────────
    # When asset_class=="stock" and the market has a custom prefix,
    # the resolved method is f"get_{prefix}_{function}".
    MARKET_PREFIX_MAP: dict[str, str] = {
        "au": "asx",
        "us": "us",
        "jp": "jp",
        "cn": "cn",
        "hk": "hk",
        "vn": "vn",
    }

    # ── Universal function -> method name map ─────────────────────────────────
    # Used as fallback when no market prefix match is found.
    # These are the generic, asset-class-agnostic method names.
    UNIVERSAL_METHOD_MAP: dict[str, str] = {
        # Core market data
        "ohlcv":               "get_ohlcv",
        "profile":             "get_company_profile",
        "derivative_profile":  "get_derivative_profile",
        "quote":               "get_realtime_quote",
        # Financial statements (all share the same method, stmt_type differentiates)
        "balance_sheet":       "get_financial_statements",
        "income_statement":    "get_financial_statements",
        "cashflow":            "get_financial_statements",
        "ratios":              "get_financial_statements",
        # Order flow
        "order_book":          "get_order_book",
        "ticks":               "get_intraday_ticks",
        # Ownership & trading activity
        "foreign_trade":       "get_foreign_trading",
        "insider_trade":       "get_insider_trading",
        "prop_trade":          "get_prop_trading",
        # Macro & funds
        "macro_indicators":    "get_macro_indicators",
        "fund_details":        "get_fund_details",
        "market_index":        "get_market_index",
        # News & events
        "company_news":        "get_company_news",
        "company_events":      "get_company_events",
        # Crypto specific
        "depth":               "get_crypto_depth",
        "derivatives":         "get_crypto_derivatives",
        "footprint":           "get_crypto_footprint",
        "simulate":            "simulate_crypto_leverage",
        "symbols":             "get_crypto_symbols",
        "tickers":             "get_crypto_tickers",
        "options_instruments": "get_crypto_options_instruments",
        "options_chain":       "get_crypto_options_chain",
        "options_ticker":      "get_crypto_options_ticker",
        "news":                "get_crypto_news",
        "events":              "get_crypto_events",
        # Forex specific
        "rates":               "get_forex_rates",
        "compare":             "compare_forex_rates",
        "commodities":         "get_commodities_prices",
        "indices_etf":         "get_global_indices_etf",
    }

    # ── Asset-class scoped overrides ──────────────────────────────────────────
    # When function is ambiguous (e.g. "symbols" could be crypto or forex),
    # asset_class is used to pick the right method.
    ASSET_CLASS_METHOD_MAP: dict[str, dict[str, str]] = {
        "crypto": {
            "ohlcv":   "get_crypto_ohlcv",
            "profile": "get_crypto_profile",
            "symbols": "get_crypto_symbols",
            "news":    "get_crypto_news",
            "events":  "get_crypto_events",
            "heatmap": "get_crypto_heatmap",
        },
        "forex": {
            "ohlcv":   "get_forex_ohlcv",
            "profile": "get_forex_profile",
            "symbols": "get_forex_symbols",
            "news":    "get_forex_news",
            "events":  "get_forex_events",
        },
    }

    # ── Financial statement type -> stmt_type param ────────────────────────────
    STMT_TYPE_MAP: dict[str, str] = {
        "balance_sheet":    "balance",
        "income_statement": "income",
        "cashflow":         "cashflow",
        "ratios":           "ratios",
    }

    def resolve_method(
        self,
        provider: Any,
        function: str,
        asset_class: str,
        market: str,
    ) -> str:
        """
        Resolve the concrete method name to call on a provider instance.

        Resolution order:
            1. Asset-class scoped map  (crypto/forex have unique method names)
            2. Market prefix override  (stock + vn + ohlcv -> get_vn_ohlcv)
            3. Universal map           (generic fallback)
            4. Dynamic hasattr         (last-resort for legacy providers)

        Args:
            provider:    The provider instance (used for hasattr fallback).
            function:    The action function string (e.g. "ohlcv", "quote").
            asset_class: The asset class string (e.g. "stock", "crypto", "forex").
            market:      The lowercase market code (e.g. "vn", "us", "global").

        Returns:
            str: The method name to call on the provider.

        Raises:
            NotImplementedError: If no method can be resolved for this combination.
        """
        # 1. Asset-class scoped override (crypto & forex have distinct method names)
        if asset_class in self.ASSET_CLASS_METHOD_MAP:
            asset_map = self.ASSET_CLASS_METHOD_MAP[asset_class]
            if function in asset_map:
                method_name = asset_map[function]
                if hasattr(provider, method_name):
                    logger.debug(
                        "Registry: asset-class route [%s.%s] -> %s",
                        asset_class, function, method_name,
                    )
                    return method_name

        # 2. Market-prefix override for stock providers
        if asset_class == "stock" and market in self.MARKET_PREFIX_MAP:
            prefix = self.MARKET_PREFIX_MAP[market]
            market_method = f"get_{prefix}_{function}"
            if hasattr(provider, market_method):
                logger.debug(
                    "Registry: market-prefix route [%s.%s.%s] -> %s",
                    asset_class, market, function, market_method,
                )
                return market_method
            
            # Fallback for news and calendar/events naming mismatches
            if function == "company_news":
                alt_method = f"get_{prefix}_news"
                if hasattr(provider, alt_method):
                    logger.debug(
                        "Registry: market-prefix news fallback [%s.%s.%s] -> %s",
                        asset_class, market, function, alt_method,
                    )
                    return alt_method
            elif function == "company_events":
                for alt_name in ["calendar", "events"]:
                    alt_method = f"get_{prefix}_{alt_name}"
                    if hasattr(provider, alt_method):
                        logger.debug(
                            "Registry: market-prefix events fallback [%s.%s.%s] -> %s",
                            asset_class, market, function, alt_method,
                        )
                        return alt_method

        # 3. Universal method map
        if function in self.UNIVERSAL_METHOD_MAP:
            method_name = self.UNIVERSAL_METHOD_MAP[function]
            if hasattr(provider, method_name):
                logger.debug(
                    "Registry: universal route [%s] -> %s",
                    function, method_name,
                )
                return method_name

        # 4. Dynamic hasattr fallback (legacy / non-standard providers)
        #    Try common naming conventions before giving up.
        fallback_candidates = [
            f"get_{function}",
            f"get_{asset_class}_{function}",
            f"get_{market}_{function}",
        ]
        for candidate in fallback_candidates:
            if hasattr(provider, candidate):
                logger.debug(
                    "Registry: dynamic fallback [%s.%s.%s] -> %s",
                    asset_class, market, function, candidate,
                )
                return candidate

        raise NotImplementedError(
            f"Provider '{provider.name}' does not implement '{function}' "
            f"(asset_class='{asset_class}', market='{market}'). "
            f"Check supported_methods or add the method to the provider."
        )

    def get_stmt_type_param(self, function: str) -> Optional[str]:
        """
        Returns the stmt_type parameter value for financial statement functions.

        Args:
            function: The gateway action function string.

        Returns:
            The stmt_type string, or None if the function is not a financial statement.
        """
        return self.STMT_TYPE_MAP.get(function)

    def get_supported_functions(self, provider: Any) -> list[str]:
        """
        Inspect a provider instance and return all functions it supports,
        based on declared supported_methods and method existence.

        Args:
            provider: A provider instance.

        Returns:
            List of function strings (e.g. ["ohlcv", "profile", "quote"]).
        """
        supported = []
        # Check universal map
        for function, method_name in self.UNIVERSAL_METHOD_MAP.items():
            if hasattr(provider, method_name):
                method = getattr(provider, method_name)
                # Exclude methods that just raise NotImplementedError
                try:
                    import inspect
                    src = inspect.getsource(method)
                    if "raise NotImplementedError" not in src:
                        supported.append(function)
                except (OSError, TypeError):
                    # Cannot read source (e.g. C extension), include it anyway
                    supported.append(function)
        return list(set(supported))


# Module-level singleton — import and use directly.
registry = ProviderCapabilityRegistry()
