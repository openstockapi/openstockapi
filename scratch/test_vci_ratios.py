import requests
import urllib3
urllib3.disable_warnings()

url = "https://trading.vietcap.com.vn/data-mt/graphql"
payload = {
    "query": "query Query($ticker: String!, $lang: String!) { TickerPriceInfo(ticker: $ticker) { ticker exchange financialRatio { pe pb eps roe roa } } }",
    "variables": {"ticker": "HPG", "lang": "vi"}
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://trading.vietcap.com.vn",
    "Referer": "https://trading.vietcap.com.vn/"
}

r = requests.post(url, json=payload, headers=headers, verify=False)
print("Status:", r.status_code)
print("Response:", r.text)
