import os
import sys
import openstockapi as osapi

print("=== Testing with real API Key from .env.local ===")

env_file = ".env.local"
if not os.path.exists(env_file):
    print("Error: .env.local not found!")
    sys.exit(1)

key = None
with open(env_file, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("OPENSTOCKAPI_KEY="):
            key = line.split("OPENSTOCKAPI_KEY=")[1].strip()
            os.environ["OPENSTOCKAPI_KEY"] = key
            break

if not key:
    print("Error: OPENSTOCKAPI_KEY not found in .env.local!")
    sys.exit(1)

print(f"Loaded key: {key}")

try:
    # Initialize session
    osapi.init(key)
    current_session = osapi.license.session.get_current_session()
    print(f"Session initialized successfully. Resolved Tier: {current_session.tier.value}")

    print("\n1. Testing Crypto OHLCV (Free tier API)...")
    crypto_data = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=3)
    print(f"Success! BTCUSDT last price: {crypto_data[-1]['close']} USD")

    print("\n2. Testing Forex Rates (Free tier API)...")
    forex_data = osapi.forex_rates(base="USD")
    print(f"Success! USD/VND: {forex_data['rates']['VND']}")

    print("\n3. Testing Crypto Depth (Requires PRO tier)...")
    try:
        depth_data = osapi.crypto_depth("BTCUSDT", limit=2)
        print(f"Success! Depth returned: {depth_data}")
    except Exception as e:
        print(f"Expected fail/restriction if key is Free: {e}")

except Exception as e:
    print(f"Error occurred during testing: {e}")
    sys.exit(1)
