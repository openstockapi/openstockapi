import asyncio
import json
import logging
from typing import Callable, List, Optional
import websockets
from openstockapi.license.session import get_current_session
from openstockapi.config.settings import BACKEND_URL

logger = logging.getLogger("openstockapi.stream")

class CryptoStream:
    """Real-time WebSocket streaming client for Cryptocurrency data."""
    def __init__(self, symbols: Optional[List[str]] = None):
        self.symbols = [s.upper() for s in (symbols or [])]
        self._ws = None
        self._running = False
        self._on_message = None

    async def connect(self, on_message: Callable[[dict], None]):
        """Connects to the Core Engine WebSocket server and listens for events."""
        session = get_current_session()
        
        # Adapt HTTP URL to WebSocket protocol
        base_ws = BACKEND_URL.replace("http://", "ws://").replace("https://", "wss://")
        ws_url = f"{base_ws}/v1/crypto/ws?api_key={session.api_key}"
        
        self._on_message = on_message
        self._running = True
        
        async with websockets.connect(ws_url) as ws:
            self._ws = ws
            # Subscribe to initial list of symbols
            for sym in self.symbols:
                await self._ws.send(json.dumps({"action": "subscribe", "symbol": sym}))
            
            while self._running:
                try:
                    msg = await self._ws.recv()
                    data = json.loads(msg)
                    if self._on_message:
                        self._on_message(data)
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    logger.error(f"Error receiving WebSocket message: {e}")
                    await asyncio.sleep(1)

    async def subscribe(self, symbol: str):
        """Subscribe to a new token's real-time stream."""
        symbol_upper = symbol.upper()
        if symbol_upper not in self.symbols:
            self.symbols.append(symbol_upper)
        if self._ws and self._running:
            try:
                await self._ws.send(json.dumps({"action": "subscribe", "symbol": symbol_upper}))
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Failed to subscribe to {symbol_upper}: connection closed.")

    async def unsubscribe(self, symbol: str):
        """Unsubscribe from a token's real-time stream."""
        symbol_upper = symbol.upper()
        if symbol_upper in self.symbols:
            self.symbols.remove(symbol_upper)
        if self._ws and self._running:
            try:
                await self._ws.send(json.dumps({"action": "unsubscribe", "symbol": symbol_upper}))
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Failed to unsubscribe from {symbol_upper}: connection closed.")

    async def close(self):
        """Disconnects the WebSocket client."""
        self._running = False
        if self._ws:
            await self._ws.close()
            self._ws = None
