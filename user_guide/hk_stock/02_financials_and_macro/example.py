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

# 3. Fetch Split Financial Statements (Annual Balance Sheet)
try:
    bs = osapi.hk_balance_sheet("0700", period="annual", provider="yahoo")
    print(f"\n3. HK Balance Sheet (0700 - Annual) (provider='yahoo'): Found {len(bs)} periods.")
    print(bs.head(1) if hasattr(bs, "head") else bs[:1])
except Exception as e:
    print(f"Error fetching Balance Sheet: {e}")

# 4. Fetch Split Financial Statements (Quarterly Income Statement)
try:
    inc = osapi.hk_income_statement("0700", period="quarter", provider="yahoo")
    print(f"\n4. HK Income Statement (0700 - Quarterly) (provider='yahoo'): Found {len(inc)} periods.")
    print(inc.head(1) if hasattr(inc, "head") else inc[:1])
except Exception as e:
    print(f"Error fetching Income Statement: {e}")

# 5. Fetch Split Financial Statements (Annual Cash Flow)
try:
    cf = osapi.hk_cashflow("0700", period="annual", provider="yahoo")
    print(f"\n5. HK Cashflow (0700 - Annual) (provider='yahoo'): Found {len(cf)} periods.")
    print(cf.head(1) if hasattr(cf, "head") else cf[:1])
except Exception as e:
    print(f"Error fetching Cashflow: {e}")

# 6. Fetch Financial Ratios
try:
    ratios = osapi.hk_ratios("0700", provider="yahoo")
    print(f"\n6. HK Ratios (0700) (provider='yahoo'): {ratios.get('ratios')}")
except Exception as e:
    print(f"Error fetching ratios: {e}")


print("\n=== HK Stock Examples Completed ===")
