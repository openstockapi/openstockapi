<div align="center">
  <h1> OpenStockAPI</h1>
  <img src="public/banner.png" alt="OpenStockAPI Banner" width="100%" />
  
  <p align="center">
    <a href="./README.md">English</a> · <b>Tiếng Việt</b> · <a href="./README_JP.md">日本語</a> · <a href="./README_CN.md">简体中文</a> · <a href="./README_HK.md">繁體中文</a>
  </p>

  <p><strong>Thư viện Python miễn phí, mã nguồn mở giúp tải dữ liệu lịch sử chứng khoán (OHLCV), bảng giá trực tuyến (real-time), sổ lệnh, khớp lệnh chi tiết và tin tức tài chính Việt Nam & Quốc tế.</strong></p>

  <p>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/v/openstockapi.svg?color=blue&label=PyPI" alt="PyPI version"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/dm/openstockapi.svg?color=brightgreen&label=Downloads" alt="Lượt tải"></a>
    <a href="https://pypi.org/project/openstockapi/"><img src="https://img.shields.io/pypi/pyversions/openstockapi.svg" alt="Python Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL%203.0-orange.svg" alt="License"></a>
  </p>

  <p>
    <a href="./user_guide/getting_started.md"><strong> Đọc tài liệu đầy đủ »</strong></a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=bug">Báo lỗi</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/YOUR_USERNAME/openstockapi/issues/new?labels=enhancement">Đề xuất tính năng</a>
  </p>
</div>

---

>  An English version of this README is available: **[README.md](./README.md)**

---

<!-- MỤC LỤC -->
<details>
  <summary>📋 Mục lục</summary>
  <ol>
    <li><a href="#gioi-thieu">Giới thiệu dự án</a></li>
    <li><a href="#tinh-nang"> Tính năng nổi bật</a></li>
    <li><a href="#bat-dau-nhanh"> Bắt đầu nhanh</a></li>
    <li><a href="#cai-dat"> Cài đặt</a></li>
    <li><a href="#su-dung"> Hướng dẫn sử dụng</a></li>
    <li><a href="#providers"> Danh sách Providers</a></li>
    <li><a href="#modules"> Tổng quan các Module</a></li>
    <li><a href="#faq"> Câu hỏi thường gặp</a></li>
    <li><a href="#roadmap"> Roadmap</a></li>
    <li><a href="#dong-gop"> Đóng góp</a></li>
    <li><a href="#changelog"> Nhật ký thay đổi</a></li>
    <li><a href="#license"> Giấy phép</a></li>
  </ol>
</details>

---

<a id="gioi-thieu"></a>
## Giới thiệu dự án

**OpenStockAPI** là thư viện Python miễn phí, mã nguồn mở đóng vai trò là **Data Plane** chuyên nghiệp để tải, phân tích và chuẩn hóa dữ liệu lịch sử chứng khoán (OHLCV), bảng giá trực tuyến (real-time quotes), sổ lệnh (orderbook), khớp lệnh chi tiết (ticks), tin tức doanh nghiệp, và báo cáo tài chính từ thị trường Việt Nam (`HOSE`, `HNX`, `UPCOM`), Mỹ, Nhật Bản, Trung Quốc, Hồng Kông, Úc cùng các cặp Crypto và Forex toàn cầu.

Thư viện được thiết kế tối ưu làm tầng thu thập dữ liệu nguồn vào cho các ứng dụng tài chính, hệ thống giao dịch tự động (algorithmic trading), Excel add-in và Amibroker plugin — xử lý tự động cơ chế chuyển nguồn (provider fallback), rate limiting cục bộ, cache validation và kiểm soát phân quyền thiết bị.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="tinh-nang"></a>
## Tính năng nổi bật

- ** Đa thị trường & Đa tài sản** — Hỗ trợ cổ phiếu Việt Nam (`VN`), Tiền điện tử (`Crypto`), và Ngoại hối & Hàng hóa (`Forex & Commodities`).
- ** Tự động Fallback đa nguồn** — Tích hợp các Provider (KBS, VCI, MSN, MAS, Maybank, Fmarket, Core Engine) với cơ chế tự động chuyển nguồn minh bạch.
- ** Xác thực JWT & Phân quyền Freemium** — Hỗ trợ cơ chế Handshake lấy token JWT và kiểm soát phân quyền `Free`, `Pro` và `Premium` kèm Token Bucket Rate Limiter chạy hoàn toàn phía client.
- ** Hỗ trợ Async** — Hỗ trợ `async/await` đầy đủ qua `async_ohlcv()` và `async_crypto_ohlcv()`.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="bat-dau-nhanh"></a>
## Bắt đầu nhanh

```python
import openstockapi as osapi

# Khởi tạo với API key (bắt buộc cho tất cả tất cả tier)
# Đăng ký miễn phí tại: https://openstockapi.dev/register
osapi.init("free_YOUR_KEY")   # hoặc "pro_YOUR_KEY" / "premium_YOUR_KEY"

# Lịch sử giá OHLCV (đồng bộ)
df = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-12-31")
print(df.head())

# Lấy dữ liệu Crypto (Tiền điện tử)
btc_ohlcv = osapi.crypto_ohlcv("BTCUSDT", interval="1h", limit=5)
print(btc_ohlcv)

# Lấy dữ liệu Forex & Hàng hóa (Tỷ giá & Giá Vàng)
rates = osapi.forex_rates(base="USD")
gold_price = osapi.commodities_prices(symbol="GOLD", range_val="5d", interval="1h")
print(f"USD/VND: {rates['rates']['VND']} | Gold: {gold_price['regularMarketPrice']} USD")
```

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="cai-dat"></a>
## Cài đặt

**Cài đặt cơ bản:**
```bash
pip install openstockapi
```

**Cài đặt kèm hỗ trợ Pandas DataFrame & xuất Excel:**
```bash
pip install openstockapi[pandas]
```

**Yêu cầu:** Python 3.8 trở lên.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="su-dung"></a>
## Hướng dẫn sử dụng

Tài liệu đầy đủ, ví dụ mã nguồn và kết quả mẫu cho từng module:

 **[User Guide — Bắt đầu](./user_guide/getting_started.md)**

| Module | Mô tả | Tài liệu |
|--------|-------|----------|
| 01 — OHLCV & Hồ sơ | Lịch sử giá, hồ sơ doanh nghiệp | [](./user_guide/01_stock_market_data.md) |
| 02 — Báo cáo tài chính | Cân đối kế toán, KQKD, Lưu chuyển tiền | [](./user_guide/02_financial_statements.md) |
| 03 — Giá thời gian thực | Giá live, sổ lệnh | [](./user_guide/03_realtime_quote.md) |
| 04 — Chỉ số thị trường | VNINDEX, thành phần VN30 | [](./user_guide/04_order_book.md) |
| 05 — Chỉ số vĩ mô | CPI, Cung tiền M2, Tăng trưởng tín dụng | [](./user_guide/05_macro_indicators.md) |
| 06 — Quỹ đầu tư | NAV quỹ mở, danh mục nắm giữ | [](./user_guide/06_mutual_funds.md) |
| 07 — Tin tức & Sự kiện | Tin tức, cổ tức, ĐHCĐ | [](./user_guide/07_news_and_events.md) |
| 10 — Dữ Liệu Chứng Khoán Úc | Mã niêm yết, OHLCV, Báo cáo tài chính, Cổ tức, Thông báo, Tin tức ASX | [Tài liệu Module 10](./user_guide/asx/01_asx_market_data.md) |
| 11 — Dữ Liệu Chứng Khoán Mỹ | OHLCV, Hồ sơ công ty, Báo cáo tài chính, Cổ tức, Lịch chia tách, Tin tức US | [Tài liệu Module 11](./user_guide/us_stock/01_us_market_data.md) |
| 12 — Dữ Liệu Chứng Khoán Nhật | Mã niêm yết, OHLCV, Hồ sơ công ty, Báo cáo tài chính, Cổ tức, Lịch sự kiện, Tin tức JP | [Tài liệu Module 12](./user_guide/jp_stock/01_jp_market_data.md) |
| 13 — Dữ Liệu Chứng Khoán Trung Quốc | Mã niêm yết, OHLCV, Hồ sơ công ty, Báo cáo tài chính, Cổ tức, Giá live, Ticks, Sổ lệnh, Heatmap CN | [Tài liệu Module 13](./user_guide/cn_stock/01_cn_market_data.md) |
| 14 — Dữ Liệu Chứng Khoán Hồng Kông | Mã niêm yết, OHLCV, Hồ sơ công ty, Báo cáo tài chính, Cổ tức, Lịch sự kiện, Tin tức, Heatmap HK | [Tài liệu Module 14](./user_guide/hk_stock/01_hk_market_data.md) |


<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="providers"></a>
## Danh sách Providers

Các Provider được phân nhóm theo thị trường/loại tài sản. Trong mỗi nhóm, Provider được thử lần lượt theo thứ tự ưu tiên — nếu một nguồn lỗi, hệ thống tự động chuyển sang nguồn tiếp theo mà không cần can thiệp thủ công.

### Cổ phiếu Việt Nam
| Provider | Nguồn | Tier | Loại dữ liệu |
|---|---|---|---|
| `kbs` | KB Securities Vietnam | Free | OHLCV, Hồ sơ công ty, Tin tức, Sự kiện |
| `vci` | Vietcap Securities | Free | OHLCV, Hồ sơ, BCTC, GD Nội bộ/Ngoại tệ/Tự doanh, Sự kiện |
| `msn` | MSN Finance (Bing) | Free | OHLCV (VN & Quốc tế) |
| `mas` | MAS (Mass Asset Securities) | Free | BCTC, Chỉ số tài chính |
| `mbk` | Maybank Securities Vietnam | Free | Chỉ số vĩ mô (M2, Tăng trưởng tín dụng) |
| `fmarket` | Fmarket Vietnam | Free | NAV và danh mục quỹ mở |
| `tcbs` | TCBS (Techcom Securities) | Free | Giá live, Sổ lệnh |

### Tiền điện tử (Cryptocurrency)

Dữ liệu tiền điện tử được cung cấp thông qua **OpenStockAPI Core Engine** — một tầng tích hợp được quản lý và đóng nguồn với khả năng tự động chuyển đổi nguồn (failover) và chuẩn hóa dữ liệu đa nguồn. Các sàn giao dịch và nguồn dữ liệu đầu nguồn cụ thể không được công bố.

| Tính năng | Tier |
|---|---|
| Crypto OHLCV (historical klines) | Free |
| Crypto OHLCV (async) | Free |
| Sổ lệnh & độ sâu (Depth) | Pro |
| Chỉ báo Phái sinh (OI, Funding Rate) | Pro |
| Bản đồ nhiệt Delta Footprint | Premium |
| Mô phỏng Đòn bẩy & Ký quỹ | Pro |
| Danh sách mã hỗ trợ | Free |
| Bảng giá thời gian thực (Tickers) | Pro |
| Danh sách hợp đồng Quyền chọn | Pro |
| Chuỗi dữ liệu Quyền chọn (Strikes, IV, Bid/Ask) | Pro |
| Greeks & Báo giá chi tiết Quyền chọn | Pro |
| Heatmap thị trường Crypto | Free |

### Ngoại hối & Hàng hóa (Forex & Commodities)

Dữ liệu Ngoại hối và Hàng hóa được cung cấp thông qua **OpenStockAPI Core Engine** với cơ chế tự động chuyển mạch (failover) qua nhiều nhà cung cấp giá và tỷ giá. Các nguồn cung cấp cụ thể không được công bố.

| Tính năng | Tier |
|---|---|
| Tỷ giá Forex (Forex Spot Rates) | Free |
| Forex OHLCV | Free |
| Giá Hàng hóa (Vàng, Dầu thô...) | Free |
| Chỉ số toàn cầu & ETF (SPY, QQQ) | Free |
| So sánh tỷ giá liên sàn | Pro |
| Danh sách mã Forex hỗ trợ | Free |
| Tin tức thị trường Forex | Free |
| Lịch sự kiện vĩ mô toàn cầu | Free |

### Cổ phiếu Úc (Australian Stock Market)
| Provider | Nguồn | Tier | Loại dữ liệu |
|---|---|---|---|
| `core` | Core Engine | Free | Danh sách mã, OHLCV, Hồ sơ công ty, BCTC (Balance Sheet, Income Statement, Cashflow, Ratios), Cổ tức, Thông báo, Tin tức |

### Cổ phiếu Mỹ (US Stock Market)
| Provider | Nguồn | Tier | Loại dữ liệu |
|---|---|---|---|
| `core` | Core Engine | Free | OHLCV, Hồ sơ công ty, BCTC (Balance Sheet, Income Statement, Cashflow, Ratios), Cổ tức, Lịch chia tách, Lịch sự kiện, Tin tức |

### Cổ phiếu Nhật Bản (Japanese Stock Market)
| Provider | Nguồn | Tier | Loại dữ liệu |
|---|---|---|---|
| `core` | Core Engine | Free | Danh sách mã, OHLCV, Hồ sơ công ty, BCTC (Balance Sheet, Income Statement, Cashflow, Ratios), Cổ tức, Lịch sự kiện, Tin tức |

### Cổ phiếu Trung Quốc (China Stock Market)
| Provider | Nguồn | Tier | Loại dữ liệu |
|---|---|---|---|
| `core` | Core Engine | Free / Pro | Danh sách mã, OHLCV, Hồ sơ công ty, BCTC, Cổ tức, Lịch chia tách (Free); Giá live, Sổ lệnh, Ticks (Pro) |

### Cổ phiếu Hồng Kông (HK Stock Market)
| Provider | Nguồn | Tier | Loại dữ liệu |
|---|---|---|---|
| `core` | Core Engine | Free | Danh sách mã, OHLCV, Hồ sơ công ty, BCTC, Cổ tức, Lịch sự kiện, Tin tức |

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>



---

<a id="modules"></a>
## Tổng quan các Module

```
openstockapi
├── symbols()                # Lấy danh sách mã chứng khoán (symbols)
├── ohlcv()                  # Lịch sử OHLCV Stock (đồng bộ)
├── async_ohlcv()            # Lịch sử OHLCV Stock (bất đồng bộ)
├── profile()                # Hồ sơ doanh nghiệp Stock
├── derivative_profile()     # Thông tin Phái sinh (HĐTL/Chứng quyền) Stock
├── balance_sheet()          # Bảng cân đối kế toán Stock
├── income_statement()       # Kết quả kinh doanh Stock
├── cashflow()               # Lưu chuyển tiền tệ Stock
├── ratios()                 # Chỉ số tài chính Stock
├── quote()                  # Giá Stock thời gian thực
├── order_book()             # Sổ lệnh Stock (Order Book)
├── market_index()           # OHLCV chỉ số Stock
├── macro_indicators()       # Chỉ số kinh tế vĩ mô
├── fund_details()           # Thông tin quỹ đầu tư Stock
├── company_news()           # Tin tức doanh nghiệp Stock (hỗ trợ route sang Crypto/Forex qua market)
├── company_events()         # Sự kiện doanh nghiệp Stock (hỗ trợ route sang Crypto/Forex qua market)
├── vn_heatmap()             # Bản đồ nhiệt thị trường VN
│
├── crypto_ohlcv()           # Lịch sử Crypto (đồng bộ)
├── async_crypto_ohlcv()     # Lịch sử Crypto (bất đồng bộ)
├── crypto_depth()           # Sổ lệnh Crypto (Order Book)
├── crypto_derivatives()     # Chỉ báo phái sinh Crypto (OI, Funding)
├── crypto_footprint()       # Bản đồ Footprint & Delta Crypto
├── simulate_leverage()      # Mô phỏng margin/leverage Crypto
├── crypto_symbols()         # Danh sách mã Crypto hỗ trợ
├── crypto_tickers()         # Giá ticker Crypto thời gian thực
├── crypto_options_instruments() # Danh sách hợp đồng Quyền chọn hỗ trợ
├── crypto_options_chain()   # Chuỗi dữ liệu Quyền chọn (Options Chain)
├── crypto_options_ticker()  # Giá chi tiết & chỉ số Greeks Quyền chọn
├── crypto_news()            # Tin tức Crypto
├── crypto_events()          # Lịch sự kiện Crypto
├── crypto_profile()         # Hồ sơ mã Token & logo Crypto
├── crypto_heatmap()         # Bản đồ nhiệt thị trường Crypto
├── CryptoStream             # Client WebSocket streaming giá trực tuyến
│
├── forex_rates()            # Tỷ giá Forex
├── forex_ohlcv()            # Biểu đồ nến Forex
├── commodities_prices()     # Giá Vàng/Dầu thô
├── global_indices_etf()     # Chỉ số quốc tế & ETF Mỹ (SPY)
├── compare_rates()          # So sánh tỷ giá liên ngân hàng
├── forex_symbols()          # Danh sách mã Forex hỗ trợ
├── forex_news()             # Tin tức Forex
├── forex_events()           # Lịch sự kiện Forex
│
├── asx_symbols()            # Danh sách mã ASX niêm yết
├── asx_ohlcv()              # Lịch sử OHLCV ASX
├── asx_profile()            # Hồ sơ doanh nghiệp ASX
├── asx_balance_sheet()      # Bảng cân đối kế toán ASX
├── asx_income_statement()   # Kết quả kinh doanh ASX
├── asx_cashflow()           # Lưu chuyển tiền tệ ASX
├── asx_ratios()             # Chỉ số tài chính ASX
├── asx_dividends()          # Lịch sử trả cổ tức ASX
├── asx_announcements()      # PDF thông báo doanh nghiệp ASX
│   └── asx_news()               # Tin tức doanh nghiệp ASX
│
├── us_ohlcv()               # Lịch sử OHLCV US
├── us_profile()             # Hồ sơ doanh nghiệp US
├── us_financials()          # Báo cáo tài chính raw US
├── us_balance_sheet()       # Bảng cân đối kế toán US
├── us_income_statement()    # Kết quả kinh doanh US
├── us_cashflow()            # Lưu chuyển tiền tệ US
├── us_ratios()              # Chỉ số tài chính US
├── us_dividends()           # Lịch sử trả cổ tức US
├── us_splits()              # Lịch sử chia tách cổ phiếu US
├── us_calendar()            # Lịch sự kiện doanh nghiệp US
├── us_news()                # Tin tức doanh nghiệp US
│
├── jp_symbols()             # Danh sách mã JP niêm yết
├── jp_ohlcv()               # Lịch sử OHLCV JP
├── jp_profile()             # Hồ sơ doanh nghiệp JP
├── jp_financials()          # Báo cáo tài chính raw JP
├── jp_balance_sheet()       # Bảng cân đối kế toán JP
├── jp_income_statement()    # Kết quả kinh doanh JP
├── jp_cashflow()            # Lưu chuyển tiền tệ JP
├── jp_ratios()              # Chỉ số tài chính JP
├── jp_dividends()           # Lịch sử trả cổ tức JP
├── jp_splits()              # Lịch sử chia tách cổ phiếu JP
├── jp_calendar()            # Lịch sự kiện doanh nghiệp JP
├── jp_news()                # Tin tức doanh nghiệp JP
│
├── cn_symbols()             # Danh sách mã CN niêm yết
├── cn_ohlcv()               # Lịch sử OHLCV CN
├── cn_profile()             # Hồ sơ doanh nghiệp CN
├── cn_financials()          # Báo cáo tài chính raw CN
├── cn_balance_sheet()       # Bảng cân đối kế toán CN
├── cn_income_statement()    # Kết quả kinh doanh CN
├── cn_cashflow()            # Lưu chuyển tiền tệ CN
├── cn_ratios()              # Chỉ số tài chính CN
├── cn_dividends()           # Lịch sử trả cổ tức CN
├── cn_splits()              # Lịch sử chia tách cổ phiếu CN
├── cn_quote()               # Giá live CN thời gian thực (Pro)
├── cn_order_book()          # Sổ lệnh CN thời gian thực (Pro)
├── cn_tick()                # Ticks giao dịch CN trong ngày (Pro)
├── cn_heatmap()             # Heatmap thị trường CN
│
├── hk_symbols()             # Danh sách mã HK niêm yết
├── hk_ohlcv()               # Lịch sử OHLCV HK
├── hk_profile()             # Hồ sơ doanh nghiệp HK
├── hk_financials()          # Báo cáo tài chính raw HK
├── hk_balance_sheet()       # Bảng cân đối kế toán HK
├── hk_income_statement()    # Kết quả kinh doanh HK
├── hk_cashflow()            # Lưu chuyển tiền tệ HK
├── hk_ratios()              # Chỉ số tài chính HK
├── hk_dividends()           # Lịch sử trả cổ tức HK
├── hk_splits()              # Lịch sử chia tách cổ phiếu HK
├── hk_calendar()            # Lịch sự kiện doanh nghiệp HK
├── hk_heatmap()             # Heatmap thị trường HK
└── hk_news()                # Tin tức doanh nghiệp HK

```

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="faq"></a>
## Câu hỏi thường gặp

**Q: Có cần API Key không?**
> **Có.** Tất cả tiế kể cả Free đều yêu cầu đăng ký để nhận API Key. Đăng ký miễn phí tại [openstockapi.dev/register](https://openstockapi.dev/register).
> Key Free có dạng `free_xxx`, Pro là `pro_xxx`, Premium là `premium_xxx`.

**Q: Dữ liệu OHLCV lấy từ nguồn nào? Có chính xác không?**
> Dữ liệu được lấy từ KB Securities, Vietcap và MSN Finance — đây là các nguồn công khai chuẩn từ sàn HOSE/HNX. Ba nguồn được kiểm tra chéo qua bộ UAT tự động.

**Q: Tại sao đôi khi một module trả về ít dữ liệu hơn dự kiến?**
> Hệ thống tự động chọn nguồn khả dụng. Có thể chỉ định nguồn cụ thể bằng tham số `provider="kbs"` hoặc `provider="vci"` để kiểm tra từng nguồn.

**Q: Phân quyền `Pro` / `Premium` hoạt động như thế nào?**
> Tier được xác định tự động dựa trên tiền tố API Key (`free_`, `pro_`, `premium_`). Tỷ lệ request được giới hạn theo tier qua Token Bucket Rate Limiter phía client.

**Q: Có hỗ trợ `async` không?**
> Có. Dùng `await osapi.async_ohlcv(...)` trong vòng lặp async để tải dữ liệu nhiều mã song song hiệu quả hơn.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="roadmap"></a>
## Roadmap

- [x] OHLCV cổ phiếu Việt Nam (KBS, VCI, MSN)
- [x] Báo cáo tài chính (MAS, VCI)
- [x] Chỉ số kinh tế vĩ mô (World Bank, Maybank)
- [x] Dữ liệu quỹ mở (Fmarket)
- [x] Tin tức & sự kiện doanh nghiệp (KBS, VCI)
- [x] Dữ liệu tiền mã hóa (Cryptocurrency) (Core Engine)
- [x] Dữ liệu quyền chọn Crypto Options (Deribit, OKX)
- [x] Ngoại hối & Hàng hóa (Forex & Commodities) (Core Engine)
- [x] Dữ liệu cổ phiếu thị trường Úc (ASX)
- [x] Dữ liệu cổ phiếu thị trường Mỹ (US)
- [ ] WebSocket streaming giá thời gian thực

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="dong-gop"></a>
## Đóng góp

Mọi đóng góp đều được chào đón! Nếu bạn muốn thêm một nhà cung cấp dữ liệu mới (provider), hãy sử dụng bộ công cụ **Connector Development Kit (CDK)** của chúng tôi để tự động hóa việc sinh mã nguồn mẫu và kiểm tra chất lượng dữ liệu.

Xem hướng dẫn từng bước chi tiết tại **[Tài liệu hướng dẫn CDK Contributor](./CONTRIBUTING.md)**.

Quy trình cơ bản:
1. Fork repository
2. Tạo nhánh: `git checkout -b feature/ten-provider`
3. Sinh template provider: `openstock-cdk generate --name <tên> --market <thị trường> --type <loại>`
4. Viết logic parse dữ liệu trong file provider và viết unit test
5. Chạy kiểm thử tự động: `pytest tests/cdk/ -v`
6. Mở Pull Request

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="changelog"></a>
## Nhật ký thay đổi

Theo dõi các cập nhật, tính năng mới và sửa lỗi tại:

 **[CHANGELOG.md](./CHANGELOG.md)**

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="license"></a>
## Giấy phép

Dự án này được phát hành theo giấy phép **GNU Affero General Public License v3.0 (AGPL-3.0)**. Xem [`LICENSE`](LICENSE) để biết thêm chi tiết.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>
