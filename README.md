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

- ** Multi-market Support** — Covers Vietnamese (`VN`) equities and can be extended to International (`US`) markets with the same API.
- ** Automatic Multi-source Fallback** — Integrates providers (KBS, VCI, MSN, MAS, Maybank, Fmarket) with transparent automatic failover when any source is unavailable.
- ** Freemium Tier Access Control** — Supports `Free`, `Pro` (200 req/min), and `Premium` (500 req/min) tiers with a client-side Token Bucket Rate Limiter.
- ** Async Support** — First-class `async/await` support via `async_ohlcv()` for high-throughput data pipelines.

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

# Company financial statements
bs = osapi.balance_sheet("VNM", period="annual")

# Realtime market quote
quote = osapi.quote("HPG")
print(f"{quote.symbol}: {quote.price:,.0f} VND ({quote.pct_change:+.2f}%)")

# Corporate news & events
news   = osapi.company_news("FPT", limit=5)
events = osapi.company_events("FPT", limit=5)
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

| Module | Description | Guide |
|--------|-------------|-------|
| 01 — OHLCV & Profile | Historical price data, company profile | [](./user_guide/01_stock_market_data.md) |
| 02 — Financial Statements | Balance sheet, income, cash flow, ratios | [](./user_guide/02_financial_statements.md) |
| 03 — Realtime Quote | Live price, order book depth | [](./user_guide/03_realtime_quote.md) |
| 04 — Market Indices | VNINDEX, VN30 constituents | [](./user_guide/04_order_book.md) |
| 05 — Macro Indicators | CPI, M2 money supply, credit growth | [](./user_guide/05_macro_indicators.md) |
| 06 — Mutual Funds | Fund NAV, portfolio holdings | [](./user_guide/06_mutual_funds.md) |
| 07 — News & Events | Corporate news, dividends, events | [](./user_guide/07_news_and_events.md) |

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="providers"></a>
## Supported Providers

| Provider | Source | Tier | Data Types |
|----------|--------|------|------------|
| `kbs` | KB Securities Vietnam | Free | OHLCV, Profile, News, Events |
| `vci` | Vietcap Securities | Free | OHLCV, Profile, Financial Statements, Insider/Foreign/Prop Trading, Events |
| `msn` | MSN Finance (Bing) | Free | OHLCV (VN & International) |
| `mas` | MAS (Mass Asset Securities) | Free | Financial Statements, Ratios |
| `mbk` | Maybank Securities Vietnam | Free | Macro Indicators (M2, Credit) |
| `fmarket` | Fmarket Vietnam | Free | Mutual Fund NAV & Holdings |
| `tcbs` | TCBS (Techcom Securities) | Free | Realtime Quote, Order Book |

> Providers are tried in priority order per data type. If one fails, the next is used automatically.

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="data-modules"></a>
## Data Modules Overview

```
openstockapi
├── ohlcv()                  # Historical OHLCV (sync)
├── async_ohlcv()            # Historical OHLCV (async)
├── profile()                # Company profile
├── balance_sheet()          # Balance sheet
├── income_statement()       # Income statement
├── cashflow()               # Cash flow statement
├── ratios()                 # Financial ratios (PE, PB, ROE...)
├── quote()                  # Realtime price quote
├── order_book()             # Order book depth
├── market_index()           # Market index OHLCV
├── index_constituents()     # Index member list
├── macro_indicators()       # Macroeconomic data
├── fund_details()           # Mutual fund info
├── company_news()           # Corporate news
└── company_events()         # Corporate events (dividends, ESOP...)
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
- [ ] International equity OHLCV
- [ ] Cryptocurrency data
- [ ] Derivatives / Futures data
- [ ] WebSocket streaming quotes

<p align="right">(<a href="#readme-top">back to top ↑</a>)</p>

---

<a id="contributing"></a>
## Contributing

Contributions are welcome! If you'd like to add a new provider, fix a bug, or improve documentation:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-provider`
3. Commit your changes
4. Open a Pull Request

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
