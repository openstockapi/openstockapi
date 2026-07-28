# 日本株財務データ

## ユースケース 12.3 — 日本株財務データ (未処理一括)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_financials(symbol: str, period: str = "annual", provider: Optional[str] = None)`

未処理の統合財務報告書および過去のデータ期間メタデータを取得します。

### コードスニペット

```python
financials = osapi.jp_financials("7203", period="annual", provider="yahoo")
print(financials["available_periods"])
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "period_type": "annual",
  "available_periods": ["2026-03-31"],
  "periods": [
    {
      "period": "2026-03-31",
      "financials": {
        "balance_sheet": {
          "total_assets": 105522331000000.0,
          "total_liabilities": 64502263000000.0
        },
        "income_statement": {
          "revenue": 45095324000000.0,
          "net_income": 4944985000000.0
        }
      }
    }
  ],
  "provider": "yahoo",
  "market": "jp",
  "asset_class": "stock"
}
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`, `"6758"`)。 |
| `period` | `str` | いいえ | `"annual"` | 財務諸表の報告期間。選択肢: `"annual"`, `"quarterly"`。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.4 — 日本株貸借対照表 (Balance Sheet)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_balance_sheet(symbol: str, period: str = "annual", provider: Optional[str] = None)`

解析済みの貸借対照表データを取得します。

### コードスニペット

```python
import openstockapi as osapi

# セッションの初期化
osapi.init("your_free_api_key")

# トヨタの年間貸借対照表を取得
bs = osapi.jp_balance_sheet("7203", period="annual", provider="yahoo")
print(bs)
```

### 出力例 (Sample Output)

```json
[
  {
    "symbol": "7203",
    "year": 2026,
    "quarter": null,
    "statement_type": "balance",
    "items": {
      "total_assets": 105522331000000.0,
      "total_liabilities": 64502263000000.0
    },
    "provider": "yahoo",
    "market": "jp",
    "asset_class": "stock"
  }
]
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`, `"6758"`)。 |
| `period` | `str` | いいえ | `"annual"` | 財務諸表の報告頻度。選択肢: `"annual"`, `"quarterly"` (または `"quarter"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.5 — 日本株損益計算書 (Income Statement)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_income_statement(symbol: str, period: str = "annual", provider: Optional[str] = None)`

解析済みの損益計算書データを取得します。

### コードスニペット

```python
import openstockapi as osapi

# セッションの初期化
osapi.init("your_free_api_key")

# トヨタの年間損益計算書を取得
inc = osapi.jp_income_statement("7203", period="annual", provider="yahoo")
print(inc)
```

### 出力例 (Sample Output)

```json
[
  {
    "symbol": "7203",
    "year": 2026,
    "quarter": null,
    "statement_type": "income",
    "items": {
      "revenue": 45095324000000.0,
      "net_income": 4944985000000.0
    },
    "provider": "yahoo",
    "market": "jp",
    "asset_class": "stock"
  }
]
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`, `"6758"`)。 |
| `period` | `str` | いいえ | `"annual"` | 財務諸表の報告頻度。選択肢: `"annual"`, `"quarterly"` (または `"quarter"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.6 — 日本株キャッシュフロー計算書 (Cash Flow)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_cashflow(symbol: str, period: str = "annual", provider: Optional[str] = None)`

解析済みのキャッシュフロー計算書データを取得します。

### コードスニペット

```python
import openstockapi as osapi

# セッションの初期化
osapi.init("your_free_api_key")

# トヨタの年間キャッシュフロー計算書を取得
cf = osapi.jp_cashflow("7203", period="annual", provider="yahoo")
print(cf)
```

### 出力例 (Sample Output)

```json
[
  {
    "symbol": "7203",
    "year": 2026,
    "quarter": null,
    "statement_type": "cashflow",
    "items": {
      "operating_cash_flow": 5500000000000.0
    },
    "provider": "yahoo",
    "market": "jp",
    "asset_class": "stock"
  }
]
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`, `"6758"`)。 |
| `period` | `str` | いいえ | `"annual"` | 財務諸表の報告頻度。選択肢: `"annual"`, `"quarterly"` (または `"quarter"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定 of プロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.7 — 日本株財務比率 (Financial Ratios)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_ratios(symbol: str, provider: Optional[str] = None)`

各種財務比率（PER、PBR、ROE、ROA、自己資本比率関連など）を取得します。

### コードスニペット

```python
ratios = osapi.jp_ratios("7203", provider="yahoo")
print(ratios["ratios"])
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "ratios": {
    "pe_trailing": 9.81,
    "pe_forward": 8.93,
    "pb": 0.94,
    "roe": 10.23,
    "roa": 2.36,
    "debt_to_equity": 107.06
  },
  "provider": "yahoo",
  "market": "jp",
  "asset_class": "stock"
}
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

