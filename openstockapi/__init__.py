__version__ = "0.13.10"

# ── Core stock API (multi-market, routed via `market` param) ──────────────────
from openstockapi.api.stock import ohlcv, profile, quote, async_ohlcv, derivative_profile, symbols, heatmap
from openstockapi.api.financial import income_statement, balance_sheet, cashflow, ratios, dividends, splits, calendar
from openstockapi.api.trading import foreign, insider, prop_trade
from openstockapi.api.orderbook import bid_ask, depth, ticks
from openstockapi.api.macro import indicators
from openstockapi.api.fund import details as fund_details
from openstockapi.api.news import news as company_news, events as company_events

# ── Market-specific helper functions (for backward compatibility) ─────────────
from openstockapi.api.asx import asx_symbols, asx_ohlcv, asx_profile, asx_financials, asx_dividends, asx_announcements, asx_news, asx_balance_sheet, asx_income_statement, asx_cashflow, asx_ratios, asx_heatmap
from openstockapi.api.us_stock import us_symbols, us_ohlcv, us_profile, us_financials, us_balance_sheet, us_income_statement, us_cashflow, us_ratios, us_dividends, us_splits, us_calendar, us_news, us_heatmap
from openstockapi.api.jp_stock import jp_symbols, jp_ohlcv, jp_profile, jp_financials, jp_balance_sheet, jp_income_statement, jp_cashflow, jp_ratios, jp_dividends, jp_splits, jp_calendar, jp_news, jp_heatmap
from openstockapi.api.cn_stock import cn_symbols, cn_ohlcv, cn_profile, cn_financials, cn_balance_sheet, cn_income_statement, cn_cashflow, cn_ratios, cn_dividends, cn_splits, cn_calendar, cn_news, cn_quote, cn_tick, cn_order_book, cn_heatmap
from openstockapi.api.hk_stock import hk_symbols, hk_ohlcv, hk_profile, hk_financials, hk_balance_sheet, hk_income_statement, hk_cashflow, hk_ratios, hk_dividends, hk_splits, hk_calendar, hk_news, hk_heatmap

# ── Crypto ────────────────────────────────────────────────────────────────────
from openstockapi.api.crypto import (
    crypto_ohlcv, async_crypto_ohlcv, crypto_depth, crypto_derivatives,
    crypto_footprint, simulate_leverage, crypto_symbols, crypto_tickers,
    crypto_options_instruments, crypto_options_chain, crypto_options_ticker,
    crypto_news, crypto_events, crypto_profile, crypto_heatmap,
)

# ── Forex ─────────────────────────────────────────────────────────────────────
from openstockapi.api.forex import (
    forex_rates, forex_ohlcv, commodities_prices, global_indices_etf,
    compare_rates, forex_symbols, forex_news, forex_events, forex_profile,
)

# ── Session / core ────────────────────────────────────────────────────────────
from openstockapi.core import exceptions
from openstockapi.license.session import init, set_current_session
from openstockapi.license import session
from openstockapi.core.stream import CryptoStream

__all__ = [
    # Stock - common (multi-market)
    "ohlcv",
    "async_ohlcv",
    "profile",
    "derivative_profile",
    "quote",
    "symbols",
    "heatmap",
    # Financial - common (multi-market)
    "income_statement",
    "balance_sheet",
    "cashflow",
    "ratios",
    "dividends",
    "splits",
    "calendar",
    # Trading / orderbook
    "foreign",
    "insider",
    "prop_trade",
    "bid_ask",
    "depth",
    "ticks",
    # Macro / fund / news
    "indicators",
    "fund_details",
    "company_news",
    "company_events",
    # Market-specific helpers
    "asx_symbols",
    "asx_ohlcv",
    "asx_profile",
    "asx_financials",
    "asx_balance_sheet",
    "asx_income_statement",
    "asx_cashflow",
    "asx_ratios",
    "asx_dividends",
    "asx_announcements",
    "asx_news",
    "asx_heatmap",
    "us_symbols",
    "us_ohlcv",
    "us_profile",
    "us_financials",
    "us_balance_sheet",
    "us_income_statement",
    "us_cashflow",
    "us_ratios",
    "us_dividends",
    "us_splits",
    "us_calendar",
    "us_news",
    "us_heatmap",
    "jp_symbols",
    "jp_ohlcv",
    "jp_profile",
    "jp_financials",
    "jp_balance_sheet",
    "jp_income_statement",
    "jp_cashflow",
    "jp_ratios",
    "jp_dividends",
    "jp_splits",
    "jp_calendar",
    "jp_news",
    "jp_heatmap",
    "cn_symbols",
    "cn_ohlcv",
    "cn_profile",
    "cn_financials",
    "cn_balance_sheet",
    "cn_income_statement",
    "cn_cashflow",
    "cn_ratios",
    "cn_dividends",
    "cn_splits",
    "cn_calendar",
    "cn_news",
    "cn_quote",
    "cn_tick",
    "cn_order_book",
    "cn_heatmap",
    "hk_symbols",
    "hk_ohlcv",
    "hk_profile",
    "hk_financials",
    "hk_balance_sheet",
    "hk_income_statement",
    "hk_cashflow",
    "hk_ratios",
    "hk_dividends",
    "hk_splits",
    "hk_calendar",
    "hk_news",
    "hk_heatmap",
    # Crypto
    "crypto_ohlcv",
    "async_crypto_ohlcv",
    "crypto_depth",
    "crypto_derivatives",
    "crypto_footprint",
    "simulate_leverage",
    "crypto_symbols",
    "crypto_tickers",
    "crypto_options_instruments",
    "crypto_options_chain",
    "crypto_options_ticker",
    "crypto_news",
    "crypto_events",
    "crypto_profile",
    "crypto_heatmap",
    # Forex
    "forex_rates",
    "forex_ohlcv",
    "commodities_prices",
    "global_indices_etf",
    "compare_rates",
    "forex_symbols",
    "forex_news",
    "forex_events",
    "forex_profile",
    # Session
    "init",
    "set_current_session",
    "CryptoStream",
]
