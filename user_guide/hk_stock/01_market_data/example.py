import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== HK Stock Integration Examples ===")

# 1. Fetch OHLCV
try:
    ohlcv = osapi.hk_ohlcv("0700", range="5d", interval="1h", provider="yahoo")
    print(f"\n1. HK OHLCV (0700) (provider='yahoo'): Found {len(ohlcv)} bars.")
    print(ohlcv.head(2) if hasattr(ohlcv, "head") else ohlcv[:2])
except Exception as e:
    print(f"Error fetching OHLCV: {e}")

# 2. Fetch Profile
try:
    profile = osapi.hk_profile("0700", provider="yahoo")
    print(f"\n2. HK Profile (0700) (provider='yahoo'):")
    print(f"   Name: {profile.get('company_name')}")
    print(f"   Industry: {profile.get('industry')}")
except Exception as e:
    print(f"Error fetching profile: {e}")


print("\n=== HK Stock Examples Completed ===")
