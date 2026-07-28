import httpx

BACKEND_URL = "https://api.openstockapi.com"

# Handshake first to get a session token using "premium_sample_key"
res = httpx.post(
    f"{BACKEND_URL}/v1/license/handshake",
    json={
        "api_key": "premium_sample_key",
        "device_fingerprint": "debug_fingerprint",
        "version": "0.8.0"
    }
)
print("Handshake Response status:", res.status_code)
print("Handshake Response:", res.json())

if res.status_code == 200:
    session_token = res.json()["session_token"]
    
    # Now validate
    res_val = httpx.post(
        f"{BACKEND_URL}/v1/license/validate",
        json={
            "session_token": session_token,
            "action": "stock.us.ohlcv"
        }
    )
    print("Validate Response status:", res_val.status_code)
    print("Validate Response:", res_val.json())
