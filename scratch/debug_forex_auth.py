import httpx

url_handshake = "https://api.openstockapi.com/v1/license/handshake"
url_validate = "https://api.openstockapi.com/v1/license/validate"

# Handshake
resp = httpx.post(url_handshake, json={"api_key": "pro_sample_key", "device_fingerprint": "debug_fingerprint", "version": "0.1.0"})
print("Handshake Response:", resp.status_code, resp.json())
token = resp.json()["session_token"]

# Validate
resp_val = httpx.post(url_validate, json={"session_token": token, "action": "forex.global.rates"})
print("Validate Response:", resp_val.status_code, resp_val.json())
