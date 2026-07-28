---
title: Getting Started with OpenStockAPI
description: Quick start guide and module index for openstockapi.
---

# Getting Started with OpenStockAPI

Welcome to **OpenStockAPI** — an open-source library (GNU AGPL-3.0) providing market data for Vietnamese stocks, international equities, cryptocurrency, and forex & commodities. Designed to run **entirely on your local machine** without a mandatory backend server.

Please review the [Disclaimer & Terms of Service](./terms_and_disclaimer.md) before use.

---

## Installation

```bash
pip install openstockapi
```

Optional: install with Pandas DataFrame support:

```bash
pip install openstockapi[pandas]
```

---

## Session Setup

```python
import openstockapi as osapi

# Free tier (no key required for public data)
osapi.init("free")

# Pro / Premium tier (use your API key)
osapi.init("YOUR_API_KEY")
```

---

## Tier Model (Access Control)

| Tier | Rate Limit | Features |
| :--- | :--- | :--- |
| `Free` | 30 req/min | VN Stock (OHLCV, Financial Statements, Company Profile, News, Mutual Funds, Macro), Crypto OHLCV, Forex Rates & OHLCV, Commodities Prices, Global Indices & ETFs, ASX / US / JP / CN / HK Stock data |
| `Pro` ⭐ | 200 req/min | **All Free** + VN Stock (Realtime Quote, Order Book, Block Trading, Derivatives), Crypto Depth & Derivatives & Leverage Simulation, Forex Rate Comparison, US/JP/CN/HK News & Events |
| `Premium` | 500 req/min | **All Pro** + Crypto Footprint & Delta Heatmap at higher rate limits |

---

## Module Index

### 🪙 Cryptocurrency

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 08 | [Crypto Market Data](./crypto/01_crypto_market_data.md) | Historical OHLCV, realtime tickers, order book depth, derivatives indicators, footprint heatmap, leverage simulation, options chain & Greeks, crypto news & events | Free / Pro / Premium |
| — | [Realtime WebSocket](./crypto/02_realtime_websocket.md) | Live price streaming via WebSocket | Pro |

> **Supported providers:** Binance, Bybit, OKX, BingX, Hyperliquid

---

### 💱 Forex & Commodities

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 09 | [Forex & Commodities Data](./forex/01_forex_market_data.md) | Exchange rates, historical OHLCV, gold/oil prices, global indices & ETFs, cross-source rate comparison, forex news & macro events | Free / Pro |

> **Supported providers:** ExchangeRate API, OpenExchangeRates, Yahoo Finance, Frankfurter, Bybit, OKX, BingX, ForexFactory, DailyFX, CNBC

---

### 🇦🇺 Australian Stock Exchange (ASX)

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 10 | [ASX Market Data](./asx/01_asx_market_data.md) | Listed securities, historical OHLCV, financial statements, dividends, announcements, company news | Free |

> **Supported providers:** Yahoo Finance, ASX Official Site (`asx.com.au`), Market Index, TradingView

---

### 🇺🇸 US Stock Market

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 11 | [US Market Data](./us_stock/01_us_market_data.md) | Historical OHLCV, company profile, financial statements, financial ratios, dividends, splits calendar, insider trades, institutional ownership, news & events | Free / Pro |

> **Supported providers:** Yahoo Finance (`yfinance`), Nasdaq, SEC EDGAR, OpenInsider, TradingView, Google News

---

### 🇯🇵 Japan Stock Exchange (TSE/JPX)

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 12 | [JP Market Data](./jp_stock/01_jp_market_data.md) | Listed securities, historical OHLCV, company profile, financial statements, financial ratios, dividends, splits calendar, news & events | Free / Pro |

> **Supported providers:** Yahoo Finance Japan (`yahoo_jp`), Google News (JP)

---

### 🇨🇳 China Stock Market (A-Share)

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 13 | [CN Market Data](./cn_stock/01_cn_market_data.md) | Listed securities, historical OHLCV, company profile, financial statements, financial ratios, dividends, splits calendar, realtime quote, order book & match history, news & events, heatmap | Free / Pro |

> **Supported providers:** Yahoo Finance China (`yahoo_cn`), Sina Finance, Tencent Finance, Google News (CN)

---

### 🇭🇰 Hong Kong Stock Exchange (HKEX)

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 14 | [HK Market Data](./hk_stock/01_hk_market_data.md) | Listed securities, historical OHLCV, company profile, financial statements, financial ratios, dividends, splits calendar, news & events, heatmap | Free / Pro |

> **Supported providers:** Yahoo Finance HK (`yahoo_hk`), Google News (HK)


### 🇻🇳 Vietnam Stock Market

| # | Module | Description | Tier |
| :--- | :--- | :--- | :--- |
| 01 | [Stock Market Data](./vn_stock/01_stock_market_data.md) | Historical OHLCV, company profile, realtime quote | Free / Pro |
| 02 | [Financial Statements](./vn_stock/02_financial_statements.md) | Balance sheet, income statement, cash flow, financial ratios | Free |
| 03 | [Block Trading](./vn_stock/03_block_trading.md) | Foreign, proprietary & insider block trades | **Pro** |
| 04 | [Order Book & Depth](./vn_stock/04_order_book.md) | Bid/Ask spread, market depth | **Pro** |
| 05 | [Macro Indicators](./vn_stock/05_macro_indicators.md) | M2 money supply, SBV credit data | Free |
| 06 | [Mutual Funds](./vn_stock/06_mutual_funds.md) | NAV, management fees, portfolio holdings | Free |
| 07 | [News & Events](./vn_stock/07_news_and_events.md) | Corporate news, dividend & event calendar | Free |
| 08 | [Derivatives](./vn_stock/08_derivatives.md) | Futures & covered warrants profile | **Pro** |

---


---

## Quick Example

```python
import openstockapi as osapi

# Initialize session (Pro tier example)
osapi.init("your_pro_api_key")

# 1. Vietnam Stock — historical OHLCV
vn_data = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-06-30")
print(f"VNM: {len(vn_data)} sessions fetched")

# 2. Cryptocurrency — candlestick data
crypto_data = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=3)
print(f"BTC last close: {crypto_data[-1]['close']} USD")

# 3. Forex — exchange rates
forex_data = osapi.forex_rates(base="USD", provider="exchangerate")
print(f"USD/VND: {forex_data['rates']['VND']}")

# 4. US Stock — company profile
profile = osapi.profile("AAPL", market="US")
print(f"Apple: {profile.full_name} ({profile.exchange})")

# 5. Crypto News
news = osapi.company_news("BTC", limit=3, market="crypto")
print(f"Crypto news: {len(news)} articles")
```

---

## Provider Architecture

OpenStockAPI fetches data **directly from source APIs** on your local machine — no intermediate backend required. Each market has its own provider module:

```
openstockapi/providers/
├── vn_stock/providers/    → dnse, kbs, vci, vndirect, mas, mbk, fmarket, tcbs, msn
├── crypto/providers/      → binance, bybit, okx, bingx, hyperliquid
├── forex/providers/       → exchangerate, openexchangerates, yahoo, frankfurter, bybit, okx, bingx
├── us_stock/providers/    → yahoo
├── jp_stock/providers/    → yahoo
├── cn_stock/providers/    → yahoo
├── hk_stock/providers/    → yahoo
└── asx/providers/         → yahoo
```

---

> This project is released under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. Users are responsible for complying with the Terms of Service of all upstream data providers. Contributions are welcome at [GitHub](https://github.com/openstockapi/openstockapi).
