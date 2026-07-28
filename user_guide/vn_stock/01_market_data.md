---
id: market-data
title: "Module 01: Dữ Liệu Thị Trường (Market Data)"
description: Hướng dẫn lấy dữ liệu OHLCV lịch sử, hồ sơ công ty, báo giá thời gian thực, sổ lệnh bid/ask và giao dịch thỏa thuận.
category: Stock
difficulty: Trung bình
tier: Free / Pro
tags: [stock, ohlcv, profile, quote, realtime, async, order-book, block-trading]
---

# Module 01: Dữ Liệu Thị Trường (Market Data)

Module này cung cấp dữ liệu về giá cổ phiếu lịch sử (OHLCV), hồ sơ công ty, báo giá thời gian thực, giao dịch khối/thỏa thuận và sổ lệnh/sổ khớp lệnh.

---

## 1. Dữ liệu cổ phiếu và báo giá thời gian thực

### Use Case 1.1 — Lấy dữ liệu giá lịch sử OHLCV (Đồng bộ)

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

### Use Case 1.2 — Lấy dữ liệu OHLCV (Bất đồng bộ / Async)

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

### Use Case 1.3 — Lấy hồ sơ công ty (Company Profile)

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

### Use Case 1.4 — Báo giá thời gian thực (Realtime Quote)

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

---

### Use Case 1.5 — Bản đồ nhiệt thị trường (Vietnam Stock Heatmap)

**Tier yêu cầu**: `Free`  
**Provider**: Auto-Switched / `tradingview`

```python
import openstockapi as osapi

# Lấy dữ liệu heatmap thị trường Việt Nam (Mặc định top 500 mã theo vốn hoá)
heatmap = osapi.vn_heatmap(limit=5, provider="tradingview")
print(heatmap)
```

**Kết quả trả về mẫu (danh sách `HeatmapItem`):**
```json
[
  {
    "symbol": "VCB",
    "name": "Joint Stock Commercial Bank for Foreign Trade of Vietnam",
    "change": -0.5,
    "market_cap": 500000000000000.0,
    "sector": "Finance",
    "industry": "Regional Banks",
    "logo_url": "https://s3-symbol-logo.tradingview.com/vietnam-com.svg",
    "provider": "tradingview",
    "market": "vn",
    "asset_class": "stock"
  }
]
```

**Tham số:**

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | Không | `500` | Số lượng mã tối đa trả về |
| `provider` | `str` | Không | `None` | Nguồn dữ liệu: `"tradingview"` |

---

## 2. Giao dịch khối (Block Trading Data)

> [!IMPORTANT]
> Toàn bộ phần giao dịch khối yêu cầu tối thiểu tài khoản **Pro**. Gọi API với tài khoản Free sẽ nhận lỗi `TierRequiredError`.

**Tier yêu cầu**: `Pro` ⭐  
**Provider**: VCI (Vietcap Securities)

### Use Case 1.6 — Giao dịch khối ngoại (Foreign Trading)

Theo dõi hành động mua bán của nhà đầu tư nước ngoài (khối ngoại):

```python
import openstockapi as osapi

# Lấy 20 giao dịch khối ngoại gần nhất của VNM
data = osapi.foreign("VNM", limit=20)

for entry in data:
    action = "MUA" if entry.buy_volume > entry.sell_volume else "BÁN"
    print(f"{entry.date} | {action} | Mua: {entry.buy_volume:,} | Bán: {entry.sell_volume:,} | Net: {entry.net_volume:,}")
```

**Kết quả mẫu:**
```
2025-06-30 | MUA | Mua: 850,000 | Bán: 320,000 | Net: +530,000
2025-06-27 | BÁN | Mua: 120,000 | Bán: 980,000 | Net: -860,000
```

**Tham số:**

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Có** | — | Mã cổ phiếu |
| `limit` | `int` | Không | `10` | Số lượng bản ghi trả về |

---

### Use Case 1.7 — Giao dịch tự doanh (Proprietary Trading)

Theo dõi hoạt động tự doanh của các công ty chứng khoán:

```python
import openstockapi as osapi

# Lấy 10 giao dịch tự doanh gần nhất
data = osapi.prop_trade("HPG", limit=10)

for entry in data:
    print(f"{entry.date} | {entry.firm_name}")
    print(f"  Mua: {entry.buy_volume:,} cổ phiếu | Bán: {entry.sell_volume:,} cổ phiếu")
```

---

### Use Case 1.8 — Giao dịch nội bộ / Cổ đông lớn (Insider Trading)

Theo dõi hành động mua bán của ban lãnh đạo và cổ đông lớn:

```python
import openstockapi as osapi

# Lấy giao dịch nội bộ của FPT
data = osapi.insider("FPT", limit=10)

for entry in data:
    print(f"{entry.date} | {entry.person_name} ({entry.position})")
    print(f"  Loại: {entry.transaction_type} | Khối lượng: {entry.volume:,} | Giá: {entry.price:,.0f} VND")
```

**Kết quả mẫu:**
```
2025-06-15 | Nguyễn Văn A (Chủ tịch HĐQT)
  Loại: Mua | Khối lượng: 100,000 | Giá: 95,200 VND
2025-06-01 | Trần Thị B (Thành viên HĐQT)
  Loại: Bán | Khối lượng: 50,000 | Giá: 96,500 VND
```

---

### Use Case 1.9 — Phân tích tâm lý thị trường qua dòng tiền ngoại

Kết hợp foreign trading để phân tích xu hướng mua/bán ròng của khối ngoại:

```python
import openstockapi as osapi

SYMBOL = "VNM"
data = osapi.foreign(SYMBOL, limit=30)

total_buy  = sum(e.buy_volume  for e in data)
total_sell = sum(e.sell_volume for e in data)
net        = total_buy - total_sell

trend = "MUA RÒNG 📈" if net > 0 else "BÁN RÒNG 📉"

print(f"=== Phân tích dòng tiền ngoại: {SYMBOL} (30 phiên) ===")
print(f"Tổng mua  : {total_buy:,}")
print(f"Tổng bán  : {total_sell:,}")
print(f"Mua/Bán ròng: {net:+,} → Khối ngoại đang {trend}")
```

> [!TIP]
> Theo dõi hành động của khối ngoại là một trong những chỉ báo quan trọng về tâm lý thị trường trong ngắn hạn đối với các mã cổ phiếu có vốn hóa lớn (VN30).

---

## 3. Sổ Lệnh & Sổ Khớp Lệnh (Order Book & Ticks)

> [!IMPORTANT]
> Phần này yêu cầu tối thiểu tài khoản **Pro**. Gọi API với tài khoản Free sẽ nhận lỗi `TierRequiredError`.

**Tier yêu cầu**: `Pro` ⭐  
**Provider**: VCI (Vietcap - Sổ lệnh) / MAS & KBS (Sổ khớp lệnh)

### Use Case 1.10 — Sổ lệnh chờ khớp (Bid/Ask Board)

Lấy danh sách các mức giá mua chờ khớp (bids) và bán chờ khớp (asks) hiện tại của một mã cổ phiếu (Vietcap hỗ trợ 3 mức tốt nhất):

```python
import openstockapi as osapi

data = osapi.bid_ask("HPG")

print(f"Mã CP: {data.get('symbol')}")
print("Bids:")
for b in data.get('bids', []):
    print(f"  Giá: {b.get('price'):,.0f} VND | Vol: {b.get('volume'):,} CP")

print("Asks:")
for a in data.get('asks', []):
    print(f"  Giá: {a.get('price'):,.0f} VND | Vol: {a.get('volume'):,} CP")
```

**Kết quả mẫu:**
```
Mã CP: HPG
Bids:
  Giá: 21,800 VND | Vol: 850,600 CP
  Giá: 21,750 VND | Vol: 104,200 CP
  Giá: 21,700 VND | Vol: 15,300 CP
Asks:
  Giá: 21,850 VND | Vol: 1,047,300 CP
  Giá: 21,900 VND | Vol: 59,000 CP
  Giá: 21,950 VND | Vol: 60,500 CP
```

---

### Use Case 1.11 — Sổ khớp lệnh trong ngày (Intraday Ticks)

Theo dõi lịch sử các lệnh đã khớp thành công từng giây/phút trong ngày giao dịch từ MAS hoặc KBS:

```python
import openstockapi as osapi

# Lấy 5 lệnh khớp gần nhất
ticks = osapi.ticks("VNM", limit=5)

for t in ticks:
    print(f"[{t.get('timestamp')}] Giá: {t.get('price'):,.1f} | Khối lượng: {t.get('volume'):,} | Bên chủ động: {t.get('side')}")
```

**Kết quả mẫu:**
```
[2026-07-21 14:45:24] Giá: 59,000.0 | Khối lượng: 2,800 | Bên chủ động: BUY
[2026-07-21 14:29:57] Giá: 59,000.0 | Khối lượng: 5,900 | Bên chủ động: SELL
[2026-07-21 14:29:55] Giá: 59,000.0 | Khối lượng: 100 | Bên chủ động: SELL
```

> [!TIP]
> Bạn có thể chuyển đổi danh sách Ticks sang Pandas DataFrame rất dễ dàng bằng cách cài gói `openstockapi[pandas]` để phân tích luồng tiền chủ động (Buy/Sell Volume Imbalance).
