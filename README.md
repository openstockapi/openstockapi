<div align="center">
  <h1> OpenStockAPI</h1>
  <p><strong>A modular, multi-source Python Data Plane for Vietnamese & International financial market data.</strong></p>

  <p>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/v/openstockapi.svg?color=blue&label=PyPI" alt="PyPI version"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/dm/openstockapi.svg?color=brightgreen&label=Downloads" alt="Downloads"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/pyversions/openstockapi.svg" alt="Python Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL%203.0-orange.svg" alt="License"></a>
  </p>

  <p>
    <a href="./user_guide/getting_started.md"><strong> Read the Docs »</strong></a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=bug">Report Bug</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>📋 Table of Contents</summary>
  <ol>
    <li><a href="#about">About The Project</a></li>
    <li><a href="#features"> Features</a></li>
    <li><a href="#quick-start"> Quick Start</a></li>
    <li><a href="#installation"> Installation</a></li>
    <li><a href="#usage"> Usage & Documentation</a></li>
    <li><a href="#providers"> Supported Providers</a></li>
    <li><a href="#data-modules"> Data Modules</a></li>
    <li><a href="#roadmap"> Roadmap</a></li>
    <li><a href="#contributing"> Contributing</a></li>
    <li><a href="#changelog"> Changelog</a></li>
    <li><a href="#license"> License</a></li>
  </ol>
</details>

---

<a id="about"></a>
## About The Project

**OpenStockAPI** is an open-source Python library that acts as a modular **Data Plane** for collecting and standardizing financial data from multiple Vietnamese and international sources.

It is designed to be the upstream data acquisition layer for financial applications — handling provider fallback, rate limiting, and tier-based access control — so your application logic never has to worry about data source reliability.

> 📘 A Vietnamese version of this README is available: **[README_VN.md](./README_VN.md)**

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="features"></a>
## Features

- ** Multi-market & Multi-asset Support** — Covers Vietnamese (`VN`) equities, Cryptocurrencies (`Crypto`), and Forex & Commodities.
- ** Automatic Multi-source Fallback** — Integrates providers (KBS, VCI, MSN, MAS, Maybank, Fmarket, Core Engine) with transparent automatic failover when any source is unavailable.
- ** JWT Handshake & Freemium Tier Access Control** — Supports short-lived JWT session token verification and `Free`, `Pro`, and `Premium` tier rate limits via a client-side Token Bucket Limiter.
- ** Async Support** — First-class `async/await` support via `async_ohlcv()` and `async_crypto_ohlcv()` for high-throughput data pipelines.

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="quick-start"></a>
## Quick Start

```python
import openstockapi as osapi

# Initialize with your API key (required for all tiers)
# Register for free at: https://openstockapi.com/register
osapi.init("free_YOUR_KEY")   # or "pro_YOUR_KEY" / "premium_YOUR_KEY"

# Historical OHLCV price data
df = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-12-31")
print(df.head())

# Fetch Cryptocurrency data
btc_ohlcv = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=5)
print(btc_ohlcv)

# Fetch Forex & Commodities data
rates = osapi.forex_rates(base="USD")
gold_price = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h")
print(f"USD/VND: {rates['rates']['VND']} | Gold: {gold_price['regularMarketPrice']} USD")
```

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="installation"></a>
## Installation

**Minimum install:**
```bash
pip install openstockapi
```

**With Pandas DataFrame & Excel export support:**
```bash
pip install openstockapi[pandas]
```

**Requirements:** Python 3.8+

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="usage"></a>
## Usage & Documentation

Full documentation, use case examples, and sample outputs are available in the User Guide:

 **[User Guide — Getting Started](./user_guide/getting_started.md)**

| Category | Module / Guide | Description |
|----------|----------------|-------------|
| **Vietnamese Stock** | [01 — Stock Market Data](./user_guide/vn_stock/01_stock_market_data.md) | Historical OHLCV, company profile, realtime quotes |
| **Cryptocurrency** | [08 — Crypto Market Data](./user_guide/crypto/01_crypto_market_data.md) | Crypto OHLCV, depth, derivatives, delta footprint, leverage simulation |
| **Forex & Commodities** | [09 — Forex Market Data](./user_guide/forex/01_forex_market_data.md) | Exchange rates, Forex OHLCV, commodities (Gold/Crude Oil), global indices |
| **Australian Stock** | [10 — Dữ Liệu Chứng Khoán Úc](./user_guide/asx/01_asx_market_data.md) | ASX symbols list, OHLCV, company profile, balance sheet, income statement, cashflow, ratios, dividends, announcements, news |
| **US Stock** | [11 — US Stock Market Data](./user_guide/us_stock/01_us_market_data.md) | US Stock OHLCV, company profile, financials, balance sheet, income statement, cashflow, ratios, dividends, splits, calendar, news |
| **Japanese Stock** | [12 — JP Stock Market Data](./user_guide/jp_stock/01_jp_market_data.md) | JP Stock symbols list, OHLCV, company profile, balance sheet, income statement, cashflow, ratios, dividends, splits, calendar, news |
| **China Stock** | [13 — CN Stock Market Data](./user_guide/cn_stock/01_cn_market_data.md) | CN Stock symbols list, OHLCV, company profile, balance sheet, income statement, cashflow, ratios, dividends, splits, realtime quote, order book, ticks, heatmap |
| **HK Stock** | [14 — HK Stock Market Data](./user_guide/hk_stock/01_hk_market_data.md) | HK Stock symbols list, OHLCV, company profile, balance sheet, income statement, cashflow, ratios, dividends, splits, calendar, news, heatmap |


<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="providers"></a>
## Supported Providers

Providers are grouped by market/asset class. Within each group, they are tried in priority order — if one fails, the next is used automatically.

### Vietnamese Stock Market
| Provider | Source | Tier | Data Types |
|---|---|---|---|
| `kbs` | KB Securities Vietnam | Free | OHLCV, Company Profile, News, Events |
| `vci` | Vietcap Securities | Free | OHLCV, Profile, Financial Statements, Insider/Foreign/Prop Trading, Events |
| `msn` | MSN Finance (Bing) | Free | OHLCV (VN & International) |
| `mas` | MAS (Mass Asset Securities) | Free | Financial Statements, Financial Ratios |
| `mbk` | Maybank Securities Vietnam | Free | Macro Indicators (M2, Credit Growth) |
| `fmarket` | Fmarket Vietnam | Free | Mutual Fund NAV & Portfolio Holdings |
| `tcbs` | TCBS (Techcom Securities) | Free | Realtime Quote, Order Book Depth |

### Cryptocurrency

Crypto data is sourced through the **OpenStockAPI Core Engine** — a managed, closed-source aggregation layer with automatic multi-provider failover and normalization. The specific upstream exchanges and data sources are not disclosed.

| Capability | Tier |
|---|---|
| Crypto OHLCV (historical klines) | Free |
| Crypto OHLCV (async) | Free |
| Order Book Depth | Pro |
| Derivatives Indicators (OI, Funding Rate) | Pro |
| Delta Footprint Heatmap | Premium |
| Leverage & Margin Simulation | Pro |
| Supported Symbols List | Free |
| Realtime Tickers | Pro |
| Options Instruments List | Pro |
| Options Chain (Strikes, IV, Bid/Ask) | Pro |
| Options Ticker & Greeks | Pro |
| Crypto Market Heatmap | Free |

### Forex & Commodities

Forex and Commodities data is sourced through the **OpenStockAPI Core Engine** with automatic fallback across multiple rate and price providers. Specific upstream sources are not disclosed.

| Forex Spot Rates | Free |
| Forex OHLCV | Free |
| Commodities Prices (Gold, Oil, etc.) | Free |
| Global Indices & ETF (SPY, QQQ) | Free |
| Cross-broker Rate Comparison | Pro |
| Supported Forex Symbols List | Free |
| Forex & Financial News | Free |
| Global Macro Events Calendar | Free |

### Australian Stock Market
| Provider | Source | Tier | Data Types |
|---|---|---|---|
| `core` | Core Engine | Free | Symbols, OHLCV, Profile, Financials, Dividends, Announcements, News |

### US Stock Market
| Provider | Source | Tier | Data Types |
|---|---|---|---|
| `core` | Core Engine | Free | OHLCV, Profile, Financials, Dividends, Splits, Calendar, News |

### Japanese Stock Market
| Provider | Source | Tier | Data Types |
|---|---|---|---|
| `core` | Core Engine | Free | Symbols, OHLCV, Profile, Financials (Balance Sheet, Income Statement, Cashflow, Ratios), Dividends, Splits, Calendar, News |

### China Stock Market
| Provider | Source | Tier | Data Types |
|---|---|---|---|
| `core` | Core Engine | Free / Pro | Symbols, OHLCV, Profile, Financials (Balance Sheet, Income Statement, Cashflow, Ratios), Dividends, Splits (Free); Realtime Quote, Order Book, Ticks (Pro) |

### HK Stock Market
| Provider | Source | Tier | Data Types |
|---|---|---|---|
| `core` | Core Engine | Free | Symbols, OHLCV, Profile, Financials (Balance Sheet, Income Statement, Cashflow, Ratios), Dividends, Splits, Calendar, News |

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>


---

<a id="data-modules"></a>
## Data Modules Overview

```
openstockapi
├── ohlcv()                  # Historical Stock OHLCV (sync)
├── async_ohlcv()            # Historical Stock OHLCV (async)
├── profile()                # Stock Company profile
├── derivative_profile()     # Stock Derivatives (Futures/Warrants) profile
├── balance_sheet()          # Stock Balance sheet
├── income_statement()       # Stock Income statement
├── cashflow()               # Stock Cash flow statement
├── ratios()                 # Stock Financial ratios
├── quote()                  # Stock Realtime price quote
├── order_book()             # Stock Order book depth
├── market_index()           # Stock Market index OHLCV
├── macro_indicators()       # Macroeconomic data
├── fund_details()           # Stock Mutual fund info
├── company_news()           # Stock Corporate news (supports routing to Crypto/Forex via market param)
├── company_events()         # Stock Corporate events (supports routing to Crypto/Forex via market param)
├── vn_heatmap()             # VN Stock Market Heatmap data & logos
│
├── crypto_ohlcv()           # Historical Crypto OHLCV (sync)
├── async_crypto_ohlcv()     # Historical Crypto OHLCV (async)
├── crypto_depth()           # Crypto Order book depth
├── crypto_derivatives()     # Crypto Derivatives indicators
├── crypto_footprint()       # Crypto Delta footprint heatmap
├── simulate_leverage()      # Crypto Margin/leverage position simulator
├── crypto_symbols()         # Supported Crypto symbols list
├── crypto_tickers()         # Realtime Crypto tickers list
├── crypto_options_instruments() # Supported Crypto Options list
├── crypto_options_chain()   # Crypto Options chain data
├── crypto_options_ticker()  # Crypto Options detailed Greeks
├── crypto_news()            # Crypto News articles
├── crypto_events()          # Crypto Calendar events
├── crypto_profile()         # Crypto Token profile & logo
├── crypto_heatmap()         # Cryptocurrency market Heatmap
├── CryptoStream             # Realtime WebSocket streaming client
│
├── forex_rates()            # Forex Exchange rates
├── forex_ohlcv()            # Historical Forex OHLCV
├── commodities_prices()     # Commodities Prices (Gold, Oil)
├── global_indices_etf()     # Global indices and ETFs (SPY, QQQ)
├── compare_rates()          # Forex cross-broker arbitrage rates comparison
├── forex_symbols()          # Supported Forex symbols list
├── forex_news()             # Forex & Financial News articles
├── forex_events()           # Global Macro Events Calendar
├── forex_profile()          # Forex Currency Pair profile & cdn flags
│
├── asx_symbols()            # Supported ASX symbols list
├── asx_ohlcv()              # Historical ASX OHLCV
├── asx_profile()            # ASX Company profile
├── asx_balance_sheet()      # ASX Balance sheet
├── asx_income_statement()   # ASX Income statement
├── asx_cashflow()           # ASX Cash flow statement
├── asx_ratios()             # ASX Financial ratios
├── asx_dividends()          # ASX Dividend history
├── asx_announcements()      # ASX PDF announcements feed
├── asx_news()               # ASX Company news
├── asx_heatmap()            # ASX Market Heatmap data & logos
│
├── us_ohlcv()               # Historical US Stock OHLCV
├── us_profile()             # US Stock Company profile
├── us_financials()          # US Stock Financial statements
├── us_balance_sheet()       # US Stock Balance sheet
├── us_income_statement()    # US Stock Income statement
├── us_cashflow()            # US Stock Cash flow statement
├── us_ratios()              # US Stock Financial ratios
├── us_dividends()           # US Stock Dividend history
├── us_splits()              # US Stock Stock split history
├── us_calendar()            # US Stock Corporate calendar
├── us_news()                # US Stock Company news
├── us_heatmap()             # US Stock Market Heatmap data & logos
│
├── jp_symbols()             # JP Stock symbols list
├── jp_ohlcv()               # Historical JP Stock OHLCV
├── jp_profile()             # JP Stock Company profile
├── jp_financials()          # JP Stock Financial statements
├── jp_balance_sheet()       # JP Stock Balance sheet
├── jp_income_statement()    # JP Stock Income statement
├── jp_cashflow()            # JP Stock Cash flow statement
├── jp_ratios()              # JP Stock Financial ratios
├── jp_dividends()           # JP Stock Dividend history
├── jp_splits()              # JP Stock Stock split history
├── jp_calendar()            # JP Stock Corporate calendar
├── jp_news()                # JP Stock Company news
├── jp_heatmap()             # JP Stock Market Heatmap data & logos
│
├── cn_symbols()             # CN Stock symbols list
├── cn_ohlcv()               # Historical CN Stock OHLCV
├── cn_profile()             # CN Stock Company profile
├── cn_financials()          # CN Stock Financial statements
├── cn_balance_sheet()       # CN Stock Balance sheet
├── cn_income_statement()    # CN Stock Income statement
├── cn_cashflow()            # CN Stock Cash flow statement
├── cn_ratios()              # CN Stock Financial ratios
├── cn_dividends()           # CN Stock Dividend history
├── cn_splits()              # CN Stock Stock split history
├── cn_quote()               # CN Stock Realtime price quote (Pro)
├── cn_order_book()          # CN Stock Order book depth (Pro)
├── cn_tick()                # CN Stock Intraday ticks (Pro)
├── cn_heatmap()             # CN Stock Market Heatmap data & logos
│
├── hk_symbols()             # HK Stock symbols list
├── hk_ohlcv()               # Historical HK Stock OHLCV
├── hk_profile()             # HK Stock Company profile
├── hk_financials()          # HK Stock Financial statements
├── hk_balance_sheet()       # HK Stock Balance sheet
├── hk_income_statement()    # HK Stock Income statement
├── hk_cashflow()            # HK Stock Cash flow statement
├── hk_ratios()              # HK Stock Financial ratios
├── hk_dividends()           # HK Stock Dividend history
├── hk_splits()              # HK Stock Stock split history
├── hk_calendar()            # HK Stock Corporate calendar
├── hk_heatmap()             # HK Stock Market Heatmap data & logos
└── hk_news()                # HK Stock Company news

```

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="roadmap"></a>
## Roadmap

- [x] Vietnamese equity OHLCV (KBS, VCI, MSN)
- [x] Financial statements (MAS, VCI)
- [x] Macroeconomic indicators (World Bank, Maybank)
- [x] Mutual fund data (Fmarket)
- [x] Corporate news & events (KBS, VCI)
- [x] Cryptocurrency data (Core Engine)
- [x] Crypto Options data (Deribit, OKX)
- [x] Forex & Commodities data (Core Engine)
- [x] Australian equity market data (ASX)
- [x] US equity market data (US)
- [ ] WebSocket streaming quotes

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="contributing"></a>
## Contributing

Contributions are welcome! If you'd like to add a new data provider, please use our **Connector Development Kit (CDK)** which automates boilerplate code generation and validation.

For a step-by-step guide on how to add a provider using CDK, please refer to the **[CDK Contributor Guide](./CONTRIBUTING.md)**.

General workflow:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-provider`
3. Generate provider template: `openstock-cdk generate --name <name> --market <market> --type <type>`
4. Implement your API parser logic and write tests
5. Run tests: `pytest tests/cdk/ -v`
6. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="changelog"></a>
## Changelog

See all version updates, new features, and bug fixes at:

 **[CHANGELOG.md](./CHANGELOG.md)**

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="license"></a>
## License

Distributed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See [`LICENSE`](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>
