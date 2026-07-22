---
id: block-trading
title: "Module 03: Giao Dịch Khối (Block Trading Data)"
description: Hướng dẫn lấy dữ liệu giao dịch khối ngoại, giao dịch tự doanh và giao dịch nội bộ/cổ đông lớn.
category: Trading
difficulty: Trung bình
tier: Pro
tags: [trading, foreign, insider, prop-trade, block-trading]
---

# Module 03: Giao Dịch Khối (Block Trading Data)

Module này cung cấp dữ liệu về các giao dịch lớn của nhà đầu tư nước ngoài, các công ty tự doanh và giao dịch của cổ đông nội bộ.

> [!IMPORTANT]
> Toàn bộ module này yêu cầu tối thiểu tài khoản **Pro**. Gọi API với tài khoản Free sẽ nhận lỗi `TierRequiredError`.

**Tier yêu cầu**: `Pro` ⭐  
**Provider**: VCI (Vietcap Securities)

---

## Thiết lập session Pro

Trước tiên, bạn cần khởi tạo session với API key Pro:

```python
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiết lập session với API key Pro của bạn
set_current_session("YOUR_PRO_API_KEY")
```

---

## Use Case 3.1 — Giao dịch khối ngoại (Foreign Trading)

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

## Use Case 3.2 — Giao dịch tự doanh (Proprietary Trading)

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

## Use Case 3.3 — Giao dịch nội bộ / Cổ đông lớn (Insider Trading)

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

## Use Case 3.4 — Phân tích tâm lý thị trường qua dòng tiền ngoại

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
