---
id: news-and-events
title: "Module 07: Tin Tức & Sự Kiện Doanh Nghiệp (News & Events)"
description: Hướng dẫn lấy tin tức và sự kiện quan trọng của các doanh nghiệp niêm yết trên sàn chứng khoán Việt Nam.
category: News
difficulty: Cơ bản
tier: Free
tags: [news, events, corporate-actions, announcement]
---

# Module 07: Tin Tức & Sự Kiện Doanh Nghiệp (News & Events)

Module này cung cấp tin tức và sự kiện quan trọng của doanh nghiệp (chia cổ tức, họp ĐHCĐ, phát hành thêm cổ phiếu...) được tổng hợp từ nhiều nguồn tự động theo thứ tự ưu tiên.

**Tier yêu cầu**: `Free`  
**Providers:**
- **Tin tức** (`company_news`): `kbs` (KB Securities Vietnam)
- **Sự kiện** (`company_events`): `vci` (Vietcap — ưu tiên), `kbs` (KB Securities — fallback khi có sự kiện lịch sử)

---

## Use Case 7.1 — Lấy tin tức doanh nghiệp

```python
import openstockapi as osapi

# Lấy 15 tin tức mới nhất của VNM
news = osapi.company_news("VNM", limit=15)

for item in news:
    print(f"[{item.published_at.strftime('%Y-%m-%d %H:%M')}] {item.title}")
    print(f"  Nguồn: {item.source} | URL: {item.url}\n")
```

**Kết quả mẫu:**
```
[2025-07-15 09:30] VNM công bố kết quả kinh doanh Quý 2/2025
  Nguồn: KB Securities | URL: https://...

[2025-07-10 14:00] Vinamilk đẩy mạnh xuất khẩu sang thị trường Trung Đông
  Nguồn: KB Securities | URL: https://...
```

**Tham số:**

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Có** | — | Mã cổ phiếu |
| `limit` | `int` | Không | `10` | Số lượng tin trả về |
| `provider` | `str` | Không | `None` (tự động) | Chỉ định nguồn: `"kbs"` |

---

## Use Case 7.2 — Lấy sự kiện doanh nghiệp

Theo dõi các sự kiện quan trọng như: chia cổ tức, phát hành thêm cổ phiếu, họp ĐHCĐ, ngày giao dịch không hưởng quyền...

```python
import openstockapi as osapi

# Lấy sự kiện của FPT (tự động dùng VCI làm nguồn ưu tiên)
events = osapi.company_events("FPT", limit=10)

for event in events:
    print(f"[{event.event_date.strftime('%Y-%m-%d')}] {event.title}")
    print(f"  Chi tiết: {event.details}\n")

# Chỉ định nguồn cụ thể
events_vci = osapi.company_events("FPT", limit=10, provider="vci")
events_kbs = osapi.company_events("FPT", limit=10, provider="kbs")
```

**Tham số:**

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Có** | — | Mã cổ phiếu |
| `limit` | `int` | Không | `10` | Số lượng sự kiện trả về |
| `provider` | `str` | Không | `None` (tự động) | Chỉ định nguồn: `"vci"`, `"kbs"` |

**Kết quả mẫu (nguồn VCI):**
```
[2026-06-29] Mai Thị Lan Anh - Đăng kí Mua 19,767 FPT
  Chi tiết: Giao dịch nội bộ - Đăng ký mua cổ phiếu

[2026-06-29] Phát hành cổ phiếu - Phát hành cho CBCNV tỉ lệ 0.1%
  Chi tiết: Phát hành thêm cổ phiếu cho cán bộ nhân viên
```

> [!NOTE]
> Nguồn `vci` trả về nhiều loại sự kiện hơn (giao dịch nội bộ, phát hành cổ phiếu, cổ tức...).
> Nguồn `kbs` trả về dữ liệu khi có sự kiện cổ tức/quyền sắp tới, có thể rỗng khi ngoài mùa.

---

## Use Case 7.3 — Theo dõi tin tức nhiều mã cùng lúc

Sử dụng `async_ohlcv` kết hợp với `company_news` để giám sát nhiều mã đồng thời:

```python
import openstockapi as osapi

WATCHLIST = ["VNM", "FPT", "VIC", "HPG", "MBB"]

print("=== Tin tức mới nhất cho danh mục theo dõi ===\n")
for symbol in WATCHLIST:
    news = osapi.company_news(symbol, limit=1)
    if news:
        latest = news[0]
        print(f"[{symbol}] {latest.published_at.strftime('%Y-%m-%d')} — {latest.title[:80]}...")
    else:
        print(f"[{symbol}] Không có tin tức mới.")
```

---

## Use Case 7.4 — Cảnh báo sự kiện quan trọng sắp tới

Lọc các sự kiện trong tương lai để lên lịch theo dõi:

```python
import openstockapi as osapi
from datetime import datetime, timedelta

SYMBOL = "VNM"
today  = datetime.today()
events = osapi.company_events(SYMBOL, limit=20)

upcoming = [e for e in events if e.event_date >= today]

print(f"=== Sự kiện sắp tới của {SYMBOL} ===\n")
if not upcoming:
    print("Không có sự kiện nào trong tương lai gần.")
else:
    for event in upcoming:
        days_left = (event.event_date - today).days
        print(f"⏰ Còn {days_left} ngày | {event.event_date.strftime('%Y-%m-%d')} | {event.event_type}")
        print(f"   {event.description}\n")
```

> [!TIP]
> Kết hợp module này với lịch cổ tức và phân tích kỹ thuật để tìm điểm vào lệnh tốt trước các sự kiện quan trọng như ngày GDKHQ (Ngày giao dịch không hưởng quyền).
