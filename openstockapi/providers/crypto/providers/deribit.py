"""
DeribitProvider - Crypto Options & Derivatives Data Provider
Source: Deribit Public REST API v2 (No API key required for public endpoints)
API Docs: https://docs.deribit.com/#public-endpoints
"""
import httpx
import json
from typing import List, Dict, Any, Optional
from openstockapi.providers.crypto.base import CryptoBaseProvider


class DeribitProvider(CryptoBaseProvider):
    """
    Provider for Deribit crypto options and derivatives data.
    Uses public endpoints - no authentication required.
    """

    BASE_URL = "https://www.deribit.com/api/v2/public"

    # ─── Abstract method stubs (Required by CryptoBaseProvider) ─────────────
    async def get_tickers(self) -> List[Dict[str, Any]]:
        """Not primary use-case for Deribit. Returns empty list."""
        return []

    async def get_depth(self, symbol: str, limit: int = 20) -> Optional[Dict[str, Any]]:
        """Not primary use-case for Deribit. Returns None."""
        return None

    async def get_footprint(self, symbol: str, timeframe: str = "5min", limit: int = 50) -> Optional[Dict[str, Any]]:
        """Not primary use-case for Deribit. Returns None."""
        return None

    # ─── Deribit-specific methods ────────────────────────────────────────────

    async def get_instruments(self, currency: str = "BTC", kind: str = "option") -> List[Dict[str, Any]]:
        """
        Retrieves all active instruments for a given currency and kind.
        
        Args:
            currency: "BTC" or "ETH"
            kind: "option", "future", "spot"
        
        Returns:
            List of instrument definitions including strike, expiry, option_type, etc.
        """
        url = f"{self.BASE_URL}/get_instruments"
        params = {
            "currency": currency.upper(),
            "kind": kind,
            "expired": "false"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("result"):
                        instruments = data["result"]
                        # Normalize key fields
                        return [
                            {
                                "instrument_name": inst.get("instrument_name"),
                                "currency": inst.get("base_currency"),
                                "kind": inst.get("kind"),
                                "strike": inst.get("strike"),
                                "expiration_timestamp": inst.get("expiration_timestamp"),
                                "option_type": inst.get("option_type"),  # "call" or "put"
                                "is_active": inst.get("is_active"),
                            }
                            for inst in instruments
                        ]
        except Exception as e:
            pass
        return []

    async def get_options_chain(self, currency: str = "BTC") -> List[Dict[str, Any]]:
        """
        Retrieves a full options chain (summary for all active option contracts).
        Shows IV, mark_price, greeks for each strike price.
        
        Args:
            currency: "BTC" or "ETH"
        
        Returns:
            List of option contracts with bid/ask, IV, Greeks.
        """
        url = f"{self.BASE_URL}/get_book_summary_by_currency"
        params = {
            "currency": currency.upper(),
            "kind": "option"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("result"):
                        chain = data["result"]
                        return [
                            {
                                "instrument_name": item.get("instrument_name"),
                                "underlying_price": item.get("underlying_price"),
                                "mark_price": item.get("mark_price"),
                                "bid_price": item.get("bid_price"),
                                "ask_price": item.get("ask_price"),
                                "mark_iv": item.get("mark_iv"),         # Implied Volatility
                                "bid_iv": item.get("bid_iv"),
                                "ask_iv": item.get("ask_iv"),
                                "volume": item.get("volume"),
                                "open_interest": item.get("open_interest"),
                                "creation_timestamp": item.get("creation_timestamp"),
                            }
                            for item in chain
                        ]
        except Exception as e:
            pass
        return []

    async def get_options_ticker(self, instrument_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed ticker for a single option contract, including Greeks.
        
        Args:
            instrument_name: e.g. "BTC-25JUL25-100000-C" (format: CURRENCY-DDMMMYY-STRIKE-TYPE)
        
        Returns:
            Detailed ticker with Greeks (Delta, Gamma, Theta, Vega), IV, mark price.
        """
        url = f"{self.BASE_URL}/ticker"
        params = {"instrument_name": instrument_name}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("result"):
                        ticker = data["result"]
                        greeks = ticker.get("greeks", {})
                        return {
                            "instrument_name": ticker.get("instrument_name"),
                            "underlying_index": ticker.get("underlying_index"),
                            "underlying_price": ticker.get("underlying_price"),
                            "mark_price": ticker.get("mark_price"),
                            "mark_iv": ticker.get("mark_iv"),           # Implied Volatility (%)
                            "bid_price": ticker.get("best_bid_price"),
                            "ask_price": ticker.get("best_ask_price"),
                            "last_price": ticker.get("last_price"),
                            "volume": ticker.get("stats", {}).get("volume"),
                            "open_interest": ticker.get("open_interest"),
                            "settlement_price": ticker.get("settlement_price"),
                            "timestamp": ticker.get("timestamp"),
                            "greeks": {
                                "delta": greeks.get("delta"),    # Rate of change vs. underlying price
                                "gamma": greeks.get("gamma"),    # Rate of change of delta
                                "theta": greeks.get("theta"),    # Time decay per day
                                "vega": greeks.get("vega"),      # Sensitivity to volatility
                                "rho": greeks.get("rho"),        # Sensitivity to interest rate
                            },
                        }
        except Exception as e:
            pass
        return None
