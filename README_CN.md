<div align="center">
  <h1> OpenStockAPI</h1>
  <img src="public/banner.png" alt="OpenStockAPI Banner" width="100%" />
  
  <p align="center">
    <a href="./README.md">English</a> · <a href="./README_VN.md">Tiếng Việt</a> · <a href="./README_JP.md">日本語</a> · <b>简体中文</b> · <a href="./README_HK.md">繁體中文</a>
  </p>

  <p><strong>免费、开源的 Python 金融数据接口库，支持下载越南及国际股票历史 K 线 (OHLCV)、实时行情报价、订单簿、逐笔交易、财经新闻和财务报表。</strong></p>

  <p>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/v/openstockapi.svg?color=blue&label=PyPI" alt="PyPI version"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/dm/openstockapi.svg?color=brightgreen&label=Downloads" alt="Downloads"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/pyversions/openstockapi.svg" alt="Python Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL%203.0-orange.svg" alt="License"></a>
  </p>

  <p>
    <a href="./user_guide/getting_started.md"><strong> 阅读文档 »</strong></a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=bug">汇报错误</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=enhancement">请求新功能</a>
  </p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>📋 目录</summary>
  <ol>
    <li><a href="#about">关于项目</a></li>
    <li><a href="#features">功能特色</a></li>
    <li><a href="#quick-start">快速开始</a></li>
    <li><a href="#installation">安装指南</a></li>
    <li><a href="#usage">使用方法与文档</a></li>
    <li><a href="#providers">支持的数据源</a></li>
    <li><a href="#data-modules">数据模块结构</a></li>
    <li><a href="#roadmap">项目路线图</a></li>
    <li><a href="#contributing">如何贡献</a></li>
    <li><a href="#changelog">更新日志</a></li>
    <li><a href="#license">开源协议</a></li>
  </ol>
</details>

---

<a id="about"></a>
## 关于项目

**OpenStockAPI** 是一个免费、开源的 Python 金融数据获取库，旨在作为一个模块化的 **数据中台 (Data Plane)**，用于下载和标准化来自越南 (`HOSE`, `HNX`, `UPCOM`)、美股、日股、港股、A股、澳股以及全球加密货币和外汇市场的历史股票数据 (OHLCV)、实时行情、订单簿、财经新闻和财务报表。

它专为金融数据应用、量化交易系统、Excel add-in 和 Amibroker 插件的上游数据层而设计，自动处理数据源故障转移 (provider fallback)、本地缓存、访问频率限制 (rate limit) 和 API 权限控制。

> 📘 其他语言版本的 README：**[英文版](./README.md)** | **[越南文版](./README_VN.md)**

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="features"></a>
## 功能特色

- **多市场与多资产支持** — 涵盖越南 (`VN`) 股票、港股 (`HK`)、A股 (`CN`)、美股 (`US`)、日股 (`JP`)、澳股 (`ASX`)，以及加密货币 (`Crypto`) 和外汇商品数据。
- **自动多源故障转移** — 整合 KBS、VCI、MSN、MAS、Maybank、Fmarket 及 Core Engine 数据源，在任一源不可用时自动进行故障转移。
- **安全验证与频率限制** — 支持短效 JWT 会话令牌验证，并通过客户端 Token Bucket 限制器管理 `Free`、`Pro` 和 `Premium` 层级的速率限制。
- **异步 (Async) 支持** — 提供 `async_ohlcv()` 和 `async_crypto_ohlcv()` 接口，以实现高吞吐量的数据流管道。

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="quick-start"></a>
## 快速开始

```python
import openstockapi as osapi

# 使用 API 密钥初始化会话（所有层级均需注册）
# 免费注册网址：https://openstockapi.com/register
osapi.init("free_YOUR_KEY")   # 或 "pro_YOUR_KEY" / "premium_YOUR_KEY"

# 获取历史股价 OHLCV
df = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-12-31")
print(df.head())

# 获取加密货币数据
btc_ohlcv = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=5)
print(btc_ohlcv)

# 获取外汇和商品数据
rates = osapi.forex_rates(base="USD")
gold_price = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h")
print(f"USD/VND: {rates['rates']['VND']} | 黄金价格: {gold_price['regularMarketPrice']} 美元")
```

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="installation"></a>
## 安装指南

**基础安装：**
```bash
pip install openstockapi
```

**带 Pandas DataFrame 及 Excel 导出支持的安装：**
```bash
pip install openstockapi[pandas]
```

**环境要求：** Python 3.8+

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="usage"></a>
## 使用方法与文档

完整的文档、使用场景示例及输出格式样本，可在用户指南中查看：

 **[用户指南 — 开始使用](./user_guide/getting_started.md)**

| 资产类别 | 文档路径 | 描述 |
|----------|----------------|-------------|
| **越南股票** | [01 — 越南股票市场数据](./user_guide/vn_stock/01_stock_market_data.md) | 历史日K线、公司简介、实时报价 |
| **加密货币** | [08 — 加密货币市场数据](./user_guide/crypto/01_crypto_market_data.md) | 历史K线、订单簿深度、衍生品指标、Delta 资金流向、杠杆模拟 |
| **外汇与商品** | [09 — 外汇市场数据](./user_guide/forex/01_forex_market_data.md) | 汇率、外汇历史K线、黄金原油价格、全球指数 |
| **澳股** | [10 — 澳股市场数据](./user_guide/asx/01_asx_market_data.md) | ASX 股代码列表、历史K线、资产负债表、损益表、现金流量表、比率、分红、公告与新闻 |
| **美股** | [11 — 美股市场数据](./user_guide/us_stock/01_us_market_data.md) | 美股历史K线、公司简介、财务报表、分红与拆股历史、公司日历、新闻 |
| **日股** | [12 — 日股市场数据](./user_guide/jp_stock/01_jp_market_data.md) | 日本股票代码列表、历史K线、资产负债表、损益表、现金流量表、分红与拆股历史、财经新闻 |
| **A股** | [13 — A股市场数据](./user_guide/cn_stock/01_cn_market_data.md) | A股代码列表、历史K线、资产负债表、损益表、现金流量表、分红与拆股历史、实时行情、订单簿及 ticks |
| **港股** | [14 — 港股市场数据](./user_guide/hk_stock/01_hk_market_data.md) | 港股代码列表、历史K线、资产负债表、损益表、现金流量表、分红与拆股历史、财经新闻 |

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="providers"></a>
## 支持的数据源

详细数据源清单，请参阅 **[英文版 README](./README.md#supported-providers)**。

### 日本股票市场
| 数据源 | 来源 | 权限 | 数据类型 |
|---|---|---|---|
| `core` | Core Engine | Free | 代码、历史K线、公司简介、财务报表 (BS, IS, CF, 比率)、分红、拆股、决算日程、新闻 |

### 中国 A股 市场
| 数据源 | 来源 | 权限 | 数据类型 |
|---|---|---|---|
| `core` | Core Engine | Free / Pro | 代码、历史K线、简介、财务报表、分红、拆股 (Free); 实时行情、订单簿、 ticks (Pro) |

### 香港股票市场
| 数据源 | 来源 | 权限 | 数据类型 |
|---|---|---|---|
| `core` | Core Engine | Free | 代码、历史K线、公司简介、财务报表 (BS, IS, CF, 比率)、分红、拆股、业绩公布日程、新闻 |

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="data-modules"></a>
## 数据模块结构

```
openstockapi
├── ohlcv()                  # 历史 Stock OHLCV (sync)
├── async_ohlcv()            # 历史 Stock OHLCV (async)
├── profile()                # 公司简介 Stock
├── derivative_profile()     # 衍生品简介 Stock
├── balance_sheet()          # 资产负债表 Stock
├── income_statement()       # 损益表 Stock
├── cashflow()               # 现金流量表 Stock
├── ratios()                 # 财务比率 Stock
├── quote()                  # 实时报价 Stock
├── order_book()             # 订单簿深度 Stock
├── market_index()           # 指数 K线 Stock
├── macro_indicators()       # 宏观经济指标
├── fund_details()           # 基金信息 Stock
├── company_news()           # 公司新闻 Stock
├── company_events()         # 公司日程 Stock
│
├── crypto_ohlcv()           # 历史 Crypto OHLCV (sync)
├── async_crypto_ohlcv()     # 历史 Crypto OHLCV (async)
├── crypto_depth()           # 加密货币订单簿深度
├── crypto_derivatives()     # 加密货币衍生品指标
├── crypto_footprint()       # 资金流向热力图
├── simulate_leverage()      # 杠杆模拟器
├── crypto_symbols()         # 加密货币支持代码
├── crypto_tickers()         # 加密货币实时价格
├── crypto_options_instruments() # 支持期权列表
├── crypto_options_chain()   # 期权链数据
├── crypto_options_ticker()  # 期权报价及 Greeks
├── crypto_news()            # 加密货币新闻
├── crypto_events()          # 加密货币事件
├── crypto_profile()         # 加密货币代币信息及 Logo
├── crypto_heatmap()         # 加密货币市场热力图
├── CryptoStream             # WebSocket 实时流客户端
│
├── forex_rates()            # 外汇汇率
├── forex_ohlcv()            # 外汇历史K线
├── commodities_prices()     # 商品价格 (黄金、石油)
├── global_indices_etf()     # 全球指数及美国ETF
├── compare_rates()          # 汇率套利比较
├── forex_symbols()          # 支持外汇代码
├── forex_news()             # 外汇新闻
├── forex_events()           # 宏观事件日历
│
├── asx_symbols()            # 支持 ASX 代码
├── asx_ohlcv()              # 历史 ASX OHLCV
├── asx_profile()            # 公司简介 ASX
├── asx_balance_sheet()      # 资产负债表 ASX
├── asx_income_statement()   # 损益表 ASX
├── asx_cashflow()           # 现金流量表 ASX
├── asx_ratios()             # 财务比率 ASX
├── asx_dividends()          # 分红历史 ASX
├── asx_announcements()      # 公司 PDF 公告 ASX
│   └── asx_news()               # 公司新闻 ASX
│
├── us_ohlcv()               # 历史 US Stock OHLCV
├── us_profile()             # 公司简介 US
├── us_financials()          # 财务报表合并 US
├── us_balance_sheet()       # 资产负债表 US
├── us_income_statement()    # 损益表 US
├── us_cashflow()            # 现金流量表 US
├── us_ratios()              # 财务比率 US
├── us_dividends()           # 分红历史 US
├── us_splits()              # 拆股历史 US
├── us_calendar()            # 公司日历 US
├── us_news()                # 公司新闻 US
│
├── jp_symbols()             # JP股票代码列表
├── jp_ohlcv()               # 历史 JPK线
├── jp_profile()             # 公司简介 JP
├── jp_financials()          # 财务报表合并 JP
├── jp_balance_sheet()       # 资产负债表 JP
├── jp_income_statement()    # 损益表 JP
├── jp_cashflow()            # 现金流量表 JP
├── jp_ratios()              # 财务比率 JP
├── jp_dividends()           # 分红历史 JP
├── jp_splits()              # 拆股历史 JP
├── jp_calendar()            # 决算日程 JP
├── jp_news()                # 公司新闻 JP
│
├── cn_symbols()             # CN股票代码列表
├── cn_ohlcv()               # 历史 CNK线
├── cn_profile()             # 公司简介 CN
├── cn_financials()          # 财务报表合并 CN
├── cn_balance_sheet()       # 资产负债表 CN
├── cn_income_statement()    # 损益表 CN
├── cn_cashflow()            # 现金流量表 CN
├── cn_ratios()              # 财务比率 CN
├── cn_dividends()           # 分红历史 CN
├── cn_splits()              # 拆股历史 CN
├── cn_quote()               # 实时行情 CN (Pro)
├── cn_order_book()          # 订单簿深度 CN (Pro)
├── cn_tick()                # 逐笔成交 ticks CN (Pro)
├── cn_heatmap()             # 市场热力图 CN
│
├── hk_symbols()             # HK股票代码列表
├── hk_ohlcv()               # 历史 HKK线
├── hk_profile()             # 公司简介 HK
├── hk_financials()          # 财务报表合并 HK
├── hk_balance_sheet()       # 资产负债表 HK
├── hk_income_statement()    # 损益表 HK
├── hk_cashflow()            # 现金流量表 HK
├── hk_ratios()              # 财务比率 HK
├── hk_dividends()           # 分红历史 HK
├── hk_splits()              # 拆股历史 HK
├── hk_calendar()            # 业绩日程 HK
├── hk_heatmap()             # 市场热力图 HK
└── hk_news()                # 公司新闻 HK
```

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

<a id="roadmap"></a>
## 项目路线图

- [x] 越南股票数据 (KBS, VCI, MSN)
- [x] 越南股票财务报表 (MAS, VCI)
- [x] 世界宏观经济指标 (World Bank, Maybank)
- [x] 互惠基金数据 (Fmarket)
- [x] 企业新闻及活动日程 (KBS, VCI)
- [x] 加密货币数据 (Core Engine)
- [x] 加密货币期权数据 (Deribit, OKX)
- [x] 外汇及商品数据 (Core Engine)
- [x] 澳大利亚股票市场数据 (ASX)
- [x] 美国股票市场数据 (US)
- [x] 日本股票市场数据 (JP)
- [x] 中国 A股 市场数据 (CN)
- [x] 香港股票市场数据 (HK)
- [ ] WebSocket 实时数据串流

<p align="right">(<a href="#readme-top">回到顶部 ↑</a>)</p>

---

我们欢迎任何形式的的贡献！如果您想添加新的数据提供商 (provider)，请使用我们的 **Connector Development Kit (CDK)** 自动化生成模板代码并进行规范化验证。

请参阅 **[CDK 贡献者指南 (CDK Contributor Guide)](./CONTRIBUTING.md)** 获取详细的逐步指南。

基本流程：
1. Fork 本仓库
2. 创建分支：`git checkout -b feature/new-provider`
3. 自动生成模板代码：`openstock-cdk generate --name <名称> --market <市场> --type <类型>`
4. 编写 API 解析逻辑和单元测试
5. 运行 CDK 契约测试：`pytest tests/cdk/ -v`
6. 提交 Pull Request

---

<a id="license"></a>
## 开源协议

本项目根据 **GNU Affero General Public License v3.0 (AGPL-3.0)** 条款分发。详见 [`LICENSE`](LICENSE) 文件。
