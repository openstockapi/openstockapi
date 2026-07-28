import asyncio
import traceback
from openstockapi.providers.asx.providers.yahoo import YahooASXProvider
from openstockapi.providers.asx.providers.asx_site import ASXSiteProvider
from openstockapi.providers.asx.providers.marketindex import MarketIndexProvider

async def main():
    symbol = "BHP"
    
    print("--- Testing YahooASXProvider ---")
    try:
        y = YahooASXProvider()
        res = await y.get_profile(symbol)
        print("Yahoo Result:", res)
    except Exception as e:
        traceback.print_exc()

    print("\n--- Testing ASXSiteProvider ---")
    try:
        a = ASXSiteProvider()
        res = await a.get_profile(symbol)
        print("ASX Site Result:", res)
    except Exception as e:
        traceback.print_exc()

    print("\n--- Testing MarketIndexProvider ---")
    try:
        m = MarketIndexProvider()
        res = await m.get_profile(symbol)
        print("MarketIndex Result:", res)
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
