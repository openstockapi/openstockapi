<div align="center">
  <h1> OpenStockAPI</h1>
  <p><strong>Thư viện Python mã nguồn mở — Data Plane mô-đun hóa cho dữ liệu thị trường tài chính Việt Nam & Quốc tế.</strong></p>

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

**OpenStockAPI** là thư viện Python mã nguồn mở, đóng vai trò là **Data Plane** (tầng thu thập và chuẩn hóa dữ liệu) cho các ứng dụng tài chính.

Thư viện tổng hợp dữ liệu từ nhiều nguồn cấp (KB Securities, Vietcap, MSN Finance...) với cơ chế tự động chuyển nguồn khi gián đoạn — ứng dụng của bạn không cần biết nguồn dữ liệu đến từ đâu, chỉ cần gọi API và nhận kết quả.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="tinh-nang"></a>
## Tính năng nổi bật

- ** Đa thị trường** — Hỗ trợ cổ phiếu Việt Nam (`VN`) và có thể mở rộng ra quốc tế (`US`) với cùng một API.
- ** Tự động Fallback đa nguồn** — Tích hợp các Provider (KBS, VCI, MSN, MAS, Maybank, Fmarket) với cơ chế tự động chuyển nguồn minh bạch.
- ** Phân quyền Freemium** — Hỗ trợ phân quyền `Free`, `Pro` (200 req/phút) và `Premium` (500 req/phút) với Token Bucket Rate Limiter chạy hoàn toàn phía client.
- ** Hỗ trợ Async** — Hỗ trợ `async/await` đầy đủ qua `async_ohlcv()` cho pipeline dữ liệu hiệu năng cao.

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

# Báo cáo tài chính — Bảng cân đối kế toán
bs = osapi.balance_sheet("VNM", period="annual")

# Giá thị trường thời gian thực
quote = osapi.quote("HPG")
print(f"{quote.symbol}: {quote.price:,.0f} VND ({quote.pct_change:+.2f}%)")

# Tin tức & Sự kiện doanh nghiệp
news   = osapi.company_news("FPT", limit=5)
events = osapi.company_events("FPT", limit=5)
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

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="providers"></a>
## Danh sách Providers

| Provider | Nguồn | Tier | Loại dữ liệu |
|----------|-------|------|--------------|
| `kbs` | KB Securities Vietnam | Free | OHLCV, Hồ sơ công ty, Tin tức, Sự kiện |
| `vci` | Vietcap Securities | Free | OHLCV, Hồ sơ, BCTC, GD Nội bộ/Ngoại tệ/Tự doanh, Sự kiện |
| `msn` | MSN Finance (Bing) | Free | OHLCV (VN & Quốc tế) |
| `mas` | MAS (Mass Asset Securities) | Free | BCTC, Chỉ số tài chính |
| `mbk` | Maybank Securities Vietnam | Free | Chỉ số vĩ mô (M2, Tín dụng) |
| `fmarket` | Fmarket Vietnam | Free | NAV và danh mục quỹ mở |
| `tcbs` | TCBS (Techcom Securities) | Free | Giá live, Sổ lệnh |

>  Mỗi loại dữ liệu có danh sách provider ưu tiên riêng. Khi một provider gặp sự cố, hệ thống tự động chuyển sang provider tiếp theo mà không cần can thiệp thủ công.

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="modules"></a>
## Tổng quan các Module

```
openstockapi
├── ohlcv()                  # Lịch sử OHLCV (đồng bộ)
├── async_ohlcv()            # Lịch sử OHLCV (bất đồng bộ)
├── profile()                # Hồ sơ doanh nghiệp
├── balance_sheet()          # Bảng cân đối kế toán
├── income_statement()       # Kết quả kinh doanh
├── cashflow()               # Lưu chuyển tiền tệ
├── ratios()                 # Chỉ số tài chính (PE, PB, ROE...)
├── quote()                  # Giá thị trường thời gian thực
├── order_book()             # Sổ lệnh (Order Book)
├── market_index()           # OHLCV chỉ số thị trường
├── index_constituents()     # Danh sách thành phần chỉ số
├── macro_indicators()       # Chỉ số kinh tế vĩ mô
├── fund_details()           # Thông tin quỹ đầu tư
├── company_news()           # Tin tức doanh nghiệp
└── company_events()         # Sự kiện doanh nghiệp (cổ tức, ESOP...)
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
- [ ] OHLCV cổ phiếu Quốc tế (MSN, Yahoo Finance)
- [ ] Dữ liệu tiền mã hóa (Cryptocurrency)
- [ ] Dữ liệu phái sinh / Hợp đồng tương lai
- [ ] WebSocket streaming giá thời gian thực

<p align="right">(<a href="#readme-top">lên đầu trang ↑</a>)</p>

---

<a id="dong-gop"></a>
## Đóng góp

Mọi đóng góp đều được chào đón! Nếu bạn muốn thêm provider mới, sửa lỗi hay cải thiện tài liệu:

1. Fork repository
2. Tạo nhánh: `git checkout -b feature/ten-tinh-nang`
3. Commit thay đổi
4. Mở Pull Request

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
