import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== JP Stock Integration Examples ===")

# 9. Fetch Dividends
try:
    divs = osapi.jp_dividends("7203")
    print(f"\n9. JP Dividends (7203): Found {len(divs.get('dividends', []))} entries.")
except Exception as e:
    print(f"Error fetching dividends: {e}")

# 10. Fetch Splits
try:
    splits = osapi.jp_splits("7203")
    print(f"\n10. JP Splits (7203): Found {len(splits.get('splits', []))} entries.")
except Exception as e:
    print(f"Error fetching splits: {e}")

# 11. Fetch Calendar
try:
    calendar = osapi.jp_calendar("7203")
    print(f"\n11. JP Calendar (7203): Earnings Date: {calendar.get('calendar', {}).get('Earnings Date')}")
except Exception as e:
    print(f"Error fetching calendar: {e}")

# 12. Fetch News
try:
    news = osapi.jp_news("7203")
    print(f"\n12. JP News (7203): Found {len(news.get('news', []))} entries.")
except Exception as e:
    print(f"Error fetching news: {e}")


print("\n=== JP Stock Examples Completed ===")
