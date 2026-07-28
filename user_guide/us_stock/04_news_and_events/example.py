import openstockapi as osapi
from openstockapi.license.session import set_current_session
import os

# Initialize session
api_key = os.getenv("OPENSTOCKAPI_API_KEY", "premium_sample_key")
set_current_session(api_key)

print("=== US Stock Integration Examples ===")

# 5. Fetch Dividends
try:
    divs = osapi.us_dividends("AAPL")
    print(f"\n5. US Dividends (AAPL): Found {len(divs.get('dividends', []))} entries.")
except Exception as e:
    print(f"Error fetching dividends: {e}")

# 6. Fetch Splits
try:
    splits = osapi.us_splits("AAPL")
    print(f"\n6. US Splits (AAPL): Found {len(splits.get('splits', []))} entries.")
except Exception as e:
    print(f"Error fetching splits: {e}")

# 7. Fetch Calendar
try:
    calendar = osapi.us_calendar("AAPL")
    print(f"\n7. US Calendar (AAPL): Dividend Date: {calendar.get('calendar', {}).get('Dividend Date')}")
except Exception as e:
    print(f"Error fetching calendar: {e}")

# 8. Fetch News
try:
    news = osapi.us_news("AAPL")
    print(f"\n8. US News (AAPL): Found {len(news.get('news', []))} entries.")
except Exception as e:
    print(f"Error fetching news: {e}")


print("\n=== US Stock Examples Completed ===")
