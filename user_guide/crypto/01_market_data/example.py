import asyncio
import openstockapi as osapi

def main():
    # 1. Initialize session with a sample key (e.g., Premium tier to access all features)
    osapi.init("premium_sample_key")
    print("=== OpenStockAPI Crypto Module Example ===\n")

    # 2. Fetch Crypto OHLCV (Sync)
    print("--- 1. Fetching BTCUSDT Spot OHLCV (Sync - Binance) ---")
    klines = osapi.crypto_ohlcv(symbol="BTCUSDT", interval="1h", limit=3, market_type="spot", provider="binance")
    if hasattr(klines, "to_dict"):
        print(klines.head(3))
    else:
        for k in klines:
            print(f"Time: {k['timestamp']} | O: {k['open']} | H: {k['high']} | L: {k['low']} | C: {k['close']} | Vol: {k['volume']} | P: {k.get('provider')}")
    print()

    # 3. Fetch Crypto Order Book Depth
    print("--- 2. Fetching BTCUSDT Order Book Depth (OKX) ---")
    depth = osapi.crypto_depth(symbol="BTCUSDT", limit=3, provider="okx")
    print(f"Symbol: {depth['symbol']} | Provider: {depth.get('provider')}")
    print(f"Top 3 Bids: {depth['bids']}")
    print(f"Top 3 Asks: {depth['asks']}")
    print()

    # 4. Fetch Crypto Derivatives Indicators
    print("--- 3. Fetching BTCUSDT Derivatives Indicators (Bybit) ---")
    derivs = osapi.crypto_derivatives(symbol="BTCUSDT", provider="bybit")
    print(f"Symbol: {derivs['symbol']} | Provider: {derivs.get('provider')}")
    print(f"Open Interest: {derivs['open_interest']}")
    print(f"Funding Rate: {derivs['funding_rate']}")
    print()

    # 5. Fetch Crypto Footprint
    print("--- 4. Fetching BTCUSDT Footprint (Binance) ---")
    footprint = osapi.crypto_footprint(symbol="BTCUSDT", timeframe="5min", limit=2, provider="binance")
    print(f"Symbol: {footprint['symbol']} | Timeframe: {footprint['timeframe']} | Provider: {footprint.get('provider')}")
    print(f"Session Profile POC: {footprint['session_profile']['poc']}")
    print(f"First Bar POC: {footprint['bars'][0]['metrics']['poc']}")
    print()

    # 6. Simulate Leverage Position
    print("--- 5. Simulating BTCUSDT Leverage Position ---")
    sim = osapi.simulate_leverage(
        symbol="BTCUSDT",
        entry_price=60000.0,
        leverage=10.0,
        position_size=0.5,
        direction="long"
    )
    print(f"Direction: {sim['direction']} | Leverage: {sim['leverage']}x")
    print(f"Required Margin: {sim['initial_margin']} USDT")
    print(f"Estimated Liquidation Price: {sim['liquidation_price']} USDT")
    print()

    # 5b. Fetch Symbols and Tickers
    print("--- 5b. Fetching Supported Symbols and Tickers ---")
    symbols = osapi.crypto_symbols()
    print(f"Supported Crypto Symbols: {symbols['symbols']}")
    tickers = osapi.crypto_tickers(provider="okx")
    print(f"Realtime OKX Tickers Count: {len(tickers)}")
    print()

    # 5c. Fetch Options Instruments, Chain, and Ticker
    print("--- 5c. Fetching Options Instruments, Chain, and Ticker (OKX) ---")
    instruments = osapi.crypto_options_instruments(currency="BTC", kind="option", provider="okx")
    print(f"Options Instruments Count: {len(instruments)}")
    
    chain = osapi.crypto_options_chain(currency="BTC", provider="okx")
    print(f"Options Chain Entries Count: {len(chain)}")
    
    # Get ticker details for the first option instrument
    target_instrument = "BTC-USD-260726-60000-C"
    if instruments is not None:
        if isinstance(instruments, list) and len(instruments) > 0:
            target_instrument = instruments[0].get("instrument_name", target_instrument)
        elif not isinstance(instruments, list) and hasattr(instruments, "empty") and not instruments.empty:
            target_instrument = instruments.iloc[0]["instrument_name"]
            
    ticker = osapi.crypto_options_ticker(instrument_name=target_instrument, provider="okx")
    print(f"Options Ticker for {target_instrument}:")
    print(f"  Underlying Price: {ticker.get('underlying_price')}")
    print(f"  Mark Price: {ticker.get('mark_price')}")
    print(f"  Greeks Delta: {ticker.get('greeks', {}).get('delta')}")
    print(f"  Provider: {ticker.get('provider')}")
    print()

    # 5d. Fetch Crypto News and Events
    print("--- 5d. Fetching Crypto News and Events ---")
    news_data = osapi.crypto_news(limit=2, provider="cointelegraph")
    print(f"Crypto News count: {len(news_data)}")
    if len(news_data) > 0:
        print(f"  First news title: {news_data[0].get('title') if isinstance(news_data, list) else news_data.iloc[0]['title']}")
        
    events_data = osapi.crypto_events(provider="coingecko")
    print(f"Crypto Events count: {len(events_data)}")
    if len(events_data) > 0:
        print(f"  First event title: {events_data[0].get('title') if isinstance(events_data, list) else events_data.iloc[0]['title']}")
    
    # Unified APIs
    unified_news = osapi.company_news("BTC", limit=2, market="crypto")
    print(f"Unified News count: {len(unified_news)}")
    print()


async def async_main():
    print("--- 6. Fetching Crypto OHLCV (Async - Binance) ---")
    # Fetch BTC and ETH concurrently
    results = await asyncio.gather(
        osapi.async_crypto_ohlcv("BTCUSDT", interval="1h", limit=2, provider="binance"),
        osapi.async_crypto_ohlcv("ETHUSDT", interval="1h", limit=2, provider="binance")
    )
    btc_klines, eth_klines = results
    print(f"BTC bars: {len(btc_klines)}")
    print(f"ETH bars: {len(eth_klines)}")


if __name__ == "__main__":
    main()
    asyncio.run(async_main())
