# US Stock Market Data (Module 11)

This module provides comprehensive historical and reference data for the United States Stock Market (US Stock), including Apple (AAPL), Microsoft (MSFT), Tesla (TSLA), and other listed equities.

All requests are validated by the Core Engine gateway tier control plane, but the actual data is retrieved and parsed locally via concrete providers: `yahoo`, `nasdaq`, `sec_edgar`, `tradingview`, and `google_news`.

---

## Use Case 11.0 — US Stock Symbols

**Required Tier:** `Free`

**API:** `us_symbols(provider: Optional[str] = None)`

Retrieve a list of all active stock symbols available for the US stock market.

### Code Snippet

```python
import openstockapi as osapi

# Initialize session
osapi.init("your_free_api_key")

# Fetch US stock symbols explicitly from Nasdaq
symbols = osapi.us_symbols(provider="nasdaq")
print(f"Total symbols: {len(symbols)}")
print(f"Example symbols: {symbols[:5]}")
```

### Sample Output

```json
[
  "AAPL",
  "MSFT",
  "TSLA",
  "NVDA",
  "AMZN"
]
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"nasdaq"`, `"sec_edgar"`. |

---

## Use Case 11.1 — US Stock OHLCV

**Required Tier:** `Free`

**API:** `us_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None)`

Retrieve historical Open, High, Low, Close, and Volume (OHLCV) bars for a US stock.

### Code Snippet

```python
import openstockapi as osapi

# Initialize session
osapi.init("your_free_api_key")

# Fetch AAPL 1-hour interval data for last 5 days from Yahoo Finance
df = osapi.us_ohlcv("AAPL", range="5d", interval="1h", provider="yahoo")
print(df.head())
```

### Sample Output

```json
[
  {
    "symbol": "AAPL",
    "timestamp": "2026-07-21 00:00:00",
    "open": 180.5,
    "high": 182.0,
    "low": 179.8,
    "close": 181.2,
    "volume": 52000000.0,
    "provider": "yahoo",
    "market": "us",
    "asset_class": "stock"
  }
]
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`, `TSLA`). |
| `range` | `str` | No | `"5d"` | Range of data to fetch. Valid choices: `"5d"`, `"1mo"`, `"1y"`, `"max"`. |
| `interval` | `str` | No | `"1h"` | Candlestick resolution interval. Valid choices: `"1m"`, `"5m"`, `"15m"`, `"30m"`, `"1h"`, `"4h"`, `"1d"`. |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`, `"tradingview"`. |

---

## Use Case 11.2 — US Stock Company Profile

**Required Tier:** `Free`

**API:** `us_profile(symbol: str, provider: Optional[str] = None)`

Retrieve basic corporate information, description, headcount, and official industry classification.

### Code Snippet

```python
profile = osapi.us_profile("AAPL", provider="yahoo")
print(f"Company: {profile['company_name']}, Industry: {profile['industry']}")
```

### Sample Output

```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "industry": "Consumer Electronics",
  "website": "https://www.apple.com",
  "headcount": 150000,
  "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets...",
  "provider": "yahoo",
  "market": "us",
  "asset_class": "stock"
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`, `"sec_edgar"`. |

---

## Use Case 11.11 — US Stock Heatmap

**Required Tier:** `Free`

**API:** `us_heatmap(limit: int = 500, provider: Optional[str] = None)`

Retrieve real-time price change, market cap, sector, industry classifications and SVG logo URLs for the top US stock market equities (e.g. S&P 500 components).

### Code Snippet

```python
import openstockapi as osapi

# Initialize session
osapi.init("your_free_api_key")

# Fetch top 5 US stock heatmap data points
heatmap = osapi.us_heatmap(limit=5, provider="tradingview")
print(heatmap)
```

### Sample Output

```json
[
  {
    "symbol": "NVDA",
    "name": "NVIDIA Corporation",
    "change": -0.919716,
    "market_cap": 5005527911376.999,
    "sector": "Electronic Technology",
    "industry": "Semiconductors",
    "logo_url": "https://s3-symbol-logo.tradingview.com/nvidia.svg",
    "provider": "tradingview",
    "market": "us",
    "asset_class": "stock"
  }
]
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `500` | Number of top equities sorted by market cap to retrieve. |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"tradingview"`. |
