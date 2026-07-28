# US Stock Financials

## Use Case 11.3 — US Stock Financials

**Required Tier:** `Free`

**API:** `us_financials(symbol: str, period: str = "annual", provider: Optional[str] = None)`

Retrieve raw combined financial reports and historical periods metadata.

### Code Snippet

```python
financials = osapi.us_financials("AAPL", period="annual", provider="yahoo")
print(financials["available_periods"])
```

### Sample Output

```json
{
  "symbol": "AAPL",
  "period_type": "annual",
  "available_periods": ["2025-09-30"],
  "periods": [
    {
      "period": "2025-09-30",
      "financials": {
        "balance_sheet": {
          "total_assets": 359241000000.0,
          "total_liabilities": 285508000000.0
        },
        "income_statement": {
          "revenue": 391035000000.0,
          "net_income": 93736000000.0
        }
      }
    }
  ],
  "provider": "yahoo",
  "market": "us",
  "asset_class": "stock"
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `period` | `str` | No | `"annual"` | Reporting period of the financial statements. Valid choices: `"annual"`, `"quarterly"`. |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`, `"sec_edgar"`. |

---

## Use Case 11.4 — Split US Financial Statements

**Required Tier:** `Free`

**APIs:**
*   `us_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None)`
*   `us_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None)`
*   `us_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None)`
*   `us_ratios(symbol: str, period: str = "annual", provider: Optional[str] = None)`

Retrieve parsed financial statement reports structured identically to other market metrics.

### Code Snippet

```python
inc = osapi.us_income_statement("AAPL", period="annual", provider="sec_edgar")
print(inc)
```

### Sample Output

```json
[
  {
    "symbol": "AAPL",
    "year": 2025,
    "quarter": null,
    "statement_type": "income",
    "items": {
      "revenue": 391035000000.0,
      "net_income": 93736000000.0
    },
    "provider": "sec_edgar",
    "market": "us",
    "asset_class": "stock"
  }
]
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `period` | `str` | No | `"annual"` | Financial statement reporting frequency. Valid choices: `"annual"`, `"quarterly"` (or `"quarter"`). |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`, `"sec_edgar"`. |

---

## Use Case 11.5 — US Stock Dividends

**Required Tier:** `Free`

**API:** `us_dividends(symbol: str, provider: Optional[str] = None)`

Retrieve dividend disbursement history.

### Code Snippet

```python
divs = osapi.us_dividends("AAPL", provider="nasdaq")
print(divs["dividends"])
```

### Sample Output

```json
{
  "symbol": "AAPL",
  "dividends": [
    {
      "ex_date": "2026-05-11",
      "pay_date": null,
      "amount": 0.27,
      "type": "Dividend"
    }
  ],
  "provider": "nasdaq",
  "market": "us",
  "asset_class": "stock"
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`, `"nasdaq"`. |

---

## Use Case 11.6 — US Stock Splits

**Required Tier:** `Free`

**API:** `us_splits(symbol: str, provider: Optional[str] = None)`

Retrieve historical corporate stock split ratio timeline.

### Code Snippet

```python
splits = osapi.us_splits("AAPL", provider="yahoo")
print(splits["splits"])
```

### Sample Output

```json
{
  "symbol": "AAPL",
  "splits": [
    {
      "date": "2020-08-31",
      "ratio": 4.0
    }
  ],
  "provider": "yahoo",
  "market": "us",
  "asset_class": "stock"
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`. |

---

## Use Case 11.7 — US Stock Earnings & Corporate Calendar

**Required Tier:** `Free`

**API:** `us_calendar(symbol: str, provider: Optional[str] = None)`

Retrieve scheduled earnings release dates and dividend timeline.

### Code Snippet

```python
calendar = osapi.us_calendar("AAPL", provider="yahoo")
print(calendar["calendar"])
```

### Sample Output

```json
{
  "symbol": "AAPL",
  "calendar": {
    "Dividend Date": "2026-05-14",
    "Ex-Dividend Date": "2026-05-11",
    "Earnings Date": ["2026-07-31"]
  },
  "provider": "yahoo",
  "market": "us",
  "asset_class": "stock"
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`. |

---

