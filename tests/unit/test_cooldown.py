import time
import pytest
from openstockapi.core.cooldown import is_cooling, set_cooldown

def test_cooldown_flow():
    # Initially not cooling
    assert not is_cooling("test_provider")
    
    # Set cooldown for 2 seconds
    set_cooldown("test_provider", 2.0)
    assert is_cooling("test_provider")
    
    # Wait for expiry
    time.sleep(2.1)
    assert not is_cooling("test_provider")
