from enum import Enum

class DataTier(str, Enum):
    FREE = "free"
    COMMUNITY = "community"
    PRO = "pro"
    PREMIUM = "premium"
