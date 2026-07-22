import openstockapi as ostk
import json
import sys
import io

# Setup UTF-8 console output for Windows to handle Vietnamese characters
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8", line_buffering=True)


# Initialize with PRO key to bypass rate limits & tier checks for testing
ostk.license.session.init("pro_demokey")

print("--- Testing Company Profile (VNDIRECT) ---")
try:
    profile = ostk.profile("VNM")
    print(json.dumps(profile, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error fetching profile: {e}")

print("\n--- Testing Financial Balance Sheet (MAS) ---")
try:
    balances = ostk.balance_sheet("VNM", period="Q")
    # balance_sheet returns list of dicts (or DataFrame if pandas installed)
    # Print the first item or sample info
    if hasattr(balances, "head"): # DataFrame
        print(balances.head(2))
    else:
        print(balances[:1])
except Exception as e:
    print(f"Error fetching balance sheet: {e}")

print("\n--- Testing OHLCV History (DNSE) ---")
try:
    history = ostk.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-02-01")
    if hasattr(history, "head"):
        print(history.head(5))
    else:
        print(history[:2])
except Exception as e:
    print(f"Error fetching OHLCV: {e}")

print("\n--- Testing Foreign Trading (VCI - PAID) ---")
try:
    f_trade = ostk.foreign("VNM", limit=3)
    if hasattr(f_trade, "head"):
        print(f_trade.head(3))
    else:
        print(f_trade[:3])
except Exception as e:
    print(f"Error fetching foreign trading: {e}")

print("\n--- Testing Proprietary Trading (VCI - PAID) ---")
try:
    p_trade = ostk.prop_trade("VNM", limit=3)
    if hasattr(p_trade, "head"):
        print(p_trade.head(3))
    else:
        print(p_trade[:3])
except Exception as e:
    print(f"Error fetching proprietary trading: {e}")

print("\n--- Testing Insider Trading (VCI - PAID) ---")
try:
    i_trade = ostk.insider("VNM", limit=3)
    if hasattr(i_trade, "head"):
        print(i_trade.head(3))
    else:
        print(i_trade[:3])
except Exception as e:
    print(f"Error fetching insider trading: {e}")

print("\n--- Testing Macro Indicators (MBK - FREE) ---")
try:
    macro = ostk.indicators()
    if hasattr(macro, "head"):
        print(macro.head(5))
    else:
        print(macro[:5])
except Exception as e:
    print(f"Error fetching macro indicators: {e}")

print("\n--- Testing Mutual Fund Details (Fmarket - FREE) ---")
try:
    # SSISCA has product ID 23
    ssisca = ostk.fund_details(23)
    print(json.dumps(ssisca, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error fetching fund details: {e}")

print("\n--- Testing Company News (KBS - FREE) ---")
try:
    news_list = ostk.company_news("VNM", limit=3)
    if hasattr(news_list, "head"):
        print(news_list.head(3))
    else:
        print(news_list[:3])
except Exception as e:
    print(f"Error fetching news: {e}")

print("\n--- Testing Company Events (KBS - FREE) ---")
try:
    event_list = ostk.company_events("VNM", limit=3)
    if hasattr(event_list, "head"):
        print(event_list.head(3))
    else:
        print(event_list[:3])
except Exception as e:
    print(f"Error fetching events: {e}")

print("\n--- Testing Async OHLCV History (DNSE - FREE) ---")
try:
    import asyncio
    async def run_async():
        res = await ostk.async_ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-02-01")
        if hasattr(res, "head"):
            print(res.head(2))
        else:
            print(res[:2])
    asyncio.run(run_async())
except Exception as e:
    print(f"Error fetching async OHLCV: {e}")





