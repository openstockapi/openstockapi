import os
import openstockapi as osapi

def main():
    # 1. Initialize session
    osapi.init("pro_sample_key")
    print("=== OpenStockAPI Forex & Commodities Module Example ===\n")

    # 2. Fetch Forex Rates
    print("--- 1. Fetching USD Exchange Rates (exchangerate) ---")
    rates_data = osapi.forex_rates(base="USD", provider="exchangerate")
    print(f"Base Currency: {rates_data['base']}")
    print(f"VND Rate: {rates_data['rates'].get('VND')} | Provider: {rates_data.get('provider')}")
    print()

    # 3. Fetch Forex OHLCV
    print("--- 2. Fetching EURUSD Historical Candlesticks (yahoo) ---")
    chart = osapi.forex_ohlcv(symbol="EURUSD", range_val="5d", interval="1h", provider="yahoo")
    if isinstance(chart, list):
        if len(chart) > 0:
            print(f"Ticker: {chart[0].get('symbol')} | Provider: {chart[0].get('provider')}")
            for bar in chart[:2]:
                print(f"Time: {bar['timestamp']} | O: {bar['open']} | C: {bar['close']}")
    else:
        if not chart.empty:
            print(f"Ticker: {chart.iloc[0]['symbol']} | Provider: {chart.iloc[0]['provider']}")
            for _, bar in chart.head(2).iterrows():
                print(f"Time: {bar['timestamp']} | O: {bar['open']} | C: {bar['close']}")
    print()

    # 4. Fetch Commodities Prices (Gold)
    print("--- 3. Fetching GOLD Prices (bybit) ---")
    gold = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h", provider="bybit")
    if isinstance(gold, list):
        if len(gold) > 0:
            print(f"Ticker: {gold[0].get('symbol')} | First Bar Close: {gold[0].get('close')} | Provider: {gold[0].get('provider')}")
    else:
        if not gold.empty:
            print(f"Ticker: {gold.iloc[0]['symbol']} | First Bar Close: {gold.iloc[0]['close']} | Provider: {gold.iloc[0]['provider']}")
    print()

    # 5. Fetch Global Indices & ETF (SPY)
    print("--- 4. Fetching SPY ETF Data (yahoo) ---")
    spy = osapi.global_indices_etf(symbol="SPY", range_val="5d", interval="1h", provider="yahoo")
    if isinstance(spy, list):
        if len(spy) > 0:
            print(f"Ticker: {spy[0].get('symbol')} | First Bar Close: {spy[0].get('close')} | Provider: {spy[0].get('provider')}")
    else:
        if not spy.empty:
            print(f"Ticker: {spy.iloc[0]['symbol']} | First Bar Close: {spy.iloc[0]['close']} | Provider: {spy.iloc[0]['provider']}")
    print()

    # 6. Compare Forex Rates across sources
    print("--- 5. Comparing USD Exchange Rates ---")
    compare = osapi.compare_rates(base="USD")
    print(f"Base: {compare['base']}")
    for src, rates in compare['comparison'].items():
        print(f"Source: {src:<18} | EUR: {rates.get('EUR')} | VND: {rates.get('VND')}")
    print()

    # 7. Fetch Supported Forex Symbols
    print("--- 6. Fetching Supported Forex & Commodities Symbols ---")
    symbols = osapi.forex_symbols()
    print(f"Forex Pairs: {symbols['forex']}")
    print(f"Commodities: {symbols['commodities']}")
    print()

    # 8. Fetch Forex News and Events
    print("--- 7. Fetching Forex News and Events ---")
    news_data = osapi.forex_news(limit=2, provider="yahoo")
    print(f"Forex News count: {len(news_data)}")
    if len(news_data) > 0:
        print(f"  First news title: {news_data[0].get('title') if isinstance(news_data, list) else news_data.iloc[0]['title']}")
        
    events_data = osapi.forex_events(provider="dailyfx")
    print(f"Forex Events count: {len(events_data)}")
    if len(events_data) > 0:
        print(f"  First event title: {events_data[0].get('title') if isinstance(events_data, list) else events_data.iloc[0]['title']}")
    
    # Unified APIs
    unified_news = osapi.company_news("USD", limit=2, market="forex")
    print(f"Unified Forex News count: {len(unified_news)}")
    print()


if __name__ == "__main__":
    # Ensure local UAT port is targeted if backend server is active
    os.environ["OPENSTOCKAPI_BACKEND_URL"] = "https://api.openstockapi.com"
    main()
