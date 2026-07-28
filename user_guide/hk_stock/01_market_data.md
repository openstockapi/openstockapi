# 港股市場數據 (模組 14)

此模組提供香港證券市場 (港股) 的全面歷史及參考數據，包括騰訊控股 (0700)、阿里巴巴 (9988) 及其他上市股票。

所有請求均通過核心引擎 (`core` 數據源) 本地解析，並支援多個供應商。

---

## 使用場景 14.0 — 港股代號列表

**所需權限層級:** `Free`

**API:** `hk_symbols(provider: Optional[str] = None)`

獲取港股市場所有有效股票代號列表。

### 代碼範例

```python
import openstockapi as osapi

# 初始化會話
osapi.init("your_free_api_key")

# 獲取港股代號
symbols = osapi.hk_symbols(provider="yahoo")
print(f"總股票數: {len(symbols)}")
print(f"範例代號: {symbols[:5]}")
```

### 輸出範例

```json
[
  "0700",
  "9988",
  "3690"
]
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.1 — 港股 OHLCV (歷史股價與成交量)

**所需權限層級:** `Free`

**API:** `hk_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None)`

獲取港股的歷史開市價、最高價、最低價、收市價及成交量 (OHLCV) 數據。

### 代碼範例

```python
import openstockapi as osapi

# 獲取騰訊 (0700) 過去 5 天的 1 小時 K 線數據
df = osapi.hk_ohlcv("0700", range="5d", interval="1h", provider="yahoo")
print(df.head())
```

### 輸出範例

```json
[
  {
    "symbol": "0700",
    "timestamp": "2026-07-21 00:00:00",
    "open": 465.6,
    "high": 481.8,
    "low": 465.0,
    "close": 478.2,
    "volume": 3250000.0,
    "provider": "yahoo",
    "market": "hk",
    "asset_class": "stock"
  }
]
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`, `"9988"`)。 |
| `range` | `str` | 否 | `"5d"` | 要獲取的數據範圍。有效選項: `"1d"`, `"5d"`, `"1mo"`, `"3mo"`, `"6mo"`, `"1y"`, `"2y"`, `"5y"`, `"10y"`, `"ytd"`, `"max"`。 |
| `interval` | `str` | 否 | `"1h"` | K 線時間間隔。有效選項: `"1m"`, `"2m"`, `"5m"`, `"15m"`, `"30m"`, `"60m"`, `"90m"`, `"1h"`, `"1d"`, `"5d"`, `"1wk"`, `"1mo"`, `"3mo"`。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動選擇), `"yahoo"`。 |

---

## 使用場景 14.2 — 港股公司簡介

**所需權限層級:** `Free`

**API:** `hk_profile(symbol: str, provider: Optional[str] = None)`

獲取基本的公司註冊資訊、業務描述、員工人數及官方行業分類。

### 代碼範例

```python
profile = osapi.hk_profile("0700", provider="yahoo")
print(f"公司名稱: {profile['company_name']}, 行業: {profile['industry']}")
```

### 輸出範例

```json
{
  "symbol": "0700",
  "company_name": "Tencent Holdings Limited",
  "industry": "Internet Content & Information",
  "website": "https://www.tencent.com",
  "headcount": 105000,
  "description": "Tencent Holdings Limited, an investment holding company, provides value-added services...",
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

## 使用場景 14.11 — 港股財經新聞

**所需權限層級:** `Free`

**API:** `hk_news(symbol: str, provider: Optional[str] = None)`

獲取特定個股的公司財經新聞文章。

### 代碼範例

```python
news = osapi.hk_news("0700", provider="google_news")
print(news["news"][0]["title"])
```

### 輸出範例

```json
{
  "symbol": "0700",
  "news": [
    {
      "id": "12345",
      "title": "Tencent Earnings",
      "url": "https://tencent.hk",
      "published_at": "2026-07-23T20:19:30Z",
      "publisher": "Yahoo Finance",
      "summary": "Tencent reports strong earnings growth."
    }
  ],
  "provider": "google_news",
  "market": "hk",
  "asset_class": "stock"
}
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | 港股股票代號 (例如 `"0700"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。有效選項: `None` (自動选择), `"yahoo"`, `"google_news"`。 |

---

## 使用場景 14.12 — 港股市場熱力圖 (Heatmap)

**所需權限層級:** `Free`

**API:** `hk_heatmap(limit: int = 500, provider: Optional[str] = None)`

獲取港股市場的熱力圖數據，包括股票代號、名稱、漲跌幅、市值、行業、板塊和Logo鏈接。

### 代碼範例

```python
import openstockapi as osapi

# 獲取前5個港股熱力圖數據點
heatmap = osapi.hk_heatmap(limit=5, provider="tradingview")
print(heatmap)
```

### 輸出範例

```json
[
  {
    "symbol": "700",
    "name": "Tencent Holdings Ltd",
    "change": 1.70,
    "market_cap": 3915648864171.0,
    "sector": "Technology Services",
    "industry": "Packaged Software",
    "logo_url": "https://s3-symbol-logo.tradingview.com/tencent.svg",
    "provider": "tradingview",
    "market": "hk",
    "asset_class": "stock"
  }
]
```

### 參數

| 參數 | 類型 | 必須 | 默認值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | 否 | `500` | 返回的最大股票數量。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的數據源。目前僅支持 `"tradingview"`。 |

