# Module 08: Cryptocurrency Market Data

This module provides guides for fetching various levels of cryptocurrency data through the Core Engine (`openstockapi_be_mgt`).

*   For executable code examples, check [example.py](./01_market_data/example.py).
*   For sample JSON responses, check [sample_output.json](./01_market_data/sample_output.json).

---

## Use Case 8.1 — Fetch Crypto Candlesticks (Crypto OHLCV)

**Required Tier:** `Free`  
**API:** `crypto_ohlcv(symbol, interval="1h", limit=100, market_type="spot", provider=None)` (Sync)  
**API:** `async_crypto_ohlcv(symbol, interval="1h", limit=100, market_type="spot", provider=None)` (Async)

#### Synchronous Call Example
```python
import openstockapi as osapi
osapi.init("your_free_api_key")

klines = osapi.crypto_ohlcv(symbol="BTCUSDT", interval="1h", limit=3, market_type="spot", provider="binance")
print(klines)
```

**Sample Output (List of objects):**
```json
[
  {
    "timestamp": "2026-07-25 22:00:00",
    "open": 64214.05,
    "high": 64214.05,
    "low": 64182.01,
    "close": 64206.61,
    "volume": 572.31956,
    "provider": "binance",
    "market": "global",
    "asset_class": "crypto"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Ticker symbol (e.g. `BTCUSDT`, `ETHUSDT`) |
| `interval` | `str` | No | `1h` | Time resolution: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d` |
| `limit` | `int` | No | `100` | Maximum number of bars to fetch |
| `market_type`| `str` | No | `spot` | Market type classification: `"spot"` or `"futures"` |
| `provider` | `str` | No | `None` | Explicit provider: `"binance"`, `"bybit"`, `"okx"` |

---

## Use Case 8.2 — Fetch Crypto Order Book Depth

**Required Tier:** `Pro` ⭐  
**API:** `crypto_depth(symbol, limit=100, provider=None)`

Fetches the bids and asks book depth for a specified pair.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

depth = osapi.crypto_depth(symbol="BTCUSDT", limit=2, provider="okx")
print(depth)
```

**Sample Output:**
```json
{
  "symbol": "BTCUSDT",
  "bids": [
    {"price": 64238.5, "volume": 4.78},
    {"price": 64238.0, "volume": 0.09}
  ],
  "asks": [
    {"price": 64238.6, "volume": 0.89},
    {"price": 64240.0, "volume": 0.02}
  ],
  "timestamp": "2026-07-26 00:00:00",
  "provider": "okx",
  "market": "global",
  "asset_class": "crypto"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Ticker symbol (e.g. `BTCUSDT`) |
| `limit` | `int` | No | `100` | Depth levels to fetch |
| `provider` | `str` | No | `None` | Explicit provider: `"binance"`, `"bybit"`, `"okx"`, `"bingx"`, `"hyperliquid"` |

---

## Use Case 8.3 — Fetch Derivatives Indicators

**Required Tier:** `Pro` ⭐  
**API:** `crypto_derivatives(symbol, provider=None)`

Fetches derivative statistics such as Open Interest (OI) and Funding Rate for futures markets.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

derivs = osapi.crypto_derivatives(symbol="BTCUSDT", provider="bybit")
print(derivs)
```

**Sample Output:**
```json
{
  "symbol": "BTCUSDT",
  "open_interest": 58425.018,
  "funding_rate": -0.00000405,
  "provider": "bybit",
  "market": "global",
  "asset_class": "crypto"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Futures contract symbol (e.g. `BTCUSDT`) |
| `provider` | `str` | No | `None` | Explicit provider: `"binance"`, `"bybit"`, `"okx"` |

---

## Use Case 8.4 — Simulate Leverage & Margin

**Required Tier:** `Pro` ⭐  
**API:** `simulate_leverage(symbol, entry_price, leverage, position_size, direction)`

Computes initial margin and estimated liquidation price based on inputs.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

sim = osapi.simulate_leverage(
    symbol="BTCUSDT",
    entry_price=60000.0,
    leverage=10.0,
    position_size=0.5,
    direction="long"
)
print(sim)
```

**Sample Output:**
```json
{
  "symbol": "BTCUSDT",
  "entry_price": 60000.0,
  "leverage": 10.0,
  "position_size": 0.5,
  "direction": "long",
  "initial_margin": 3000.0,
  "maintenance_margin": 120.0,
  "liquidation_price": 54240.0
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Ticker symbol (e.g. `BTCUSDT`) |
| `entry_price` | `float`| **Yes** | — | Price level at which the position is opened |
| `leverage` | `float`| **Yes** | — | Leverage scale (e.g. `10.0`, `20.0`) |
| `position_size`| `float`| **Yes** | — | Contract size of the position (in coin units) |
| `direction` | `str` | **Yes** | — | Order direction: `"long"` or `"short"` |

---

## Use Case 8.5 — Fetch Crypto Footprint & Delta

**Required Tier:** `Premium`  
**API:** `crypto_footprint(symbol, timeframe="5min", limit=10, provider=None)`

Provides specialized order flow analysis, POC, CVD, and Delta values.

```python
import openstockapi as osapi
osapi.init("your_premium_api_key")

footprint = osapi.crypto_footprint(symbol="BTCUSDT", timeframe="5min", limit=2, provider="binance")
print(footprint)
```

**Sample Output:**
```json
{
  "symbol": "BTCUSDT",
  "timeframe": "5min",
  "session_profile": {
    "poc": 64230.0,
    "vah": 64300.0,
    "val": 64100.0,
    "total_vol": 500.0
  },
  "bars": [
    {
      "timestamp": "2026-07-22 01:00:00",
      "ohlc": { "open": 64200.0, "high": 64250.0, "low": 64180.0, "close": 64206.0 },
      "metrics": { "delta": 10.5, "cvd": 10.5, "total_vol": 120.0, "poc": 64203.78 },
      "price_levels": []
    }
  ],
  "provider": "binance",
  "market": "global",
  "asset_class": "crypto"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Yes** | — | Ticker symbol (e.g. `BTCUSDT`) |
| `timeframe` | `str` | No | `5min` | Timeframe resolution: `5min`, `15min`, `1hour` |
| `limit` | `int` | No | `10` | Number of footprint columns/bars to return |
| `provider` | `str` | No | `None` | Explicit provider: `"binance"`, `"bybit"`, `"okx"` |

---

## Use Case 8.6 — Fetch Supported Crypto Symbols

**Required Tier:** `Free`  
**API:** `crypto_symbols(provider=None)`

Retrieves a list of all supported cryptocurrency ticker symbols.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

symbols = osapi.crypto_symbols()
print(symbols)
```

**Sample Output:**
```json
{
  "symbols": [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
  ],
  "market": "global",
  "asset_class": "crypto"
}
```

---

## Use Case 8.7 — Fetch Real-Time Crypto Tickers

**Required Tier:** `Pro` ⭐  
**API:** `crypto_tickers(provider=None)`

Retrieves real-time ticker prices and percentage changes for all supported symbols.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

tickers = osapi.crypto_tickers(provider="okx")
print(tickers)
```

**Sample Output:**
```json
[
  {
    "symbol": "BTCUSDT",
    "price": 66083.68,
    "provider": "okx",
    "market": "global",
    "asset_class": "crypto"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | No | `None` | Explicit provider: `"binance"`, `"bybit"`, `"okx"`, `"bingx"` |

---

## Use Case 8.8 — Fetch Crypto Options Instruments

**Required Tier:** `Pro` ⭐  
**API:** `crypto_options_instruments(currency="BTC", kind="option", provider=None)`

Retrieves active option or future contracts.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

instruments = osapi.crypto_options_instruments(currency="BTC", kind="option", provider="okx")
print(instruments)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `currency` | `str` | No | `BTC` | Base currency: `BTC` or `ETH` |
| `kind` | `str` | No | `option` | Instrument type: `option` or `future` |
| `provider` | `str` | No | `None` | Explicit provider: `"deribit"`, `"okx"` |

---

## Use Case 8.9 — Fetch Crypto Options Chain

**Required Tier:** `Pro` ⭐  
**API:** `crypto_options_chain(currency="BTC", provider=None)`

Retrieves the options chain containing active strikes, bid/ask spreads, and implied volatilities (IV).

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

chain = osapi.crypto_options_chain(currency="BTC", provider="okx")
print(chain)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `currency` | `str` | No | `BTC` | Base currency: `BTC` or `ETH` |
| `provider` | `str` | No | `None` | Explicit provider: `"deribit"`, `"okx"` |

---

## Use Case 8.10 — Fetch Crypto Options Ticker & Greeks

**Required Tier:** `Pro` ⭐  
**API:** `crypto_options_ticker(instrument_name, provider=None)`

Retrieves detailed market data and Greeks (Delta, Gamma, Theta, Vega, Rho) for a specific contract.

```python
import openstockapi as osapi
osapi.init("your_pro_api_key")

ticker = osapi.crypto_options_ticker(instrument_name="BTC-USD-260726-60000-C", provider="okx")
print(ticker)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `instrument_name` | `str` | **Yes** | — | Options contract name (e.g. `BTC-USD-260726-60000-C`) |
| `provider` | `str` | No | `None` | Explicit provider: `"deribit"`, `"okx"` |

---

## Use Case 8.11 — Fetch Crypto News

**Required Tier:** `Free`  
**API:** `crypto_news(limit=20, provider=None)`  
**Unified API:** `company_news(symbol, limit=10, market="crypto")`

Retrieves the latest cryptocurrency news articles.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

news = osapi.crypto_news(limit=3, provider="cointelegraph")
print(news)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `20` | Maximum number of news items to return |
| `provider` | `str` | No | `None` | Explicit provider: `"cryptocompare"`, `"coindesk"`, `"cointelegraph"` |

---

## Use Case 8.12 — Fetch Crypto Calendar Events

**Required Tier:** `Free`  
**API:** `crypto_events(provider=None)`  
**Unified API:** `company_events(symbol, market="crypto")`

Retrieves global cryptocurrency calendar events.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

events = osapi.crypto_events(provider="coingecko")
print(events)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | No | `None` | Explicit provider: `"coingecko"` |

---

## Use Case 8.13 — Fetch Crypto Market Heatmap

**Required Tier:** `Free`  
**API:** `crypto_heatmap(limit=500, provider=None)`

Retrieves global cryptocurrency market heatmap data ranked by market cap. It returns top coins with price change percentages, market cap, and logos, cleaned and deduplicated from multiple exchanges.

```python
import openstockapi as osapi
osapi.init("free")

# Fetch top 5 cryptocurrencies for heatmap
heatmap = osapi.crypto_heatmap(limit=5, provider="tradingview")
print(heatmap)
```

#### Output Example

```json
[
  {
    "symbol": "BTC",
    "name": "Bitcoin / Dollar",
    "change": -0.09,
    "market_cap": 1311680803746.0,
    "sector": "Cryptocurrency",
    "industry": "Digital Asset",
    "logo_url": "https://s3-symbol-logo.tradingview.com/bitcoin.svg",
    "provider": "tradingview",
    "market": "global",
    "asset_class": "crypto"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | No | `500` | Maximum number of coins to return |
| `provider` | `str` | No | `None` | Explicit provider: `"tradingview"` |

