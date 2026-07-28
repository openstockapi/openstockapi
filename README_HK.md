<div align="center">
  <h1> OpenStockAPI</h1>
  <p><strong>一個模組化、多數據源的 Python 數據中台，適用於越南及國際金融市場數據。</strong></p>

  <p>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/v/openstockapi.svg?color=blue&label=PyPI" alt="PyPI version"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/dm/openstockapi.svg?color=brightgreen&label=Downloads" alt="Downloads"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/pyversions/openstockapi.svg" alt="Python Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL%203.0-orange.svg" alt="License"></a>
  </p>

  <p>
    <a href="./user_guide/getting_started.md"><strong> 閱讀文檔 »</strong></a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=bug">回報錯誤</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=enhancement">請求新功能</a>
  </p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>📋 目錄</summary>
  <ol>
    <li><a href="#about">關於項目</a></li>
    <li><a href="#features">功能特色</a></li>
    <li><a href="#quick-start">快速開始</a></li>
    <li><a href="#installation">安裝指南</a></li>
    <li><a href="#usage">使用方法與文檔</a></li>
    <li><a href="#providers">支持的數據源</a></li>
    <li><a href="#data-modules">數據模組結構</a></li>
    <li><a href="#roadmap">項目路線圖</a></li>
    <li><a href="#contributing">如何貢獻</a></li>
    <li><a href="#changelog">更新日誌</a></li>
    <li><a href="#license">開源協議</a></li>
  </ol>
</details>

---

<a id="about"></a>
## 關於項目

**OpenStockAPI** 是一個開源的 Python 函數庫，旨在作為一個模組化的 **數據中台 (Data Plane)**，用於收集及標準化來自越南和多個市場的金融數據。

它專為金融應用程序的上游數據獲取層而設計，處理數據源故障轉移、訪問頻率限制和權限控制，使您的應用程序層無需擔心數據源的可靠性。

> 📘 其他語言版本的 README：**[英文版](./README.md)** | **[越南文版](./README_VN.md)**

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="features"></a>
## 功能特色

- **多市場與多資產支持** — 涵蓋越南 (`VN`) 股票、港股 (`HK`)、A股 (`CN`)、美股 (`US`)、日股 (`JP`)、澳股 (`ASX`)，以及加密貨幣 (`Crypto`) 和外匯商品數據。
- **自動多源故障轉移** — 整合 KBS、VCI、MSN、MAS、Maybank、Fmarket 及 Core Engine 數據源，在任一源不可用時自動進行故障轉移。
- **安全驗證與頻率限制** — 支持短效 JWT 會話令牌驗證，並通過客戶端 Token Bucket 限制器管理 `Free`、`Pro` 和 `Premium` 層級的速率限制。
- **非同步 (Async) 支持** — 提供 `async_ohlcv()` 和 `async_crypto_ohlcv()` 接口，以實現高吞吐量的數據流管道。

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="quick-start"></a>
## 快速開始

```python
import openstockapi as osapi

# 使用 API 密鑰初始化會話（所有層級均需註冊）
# 免費註冊網址：https://openstockapi.com/register
osapi.init("free_YOUR_KEY")   # 或 "pro_YOUR_KEY" / "premium_YOUR_KEY"

# 獲取歷史股價 OHLCV
df = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-12-31")
print(df.head())

# 獲取加密貨幣數據
btc_ohlcv = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=5)
print(btc_ohlcv)

# 獲取外匯和商品數據
rates = osapi.forex_rates(base="USD")
gold_price = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h")
print(f"USD/VND: {rates['rates']['VND']} | 黃金價格: {gold_price['regularMarketPrice']} 美元")
```

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="installation"></a>
## 安裝指南

**基礎安裝：**
```bash
pip install openstockapi
```

**帶 Pandas DataFrame 及 Excel 導出支持的安裝：**
```bash
pip install openstockapi[pandas]
```

**環境要求：** Python 3.8+

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="usage"></a>
## 使用方法與文檔

完整的文檔、使用場景範例及輸出格式樣本，可在用戶指南中查看：

 **[用戶指南 — 開始使用](./user_guide/getting_started.md)**

| 資產類別 | 文檔路徑 | 描述 |
|----------|----------------|-------------|
| **越南股票** | [01 — 越南股票市場數據](./user_guide/vn_stock/01_stock_market_data.md) | 歷史日K線、公司簡介、實時報價 |
| **加密貨幣** | [08 — 加密貨幣市場數據](./user_guide/crypto/01_crypto_market_data.md) | 歷史K線、訂單簿深度、衍生品指標、Delta 資金流向、槓桿模擬 |
| **外匯與商品** | [09 — 外匯市場數據](./user_guide/forex/01_forex_market_data.md) | 匯率、外匯歷史K線、黃金原油價格、全球指數 |
| **澳股** | [10 — 澳股市場數據](./user_guide/asx/01_asx_market_data.md) | ASX 股代號列表、歷史K線、資產負債表、損益表、現金流量表、比率、派息、公告與新聞 |
| **美股** | [11 — 美股市場數據](./user_guide/us_stock/01_us_market_data.md) | 美股歷史K線、公司簡介、財務報表、派息與拆股歷史、公司日曆、新聞 |
| **日股** | [12 — 日股市場數據](./user_guide/jp_stock/01_jp_market_data.md) | 日本股票代號列表、歷史K線、資產負債表、損益表、現金流量表、派息與分拆歷史、財經新聞 |
| **A股** | [13 — A股市場數據](./user_guide/cn_stock/01_cn_market_data.md) | A股代號列表、歷史K線、資產負債表、損益表、現金流量表、分紅與拆股歷史、實時行情、訂單簿及 ticks |
| **港股** | [14 — 港股市場數據](./user_guide/hk_stock/01_hk_market_data.md) | 港股代號列表、歷史K線、資產負債表、損益表、現金流量表、派息與分拆歷史、財經新聞 |

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="providers"></a>
## 支持的數據源

詳細數據源清單，請參閱 **[英文版 README](./README.md#supported-providers)**。

### 日本股票市場
| 數據源 | 來源 | 權限 | 數據類型 |
|---|---|---|---|
| `core` | Core Engine | Free | 代號、歷史K線、公司簡介、財務報表 (BS, IS, CF, 比率)、派息、拆股、決算日程、新聞 |

### 中國 A股 市場
| 數據源 | 來源 | 權限 | 數據類型 |
|---|---|---|---|
| `core` | Core Engine | Free / Pro | 代號、歷史K線、簡介、財務報表、派息、拆股 (Free); 實時行情、訂單簿、 ticks (Pro) |

### 香港股票市場
| 數據源 | 來源 | 權限 | 數據類型 |
|---|---|---|---|
| `core` | Core Engine | Free | 代號、歷史K線、公司簡介、財務報表 (BS, IS, CF, 比率)、派息、拆股、業績公佈日程、新聞 |

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="data-modules"></a>
## 數據模組結構

```
openstockapi
├── ohlcv()                  # 歷史 Stock OHLCV (sync)
├── async_ohlcv()            # 歷史 Stock OHLCV (async)
├── profile()                # 公司簡介 Stock
├── derivative_profile()     # 衍生品簡介 Stock
├── balance_sheet()          # 資產負債表 Stock
├── income_statement()       # 損益表 Stock
├── cashflow()               # 現金流量表 Stock
├── ratios()                 # 財務比率 Stock
├── quote()                  # 實時報價 Stock
├── order_book()             # 訂單簿深度 Stock
├── market_index()           # 指數 K線 Stock
├── macro_indicators()       # 宏觀經濟指標
├── fund_details()           # 基金信息 Stock
├── company_news()           # 公司新聞 Stock
├── company_events()         # 公司日程 Stock
│
├── crypto_ohlcv()           # 歷史 Crypto OHLCV (sync)
├── async_crypto_ohlcv()     # 歷史 Crypto OHLCV (async)
├── crypto_depth()           # 加密貨幣訂單簿深度
├── crypto_derivatives()     # 加密貨幣衍生品指標
├── crypto_footprint()       # 資金流向熱力圖
├── simulate_leverage()      # 槓桿模擬器
├── crypto_symbols()         # 加密貨幣支持代號
├── crypto_tickers()         # 加密貨幣實時價格
├── crypto_options_instruments() # 支持期權列表
├── crypto_options_chain()   # 期權鏈數據
├── crypto_options_ticker()  # 期權報價及 Greeks
├── crypto_news()            # 加密貨幣新聞
├── crypto_events()          # 加密貨幣事件
├── crypto_profile()         # 加密貨幣代幣信息及 Logo
├── crypto_heatmap()         # 加密貨幣市場熱力圖
├── CryptoStream             # WebSocket 實時流客戶端
│
├── forex_rates()            # 外匯匯率
├── forex_ohlcv()            # 外匯歷史K線
├── commodities_prices()     # 商品價格 (黃金、石油)
├── global_indices_etf()     # 全球指數及美國ETF
├── compare_rates()          # 匯率套利比較
├── forex_symbols()          # 支持外匯代號
├── forex_news()             # 外匯新聞
├── forex_events()           # 宏觀事件日曆
│
├── asx_symbols()            # 支持 ASX 代號
├── asx_ohlcv()              # 歷史 ASX OHLCV
├── asx_profile()            # 公司簡介 ASX
├── asx_balance_sheet()      # 資產負債表 ASX
├── asx_income_statement()   # 損益表 ASX
├── asx_cashflow()           # 現金流量表 ASX
├── asx_ratios()             # 財務比率 ASX
├── asx_dividends()          # 派息歷史 ASX
├── asx_announcements()      # 公司 PDF 公告 ASX
│   └── asx_news()               # 公司新聞 ASX
│
├── us_ohlcv()               # 歷史 US Stock OHLCV
├── us_profile()             # 公司簡介 US
├── us_financials()          # 財務報表合併 US
├── us_balance_sheet()       # 資產負債表 US
├── us_income_statement()    # 損益表 US
├── us_cashflow()            # 現金流量表 US
├── us_ratios()              # 財務比率 US
├── us_dividends()           # 派息歷史 US
├── us_splits()              # 拆股歷史 US
├── us_calendar()            # 公司日曆 US
├── us_news()                # 公司新聞 US
│
├── jp_symbols()             # JP股票代號列表
├── jp_ohlcv()               # 歷史 JPK線
├── jp_profile()             # 公司簡介 JP
├── jp_financials()          # 財務報表合併 JP
├── jp_balance_sheet()       # 資產負債表 JP
├── jp_income_statement()    # 損益表 JP
├── jp_cashflow()            # 現金流量表 JP
├── jp_ratios()              # 財務比率 JP
├── jp_dividends()           # 派息歷史 JP
├── jp_splits()              # 拆股歷史 JP
├── jp_calendar()            # 決算日程 JP
├── jp_news()                # 公司新聞 JP
│
├── cn_symbols()             # CN股票代號列表
├── cn_ohlcv()               # 歷史 CNK線
├── cn_profile()             # 公司簡介 CN
├── cn_financials()          # 財務報表合併 CN
├── cn_balance_sheet()       # 資產負債表 CN
├── cn_income_statement()    # 損益表 CN
├── cn_cashflow()            # 現金流量表 CN
├── cn_ratios()              # 財務比率 CN
├── cn_dividends()           # 派息歷史 CN
├── cn_splits()              # 拆股歷史 CN
├── cn_quote()               # 實時行情 CN (Pro)
├── cn_order_book()          # 訂單簿深度 CN (Pro)
├── cn_tick()                # 逐筆成交 ticks CN (Pro)
├── cn_heatmap()             # 市場熱力圖 CN
│
├── hk_symbols()             # HK股票代號列表
├── hk_ohlcv()               # 歷史 HKK線
├── hk_profile()             # 公司簡介 HK
├── hk_financials()          # 財務報表合併 HK
├── hk_balance_sheet()       # 資產負債表 HK
├── hk_income_statement()    # 損益表 HK
├── hk_cashflow()            # 現金流量表 HK
├── hk_ratios()              # 財務比率 HK
├── hk_dividends()           # 派息歷史 HK
├── hk_splits()              # 拆股歷史 HK
├── hk_calendar()            # 業績日程 HK
├── hk_heatmap()             # 市場熱力圖 HK
└── hk_news()                # 公司新聞 HK
```

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

<a id="roadmap"></a>
## 項目路線圖

- [x] 越南股票數據 (KBS, VCI, MSN)
- [x] 越南股票財務報表 (MAS, VCI)
- [x] 世界宏觀經濟指標 (World Bank, Maybank)
- [x] 互惠基金數據 (Fmarket)
- [x] 企業新聞及活動日程 (KBS, VCI)
- [x] 加密貨幣數據 (Core Engine)
- [x] 加密貨幣期權數據 (Deribit, OKX)
- [x] 外匯及商品數據 (Core Engine)
- [x] 澳大利亞股票市場數據 (ASX)
- [x] 美國股票市場數據 (US)
- [x] 日本股票市場數據 (JP)
- [x] 中國 A股 市場數據 (CN)
- [x] 香港股票市場數據 (HK)
- [ ] WebSocket 實時數據串流

<p align="right">(<a href="#readme-top">回到頂部 ↑</a>)</p>

---

我們歡迎任何形式的貢獻！如果您想添加新的數據提供商 (provider)，請使用我們的 **Connector Development Kit (CDK)** 自動化生成模板代碼並進行規範化驗證。

請參閱 **[CDK 貢獻者指南 (CDK Contributor Guide)](./CONTRIBUTING.md)** 獲取詳細的逐步指南。

基本流程：
1. Fork 本倉庫
2. 創建分支：`git checkout -b feature/new-provider`
3. 自動生成模板代碼：`openstock-cdk generate --name <名稱> --market <市場> --type <類型>`
4. 編寫 API 解析邏輯和單元測試
5. 運行 CDK 契約測試：`pytest tests/cdk/ -v`
6. 提交 Pull Request

---

<a id="license"></a>
## 開源協議

本項目根據 **GNU Affero General Public License v3.0 (AGPL-3.0)** 條款分發。詳見 [`LICENSE`](LICENSE) 文件。
