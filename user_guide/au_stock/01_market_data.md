---
id: au-stock-market-data
title: "Module 10: Australian Stock Market Data (AU Stock)"
description: Guide for integrating Australian Securities Exchange (ASX) equity data including historical prices, corporate profiles, financial statements, dividends, announcements, and news.
category: Stock
difficulty: Beginner
tier: Free (Symbols, OHLCV, Profile, Financials, Dividends, Announcements, News)
tags: [stock, asx, au, ohlcv, profile, financials, dividends, news]
---

# Module 10: Australian Stock Market Data (AU Stock)

This module provides financial and market data for companies listed on the Australian Securities Exchange (ASX).

*   For executable code examples, check [example.py](./01_market_data/example.py).
*   For sample JSON responses, check [sample_output.json](./01_market_data/sample_output.json).

---

## Use Case 10.1 — Get ASX Symbols List

**Required Tier:** `Free`  
**API:** `asx_symbols(provider=None)`

Retrieves the list of active symbols currently listed on the ASX.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

symbols = osapi.asx_symbols(provider="asx")
print(symbols[:5])
```

**Sample Output:**
```json
[
  "BHP",
  "CBA",
  "CSL",
  "NAB",
  "WBC"
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `asx` |

---

## Use Case 10.2 — Get Historical Price Data (ASX OHLCV)

**Required Tier:** `Free`  
**API:** `asx_ohlcv(symbol, range="5d", interval="1h", provider=None)`

Retrieves historical price bars (Open, High, Low, Close, Volume) for a given symbol.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

df = osapi.asx_ohlcv(symbol="BHP", range="5d", interval="1h", provider="yahoo")
print(df.head(2))
```

**Sample Output:**
```json
[
  {
    "time": 1735689600,
    "open": 42.5,
    "high": 43.1,
    "low": 42.4,
    "close": 43.0,
    "volume": 2500000
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`, `CBA`) |
| `range` | `str` | No | `5d` | Lookback range (e.g. `1d`, `5d`, `1mo`, `1y`) |
| `interval` | `str` | No | `1h` | Bar interval (e.g. `1m`, `5m`, `15m`, `1h`, `1d`) |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo`, `marketindex` |

---

## Use Case 10.11 — Get ASX Stock Heatmap (ASX Heatmap)

**Required Tier:** `Free`  
**API:** `asx_heatmap(limit=500, provider=None)`

Retrieves real-time price change, market cap, sector, industry classifications and SVG logo URLs for the top ASX stock market equities.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

heatmap_data = osapi.asx_heatmap(limit=5, provider="tradingview")
print(heatmap_data)
```

**Sample Output:**
```json
[
  {
    "symbol": "BHP",
    "name": "BHP Group Ltd",
    "change": -2.93584,
    "market_cap": 298998595299.0,
    "sector": "Non-Energy Minerals",
    "industry": "Steel",
    "logo_url": "https://s3-symbol-logo.tradingview.com/bhp.svg",
    "provider": "tradingview",
    "market": "au",
    "asset_class": "stock"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `500` | Number of top equities sorted by market cap to retrieve. |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"tradingview"`. |
