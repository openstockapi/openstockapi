import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== US Stock Integration Examples ===")

# 3. Fetch Split Financial Statements (Annual)
try:
    bs = osapi.us_balance_sheet("AAPL", period="annual")
    print(f"\n3. US Balance Sheet (AAPL - Annual): Found {len(bs)} periods.")
    print(bs.head(1) if hasattr(bs, "head") else bs[:1])
except Exception as e:
    print(f"Error fetching Balance Sheet: {e}")

# 4. Fetch Split Financial Statements (Quarterly)
try:
    inc = osapi.us_income_statement("AAPL", period="quarter")
    print(f"\n4. US Income Statement (AAPL - Quarterly): Found {len(inc)} periods.")
    print(inc.head(1) if hasattr(inc, "head") else inc[:1])
except Exception as e:
    print(f"Error fetching Income Statement: {e}")


print("\n=== US Stock Examples Completed ===")
