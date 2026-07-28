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

print("=== CN Stock Integration Examples ===")

# 1. Fetch Symbols
try:
    symbols = osapi.cn_symbols(provider="sina")
    print(f"\n1. CN Symbols (provider='sina'): Found {len(symbols)} symbols.")
    print(f"   Example symbols: {symbols[:5]}")
except Exception as e:
    print(f"Error fetching symbols: {e}")

# 2. Fetch OHLCV
try:
    ohlcv = osapi.cn_ohlcv("600519", range="5d", interval="1h", provider="yahoo")
    print(f"\n2. CN OHLCV (600519) (provider='yahoo'): Found {len(ohlcv)} bars.")
    print(ohlcv.head(2) if hasattr(ohlcv, "head") else ohlcv[:2])
except Exception as e:
    print(f"Error fetching OHLCV: {e}")

# 3. Fetch Profile
try:
    profile = osapi.cn_profile("600519", provider="sina")
    print(f"\n3. CN Profile (600519) (provider='sina'):")
    try:
        print(f"   Name: {profile.get('company_name')}")
    except UnicodeEncodeError:
        print(f"   Name: {profile.get('company_name').encode('ascii', errors='backslashreplace').decode('ascii')}")
    print(f"   Industry: {profile.get('industry')}")
except Exception as e:
    print(f"Error fetching profile: {e}")

# 11. Fetch Realtime Quote (Requires Pro Tier)
try:
    quote = osapi.cn_quote("600519", provider="tencent")
    print(f"\n11. CN Quote (600519) (provider='tencent'): Price: {quote.get('price')}")
except Exception as e:
    print(f"Error fetching quote: {e}")

# 12. Fetch Order Book (Requires Pro Tier)
try:
    book = osapi.cn_order_book("600519", provider="tencent")
    print(f"\n12. CN Order Book (600519) (provider='tencent'): Asks: {len(book.get('asks', []))}, Bids: {len(book.get('bids', []))}")
except Exception as e:
    print(f"Error fetching order book: {e}")

# 13. Fetch Ticks (Requires Pro Tier)
try:
    ticks = osapi.cn_tick("600519", provider="tencent")
    print(f"\n13. CN Ticks (600519) (provider='tencent'): Found {len(ticks)} ticks.")
except Exception as e:
    print(f"Error fetching ticks: {e}")


print("\n=== CN Stock Examples Completed ===")
