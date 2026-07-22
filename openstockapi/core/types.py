from enum import Enum

class DataTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"
