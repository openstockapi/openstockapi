# 日本株ニュース・企業スケジュール

## ユースケース 12.8 — 日本株配当金実績 (Dividends)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_dividends(symbol: str, provider: Optional[str] = None)`

配当金の支払い履歴履歴を取得します。

### コードスニペット

```python
divs = osapi.jp_dividends("7203", provider="yahoo")
print(divs["dividends"])
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "dividends": [
    {
      "ex_date": "2025-03-27",
      "pay_date": null,
      "amount": 45.0,
      "type": "Dividend"
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
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.9 — 日本株株式分割履歴 (Splits)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_splits(symbol: str, provider: Optional[str] = None)`

株式分割の履歴と分割比率を取得します。

### コードスニペット

```python
splits = osapi.jp_splits("7203", provider="yahoo")
print(splits["splits"])
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "splits": [
    {
      "date": "2021-09-28",
      "ratio": 5.0
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
| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.10 — 日本株決算カレンダー (Corporate Calendar)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_calendar(symbol: str, provider: Optional[str] = None)`

予定されている決算発表日スケジュールを取得します。

### コードスニペット

```python
calendar = osapi.jp_calendar("7203", provider="yahoo")
print(calendar["calendar"])
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "calendar": {
    "Earnings Date": ["2026-05-08"]
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

