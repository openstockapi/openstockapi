import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== ASX Integration Examples ===")

# 4. Fetch Split Financial Statements (Annual)
try:
    bs = osapi.asx_balance_sheet("BHP", period="annual")
    print(f"\n4. ASX Balance Sheet (BHP - Annual): Found {len(bs)} periods.")
    print(bs.head(1) if hasattr(bs, "head") else bs[:1])
except Exception as e:
    print(f"Error fetching Balance Sheet: {e}")

# 5. Fetch Split Financial Statements (Quarterly)
try:
    inc = osapi.asx_income_statement("BHP", period="quarter")
    print(f"\n5. ASX Income Statement (BHP - Quarterly): Found {len(inc)} periods.")
    print(inc.head(1) if hasattr(inc, "head") else inc[:1])
except Exception as e:
    print(f"Error fetching Income Statement: {e}")


print("\n=== ASX Examples Completed ===")
