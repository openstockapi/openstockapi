import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== US Stock Integration Examples ===")

# 1. Fetch OHLCV
try:
    ohlcv = osapi.us_ohlcv("AAPL", range="5d", interval="1h")
    print(f"\n1. US OHLCV (AAPL): Found {len(ohlcv)} bars.")
    print(ohlcv.head(2) if hasattr(ohlcv, "head") else ohlcv[:2])
except Exception as e:
    print(f"Error fetching OHLCV: {e}")

# 2. Fetch Profile
try:
    profile = osapi.us_profile("AAPL")
    print(f"\n2. US Profile (AAPL):")
    print(f"   Name: {profile.get('company_name')}")
    print(f"   Industry: {profile.get('industry')}")
except Exception as e:
    print(f"Error fetching profile: {e}")


print("\n=== US Stock Examples Completed ===")
