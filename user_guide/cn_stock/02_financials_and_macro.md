# A股財務數據

## 使用场景 13.3 — A股财务数据 (原始合并报表)

**所需权限层级:** `Free`

**API:** `cn_financials(symbol: str, period: str = "annual", provider: Optional[str] = None)`

获取未经处理的合并财务报表及历史报告期元数据。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_free_api_key")

# 获取贵州茅台年度财务报表
financials = osapi.cn_financials("600519", period="annual", provider="yahoo")
print(financials["available_periods"])
```

### 输出示例

```json
{
  "symbol": "600519",
  "period_type": "annual",
  "available_periods": ["2025-12-31"],
  "periods": [
    {
      "period": "2025-12-31",
      "financials": {
        "balance_sheet": {
          "total_assets": 280000000000.0,
          "total_liabilities": 50000000000.0
        },
        "income_statement": {
          "revenue": 150000000000.0,
          "net_income": 75000000000.0
        }
      }
    }
  ],
  "provider": "yahoo",
  "market": "cn",
  "asset_class": "stock"
}
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (example: `"600519"`)。 |
| `period` | `str` | 否 | `"annual"` | 财务报表报告频率。有效选项: `"annual"`, `"quarterly"`. |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

## 使用场景 13.4 — A股资产负债表 (Balance Sheet)

**所需权限层级:** `Free`

**API:** `cn_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None)`

获取结构化的资产负债表数据。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_free_api_key")

# 获取贵州茅台年度资产负债表
bs = osapi.cn_balance_sheet("600519", period="annual", provider="yahoo")
print(bs)
```

### 输出示例

```json
[
  {
    "symbol": "600519",
    "year": 2025,
    "quarter": null,
    "statement_type": "balance",
    "items": {
      "total_assets": 280000000000.0,
      "total_liabilities": 50000000000.0
    },
    "provider": "yahoo",
    "market": "cn",
    "asset_class": "stock"
  }
]
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `period` | `str` | 否 | `"annual"` | 财务报表报告频率。有效选项: `"annual"`, `"quarterly"` (或 `"quarter"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

## 使用场景 13.5 — A股损益表 (Income Statement)

**所需权限层级:** `Free`

**API:** `cn_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None)`

获取结构化的损益表数据。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_free_api_key")

# 获取贵州茅台年度损益表
inc = osapi.cn_income_statement("600519", period="annual", provider="yahoo")
print(inc)
```

### 输出示例

```json
[
  {
    "symbol": "600519",
    "year": 2025,
    "quarter": null,
    "statement_type": "income",
    "items": {
      "revenue": 150000000000.0,
      "net_income": 75000000000.0
    },
    "provider": "yahoo",
    "market": "cn",
    "asset_class": "stock"
  }
]
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `period` | `str` | 否 | `"annual"` | 财务报表报告频率。有效选项: `"annual"`, `"quarterly"` (或 `"quarter"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

## 使用场景 13.6 — A股现金流量表 (Cash Flow)

**所需权限层级:** `Free`

**API:** `cn_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None)`

获取结构化的现金流量表数据。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_free_api_key")

# 获取贵州茅台年度现金流量表
cf = osapi.cn_cashflow("600519", period="annual", provider="yahoo")
print(cf)
```

### 输出示例

```json
[
  {
    "symbol": "600519",
    "year": 2025,
    "quarter": null,
    "statement_type": "cashflow",
    "items": {
      "operating_cash_flow": 90000000000.0
    },
    "provider": "yahoo",
    "market": "cn",
    "asset_class": "stock"
  }
]
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `period` | `str` | 否 | `"annual"` | 财务报表报告频率。有效选项: `"annual"`, `"quarterly"` (或 `"quarter"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

## 使用场景 13.7 — A股财务比率 (Financial Ratios)

**所需权限层级:** `Free`

**API:** `cn_ratios(symbol: str, provider: Optional[str] = None)`

获取财务比率数据（市盈率、市净率等）。

### 代码示例

```python
ratios = osapi.cn_ratios("600519", provider="sina")
print(ratios["ratios"])
```

### 输出示例

```json
{
  "symbol": "600519",
  "ratios": {
    "pe_trailing": 30.5,
    "pb": 8.2
  },
  "provider": "sina",
  "market": "cn",
  "asset_class": "stock"
}
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

