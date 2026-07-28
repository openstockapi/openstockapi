import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== ASX Integration Examples ===")

# 1. Fetch symbols
try:
    symbols = osapi.asx_symbols()
    print(f"\n1. ASX Symbols: Found {len(symbols)} symbols. Example: {symbols[:5]}")
except Exception as e:
    print(f"Error fetching symbols: {e}")

# 2. Fetch OHLCV
try:
    ohlcv = osapi.asx_ohlcv("BHP", range="5d", interval="1h")
    print(f"\n2. ASX OHLCV (BHP): Found {len(ohlcv)} bars.")
    print(ohlcv.head(2) if hasattr(ohlcv, "head") else ohlcv[:2])
except Exception as e:
    print(f"Error fetching OHLCV: {e}")

# 3. Fetch Profile
try:
    profile = osapi.asx_profile("BHP")
    print(f"\n3. ASX Profile (BHP):")
    print(f"   Name: {profile.get('company_name')}")
    print(f"   Industry: {profile.get('industry')}")
except Exception as e:
    print(f"Error fetching profile: {e}")


print("\n=== ASX Examples Completed ===")
