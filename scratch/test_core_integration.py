import openstockapi as osapi
from openstockapi.license.session import set_current_session
import httpx

print("Testing connection to openstockapi_be_mgt at http://localhost:8001...")

try:
    res = httpx.get("http://localhost:8001/")
    print(f"Backend status response: {res.status_code} - {res.json()}")
    
    # Initialize session with UAT pro key
    osapi.init("pro_sample_key")
    
    print("\n1. Fetching Crypto Symbols...")
    p = osapi.providers.get_provider("core")
    # Let's call endpoint directly to see
    headers = p._get_headers()
    url = f"{p.BACKEND_URL}/v1/crypto/symbols" if hasattr(p, "BACKEND_URL") else "http://localhost:8001/v1/crypto/symbols"
    try:
        symbols_res = httpx.get(url, headers=headers)
        print(f"Crypto symbols: {symbols_res.status_code} - {symbols_res.json()}")
    except Exception as e:
        print(f"Failed to fetch symbols: {e}")
        
    print("\n2. Fetching Crypto OHLCV via library API...")
    try:
        ohlcv_data = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=5)
        print(f"Success! Retrieved {len(ohlcv_data)} OHLCV bars. Sample: {ohlcv_data[0] if ohlcv_data else 'Empty'}")
    except Exception as e:
        print(f"Failed calling osapi.crypto_ohlcv: {e}")
        
    print("\n3. Fetching Forex Rates via library API...")
    try:
        rates = osapi.forex_rates("USD")
        print(f"Success! Forex Rates response: {rates}")
    except Exception as e:
        print(f"Failed calling osapi.forex_rates: {e}")
        
except Exception as e:
    print(f"Backend http://localhost:8001/ is not reachable: {e}")
