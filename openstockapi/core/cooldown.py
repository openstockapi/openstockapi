import time
from typing import Dict

_cooldowns: Dict[str, float] = {}

def set_cooldown(provider_name: str, duration: float = 60.0) -> None:
    """Sets a cooldown period for a provider in seconds to avoid calling it."""
    _cooldowns[provider_name] = time.time() + duration

def is_cooling(provider_name: str) -> bool:
    """Checks if a provider is currently in its cooldown cooling period."""
    expiry = _cooldowns.get(provider_name, 0.0)
    return time.time() < expiry
