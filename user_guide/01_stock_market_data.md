---
id: stock-market-data
title: "Module 01: Dữ Liệu Cổ Phiếu (Stock Market Data)"
description: Hướng dẫn lấy dữ liệu OHLCV lịch sử, hồ sơ công ty và giá thời gian thực.
category: Stock
difficulty: Cơ bản
tier: Free (OHLCV, Profile) / Pro (Realtime Quote)
tags: [stock, ohlcv, profile, quote, realtime, async]
---

# Module 01: Dữ Liệu Cổ Phiếu (Stock Market Data)

Module này cung cấp dữ liệu về giá cổ phiếu lịch sử (OHLCV), hồ sơ công ty và báo giá thời gian thực.

---

## Use Case 1.1 — Lấy dữ liệu giá lịch sử OHLCV (Đồng bộ)

**Tier yêu cầu**: `Free`  
**Provider hỗ trợ**: DNSE / KBS / VCI / MSN (Hỗ trợ Tự động chọn nguồn Auto-Switching)

```python
import openstockapi as osapi

# Lấy dữ liệu OHLCV theo ngày của mã VNM
data = osapi.ohlcv(
    symbol="VNM",
    resolution="1D",       # 1D: theo ngày, 1W: theo tuần, 1M: theo tháng
    start="2025-01-01",
    end="2025-06-30",
    provider="kbs"         # Tùy chọn nguồn thủ công: "dnse", "kbs", "vci", "msn" (Bỏ qua để dùng Auto-Switching)
)

print(data)
```


**Kết quả trả về mẫu (danh sách `OHLCVBar`):**
```json
[
  {
    "time": 1735689600,
    "open": 68500.0,
    "high": 69200.0,
    "low": 68100.0,
    "close": 69000.0,
    "volume": 1250000
  }
]
```

**Tham số:**

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Có** | — | Mã cổ phiếu (VD: `VNM`, `FPT`, `VIC`) |
| `resolution` | `str` | Không | `1D` | Độ phân giải: `1`, `5`, `15`, `30`, `1D`, `1W`, `1M` |
| `start` | `str` | **Có** | — | Ngày bắt đầu định dạng `YYYY-MM-DD` |
| `end` | `str` | **Có** | — | Ngày kết thúc định dạng `YYYY-MM-DD` |
| `provider` | `str` | Không | Auto | Chỉ định nguồn dữ liệu thủ công: `"dnse"`, `"kbs"`, `"vci"`, `"msn"` |


---

## Use Case 1.2 — Lấy dữ liệu OHLCV (Bất đồng bộ / Async)

**Tier yêu cầu**: `Free`  
**Provider hỗ trợ**: DNSE / KBS / VCI / MSN (Hỗ trợ Tự động chọn nguồn Auto-Switching)

Phù hợp khi bạn cần lấy dữ liệu của nhiều mã cổ phiếu cùng lúc mà không bị chặn (non-blocking).

```python
import asyncio
import openstockapi as osapi

async def fetch_multiple():
    # Lấy đồng thời 3 mã cổ phiếu cùng một lúc
    results = await asyncio.gather(
        osapi.async_ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-06-30"),
        osapi.async_ohlcv("FPT", resolution="1D", start="2025-01-01", end="2025-06-30"),
        osapi.async_ohlcv("VIC", resolution="1D", start="2025-01-01", end="2025-06-30"),
    )
    vnm_data, fpt_data, vic_data = results
    return vnm_data, fpt_data, vic_data

vnm, fpt, vic = asyncio.run(fetch_multiple())
print(f"VNM: {len(vnm)} bars | FPT: {len(fpt)} bars | VIC: {len(vic)} bars")
```

> [!TIP]
> Sử dụng `async_ohlcv()` kết hợp `asyncio.gather()` để lấy dữ liệu nhiều mã đồng thời, giúp giảm thời gian chờ đáng kể so với gọi tuần tự.

---

## Use Case 1.3 — Lấy hồ sơ công ty (Company Profile)

**Tier yêu cầu**: `Free`  
**Provider hỗ trợ**: VNDIRECT / VCI / KBS (Hỗ trợ Tự động chọn nguồn Auto-Switching)

```python
import openstockapi as osapi

# Lấy hồ sơ công ty VNM (Tùy chọn provider: "vndirect", "vci", "kbs")
info = osapi.profile("VNM", provider="vci")


print(info.symbol)            # VNM
print(info.full_name)         # Công ty Cổ phần Sữa Việt Nam
print(info.exchange)          # HOSE
print(info.industry)          # Thực phẩm và đồ uống
print(info.tax_code)          # 0300588569
print(info.ceo)               # CEO/Đại diện pháp luật
print(info.charter_capital)   # Vốn điều lệ (Tỷ VND)
print(info.shareholders)      # Danh sách cổ đông lớn
print(info.leaders)           # Danh sách ban lãnh đạo
print(info.subsidiaries)      # Danh sách công ty con
```


---

## Use Case 1.4 — Báo giá thời gian thực (Realtime Quote)

**Tier yêu cầu**: `Pro` ⭐  
**Provider**: VCI (Vietcap)

```python
import openstockapi as osapi

# Khởi động với API key Pro
osapi.init("pro_YOUR_KEY")

quote = osapi.quote("VNM")

print(quote.symbol)       # VNM
print(quote.price)        # Giá khớp lệnh gần nhất
print(quote.volume)       # Khối lượng giao dịch luỹ kế trong ngày
print(quote.change)       # Thay đổi giá trị tuyệt đối
print(quote.pct_change)   # % thay đổi
print(quote.timestamp)    # Thời gian cập nhật
```

> [!IMPORTANT]
> Chức năng Realtime Quote yêu cầu tối thiểu tài khoản **Pro** hoặc **Premium**.

