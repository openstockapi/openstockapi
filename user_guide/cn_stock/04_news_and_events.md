# A股公司新聞與事件

## 使用场景 13.8 — A股分红记录 (Dividends)

**所需权限层级:** `Free`

**API:** `cn_dividends(symbol: str, provider: Optional[str] = None)`

获取分红派息历史记录。

### 代码示例

```python
divs = osapi.cn_dividends("600519", provider="yahoo")
print(divs["dividends"])
```

### 输出示例

```json
{
  "symbol": "600519",
  "dividends": [
    {
      "ex_date": "2025-06-15",
      "pay_date": null,
      "amount": 19.1,
      "type": "Dividend"
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
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

## 使用场景 13.9 — A股拆股记录 (Splits)

**所需权限层级:** `Free`

**API:** `cn_splits(symbol: str, provider: Optional[str] = None)`

获取历史股份分拆比例时间线。

### 代码示例

```python
splits = osapi.cn_splits("600519", provider="yahoo")
print(splits["splits"])
```

### 输出示例

```json
{
  "symbol": "600519",
  "splits": [
    {
      "date": "2020-06-25",
      "ratio": 1.0
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
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"sina"`, `"yahoo"`。 |

---

## 使用场景 13.10 — A股公司新闻

**所需权限层级:** `Free`

**API:** `cn_news(symbol: str, provider: Optional[str] = None)`

获取特定A股股票的新闻媒体报道和分析文章。

### 代码示例

```python
news = osapi.cn_news("600519", provider="google_news")
print(news["news"][:2])
```

### 输出示例

```json
{
  "symbol": "600519",
  "news": [
    {
      "id": "abc123xyz",
      "title": "Kweichow Moutai reports earnings growth",
      "url": "https://finance.yahoo.com/news/example",
      "published_at": 1784997194,
      "publisher": "Yahoo Finance",
      "summary": "Moutai's revenue surged by..."
    }
  ],
  "provider": "google_news",
  "market": "cn",
  "asset_class": "stock"
}
```

### 参数

| 参数 | 类型 | 必须 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | 是 | - | A股股票代码 (例如 `"600519"`)。 |
| `provider` | `str` | 否 | `None` | 限制使用特定的数据源。有效选项: `None` (自动选择), `"yahoo"`, `"google_news"`。 |

---

