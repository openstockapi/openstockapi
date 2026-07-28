# 港股財務數據

## 使用場景 14.3 — 港股財務數據 (原始合併報表)

**所需權限層級:** `Free`

**API:** `hk_financials(symbol: str, period: str = "annual", provider: Optional[str] = None)`

獲取未經處理的合併財務報表及歷史報告期元數據。

### 代碼範例

```python
financials = osapi.hk_financials("0700", period="annual", provider="yahoo")
print(financials["available_periods"])
```

### 輸出範例

```json
{
  "symbol": "0700",
  "period_type": "annual",
  "available_periods": ["2025-12-31"],
  "periods": [
    {
      "period": "2025-12-31",
      "financials": {
        "balance_sheet": {
          "total_assets": 1501230000000.0,
          "total_liabilities": 650230000000.0
        },
        "income_statement": {
          "revenue": 609000000000.0,
          "net_income": 115000000000.0
        }
      }
    }
  ],
  "provider": "yahoo",
  "market": "hk",
  "asset_class": "stock"
}
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`)。 |
| `period` | `str` | 否 | `"annual"` | 財務報表報告頻率。有效選項: `"annual"`, `"quarterly"`。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.4 — 港股資產負債表 (Balance Sheet)

**所需權限層級:** `Free`

**API:** `hk_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None)`

獲取結構化的資產負債表數據。

### 代碼範例

```python
# 獲取騰訊年度資產負債表
bs = osapi.hk_balance_sheet("0700", period="annual", provider="yahoo")
print(bs)
```

### 輸出範例

```json
[
  {
    "symbol": "0700",
    "year": 2025,
    "quarter": null,
    "statement_type": "balance",
    "items": {
      "total_assets": 1501230000000.0,
      "total_liabilities": 650230000000.0
    },
    "provider": "yahoo",
    "market": "hk",
    "asset_class": "stock"
  }
]
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`)。 |
| `period` | `str` | 否 | `"annual"` | 財務報表報告頻率。有效選項: `"annual"`, `"quarterly"` (或 `"quarter"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.5 — 港股損益表 (Income Statement)

**所需權限層級:** `Free`

**API:** `hk_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None)`

獲取結構化的損益表數據。

### 代碼範例

```python
# 獲取騰訊年度損益表
inc = osapi.hk_income_statement("0700", period="annual", provider="yahoo")
print(inc)
```

### 輸出範例

```json
[
  {
    "symbol": "0700",
    "year": 2025,
    "quarter": null,
    "statement_type": "income",
    "items": {
      "revenue": 609000000000.0,
      "net_income": 115000000000.0
    },
    "provider": "yahoo",
    "market": "hk",
    "asset_class": "stock"
  }
]
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`)。 |
| `period` | `str` | 否 | `"annual"` | 財務報表報告頻率。有效選項: `"annual"`, `"quarterly"` (或 `"quarter"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.6 — 港股現金流量表 (Cash Flow)

**所需權限層級:** `Free`

**API:** `hk_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None)`

獲取結構化的現金流量表數據。

### 代碼範例

```python
# 獲取騰訊年度現金流量表
cf = osapi.hk_cashflow("0700", period="annual", provider="yahoo")
print(cf)
```

### 輸出範例

```json
[
  {
    "symbol": "0700",
    "year": 2025,
    "quarter": null,
    "statement_type": "cashflow",
    "items": {
      "operating_cash_flow": 180000000000.0
    },
    "provider": "yahoo",
    "market": "hk",
    "asset_class": "stock"
  }
]
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`)。 |
| `period` | `str` | 否 | `"annual"` | 財務報表報告頻率。有效選項: `"annual"`, `"quarterly"` (或 `"quarter"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.7 — 港股財務比率 (Financial Ratios)

**所需權限層級:** `Free`

**API:** `hk_ratios(symbol: str, provider: Optional[str] = None)`

獲取財務比率數據（市盈率、市淨率等）。

### 代碼範例

```python
ratios = osapi.hk_ratios("0700", provider="yahoo")
print(ratios["ratios"])
```

### 輸出範例

```json
{
  "symbol": "0700",
  "ratios": {
    "pe_trailing": 22.4,
    "pb": 4.1
  },
  "provider": "yahoo",
  "market": "hk",
  "asset_class": "stock"
}
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

