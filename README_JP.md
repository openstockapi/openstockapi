<div align="center">
  <h1> OpenStockAPI</h1>
  <p><strong>ベトナムおよび国際金融市場データのためのモジュール式、マルチソース Python データプレーン。</strong></p>

  <p>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/v/openstockapi.svg?color=blue&label=PyPI" alt="PyPI version"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/dm/openstockapi.svg?color=brightgreen&label=Downloads" alt="Downloads"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/pyversions/openstockapi.svg" alt="Python Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL%203.0-orange.svg" alt="License"></a>
  </p>

  <p>
    <a href="./user_guide/getting_started.md"><strong> ユーザーガイドを読む »</strong></a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=bug">バグ報告</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=enhancement">機能リクエスト</a>
  </p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>📋 目次</summary>
  <ol>
    <li><a href="#about">プロジェクトについて</a></li>
    <li><a href="#features">主な機能</a></li>
    <li><a href="#quick-start">クイックスタート</a></li>
    <li><a href="#installation">インストール</a></li>
    <li><a href="#usage">使用方法とドキュメント</a></li>
    <li><a href="#providers">サポートされているデータ源</a></li>
    <li><a href="#data-modules">データモジュール構成</a></li>
    <li><a href="#roadmap">ロードマップ</a></li>
    <li><a href="#contributing">貢献方法</a></li>
    <li><a href="#changelog">変更履歴</a></li>
    <li><a href="#license">ライセンス</a></li>
  </ol>
</details>

---

<a id="about"></a>
## プロジェクトについて

**OpenStockAPI** は、ベトナムおよび国際金融市場の複数データ源からデータを収集・標準化するモジュール式の **データプレーン** として機能する、オープンソースの Python ライブラリです。

金融アプリケーションの上流データ取得層として機能するように設計されており、プロバイダーのフォールバック、レート制限、枠階ベースのアクセス制御を処理するため、アプリケーション層はデータ源 of 信頼性を心配する必要がありません。

> 📘 日本語以外のバージョンも用意されています: **[English README](./README.md)** | **[README_VN.md](./README_VN.md)**

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="features"></a>
## 主な機能

- **マルチマーケット＆マルチアセットサポート** — ベトナム（`VN`）、日本（`JP`）、米国（`US`）、中国（`CN`）、香港（`HK`）、オーストラリア（`ASX`）の株式、暗号資産（`Crypto`）、外国為替（Forex）＆コモディティに対応。
- **自動マルチソースフォールバック** — KBS、VCI、MSN、MAS、Maybank、Fmarket、Core Engine などのプロバイダーを統合し、一部が利用不可の際に透過的に自動でフェイルオーバーを実行。
- **JWT ハンドシェイク＆フリーミアム制限制御** — 短寿命の JWT セッション検証および `Free`、`Pro`、`Premium` 等のレート制限をクライアント側のトークンバケット制限器で制御。
- **非同期 (Async) サポート** — `async_ohlcv()` や `async_crypto_ohlcv()` による非同期通信を標準サポート。

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="quick-start"></a>
## クリップスタート

```python
import openstockapi as osapi

# APIキーを使用してセッションを初期化 (全プラン共通で必要)
# 無料登録はこちら: https://openstockapi.com/register
osapi.init("free_YOUR_KEY")   # または "pro_YOUR_KEY" / "premium_YOUR_KEY"

# 株価の履歴 OHLCV を取得
df = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-12-31")
print(df.head())

# 暗号資産 (Crypto) データの取得
btc_ohlcv = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=5)
print(btc_ohlcv)

# 外為 (Forex) & コモディティ データの取得
rates = osapi.forex_rates(base="USD")
gold_price = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h")
print(f"USD/VND: {rates['rates']['VND']} | 金価格: {gold_price['regularMarketPrice']} USD")
```

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="installation"></a>
## インストール

**最小構成でのインストール:**
```bash
pip install openstockapi
```

**Pandas DataFrame および Excel エクスポートをサポートする場合:**
```bash
pip install openstockapi[pandas]
```

**動作要件:** Python 3.8+

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="usage"></a>
## 使用方法とドキュメント

完全なドキュメント、ユースケース、および出力サンプルはユーザーガイドで確認できます。

 **[ユーザーガイド — クイックスタート](./user_guide/getting_started.md)**

| カテゴリ | モジュール / ガイドリンク | 説明 |
|----------|----------------|-------------|
| **ベトナム株** | [01 — Stock Market Data](./user_guide/vn_stock/01_stock_market_data.md) | 履歴 OHLCV、企業プロファイル、リアルタイム板情報 |
| **暗号資産** | [08 — Crypto Market Data](./user_guide/crypto/01_crypto_market_data.md) | 暗号資産 OHLCV、板深度、デリバティブ指標、デルタフットプリント、レバレッジシミュレーション |
| **外為＆商品** | [09 — Forex Market Data](./user_guide/forex/01_forex_market_data.md) | 為替レート、外為 OHLCV、コモディティ価格（金・原油）、世界主要インデックス |
| **オーストラリア株** | [10 — Dữ Liệu Chứng Khoán Úc](./user_guide/asx/01_asx_market_data.md) | ASX 銘柄コード一覧、四本値、財務諸表、配当、予定表、ニュース |
| **米国株** | [11 — US Stock Market Data](./user_guide/us_stock/01_us_market_data.md) | 米国株 OHLCV、企業プロファイル、財務諸表、配当、分割履歴、予定表、ニュース |
| **日本株** | [12 — 日本株市場データ](./user_guide/jp_stock/01_jp_market_data.md) | 日本株銘柄コード一覧、四本値、企業プロファイル、貸借対照表、損益計算書、キャッシュフロー、財務比率、配当、分割履歴、予定表、ニュース |
| **中国株 (A株)** | [13 — A股市場データ](./user_guide/cn_stock/01_cn_market_data.md) | A株銘柄コード一覧、四本値、企業プロファイル、財務諸表、配当、リアルタイム板情報、 ticks |
| **香港株** | [14 — 港股市場數據](./user_guide/hk_stock/01_hk_market_data.md) | 港股銘柄コード一覧、四本値、財務諸表、配当、分割履歴、予定表、ニュース |

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="providers"></a>
## サポートされているデータ源 (Providers)

詳細なデータソース一覧については、[English README](./README.md#supported-providers) をご参照ください。

### 日本株式市場
| プロバイダー | データ源 | 利用枠階 | データ種類 |
|---|---|---|---|
| `core` | Core Engine | Free | 銘柄コード、四本値、企業プロファイル、財務諸表 (BS, IS, CF, 比率)、配当、分割、予定表、ニュース |

### 中国株式市場 (A株)
| プロバイダー | データ源 | 利用枠階 | データ種類 |
|---|---|---|---|
| `core` | Core Engine | Free / Pro | 銘柄コード、四本値、プロファイル、財務諸表、配当、分割 (Free); リアルタイム板、板深度、 ticks (Pro) |

### 香港株式市場
| プロバイダー | データ源 | 利用枠階 | データ種類 |
|---|---|---|---|
| `core` | Core Engine | Free | 銘柄コード、四本値、プロファイル、財務諸表 (BS, IS, CF, 比率)、配当、分割、予定表、ニュース |

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="data-modules"></a>
## データモジュール構成

```
openstockapi
├── ohlcv()                  # 履歴 Stock OHLCV (sync)
├── async_ohlcv()            # 履歴 Stock OHLCV (async)
├── profile()                # 企業プロファイル Stock
├── derivative_profile()     # 先物・オプションプロファイル Stock
├── balance_sheet()          # 貸借対照表 Stock
├── income_statement()       # 損益計算書 Stock
├── cashflow()               # キャッシュフロー計算書 Stock
├── ratios()                 # 財務比率 Stock
├── quote()                  # リアルタイム株価 Stock
├── order_book()             # 板情報・気配値 Stock
├── market_index()           # 指数 OHLCV Stock
├── macro_indicators()       # マクロ経済指標
├── fund_details()           # 投資信託情報
├── company_news()           # 企業ニュース
├── company_events()         # 企業イベントスケジュール
│
├── crypto_ohlcv()           # 履歴 Crypto OHLCV (sync)
├── async_crypto_ohlcv()     # 履歴 Crypto OHLCV (async)
├── crypto_depth()           # 暗号資産板情報
├── crypto_derivatives()     # 暗号資産デリバティブ指標
├── crypto_footprint()       # デルタフットプリント熱マップ
├── simulate_leverage()      # レバレッジシミュレーター
├── crypto_symbols()         # サポート暗号資産一覧
├── crypto_tickers()         # リアルタイム暗号資産価格
├── crypto_options_instruments() # オプション一覧
├── crypto_options_chain()   # オプションチェーンデータ
├── crypto_options_ticker()  # オプション板およびギリシャ指標
├── crypto_news()            # 暗号資産ニュース
├── crypto_events()          # 暗号資産予定表
├── crypto_profile()         # 暗号資産プロファイルおよびロゴ
├── crypto_heatmap()         # 暗号資産市場ヒートマップ
├── CryptoStream             # WebSocket ストリーミングクライアント
│
├── forex_rates()            # 為替レート
├── forex_ohlcv()            # 履歴為替 OHLCV
├── commodities_prices()     # コモディティ価格（金・原油）
├── global_indices_etf()     # 国際指数および米国ETF
├── compare_rates()          # スプレッド比較
├── forex_symbols()          # サポート為替一覧
├── forex_news()             # 為替ニュース
├── forex_events()           # マクロ経済予定表
│
├── asx_symbols()            # サポートASX一覧
├── asx_ohlcv()              # 履歴 ASX OHLCV
├── asx_profile()            # 企業プロファイル ASX
├── asx_balance_sheet()      # 貸借対照表 ASX
├── asx_income_statement()   # 損益計算書 ASX
├── asx_cashflow()           # キャッシュフロー計算書 ASX
├── asx_ratios()             # 財務比率 ASX
├── asx_dividends()          # 配当実績 ASX
├── asx_announcements()      # 公示書類 ASX
│   └── asx_news()               # 企業ニュース ASX
│
├── us_ohlcv()               # 履歴 US Stock OHLCV
├── us_profile()             # 企業プロファイル US
├── us_financials()          # 財務諸表一括 US
├── us_balance_sheet()       # 貸借対照表 US
├── us_income_statement()    # 損益計算書 US
├── us_cashflow()            # キャッシュフロー計算書 US
├── us_ratios()              # 財務比率 US
├── us_dividends()           # 配当実績 US
├── us_splits()              # 分割履歴 US
├── us_calendar()            # 予定表 US
├── us_news()                # 企業ニュース US
│
├── jp_symbols()             # JP株銘柄コード一覧
├── jp_ohlcv()               # 履歴 JP株 OHLCV
├── jp_profile()             # 企業プロファイル JP
├── jp_financials()          # 財務諸表一括 JP
├── jp_balance_sheet()       # 貸借対照表 JP
├── jp_income_statement()    # 損益計算書 JP
├── jp_cashflow()            # キャッシュフロー計算書 JP
├── jp_ratios()              # 財務比率 JP
├── jp_dividends()           # 配当実績 JP
├── jp_splits()              # 分割履歴 JP
├── jp_calendar()            # 決算予定カレンダー JP
├── jp_news()                # 企業ニュース JP
│
├── cn_symbols()             # CN株銘柄コード一覧
├── cn_ohlcv()               # 履歴 CN株 OHLCV
├── cn_profile()             # 企業プロファイル CN
├── cn_financials()          # 財務諸表一括 CN
├── cn_balance_sheet()       # 貸借対照表 CN
├── cn_income_statement()    # 損益計算書 CN
├── cn_cashflow()            # キャッシュフロー計算書 CN
├── cn_ratios()              # 財務比率 CN
├── cn_dividends()           # 配当実績 CN
├── cn_splits()              # 分割履歴 CN
├── cn_quote()               # リアルタイム株価 CN (Pro)
├── cn_order_book()          # 板情報 CN (Pro)
├── cn_tick()                # 逐筆出来高 ticks CN (Pro)
├── cn_heatmap()             # 市場ヒートマップ CN
│
├── hk_symbols()             # HK株銘柄コード一覧
├── hk_ohlcv()               # 履歴 HK株 OHLCV
├── hk_profile()             # 企業プロファイル HK
├── hk_financials()          # 財務諸表一括 HK
├── hk_balance_sheet()       # 貸借対照表 HK
├── hk_income_statement()    # 損益計算書 HK
├── hk_cashflow()            # キャッシュフロー計算書 HK
├── hk_ratios()              # 財務比率 HK
├── hk_dividends()           # 配当実績 HK
├── hk_splits()              # 分割履歴 HK
├── hk_calendar()            # 決算予定カレンダー HK
├── hk_heatmap()             # 市場ヒートマップ HK
└── hk_news()                # 企業ニュース HK
```

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

<a id="roadmap"></a>
## ロードマップ

- [x] ベトナム株四本値 (KBS, VCI, MSN)
- [x] ベトナム株財務諸表 (MAS, VCI)
- [x] 世界マクロ経済指標 (World Bank, Maybank)
- [x] 投資信託データ (Fmarket)
- [x] 企業ニュース＆スケジュール (KBS, VCI)
- [x] 暗号資産市場データ (Core Engine)
- [x] 暗号資産オプションデータ (Deribit, OKX)
- [x] 外為・コモディティデータ (Core Engine)
- [x] オーストラリア株データ (ASX)
- [x] 米国株データ (US)
- [x] 日本株データ (JP)
- [x] 中国株データ (CN)
- [x] 香港株データ (HK)
- [ ] WebSocket によるリアルタイム配信

<p align="right">(<a href="#readme-top">上に戻る ↑</a>)</p>

---

ライブラリへの貢献を歓迎します！新しいデータプロバイダー (provider) を追加する場合は、テンプレートコードの自動生成とデータ品質検証を自動化する **Connector Development Kit (CDK)** をご使用ください。

詳細な手順については、**[CDK コントリビューターガイド (CDK Contributor Guide)](./CONTRIBUTING.md)** をご参照ください。

基本的な開発フロー：
1. 本リポジトリをフォークする
2. 開発用ブランチを作成する: `git checkout -b feature/new-provider`
3. テンプレートコードを自動生成する: `openstock-cdk generate --name <名前> --market <市場> --type <タイプ>`
4. API 解析ロジックとユニットテストを実装する
5. CDK 契約テストを実行する: `pytest tests/cdk/ -v`
6. プルリクエスト (Pull Request) を送信する

---

<a id="license"></a>
## ライセンス

当プロジェクトは **GNU Affero General Public License v3.0 (AGPL-3.0)** に基づいて配布されています。詳細は [`LICENSE`](LICENSE) をご参照ください。
