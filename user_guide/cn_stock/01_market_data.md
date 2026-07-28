# A股市場數據 (模組 13)

此模组提供中国A股市场 (CN Stock) 的全面历史、参考和实时数据，包括贵州茅台 (600519)、比亚迪 (002594) 及其他上市股票。

所有请求均通过核心引擎 (`core` 数据源) 动态解析，允许显式指定特定的底层数据源提供商。

---

## 使用场景 13.0 — A股股票代码列表

**所需权限层级:** `Free`

**API:** `cn_symbols(provider: Optional[str] = None)`

获取A股市场所有有效股票代码列表。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_free_api_key")

# 获取A股股票代码
symbols = osapi.cn_symbols(provider="sina")
print(f"总股票数: {len(symbols)}")
print(f"示例代码: {symbols[:5]}")
```

### 输出示例

```json
[
  "600519",
  "002594",
  "300750"
]
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`。 |

---

## 使用场景 13.1 — A股 OHLCV (历史股价与成交量)

**所需权限层级:** `Free`

**API:** `cn_ohlcv(symbol: str, range: str = "5d", interval: str = "1h", provider: Optional[str] = None)`

获取A股的历史开盘价、最高价、最低价、收盘价及成交量 (OHLCV) 数据。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_free_api_key")

# 获取贵州茅台 (600519) 过去 5 天的 1 小时 K 线数据
df = osapi.cn_ohlcv("600519", range="5d", interval="1h", provider="tencent")
print(df.head())
```

### 输出示例

```json
[
  {
    "symbol": "600519",
    "timestamp": "2026-07-21 00:00:00",
    "open": 1305.0,
    "high": 1309.2,
    "low": 1301.0,
    "close": 1305.0,
    "volume": 125000.0,
    "provider": "tencent",
    "market": "cn",
    "asset_class": "stock"
  }
]
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `range` | `str` | 否 | `"5d"` | 要获取的数据范围。有效选项: `"1d"`, `"5d"`, `"1mo"`, `"3mo"`, `"6mo"`, `"1y"`, `"2y"`, `"5y"`, `"10y"`, `"ytd"`, `"max"`。 |
| `interval` | `str` | 否 | `"1h"` | K 线时间间隔。有效选项: `"1m"`, `"2m"`, `"5m"`, `"15m"`, `"30m"`, `"60m"`, `"90m"`, `"1h"`, `"1d"`, `"5d"`, `"1wk"`, `"1mo"`, `"3mo"`。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"tencent"`, `"yahoo"`。 |

---

## 使用场景 13.2 — A股公司简介

**所需权限层级:** `Free`

**API:** `cn_profile(symbol: str, provider: Optional[str] = None)`

获取基本的公司注册信息、业务描述、员工人数及官方行业分类。

### 代码示例

```python
profile = osapi.cn_profile("600519", provider="sina")
print(f"公司名称: {profile['company_name']}, 行业: {profile['industry']}")
```

### 输出示例

```json
{
  "symbol": "600519",
  "company_name": "Kweichow Moutai Co., Ltd.",
  "industry": "Beverages—Brewers",
  "website": "https://www.moutaichina.com",
  "headcount": 30000,
  "description": "Kweichow Moutai Co., Ltd. produces and sells Moutai liquor in China...",
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

## 使用场景 13.11 — A股实时行情 (Realtime Quote)

**所需权限层级:** `Pro`

**API:** `cn_quote(symbol: str, provider: Optional[str] = None)`

获取A股的实时行情，包括最新价、涨跌幅、成交量和时间戳等。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_pro_api_key")

quote = osapi.cn_quote("600519", provider="tencent")
print(f"Price: {quote['price']}, Change: {quote['pct_change']}%")
```

### 输出示例

```json
{
  "symbol": "600519",
  "price": 1305.5,
  "change": 0.5,
  "pct_change": 0.04,
  "volume": 125500.0,
  "timestamp": "2026-07-25 15:00:00",
  "provider": "tencent",
  "market": "cn",
  "asset_class": "stock"
}
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"tencent"`。 |

---

## 使用场景 13.12 — A股订单簿与逐笔成交

**所需权限层级:** `Pro`

**APIs:**
*   `cn_order_book(symbol: str, provider: Optional[str] = None)`
*   `cn_tick(symbol: str, provider: Optional[str] = None)`

获取订单簿深度或日内逐笔交易行情。

### 代码示例

```python
import openstockapi as osapi

# 初始化会话
osapi.init("your_pro_api_key")

# 获取订单簿深度数据
book = osapi.cn_order_book("600519", provider="tencent")
print("Asks:", book["asks"][:2])
print("Bids:", book["bids"][:2])
```

### 输出示例

```json
{
  "symbol": "600519",
  "asks": [
    {"price": 1305.6, "volume": 100},
    {"price": 1305.7, "volume": 200}
  ],
  "bids": [
    {"price": 1305.4, "volume": 150},
    {"price": 1305.3, "volume": 300}
  ],
  "provider": "tencent",
  "market": "cn",
  "asset_class": "stock"
}
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"tencent"`。 |

---

## 使用场景 13.13 — A股市场热力图 (Heatmap)

**所需权限层级:** `Free`

**API:** `cn_heatmap(limit: int = 500, provider: Optional[str] = None)`

获取A股市场的热力图数据，包括股票代码、名称、涨跌幅、市值、行业、板块和Logo链接。

### 代码示例

```python
import openstockapi as osapi

# 获取前5个A股热力图数据点
heatmap = osapi.cn_heatmap(limit=5, provider="tradingview")
print(heatmap)
```

### 输出示例

```json
[
  {
    "symbol": "601398",
    "name": "Industrial and Commercial Bank of China Limited Class A",
    "change": 0.52,
    "market_cap": 2631557168344.62,
    "sector": "Finance",
    "industry": "Major Banks",
    "logo_url": "https://s3-symbol-logo.tradingview.com/industrial-and-commercial-bank-of-china.svg",
    "provider": "tradingview",
    "market": "cn",
    "asset_class": "stock"
  }
]
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | 否 | `500` | 返回的最大股票数量。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。目前仅支持 `"tradingview"`。 |

