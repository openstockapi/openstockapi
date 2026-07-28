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

# 9. Fetch Dividends
try:
    divs = osapi.cn_dividends("600519", provider="yahoo")
    print(f"\n9. CN Dividends (600519) (provider='yahoo'): Found {len(divs.get('dividends', []))} entries.")
except Exception as e:
    print(f"Error fetching dividends: {e}")

# 10. Fetch Splits
try:
    splits = osapi.cn_splits("600519", provider="yahoo")
    print(f"\n10. CN Splits (600519) (provider='yahoo'): Found {len(splits.get('splits', []))} entries.")
except Exception as e:
    print(f"Error fetching splits: {e}")


print("\n=== CN Stock Examples Completed ===")
