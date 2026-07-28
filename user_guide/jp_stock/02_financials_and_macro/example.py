import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== JP Stock Integration Examples ===")

# 4. Fetch Financials
try:
    financials = osapi.jp_financials("7203", period="annual")
    print(f"\n4. JP Financials (7203): available periods: {financials.get('available_periods')}")
except Exception as e:
    print(f"Error fetching financials: {e}")

# 5. Fetch Split Financial Statements (Annual Balance Sheet)
try:
    bs = osapi.jp_balance_sheet("7203", period="annual")
    print(f"\n5. JP Balance Sheet (7203 - Annual): Found {len(bs)} periods.")
    print(bs.head(1) if hasattr(bs, "head") else bs[:1])
except Exception as e:
    print(f"Error fetching Balance Sheet: {e}")

# 6. Fetch Split Financial Statements (Quarterly Income Statement)
try:
    inc = osapi.jp_income_statement("7203", period="quarter")
    print(f"\n6. JP Income Statement (7203 - Quarterly): Found {len(inc)} periods.")
    print(inc.head(1) if hasattr(inc, "head") else inc[:1])
except Exception as e:
    print(f"Error fetching Income Statement: {e}")

# 7. Fetch Split Financial Statements (Annual Cash Flow)
try:
    cf = osapi.jp_cashflow("7203", period="annual")
    print(f"\n7. JP Cashflow (7203 - Annual): Found {len(cf)} periods.")
    print(cf.head(1) if hasattr(cf, "head") else cf[:1])
except Exception as e:
    print(f"Error fetching Cashflow: {e}")

# 8. Fetch Ratios
try:
    ratios = osapi.jp_ratios("7203")
    print(f"\n8. JP Ratios (7203): PE: {ratios.get('ratios', {}).get('pe_trailing')}")
except Exception as e:
    print(f"Error fetching ratios: {e}")


print("\n=== JP Stock Examples Completed ===")
