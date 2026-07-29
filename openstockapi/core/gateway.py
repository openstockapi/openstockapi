import logging
from typing import Any, Optional, Dict, List
from openstockapi.core.types import DataTier
from openstockapi.core.security import enforce_tier_and_rate_limit
from openstockapi.config.settings import get_default_providers
from openstockapi.providers import get_provider
from openstockapi.core.exceptions import ProviderUnavailableError

logger = logging.getLogger("openstockapi.gateway")

class RequestGateway:
    """Unified Request Gateway for client API routing, security checks, and provider dispatching."""

    def execute(self, action: str, market: str, required_tier: DataTier, **params) -> Any:
        """Executes an action by validating license, resolving provider, and invoking it.

        Args:
            action: Dot-separated action name, e.g. "stock.quote", "crypto.depth".
            market: The market/country code, e.g. "VN", "US", "global".
            required_tier: The authorization tier required for this action.
            **params: Keyword arguments passed to the provider method.
        """
        # 1. Standardize action name for server validation
        asset_class, function = action.split(".", 1)
        market_code = market.lower()
        action_name = f"{asset_class}.{market_code}.{function}"

        # 2. Server-side / local fallback handshake validation
        enforce_tier_and_rate_limit(required_tier, action_name)

        # 3. Resolve providers to try
        explicit_provider = params.pop("provider", None)
        from openstockapi.providers import PROVIDERS
        
        # Translate business function names to config priority categories
        category_map = {
            "balance_sheet": "financials",
            "income_statement": "financials",
            "cashflow": "financials",
            "ratios": "financials",
            "order_book": "orderbook",
            "ticks": "orderbook",
            "macro_indicators": "macro",
            "fund_details": "fund",
            "company_news": "news",
            "company_events": "events",
            "simulate": "leverage",
            "options_instruments": "options",
            "options_chain": "options",
            "options_ticker": "options",
        }
        endpoint_category = category_map.get(function, function)
        
        # When market is 'global', resolve the priority config key using the asset class
        resolved_market = market
        if market.lower() == "global":
            resolved_market = asset_class.upper()  # e.g., "CRYPTO" or "FOREX"

        # Special case: VN heatmap always routes through 'core' (which delegates to vn_heatmap_service).
        # The user-supplied provider ('tradingview', 'kbs', 'vci') is a sub-provider selection,
        # not a top-level PROVIDERS key, so pass it as a kwarg.
        _vn_heatmap_sub_providers = {"tradingview", "kbs", "vci", "tv"}
        _is_vn_heatmap = (function == "heatmap" and market_code == "vn")

        if explicit_provider:
            if _is_vn_heatmap or explicit_provider.lower() not in PROVIDERS:
                # Pass as sub-provider kwarg; let the default provider (core) handle dispatch
                params["provider"] = explicit_provider
                providers_to_try = get_default_providers(endpoint_category, resolved_market)
            else:
                providers_to_try = [explicit_provider]
        else:
            providers_to_try = get_default_providers(endpoint_category, resolved_market)

        if not providers_to_try:
            raise ProviderUnavailableError(f"No providers configured for category '{endpoint_category}' in market '{resolved_market}'.")

        # 4. Dispatch call to resolved provider
        last_err = None
        for p_name in providers_to_try:
            p_inst = get_provider(p_name)
            if not p_inst:
                continue
            try:
                result = self._dispatch_to_provider(p_inst, function, asset_class, market=market_code, **params)
                # Apply market and asset_class metadata dynamically to standard models
                self._apply_metadata(result, market_code, asset_class)
                return result
            except Exception as e:
                logger.warning(f"Provider '{p_name}' failed to execute '{action}': {e}")
                last_err = e
                continue

        raise ProviderUnavailableError(
            f"All providers ({', '.join(providers_to_try)}) failed to execute '{action}' (market={market}): {last_err}"
        )

    def _dispatch_to_provider(self, provider: Any, /, function: str, asset_class: str, market: str = "vn", **params) -> Any:
        """Routes the standardized action function to the provider's concrete method."""
        method_name = None
        if asset_class == "crypto" and function == "ohlcv":
            method_name = "get_crypto_ohlcv"
        elif asset_class == "crypto" and function == "profile":
            method_name = "get_crypto_profile"
        elif asset_class == "forex" and function == "ohlcv":
            method_name = "get_forex_ohlcv"
        elif asset_class == "forex" and function == "profile":
            method_name = "get_forex_profile"
        elif asset_class == "crypto" and function == "symbols":
            method_name = "get_crypto_symbols"
        elif asset_class == "forex" and function == "symbols":
            method_name = "get_forex_symbols"
        elif asset_class == "crypto" and function == "news":
            method_name = "get_crypto_news"
        elif asset_class == "forex" and function == "news":
            method_name = "get_forex_news"
        elif asset_class == "crypto" and function == "events":
            method_name = "get_crypto_events"
        elif asset_class == "forex" and function == "events":
            method_name = "get_forex_events"
        elif asset_class == "crypto" and function == "heatmap":
            method_name = "get_crypto_heatmap"
        elif asset_class == "stock" and market.lower() == "au":
            method_name = f"get_asx_{function}"
        elif asset_class == "stock" and market.lower() == "us":
            method_name = f"get_us_{function}"
        elif asset_class == "stock" and market.lower() == "jp":
            method_name = f"get_jp_{function}"
        elif asset_class == "stock" and market.lower() == "cn":
            method_name = f"get_cn_{function}"
        elif asset_class == "stock" and market.lower() == "hk":
            method_name = f"get_hk_{function}"
        elif asset_class == "stock" and market.lower() == "vn":
            method_name = f"get_vn_{function}"

        if not method_name:
            method_map = {
                "ohlcv": "get_ohlcv",
                "profile": "get_company_profile",
                "derivative_profile": "get_derivative_profile",
                "quote": "get_realtime_quote",
                "balance_sheet": "get_financial_statements",
                "income_statement": "get_financial_statements",
                "cashflow": "get_financial_statements",
                "ratios": "get_financial_statements",
                "order_book": "get_order_book",
                "ticks": "get_intraday_ticks",
                "foreign_trade": "get_foreign_trading",
                "insider_trade": "get_insider_trading",
                "prop_trade": "get_prop_trading",
                "macro_indicators": "get_macro_indicators",
                "fund_details": "get_fund_details",
                "market_index": "get_market_index",
                "company_news": "get_company_news",
                "company_events": "get_company_events",
                # Crypto specific
                "depth": "get_crypto_depth",
                "derivatives": "get_crypto_derivatives",
                "footprint": "get_crypto_footprint",
                "simulate": "simulate_crypto_leverage",
                "symbols": "get_crypto_symbols",
                "tickers": "get_crypto_tickers",
                "options_instruments": "get_crypto_options_instruments",
                "options_chain": "get_crypto_options_chain",
                "options_ticker": "get_crypto_options_ticker",
                "news": "get_crypto_news",
                "events": "get_crypto_events",
                # Forex specific
                "rates": "get_forex_rates",
                "compare": "compare_forex_rates",
                "commodities": "get_commodities_prices",
                "indices_etf": "get_global_indices_etf",
            }
            method_name = method_map.get(function)

        # Override method lookup if category mapping is not direct
        if function in ("balance_sheet", "income_statement", "cashflow", "ratios"):
            stmt_type_map = {
                "balance_sheet": "balance",
                "income_statement": "income",
                "cashflow": "cashflow",
                "ratios": "ratios",
            }
            params["stmt_type"] = stmt_type_map[function]

        if not method_name or not hasattr(provider, method_name):
            # Check for direct naming fallback (e.g. get_forex_symbols for symbols)
            if function == "symbols" and hasattr(provider, "get_forex_symbols"):
                method_name = "get_forex_symbols"
            elif function == "news" and hasattr(provider, "get_forex_news"):
                method_name = "get_forex_news"
            elif function == "events" and hasattr(provider, "get_forex_events"):
                method_name = "get_forex_events"
            elif hasattr(provider, f"get_{function}"):
                method_name = f"get_{function}"
            else:
                raise NotImplementedError(f"Provider '{provider.name}' does not implement '{function}' ({method_name}).")

        import inspect
        method = getattr(provider, method_name)
        
        # Translate from_date and resolution to range and interval for Yahoo/global stock providers
        sig = inspect.signature(method)
        if "range" in sig.parameters and "interval" in sig.parameters:
            if "from_date" in params and "range" not in params:
                from datetime import datetime
                try:
                    start_dt = datetime.strptime(params["from_date"], "%Y-%m-%d")
                    days = (datetime.now() - start_dt).days
                    if days <= 5:
                        params["range"] = "5d"
                    elif days <= 30:
                        params["range"] = "1mo"
                    elif days <= 90:
                        params["range"] = "3mo"
                    elif days <= 180:
                        params["range"] = "6mo"
                    elif days <= 365:
                        params["range"] = "1y"
                    elif days <= 365 * 2:
                        params["range"] = "2y"
                    elif days <= 365 * 5:
                        params["range"] = "5y"
                    elif days <= 365 * 10:
                        params["range"] = "10y"
                    else:
                        params["range"] = "max"
                except Exception:
                    params["range"] = "max"
            if "resolution" in params and "interval" not in params:
                res = params["resolution"]
                res_lower = res.lower() if res else ""
                if res_lower in ("d", "1d"):
                    params["interval"] = "1d"
                elif res_lower in ("w", "1w"):
                    params["interval"] = "1wk"
                elif res_lower in ("m", "1m"):
                    params["interval"] = "1mo"
                else:
                    params["interval"] = res

        # Inspect signature again with updated params
        sig = inspect.signature(method)
        has_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        if has_kwargs:
            filtered_params = params
        else:
            filtered_params = {k: v for k, v in params.items() if k in sig.parameters}
        return method(**filtered_params)

    def _apply_metadata(self, result: Any, market: str, asset_class: str) -> None:
        """Injects standardized market and asset_class values into the output models/lists."""
        if result is None:
            return
        if isinstance(result, list):
            for item in result:
                self._apply_item_metadata(item, market, asset_class)
        elif isinstance(result, dict) and "data" in result:
            # Handle standardized wrappers (e.g., news/events responses)
            data = result["data"]
            if isinstance(data, list):
                for item in data:
                    self._apply_item_metadata(item, market, asset_class)
            else:
                self._apply_item_metadata(data, market, asset_class)
        else:
            self._apply_item_metadata(result, market, asset_class)

    def _apply_item_metadata(self, item: Any, market: str, asset_class: str) -> None:
        """Applies metadata to a single object or dictionary."""
        if hasattr(item, "__dict__") or hasattr(item, "model_fields"):
            # Pydantic or object
            if hasattr(item, "market"):
                item.market = market
            if hasattr(item, "asset_class"):
                if getattr(item, "asset_class", "stock") == "stock":
                    item.asset_class = asset_class
        elif isinstance(item, dict):
            item["market"] = market
            if item.get("asset_class", "stock") == "stock":
                item["asset_class"] = asset_class

# Global instance of the gateway
gateway = RequestGateway()
