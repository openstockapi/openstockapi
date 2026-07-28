import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== JP Stock Integration Examples ===")

# 1. Fetch Symbols
try:
    symbols = osapi.jp_symbols()
    print(f"\n1. JP Symbols: Found {len(symbols)} symbols.")
    print(f"   Example symbols: {symbols[:5]}")
except Exception as e:
    print(f"Error fetching symbols: {e}")

# 2. Fetch OHLCV
try:
    ohlcv = osapi.jp_ohlcv("7203", range="5d", interval="1h")
    print(f"\n2. JP OHLCV (7203): Found {len(ohlcv)} bars.")
    print(ohlcv.head(2) if hasattr(ohlcv, "head") else ohlcv[:2])
except Exception as e:
    print(f"Error fetching OHLCV: {e}")

# 3. Fetch Profile
try:
    profile = osapi.jp_profile("7203")
    print(f"\n3. JP Profile (7203):")
    print(f"   Name: {profile.get('company_name')}")
    print(f"   Industry: {profile.get('industry')}")
except Exception as e:
    print(f"Error fetching profile: {e}")


print("\n=== JP Stock Examples Completed ===")
