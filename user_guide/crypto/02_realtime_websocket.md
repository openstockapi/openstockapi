# Real-Time WebSocket Streaming Guide (Crypto)

The `openstockapi` library provides the `CryptoStream` class, which allows users to establish asynchronous (`asyncio`) connections to the Core Engine in order to receive real-time price and order book data for cryptocurrency pairs.

---

## 💡 How to Use

The `CryptoStream` class requires an initial list of symbols and an `on_message` callback function to process the JSON messages received from the server.

```python
import asyncio
import openstockapi as osapi

async def main():
    # 1. Initialize session with an authorized API key
    osapi.init("your_premium_or_pro_api_key")
    
    # 2. Define a handler function for incoming messages
    def handle_message(msg):
        msg_type = msg.get("type")
        symbol = msg.get("symbol")
        
        if msg_type == "trade":
            print(f"[TRADE] {symbol}: Price {msg['price']} | Qty {msg['qty']}")
        elif msg_type == "depth":
            depth = msg["depth"]
            print(f"[DEPTH] {symbol}: Best Bid: {depth['bids'][0][0] if depth['bids'] else 'N/A'}")
        elif msg_type == "liquidation":
            liq = msg["liquidation"]
            print(f"[LIQUIDATION] {symbol}: {liq['side']} {liq['qty']} @ {liq['price']}")
        else:
            print(f"[RAW] {msg}")

    # 3. Initialize the WebSocket stream for BTCUSDT and ETHUSDT
    stream = osapi.CryptoStream(symbols=["BTCUSDT", "ETHUSDT"])
    
    # Run connection task in the background
    connection_task = asyncio.create_task(stream.connect(on_message=handle_message))
    
    # Wait for 10 seconds to receive and print data
    await asyncio.sleep(10)
    
    # 4. Subscribe to a new symbol dynamically
    print("--- Subscribing to SOLUSDT ---")
    await stream.subscribe("SOLUSDT")
    await asyncio.sleep(5)
    
    # 5. Unsubscribe from a symbol
    print("--- Unsubscribing from ETHUSDT ---")
    await stream.unsubscribe("ETHUSDT")
    await asyncio.sleep(5)
    
    # 6. Close the connection
    print("--- Closing Stream connection ---")
    await stream.close()
    await connection_task

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📊 Event Data Formats

The Core Engine automatically normalizes messages streamed from upstream sources (such as Binance) into 3 main event types:

### 1. Trade Event (`type="trade"`)
```json
{
  "type": "trade",
  "symbol": "BTCUSDT",
  "price": 65711.04,
  "qty": 2.80333,
  "isBuyerMaker": false,
  "timestamp": 1625097600000
}
```

### 2. Order Book Depth Event (`type="depth"`)
```json
{
  "type": "depth",
  "symbol": "BTCUSDT",
  "depth": {
    "symbol": "BTCUSDT",
    "lastUpdateId": 128471029,
    "bids": [[65711.04, 2.80333], [65711.03, 0.00104]],
    "asks": [[65711.05, 4.70853], [65711.06, 0.0008]]
  }
}
```

### 3. Liquidation Event (`type="liquidation"`)
```json
{
  "type": "liquidation",
  "symbol": "BTCUSDT",
  "liquidation": {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "price": 65691.0,
    "qty": 0.054,
    "timestamp": 1625097686000
  }
}
```
