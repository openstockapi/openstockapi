class OpenStockAPIError(Exception):
    """Base exception for all OpenStockAPI errors."""
    pass

class ProviderUnavailableError(OpenStockAPIError):
    """Raised when a data provider is down or fails to respond."""
    pass

class RateLimitError(OpenStockAPIError):
    """Raised when the rate limit for the tier is exceeded."""
    def __init__(self, error_code: str, tier: str, limit: int, retry_after_seconds: int) -> None:
        self.error_code = error_code
        self.tier = tier
        self.limit = limit
        self.retry_after_seconds = retry_after_seconds
        
        if tier == "free":
            msg = (
                f"We're sorry, but you have reached the Free tier rate limit ({limit} req/min). "
                f"To enjoy higher limits, please log in or register at https://openstockapi.com/console to obtain an API key. "
                f"(You can retry in {retry_after_seconds}s)"
            )
        else:
            msg = (
                f"You have reached the rate limit for the '{tier}' tier ({limit} req/min). "
                f"To increase your limits and ensure uninterrupted service, please visit https://openstockapi.com/console to upgrade your plan. "
                f"(You can retry in {retry_after_seconds}s)"
            )
        self.message = msg
        super().__init__(msg)

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

class RateLimitExceededError(OpenStockAPIError):
    """Raised when the server-side rate limit for a tier is exceeded."""
    def __init__(self, tier: str, endpoint: str):
        self.tier = tier
        self.endpoint = endpoint
        if tier == "free":
            msg = (
                f"We're sorry, but you have reached the Free tier rate limit while calling '{endpoint}'. "
                f"Please log in or register at https://openstockapi.com/console to obtain an API key for higher limits."
            )
        else:
            msg = (
                f"You have reached the rate limit for the '{tier}' tier while calling '{endpoint}'. "
                f"Please wait a moment or visit https://openstockapi.com/console to upgrade your plan for higher limits."
            )
        super().__init__(msg)
