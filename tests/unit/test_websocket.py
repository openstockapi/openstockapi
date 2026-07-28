import asyncio
import json
import pytest
from unittest.mock import AsyncMock, patch
from openstockapi import CryptoStream, init

@pytest.mark.asyncio
async def test_websocket_stream_mocked():
    init("premium_sample_key")
    stream = CryptoStream(symbols=["BTCUSDT"])
    received = []

    def on_msg(msg):
        received.append(msg)

    # Mock WebSocket connection object
    mock_ws = AsyncMock()
    mock_ws.__aenter__.return_value = mock_ws
    
    # Mock recv to return a message, then wait/sleep to simulate active connection
    async def mock_recv():
        await asyncio.sleep(0.1)
        return json.dumps({"symbol": "BTCUSDT", "type": "trade", "price": 65000.0})

    mock_ws.recv = mock_recv
    mock_ws.send = AsyncMock()
    mock_ws.close = AsyncMock()

    with patch("websockets.connect", return_value=mock_ws) as mock_connect:
        task = asyncio.create_task(stream.connect(on_msg))
        await asyncio.sleep(0.3)
        await stream.close()
        await task
        
        mock_connect.assert_called_once()
        mock_ws.send.assert_called_with(json.dumps({"action": "subscribe", "symbol": "BTCUSDT"}))
        assert len(received) > 0
        assert received[0]["symbol"] == "BTCUSDT"
        assert received[0]["price"] == 65000.0
