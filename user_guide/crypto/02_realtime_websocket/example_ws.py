import asyncio
import os
import openstockapi as osapi

async def main():
    print("=== OpenStockAPI Crypto WebSocket Example ===\n")
    
    # 1. Initialize session using environment backend if configured
    backend_url = os.getenv("OPENSTOCKAPI_BACKEND_URL", "https://api.openstockapi.com")
    os.environ["OPENSTOCKAPI_BACKEND_URL"] = backend_url
    
    # WebSocket requires verification; init with sample premium key
    osapi.init("premium_sample_key")
    
    # 2. Define message callback handler
    def handle_message(msg):
        msg_type = msg.get("type")
        symbol = msg.get("symbol")
        
        if msg_type == "trade":
            print(f"[TRADE] {symbol}: Price={msg['price']} | Qty={msg['qty']}")
        elif msg_type == "depth":
            depth = msg["depth"]
            best_bid = depth["bids"][0][0] if depth["bids"] else "N/A"
            best_ask = depth["asks"][0][0] if depth["asks"] else "N/A"
            print(f"[DEPTH] {symbol}: Best Bid={best_bid} | Best Ask={best_ask}")
        elif msg_type == "liquidation":
            liq = msg["liquidation"]
            print(f"[LIQUIDATION] {symbol}: {liq['side']} {liq['qty']} @ {liq['price']}")
        else:
            print(f"[RAW] {msg}")

    # 3. Create CryptoStream for BTCUSDT and ETHUSDT
    print("--- Connecting to WebSocket Stream ---")
    stream = osapi.CryptoStream(symbols=["BTCUSDT", "ETHUSDT"])
    
    # Start receiving messages in a background asyncio task
    stream_task = asyncio.create_task(stream.connect(on_message=handle_message))
    
    # Listen for messages for 5 seconds
    await asyncio.sleep(5)
    
    # 4. Subscribe to another symbol (e.g. SOLUSDT) on the fly
    print("\n--- Subscribing to SOLUSDT on the fly ---")
    await stream.subscribe("SOLUSDT")
    await asyncio.sleep(5)
    
    # 5. Unsubscribe from ETHUSDT
    print("\n--- Unsubscribing from ETHUSDT ---")
    await stream.unsubscribe("ETHUSDT")
    await asyncio.sleep(5)
    
    # 6. Close the connection clean
    print("\n--- Closing WebSocket connection ---")
    await stream.close()
    await stream_task
    print("WebSocket client closed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
