# Module 04: Sổ Lệnh & Sổ Khớp Lệnh (Order Book & Ticks)

Module này cung cấp dữ liệu sổ lệnh (order book) bao gồm các mức giá mua/bán chờ khớp (bid/ask) và sổ khớp lệnh chi tiết trong ngày (intraday matching ticks).

> [!IMPORTANT]
> Module này yêu cầu tối thiểu tài khoản **Pro**. Gọi API với tài khoản Free sẽ nhận lỗi `TierRequiredError`.

**Tier yêu cầu**: `Pro` ⭐  
**Provider**: VCI (Vietcap - Sổ lệnh) / MAS & KBS (Sổ khớp lệnh)

---

## Thiết lập session Pro

```python
import openstockapi as osapi

# Khởi động với API key Pro hoặc Premium
osapi.init("pro_YOUR_KEY")
```

---

## Use Case 4.1 — Sổ lệnh chờ khớp (Bid/Ask Board)

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

## Use Case 4.2 — Sổ khớp lệnh trong ngày (Intraday Ticks)

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

