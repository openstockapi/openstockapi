# 港股公司新聞與事件

## 使用場景 14.8 — 港股派息記錄 (Dividends)

**所需權限層級:** `Free`

**API:** `hk_dividends(symbol: str, provider: Optional[str] = None)`

獲取派息發放歷史記錄。

### 代碼範例

```python
divs = osapi.hk_dividends("0700", provider="yahoo")
print(divs["dividends"])
```

### 輸出範例

```json
{
  "symbol": "0700",
  "dividends": [
    {
      "ex_date": "2025-05-20",
      "pay_date": null,
      "amount": 3.4,
      "type": "Dividend"
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
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.9 — 港股拆股記錄 (Splits)

**所需權限層級:** `Free`

**API:** `hk_splits(symbol: str, provider: Optional[str] = None)`

獲取歷史股份分拆比率時間線。

### 代碼範例

```python
splits = osapi.hk_splits("0700", provider="yahoo")
print(splits["splits"])
```

### 輸出範例

```json
{
  "symbol": "0700",
  "splits": [
    {
      "date": "2014-05-15",
      "ratio": 5.0
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
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.10 — 港股業績公佈與公司日曆

**所需權限層級:** `Free`

**API:** `hk_calendar(symbol: str, provider: Optional[str] = None)`

獲取預定的公司業績公佈日期。

### 代碼範例

```python
calendar = osapi.hk_calendar("0700", provider="yahoo")
print(calendar["calendar"])
```

### 輸出範例

```json
{
  "symbol": "0700",
  "calendar": {
    "Earnings Date": ["2026-05-14"]
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

