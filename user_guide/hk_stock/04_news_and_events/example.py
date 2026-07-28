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

# 7. Fetch Dividends
try:
    divs = osapi.hk_dividends("0700", provider="yahoo")
    print(f"\n7. HK Dividends (0700) (provider='yahoo'): Found {len(divs.get('dividends', []))} entries.")
except Exception as e:
    print(f"Error fetching dividends: {e}")

# 8. Fetch Splits
try:
    splits = osapi.hk_splits("0700", provider="yahoo")
    print(f"\n8. HK Splits (0700) (provider='yahoo'): Found {len(splits.get('splits', []))} entries.")
except Exception as e:
    print(f"Error fetching splits: {e}")

# 9. Fetch Calendar
try:
    calendar = osapi.hk_calendar("0700", provider="yahoo")
    print(f"\n9. HK Calendar (0700) (provider='yahoo'): Earnings Date: {calendar.get('calendar', {}).get('Earnings Date')}")
except Exception as e:
    print(f"Error fetching calendar: {e}")

# 10. Fetch News
try:
    news = osapi.hk_news("0700", provider="google_news")
    print(f"\n10. HK News (0700) (provider='google_news'): Found {len(news.get('news', []))} entries.")
except Exception as e:
    print(f"Error fetching news: {e}")


print("\n=== HK Stock Examples Completed ===")
