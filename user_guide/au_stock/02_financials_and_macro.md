# AU Stock Financials

## Use Case 10.3 — Get Company Profile (ASX Company Profile)

**Required Tier:** `Free`  
**API:** `asx_profile(symbol, provider=None)`

Retrieves corporate information and general profile metadata for a listed company.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

profile = osapi.asx_profile(symbol="BHP", provider="yahoo")
print(profile)
```

**Sample Output:**
```json
{
  "symbol": "BHP",
  "company_name": "BHP Group Limited",
  "exchange": "ASX",
  "industry": "Other Industrial Metals & Mining",
  "description": "BHP Group Limited operates as a resources company in Australia, Europe, China, Japan, India, North America, and internationally...",
  "provider": "yahoo"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo`, `asx` |

---

## Use Case 10.4 — Get Balance Sheet (ASX Balance Sheet)

**Required Tier:** `Free`  
**API:** `asx_balance_sheet(symbol, period="annual", provider=None)`

Retrieves historical Balance Sheet statements for the given symbol.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

df_bs = osapi.asx_balance_sheet(symbol="BHP", period="annual", provider="yahoo")
print(df_bs.head(1))
```

**Sample Output:**
```json
[
  {
    "symbol": "BHP",
    "year": 2025,
    "quarter": 2,
    "statement_type": "balance",
    "items": {
      "total_assets": 108790000000.0,
      "current_assets": 22830000000.0,
      "cash_and_equivalents": 11769000000.0,
      "total_liabilities": 56572000000.0,
      "total_equity": 52218000000.0
    },
    "provider": "yahoo",
    "market": "au",
    "asset_class": "stock"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `period` | `str` | No | `annual` | Statement period: `annual` or `quarter` |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo`, `marketindex` |

---

## Use Case 10.5 — Get Income Statement (ASX Income Statement)

**Required Tier:** `Free`  
**API:** `asx_income_statement(symbol, period="annual", provider=None)`

Retrieves historical Income Statement statements for the given symbol.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

df_inc = osapi.asx_income_statement(symbol="BHP", period="annual", provider="yahoo")
print(df_inc.head(1))
```

**Sample Output:**
```json
[
  {
    "symbol": "BHP",
    "year": 2025,
    "quarter": 2,
    "statement_type": "income",
    "items": {
      "total_revenue": 55700000000.0,
      "gross_profit": 42100000000.0,
      "net_income": 12900000000.0
    },
    "provider": "yahoo",
    "market": "au",
    "asset_class": "stock"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `period` | `str` | No | `annual` | Statement period: `annual` or `quarter` |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo`, `marketindex` |

---

## Use Case 10.6 — Get Cashflow Statement (ASX Cashflow)

**Required Tier:** `Free`  
**API:** `asx_cashflow(symbol, period="annual", provider=None)`

Retrieves historical Cash Flow statements for the given symbol.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

df_cf = osapi.asx_cashflow(symbol="BHP", period="annual", provider="yahoo")
print(df_cf.head(1))
```

**Sample Output:**
```json
[
  {
    "symbol": "BHP",
    "year": 2025,
    "quarter": 2,
    "statement_type": "cashflow",
    "items": {
      "operating_cash_flow": 18400000000.0,
      "capital_expenditure": -9200000000.0,
      "free_cash_flow": 9200000000.0
    },
    "provider": "yahoo",
    "market": "au",
    "asset_class": "stock"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `period` | `str` | No | `annual` | Statement period: `annual` or `quarter` |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo`, `marketindex` |

---

## Use Case 10.7 — Get Financial Ratios (ASX Ratios)

**Required Tier:** `Free`  
**API:** `asx_ratios(symbol, provider=None)`

Retrieves general valuation and financial ratios metrics.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

df_ratios = osapi.asx_ratios(symbol="BHP", provider="yahoo")
print(df_ratios)
```

**Sample Output:**
```json
[
  {
    "symbol": "BHP",
    "year": 2026,
    "quarter": null,
    "statement_type": "ratios",
    "items": {
      "pe_trailing": 20.43,
      "peg_ratio": 1.25,
      "dividend_yield": 0.054
    },
    "provider": "yahoo",
    "market": "au",
    "asset_class": "stock"
  }
]
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo`, `marketindex` |

---

