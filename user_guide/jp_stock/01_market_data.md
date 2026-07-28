# 日本株市場データ (モジュール 12)

このモジュールは、トヨタ自動車 (7203) やソニーグループ (6758) などを含む日本株式市場 (JP Stock) の包括的な履歴および参照データを提供します。

---

## ユースケース 12.0 — 日本株銘柄コード一覧

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_symbols(provider: Optional[str] = None)`

日本株市場で利用可能なすべてのアクティブな銘柄コードの一覧を取得します。

### コードスニペット

```python
import openstockapi as osapi

# セッションの初期化
osapi.init("your_free_api_key")

# 日本株の銘柄コードを取得
symbols = osapi.jp_symbols(provider="yahoo")
print(f"銘柄数: {len(symbols)}")
print(f"銘柄コードの例: {symbols[:5]}")
```

### 出力例 (Sample Output)

```json
[
  "7203",
  "6758",
  "9984",
  "9983",
  "8035"
]
```

### パラメータ
| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.1 — 日本株 OHLCV (株価四本値・出来高)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None)`

日本株의 履歴始値、高値、安値、終値、および出来高 (OHLCV) を取得します。

### コードスニペット

```python
import openstockapi as osapi

# セッションの初期化
osapi.init("your_free_api_key")

# トヨタ(7203)の過去5日間の1時間足データを取得
df = osapi.jp_ohlcv("7203", range="5d", interval="1h", provider="yahoo")
print(df.head())
```

### 出力例 (Sample Output)

```json
[
  {
    "symbol": "7203",
    "timestamp": "2026-07-21 09:00:00",
    "open": 2800.5,
    "high": 2850.0,
    "low": 2795.0,
    "close": 2820.0,
    "volume": 3200000.0,
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
| `range` | `str` | いいえ | `"5d"` | 取得するデータの期間。選択肢: `"1d"`, `"5d"`, `"1mo"`, `"3mo"`, `"6mo"`, `"1y"`, `"2y"`, `"5y"`, `"10y"`, `"ytd"`, `"max"`。 |
| `interval` | `str` | いいえ | `"1h"` | ローソク足の期間（解像度）。選択肢: `"1m"`, `"2m"`, `"5m"`, `"15m"`, `"30m"`, `"60m"`, `"90m"`, `"1h"`, `"1d"`, `"5d"`, `"1wk"`, `"1mo"`, `"3mo"`。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.2 — 日本株企業プロファイル

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_profile(symbol: str, provider: Optional[str] = None)`

企業の基本情報、事業説明、従業員数、および公式の業種分類を取得します。

### コードスニペット

```python
profile = osapi.jp_profile("7203", provider="yahoo")
print(f"企業名: {profile['company_name']}, 業種: {profile['industry']}")
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "company_name": "Toyota Motor Corporation",
  "industry": "Auto Manufacturers",
  "website": "https://global.toyota",
  "headcount": 375000,
  "description": "Toyota Motor Corporation designs, manufactures, assembles, and sells passenger vehicles...",
  "provider": "yahoo",
  "market": "jp",
  "asset_class": "stock"
}
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | はい | - | 日本株의 銘柄コード (例: `"7203"`, `"6758"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`。 |

---

## ユースケース 12.11 — 日本株ニュース

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_news(symbol: str, provider: Optional[str] = None)`

特定の企業に関連するニュースや金融関連記事を取得します。

### コードスニペット

```python
news = osapi.jp_news("7203", provider="google_news")
print(news["news"][0]["title"])
```

### 出力例 (Sample Output)

```json
{
  "symbol": "7203",
  "news": [
    {
      "id": "12345",
      "title": "Toyota announces solid global production results",
      "url": "https://finance.yahoo.com/news/...",
      "published_at": 1784795096,
      "publisher": "Yahoo Finance",
      "summary": "Toyota Motor Corp today released consolidated production figures..."
    }
  ],
  "provider": "yahoo",
  "market": "jp",
  "asset_class": "stock"
}
```

### パラメータ

| `symbol` | `str` | はい | - | 日本株の銘柄コード (例: `"7203"`)。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"yahoo"`, `"google_news"`。 |

---

## ユースケース 12.12 — 日本株ヒートマップ (JP Stock Heatmap)

**必要とする枠階 (Required Tier):** `Free`

**API:** `jp_heatmap(limit=500, provider=None)`

日本株市場の上位銘柄（時価総額順）のリアルタイム変動率、時価総額、セクター、業種、SVGロゴURLを取得します。

### コードスニペット

```python
import openstockapi as osapi

# セッション初期化
osapi.init("your_free_api_key")

# 上位5件の日本株ヒートマップデータを取得
heatmap = osapi.jp_heatmap(limit=5, provider="tradingview")
print(heatmap)
```

### サンプル出力

```json
[
  {
    "symbol": "8306",
    "name": "Mitsubishi UFJ Financial Group, Inc.",
    "change": 4.432,
    "market_cap": 41977228000000.0,
    "sector": "Finance",
    "industry": "Major Banks",
    "logo_url": "https://s3-symbol-logo.tradingview.com/mitsubishi-group.svg",
    "provider": "tradingview",
    "market": "jp",
    "asset_class": "stock"
  }
]
```

### パラメータ

| パラメータ | 型 | 必須 | デフォルト値 | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | いいえ | `500` | 時価総額順で取得する銘柄数。 |
| `provider` | `str` | いいえ | `None` | クエリを指定のプロバイダーに制限します。選択肢: `"tradingview"`。 |
