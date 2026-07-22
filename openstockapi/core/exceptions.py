class OpenStockAPIError(Exception):
    """Base exception for all OpenStockAPI errors."""
    pass

class ProviderUnavailableError(OpenStockAPIError):
    """Raised when a data provider is down or fails to respond."""
    pass

class RateLimitError(OpenStockAPIError):
    """Raised when the rate limit for the tier is exceeded."""
    pass

class SymbolNotFoundError(OpenStockAPIError):
    """Raised when a ticker symbol is not found."""
    pass

class DataParseError(OpenStockAPIError):
    """Raised when parsing data from provider fails."""
    pass

class TierUpgradeRequiredError(OpenStockAPIError):
    """Raised when a free user calls a paid endpoint."""
    def __init__(self, required_tier: str, endpoint: str):
        self.required_tier = required_tier
        self.endpoint = endpoint
        super().__init__(
            f"Endpoint '{endpoint}' requires '{required_tier}' tier or above. "
            f"Please upgrade your tier to access this data."
        )

class ApiKeyRequiredError(OpenStockAPIError):
    """Raised when no API key is provided. All tiers require registration."""
    def __init__(self):
        super().__init__(
            "An API key is required to use OpenStockAPI. "
            "Register for a free key at: https://openstockapi.com/register "
            "then call: osapi.init('free_YOUR_KEY') before making any requests."
        )
