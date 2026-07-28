import re
from typing import Dict, Any, Optional

class ForexProfileProvider:
    # Mapping for main currency codes to FlagCDN country codes
    _CURRENCY_TO_COUNTRY = {
        "USD": "us",
        "EUR": "eu",
        "JPY": "jp",
        "GBP": "gb",
        "AUD": "au",
        "CAD": "ca",
        "CHF": "ch",
        "NZD": "nz",
        "VND": "vn",
        "CNY": "cn",
        "HKD": "hk",
        "SGD": "sg",
        "TRY": "tr",
        "MXN": "mx",
        "ZAR": "za",
        "SEK": "se",
        "NOK": "no",
        "RUB": "ru",
        "INR": "in",
        "KRW": "kr",
        "BRL": "br",
        "THB": "th",
        "MYR": "my",
        "IDR": "id",
        "PHP": "ph",
        "TWD": "tw",
    }

    _MAJORS = {"USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "NZD"}

    def get_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        # Normalize symbol: remove non-alphanumeric characters, e.g. "EUR/USD" -> "EURUSD"
        cleaned = re.sub(r'[^A-Za-z]', '', symbol).upper()
        if len(cleaned) != 6:
            return None
        
        base = cleaned[:3]
        quote = cleaned[3:]

        # Classify Forex category
        if base in self._MAJORS and quote in self._MAJORS:
            if base == "USD" or quote == "USD":
                category = "Majors"
            else:
                category = "Minors"
        else:
            category = "Exotics"

        # Generate flag logo URLs using FlagCDN
        base_country = self._CURRENCY_TO_COUNTRY.get(base, base[:2].lower())
        quote_country = self._CURRENCY_TO_COUNTRY.get(quote, quote[:2].lower())

        base_logo_url = f"https://flagcdn.com/w160/{base_country}.png"
        quote_logo_url = f"https://flagcdn.com/w160/{quote_country}.png"

        return {
            "symbol": cleaned,
            "base_currency": base,
            "quote_currency": quote,
            "base_logo_url": base_logo_url,
            "quote_logo_url": quote_logo_url,
            "category": category,
            "provider": "local"
        }
