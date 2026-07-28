import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== ASX Integration Examples ===")

# 6. Fetch Dividends
try:
    divs = osapi.asx_dividends("BHP")
    print(f"\n6. ASX Dividends (BHP): Found {len(divs.get('dividends', []))} entries.")
except Exception as e:
    print(f"Error fetching dividends: {e}")

# 7. Fetch News
try:
    news = osapi.asx_news("BHP")
    print(f"\n7. ASX News (BHP): Found {len(news.get('news', []))} entries.")
except Exception as e:
    print(f"Error fetching news: {e}")


print("\n=== ASX Examples Completed ===")
