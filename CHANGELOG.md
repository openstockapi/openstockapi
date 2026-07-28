# Changelog

All notable changes to the **OpenStockAPI** project will be documented in this file, adhering to the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standard.

---

## [v0.10.0] - 2026-07-25

### Added
- Integrated Chinese (CN Stock) and Hong Kong (HK Stock) stock markets into the system.
- Added API wrapper functions for CN Stock: `cn_symbols()`, `cn_ohlcv()`, `cn_profile()`, `cn_financials()`, `cn_balance_sheet()`, `cn_income_statement()`, `cn_cashflow()`, `cn_ratios()`, `cn_dividends()`, `cn_splits()`, `cn_calendar()`, `cn_news()`, `cn_quote()`, `cn_tick()`, `cn_order_book()`.
- Added API wrapper functions for HK Stock: `hk_symbols()`, `hk_ohlcv()`, `hk_profile()`, `hk_financials()`, `hk_balance_sheet()`, `hk_income_statement()`, `hk_cashflow()`, `hk_ratios()`, `hk_dividends()`, `hk_splits()`, `hk_calendar()`, `hk_news()`.
- Defined Pydantic models for CN & HK Stock in `openstockapi/core/models_cn.py` and `models_hk.py`.
- Created UAT test scripts `uat/run_uat_cn_stock.py` and `uat/run_uat_hk_stock.py`.
- Created user guides for CN Stock and HK Stock.
- Added sample scripts `example.py` and `sample_output.json` for JP, HK, and CN Stock markets in their respective guide folders (`user_guide/{jp,hk,cn}_stock/01_{jp,hk,cn}_market_data/`).
- Translated and localized user guides, terms and disclaimer files, and READMEs to Japanese (`JP`), Traditional Chinese for Hong Kong (`HK`), and Simplified Chinese for China (`CN`).

### Changed
- Updated the Gateway to route requests and configure priorities for CN and HK markets.
- Synchronized endpoint registrations in backend `license.py`.
- Split the combined financial statements use cases (Balance Sheet, Income Statement, Cash Flow) for JP, HK, and CN Stocks into 3 separate, distinct use cases as required.
- Updated all versions of README files (`README.md`, `README_VN.md`, `README_JP.md`, `README_HK.md`, `README_CN.md`) to include API listings, provider permissions, and user guide links for JP, CN, and HK markets.

---

## [v0.9.0] - 2026-07-24

### Added
- Integrated Japanese stock market (JP Stock).
- Added new API wrapper functions for JP Stock: `jp_symbols()`, `jp_ohlcv()`, `jp_profile()`, `jp_financials()`, `jp_balance_sheet()`, `jp_income_statement()`, `jp_cashflow()`, `jp_ratios()`, `jp_dividends()`, `jp_splits()`, `jp_calendar()`, `jp_news()`.
- Defined Pydantic models for JP Stock in `openstockapi/core/models_jp.py`.
- Created UAT test script `uat/run_uat_jp_stock.py`.
- Created user guide for JP Stock.

### Changed
- Updated the Gateway to route requests and configure priorities for JP market.

---

## [v0.8.0] - 2026-07-24

### Added
- Integrated US stock market (US Stock) into the system.
- Added new API wrapper functions: `us_ohlcv()`, `us_profile()`, `us_financials()`, `us_balance_sheet()`, `us_income_statement()`, `us_cashflow()`, `us_ratios()`, `us_dividends()`, `us_splits()`, `us_calendar()`, `us_news()`.
- Defined Pydantic models for US Stock in `openstockapi/core/models_us.py`.
- Created US market UAT test script at `uat/run_uat_us_stock.py`.
- Wrote user guide at `user_guide/us_stock/01_us_market_data.md`.

### Changed
- Updated `RequestGateway` to dispatch `stock.us.*` requests to `get_us_*` methods on the provider.
- Registered default permissions and priority for `US` market in `settings.py`.

---

## [v0.7.0] - 2026-07-24

### Added
- Integrated Australian stock market (ASX Market) into the system.
- Added new API wrapper functions: `asx_symbols()`, `asx_ohlcv()`, `asx_profile()`, `asx_balance_sheet()`, `asx_income_statement()`, `asx_cashflow()`, `asx_ratios()`, `asx_dividends()`, `asx_announcements()`, `asx_news()`.
- Defined Pydantic models for ASX in `openstockapi/core/models_asx.py`.
- Created ASX market UAT test script at `uat/run_uat_asx.py`.
- Wrote user guide at `user_guide/asx/01_asx_market_data.md`.

### Changed
- Updated `RequestGateway` to automatically dispatch `stock.au.*` requests to `get_asx_*` methods on the provider.
- Registered default permissions and priority for `AU` market in `settings.py`.
- Upgraded financial statement period classification logic in client (`period`) by dynamically matching the first character to clearly differentiate between annual (`annual`) and quarterly (`quarterly`) reports.

---

## [v0.6.0] - 2026-07-23

### Added
- Implemented fetching stock derivatives profile (`derivative_profile`) in `stock.py` for Vietnam market (Futures & covered warrants).
- Wrote derivative symbol converting algorithms and helpers to KRX format (`convert_derivative_symbol`) and asset classification (`get_asset_type`) in pure Python inside `utils.py` to be completely independent of `vnstock` library.
- Added `DerivativeProfile` Pydantic model in `models.py`.
- Added UAT test suite for Vietnam derivatives module in `run_uat_vn_stock.py`.
- Added user guide and demo script in `08_derivatives.md`.

---

## [v0.5.0] - 2026-07-23

### Added
- Implemented **Unified Request Gateway** (`RequestGateway` in `openstockapi/core/gateway.py`) as a centralized data routing engine.
- Configured provider priority centrally for all markets in `settings.py`.
- Automatically injected normalized metadata (`market` and `asset_class`) into all core Pydantic Models.
- Added `/v1/license/validate` endpoint on `be_mgt` backend for server-side validation of API keys, Data Tiers, and Rate Limits.

### Changed
- Refactored all API wrapper functions (`stock.py`, `crypto.py`, `forex.py`, `financial.py`, `orderbook.py`, `trading.py`, `news.py`, `macro.py`, `fund.py`) to run through the Gateway instead of calling providers directly.
- Updated unit test fixtures in `conftest.py` to support mocking and offline testing of `/validate` endpoint for the entire test suite.

---

## [v0.4.0] - 2026-07-23

### Added
- Integrated direct **WebSocket Real-Time Streaming** via the `CryptoStream` client class (`openstockapi/core/stream.py`).
- Supported asynchronous methods: `subscribe(symbol)`, `unsubscribe(symbol)`, and `close()`.
- Added `02_realtime_websocket.md` guide and `example_ws.py` test script for Crypto Stream.

### Changed
- Added `"websockets>=12.0"` as a core dependency in `pyproject.toml` to support real-time data streaming.

---

## [v0.3.2] - 2026-07-23

### Added
- Added `forex_news()` API to fetch Forex and global financial news from Core Engine (Tier: Free).
- Added `forex_events()` API to fetch global macroeconomic and event calendar from Core Engine (Tier: Free).
- Defined `ForexNewsEntry` and `ForexEventEntry` Pydantic models in `openstockapi/core/models_news.py`.

### Changed
- Updated `news()` wrapper (class `company_news`) and `events()` (class `company_events`) in `api/news.py` to route to Forex data when receiving parameter `market="forex"`.
- Added user guide and usage examples for Forex News & Events in `example.py`, `01_forex_market_data.md`, and `fe_integration_brief.md`.

---

## [v0.3.1] - 2026-07-23

### Added
- Added `crypto_news()` API to retrieve the latest cryptocurrency news from Core Engine (Tier: Free).
- Added `crypto_events()` API to retrieve global cryptocurrency calendar events from Core Engine (Tier: Free).
- Defined `CryptoNewsEntry` and `CryptoEventEntry` Pydantic models in `openstockapi/core/models_news.py`.

### Changed
- Updated `news()` and `events()` wrappers in `api/news.py` to automatically route to Crypto data if the parameter `market="crypto"` is provided.
- Added testing guide and executable examples for News & Events in `example.py` and `01_crypto_market_data.md`.

---

## [v0.3.0] - 2026-07-23

### Added
- Added `crypto_options_instruments()` API to get available options contracts list from Core Engine (Tier: Pro).
- Added `crypto_options_chain()` API to get full options chain with IV and Bid/Ask (Tier: Pro).
- Added `crypto_options_ticker()` API to get detailed quote and Greeks of option contract (Tier: Pro).
- Added data standardization guidelines in `Standardization Guide` (`docs/standardize_data/README.md`).

### Changed
- Standardized data outputs for all Crypto/Forex OHLCV and Depth APIs to Pydantic object formats (`OHLCVBar` and `OrderBook`) at the Provider Layer.
- Updated `volume` field to `float` for core models `OHLCVBar`, `OrderBookEntry`, `RealtimeQuote`, and `IntradayTick` to support Crypto/Forex.
- Updated `parse_date` helper in `utils.py` to support converting numeric millisecond epoch timestamps without crashing on Windows (`[Errno 22]`).
- Added data standardization step to the new service development checklist in `docs/development_checklist.md`.
- Updated `user_guide/crypto/01_crypto_market_data.md` to add documentation for Options use cases.

---

## [v0.2.3] - 2026-07-22

### Added
- Added `crypto_symbols()` API to fetch supported Crypto symbols list (Tier: Free).
- Added `crypto_tickers()` API to fetch real-time prices for all Crypto tickers (Tier: Pro).
- Added `forex_symbols()` API to fetch supported Forex pairs, commodities, and index ETFs list (Tier: Free).
- Added unit tests for `crypto_symbols()` and `forex_symbols()` in `tests/unit/`.
- Added UAT cases 8.6, 8.7 (Crypto) and 9.6 (Forex) in `run_uat_crypto.py` and `run_uat_forex.py`.
- Added Use Case 8.6, 8.7 into `user_guide/crypto/01_crypto_market_data.md`.
- Added Use Case 9.6 into `user_guide/forex/01_forex_market_data.md`.

### Changed
- Restructured Supported Providers table in `README.md` and `README_VN.md` into 3 groups: Vietnamese Stock Market, Cryptocurrency, Forex & Commodities.
- Updated `docs/development_checklist.md` to a complete 6-part version, including a Quick Reference diagram of files to edit when adding a new market.
- Updated `docs/release_checklist.md` to add a Security Check step for `.env.local`.

---

## [v0.2.2] - 2026-07-22

### Added
- Completed **Forex & Commodities** module:
  - `forex_rates(base)` — Forex spot rates (Free).
  - `forex_ohlcv(symbol, range_val, interval)` — Forex candlestick data (Free).
  - `commodities_prices(symbol, range_val, interval)` — Gold/Crude Oil prices (Free).
  - `global_indices_etf(symbol, range_val, interval)` — Global indices & US ETFs (Free).
  - `compare_rates(base)` — Compare multi-source interbank exchange rates (Pro).
- Added `user_guide/forex/01_forex_market_data.md` documentation with 5 complete Use Cases.
- Added Forex-specific UAT test suite: `uat/run_uat_forex.py`.
- Added unit tests `tests/unit/test_forex.py`.

### Changed
- Split UAT test suites into 3 separate files by market (`run_uat_vn_stock.py`, `run_uat_crypto.py`, `run_uat_forex.py`) and a master coordinator `run_uat.py -m <market>`.

---

## [v0.2.1] - 2026-07-22

### Added
- Completed **Cryptocurrency** module:
  - `crypto_ohlcv(symbol, interval, limit, market_type)` — Historical OHLCV (Free).
  - `async_crypto_ohlcv(...)` — Asynchronous OHLCV (Free).
  - `crypto_depth(symbol, limit)` — Order book depth (Pro).
  - `crypto_derivatives(symbol)` — Derivatives indicators OI & Funding Rate (Pro).
  - `crypto_footprint(symbol, timeframe, limit)` — Delta Footprint Heatmap (Premium).
  - `simulate_leverage(symbol, entry_price, leverage, position_size, direction)` — Margin/Leverage Position Simulator (Pro).
- Added `user_guide/crypto/01_crypto_market_data.md` documentation with 5 complete Use Cases.
- Added Crypto-specific UAT test suite: `uat/run_uat_crypto.py`.
- Added unit tests `tests/unit/test_crypto.py`.
- Added `.env.example` file for API key configurations.
- Added `.env.local` to `.gitignore` to protect local API keys.

### Changed
- Increased Free tier rate limit from 10 → **30 req/min**.
- Updated `user_guide/getting_started.md` to reflect new rate limits.

---

## [v0.2.0] - 2026-07-22

### Added
- Introduced **Handshake & JWT Session Token** authentication:
  - Client automatically calls `POST /v1/license/handshake` on initialization to retrieve a JWT session token.
  - All subsequent requests send `Authorization: Bearer <token>` instead of direct API Key.
  - Automatically generated Device Fingerprint using UUID.
  - Tiers (Free/Pro/Premium) are determined server-side from the database, rather than client-side key prefixes.
- Appended `version` parameter in Handshake payload.

### Changed
- `openstockapi/license/session.py`: Implemented `_handshake()` method calling the REST API.
- `openstockapi/providers/core.py`: Changed request header to `Authorization: Bearer <token>`.

---

## [v0.1.1] - 2026-07-21

### Added
- Added Multi-market support using `market="VN"` or `market="US"` parameter.
- Supported ticker symbol formats like `AAPL.US`, `VNM.VN`.
- Created automated User Acceptance Testing (UAT) script `uat/run_uat.py` exporting timestamped JSON results.
- Created PyPI packaging and automated publishing scripts: `scripts/publish.py` and `publish.ps1`.
- Added PyPI Re-deployment documentation at `docs/pyPI_redeployment/README.md`.

### Changed
- Allowed passing raw API Key strings directly into `set_current_session("YOUR_KEY")`.
- Reconfigured default provider priority (`DEFAULT_PROVIDER_PRIORITY`) grouped by market.

---

## [v0.1.0] - 2026-07-20

### Added
- Initialized open-source Data Plane project under GNU AGPL-3.0.
- Integrated Vietnamese Stock Market modules:
  - `stock`: Historical OHLCV, Company Profile, Realtime Quote.
  - `financial`: Balance Sheet, Income Statement, Cashflow Statement, Financial Ratios.
  - `trading`: Foreign, proprietary, and insider trading.
  - `orderbook`: Best bid/ask and order book depth.
  - `macro`: M2 money supply, banking credit growth.
