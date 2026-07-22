---
title: Getting Started with OpenStockAPI
description: Quick start guide and index for openstockapi user guide.
---

# Hướng dẫn sử dụng OpenStockAPI

Chào mừng bạn đến với **OpenStockAPI** — thư viện mã nguồn mở (Apache 2.0) cung cấp dữ liệu thị trường chứng khoán Việt Nam, được thiết kế để chạy hoàn toàn trên máy người dùng (local).

---

## Cài đặt (Installation)

```bash
pip install openstockapi
```

Cài đặt thêm hỗ trợ Pandas DataFrame:

```bash
pip install openstockapi[pandas]
```

---

## Thiết lập Session

```python
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Tài khoản Free: dùng key mặc định
set_current_session("free")

# Tài khoản Pro/Premium: dùng API key của bạn
set_current_session("YOUR_API_KEY")
```

---

## Mô hình Tier (Phân quyền)

| Tier | Rate Limit | Tính năng |
| :--- | :--- | :--- |
| `Free` | 10 req/phút | OHLCV, Báo cáo tài chính, Hồ sơ công ty, Tin tức, Quỹ mở, Vĩ mô |
| `Pro` ⭐ | 200 req/phút | **Tất cả Free** + Realtime Quote, Order Book, Giao dịch khối |
| `Premium` | 500 req/phút | **Tất cả Pro** với rate limit cao hơn |

---

## Danh sách Module (Use Cases)

| Module | Mô tả | Tier |
| :--- | :--- | :--- |
| [01 — Dữ Liệu Cổ Phiếu](./01_stock_market_data.md) | OHLCV lịch sử, hồ sơ công ty, giá realtime | Free / Pro |
| [02 — Báo Cáo Tài Chính](./02_financial_statements.md) | Bảng CĐKT, KQKD, LCTT, chỉ số tài chính | Free |
| [03 — Giao Dịch Khối](./03_block_trading.md) | Giao dịch ngoại, tự doanh, nội bộ | **Pro** |
| [04 — Sổ Lệnh & Độ Sâu](./04_order_book.md) | Bid/Ask spread, Market Depth | **Pro** |
| [05 — Chỉ Số Vĩ Mô](./05_macro_indicators.md) | Cung tiền M2, Tín dụng NHNN | Free |
| [06 — Quỹ Mở](./06_mutual_funds.md) | NAV, phí quản lý, danh mục nắm giữ | Free |
| [07 — Tin Tức & Sự Kiện](./07_news_and_events.md) | Tin tức doanh nghiệp, lịch sự kiện | Free |

---

## Ví dụ nhanh (Quick Example)

```python
import openstockapi as osapi

# Lấy giá lịch sử VNM
data = osapi.ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-06-30")
print(f"Lấy được {len(data)} phiên giao dịch")

# Lấy hồ sơ công ty
profile = osapi.profile("VNM")
print(f"{profile.symbol} — {profile.company_name}")

# Lấy tin tức mới nhất
news = osapi.company_news("VNM", limit=3)
for n in news:
    print(f"[{n.published_at.date()}] {n.title}")
```

---

> Dự án này được phát hành theo **Apache License 2.0**. Mọi đóng góp đều được chào đón tại [GitHub repository](https://github.com/openstockapi/openstockapi).
