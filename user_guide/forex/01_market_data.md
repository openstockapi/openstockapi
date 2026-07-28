---
id: forex-market-data
title: "Module 09: Forex & Commodities Market Data"
description: Guide for retrieving forex conversion rates, historical exchange charts, commodity prices, global indices/ETFs, and cross-source comparisons.
category: Forex
difficulty: Basic
tier: Free (Rates, OHLCV, Commodities, Indices) / Pro (Rate Comparison)
tags: [forex, commodities, etf, indices, arbitrage]
---

# Module 09: Forex & Commodities Market Data

This module provides guides for retrieving currency exchange rates, historical charts, commodities, indices, and cross-source comparisons through the local `forex_service` provider layer.

*   For executable code examples, check [example.py](./01_market_data/example.py).
*   For sample JSON responses, check [sample_output.json](./01_market_data/sample_output.json).

---

## Use Case 9.1 — Fetch Exchange Rates (Forex Rates)

**Required Tier:** `Free`  
**API:** `forex_rates(base="USD", provider=None)`

Retrieves exchange rates from a specified base currency.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

rates = osapi.forex_rates(base="USD", provider="exchangerate")
print(rates)
```

**Sample Output:**
```json
{
  "base": "USD",
  "rates": {
    "USD": 1.0,
    "EUR": 0.876691,
    "GBP": 0.747063,
    "JPY": 163.013007,
    "VND": 26238.632049
  },
  "timestamp": 1784678551000,
  "source": "exchangerate_api",
  "provider": "exchangerate"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `base` | `str` | No | `USD` | Base currency code (e.g. `USD`, `EUR`, `VND`) |
| `provider` | `str` | No | `None` | Explicit provider: `"exchangerate"`, `"openexchangerates"`, `"yahoo"` |

---

## Use Case 9.2 — Fetch Historical Exchange Rates (Forex OHLCV)

**Required Tier:** `Free`  
**API:** `forex_ohlcv(symbol=None, base=None, target=None, range_val="5d", interval="1h", provider=None)`

Retrieves historical chart bars for a specified currency pair.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

chart = osapi.forex_ohlcv(symbol="EURUSD", range_val="5d", interval="1h", provider="yahoo")
print(chart)
```

**Sample Output:**
```json
{
  "ticker": "EURUSD=X",
  "currency": "USD",
  "regularMarketPrice": 1.085,
  "provider": "yahoo",
  "bars": [
    {
      "timestamp": "2026-07-21 00:00:00",
      "open": 1.084,
      "high": 1.086,
      "low": 1.083,
      "close": 1.085,
      "volume": 0.0
    }
  ]
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | No | — | Standard currency pair (e.g. `EURUSD`, `GBPUSD`) |
| `base` | `str` | No | — | Base currency (alternative if `symbol` is not provided) |
| `target` | `str` | No | — | Target currency (alternative if `symbol` is not provided) |
| `range_val`| `str` | No | `5d` | Lookback period: `5d`, `1mo`, `1y` |
| `interval` | `str` | No | `1h` | Time resolution: `1h`, `1d` |
| `provider` | `str` | No | `None` | Explicit provider: `"yahoo"`, `"frankfurter"`, `"bybit"`, `"okx"` |

---

## Use Case 9.3 — Fetch Commodities Prices

**Required Tier:** `Free`  
**API:** `commodities_prices(symbol, range_val="5d", interval="1h", provider=None)`

Retrieves historical commodity chart data for standardized commodities.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

gold = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h", provider="yahoo")
print(gold)
```

**Sample Output:**
```json
{
  "ticker": "GC=F",
  "currency": "USD",
  "regularMarketPrice": 2400.5,
  "provider": "yahoo",
  "bars": [
    {
      "timestamp": "2026-07-21 00:00:00",
      "open": 2398.0,
      "high": 2405.0,
      "low": 2395.0,
      "close": 2400.5,
      "volume": 12500
    }
  ]
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Commodity symbol: `"GOLD"`, `"SILVER"`, `"CRUDE_OIL"`, `"BRENT_OIL"` |
| `range_val`| `str` | No | `5d` | Lookback period: `5d`, `1mo`, `1y` |
| `interval` | `str` | No | `1h` | Time resolution: `1h`, `1d` |
| `provider` | `str` | No | `None` | Explicit provider: `"yahoo"`, `"bybit"`, `"okx"`, `"bingx"` |

---

## Use Case 9.4 — Fetch Global Indices & ETFs

**Required Tier:** `Free`  
**API:** `global_indices_etf(symbol, range_val="5d", interval="1h", provider=None)`

Retrieves historical chart data for major indices and ETFs (like S&P 500 or Nasdaq).

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

spy = osapi.global_indices_etf(symbol="SPY", range_val="5d", interval="1h", provider="yahoo")
print(spy)
```

**Sample Output:**
```json
{
  "ticker": "SPY",
  "currency": "USD",
  "regularMarketPrice": 402.0,
  "provider": "yahoo",
  "bars": [
    {
      "timestamp": "2026-07-21 00:00:00",
      "open": 401.0,
      "high": 403.5,
      "low": 400.2,
      "close": 402.0,
      "volume": 45000000
    }
  ]
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Standardized ticker symbol (e.g. `SPY`, `QQQ`) |
| `range_val`| `str` | No | `5d` | Lookback period: `5d`, `1mo`, `1y` |
| `interval` | `str` | No | `1h` | Time resolution: `1h`, `1d` |
| `provider` | `str` | No | `None` | Explicit provider: `"yahoo"`, `"bingx"` |

---

## Use Case 9.5 — Compare Forex Rates (Arbitrage)

**Required Tier:** `Pro` ⭐  
**API:** `compare_rates(base="USD")`

Compares exchange rates across different sources/brokerages to find arbitrage opportunities.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

comparison = osapi.compare_rates(base="USD")
print(comparison)
```

**Sample Output:**
```json
{
  "base": "USD",
  "comparison": {
    "exchangerate": { "EUR": 0.88, "VND": 25400.0 },
    "openexchangerates": { "EUR": 0.881, "VND": 25410.0 },
    "yahoo": { "EUR": 0.88, "VND": 25405.0 }
  },
  "timestamp": 1625097600000
}
```

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `base` | `str` | No | `USD` | Base currency code (e.g. `USD`, `EUR`) |

---

## Use Case 9.6 — Fetch Supported Forex & Commodities Symbols

**Required Tier:** `Free`  
**API:** `forex_symbols(provider=None)`

Retrieves a list of all supported forex currency pairs, commodities, and indices.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

symbols = osapi.forex_symbols()
print(symbols)
```

**Sample Output:**
```json
{
  "forex": ["EURUSD", "GBPUSD", "USDJPY", "USDVND"],
  "commodities": ["GOLD", "SILVER", "CRUDE_OIL"],
  "indices_etf": ["SPY", "QQQ"]
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | No | `None` | Explicit provider selection (unused, returns unified symbols dict) |

---

## Use Case 9.7 — Fetch Forex News

**Required Tier:** `Free`  
**API:** `forex_news(limit=20, provider=None)`  
**Unified API:** `company_news(symbol, limit=10, market="forex")`

Retrieves the latest forex and financial news.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

# Specific API
news = osapi.forex_news(limit=3, provider="yahoo")
print(news)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `20` | Maximum number of news items to return |
| `provider` | `str` | No | `None` | Explicit provider: `"yahoo"`, `"dailyfx"`, `"marketwatch"`, `"cnbc"` |

---

## Use Case 9.8 — Fetch Forex Events

**Required Tier:** `Free`  
**API:** `forex_events(provider=None)`  
**Unified API:** `company_events(symbol, market="forex")`

Retrieves global macro economic calendar events.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

# Specific API
events = osapi.forex_events(provider="forexfactory")
print(events)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | No | `None` | Explicit provider: `"forexfactory"`, `"dailyfx"` |
