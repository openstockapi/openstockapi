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

# 4. Fetch Financials
try:
    financials = osapi.cn_financials("600519", period="annual", provider="yahoo")
    print(f"\n4. CN Financials (600519) (provider='yahoo'): available periods: {financials.get('available_periods')}")
except Exception as e:
    print(f"Error fetching financials: {e}")

# 5. Fetch Split Financial Statements (Annual Balance Sheet)
try:
    bs = osapi.cn_balance_sheet("600519", period="annual", provider="yahoo")
    print(f"\n5. CN Balance Sheet (600519 - Annual) (provider='yahoo'): Found {len(bs)} periods.")
    print(bs.head(1) if hasattr(bs, "head") else bs[:1])
except Exception as e:
    print(f"Error fetching Balance Sheet: {e}")

# 6. Fetch Split Financial Statements (Quarterly Income Statement)
try:
    inc = osapi.cn_income_statement("600519", period="quarter", provider="yahoo")
    print(f"\n6. CN Income Statement (600519 - Quarterly) (provider='yahoo'): Found {len(inc)} periods.")
    print(inc.head(1) if hasattr(inc, "head") else inc[:1])
except Exception as e:
    print(f"Error fetching Income Statement: {e}")

# 7. Fetch Split Financial Statements (Annual Cash Flow)
try:
    cf = osapi.cn_cashflow("600519", period="annual", provider="yahoo")
    print(f"\n7. CN Cashflow (600519 - Annual) (provider='yahoo'): Found {len(cf)} periods.")
    print(cf.head(1) if hasattr(cf, "head") else cf[:1])
except Exception as e:
    print(f"Error fetching Cashflow: {e}")

# 8. Fetch Ratios
try:
    ratios = osapi.cn_ratios("600519", provider="yahoo")
    print(f"\n8. CN Ratios (600519) (provider='yahoo'): PE: {ratios.get('ratios', {}).get('pe_trailing')}")
except Exception as e:
    print(f"Error fetching ratios: {e}")


print("\n=== CN Stock Examples Completed ===")
