---
id: macro-indicators
title: "Module 05: Chỉ Số Vĩ Mô (Macro Economic Indicators)"
description: Hướng dẫn lấy dữ liệu kinh tế vĩ mô Việt Nam như Cung tiền M2, Tín dụng hệ thống ngân hàng.
category: Macroeconomics
difficulty: Cơ bản
tier: Free
tags: [macro, m2, credit, monetary-policy, economics]
---

# Module 05: Chỉ Số Vĩ Mô (Macro Economic Indicators)

Module này cung cấp các chỉ số kinh tế vĩ mô của Việt Nam, bao gồm Cung tiền M2, Tín dụng hệ thống ngân hàng — nguồn dữ liệu từ Ngân hàng Nhà nước (NHNN) thông qua Maybank Securities Vietnam.

**Tier yêu cầu**: `Free`  
**Provider**: MBK (Maybank Securities Vietnam)

---

## Use Case 5.1 — Lấy các chỉ số vĩ mô

```python
import openstockapi as osapi

data = osapi.indicators()

for entry in data:
    print(f"{entry.date} | {entry.indicator_name}: {entry.value:,.2f} {entry.unit}")
```

**Kết quả mẫu:**
```
2025-06-30 | Cung tiền M2          : 16,850,000.00 Tỷ VND
2025-06-30 | Tín dụng hệ thống     : 14,230,000.00 Tỷ VND
2025-05-31 | Cung tiền M2          : 16,620,000.00 Tỷ VND
2025-05-31 | Tín dụng hệ thống     : 14,010,000.00 Tỷ VND
```

---

## Use Case 5.2 — Phân tích tốc độ tăng trưởng M2 và Tín dụng

Tính toán tốc độ tăng trưởng hàng tháng (Month-over-Month growth) của các chỉ số:

```python
import openstockapi as osapi

data = osapi.indicators()

# Nhóm dữ liệu theo tên chỉ số
from collections import defaultdict

grouped = defaultdict(list)
for entry in data:
    grouped[entry.indicator_name].append(entry)

# Tính tăng trưởng MoM cho từng chỉ số
for name, entries in grouped.items():
    # Sắp xếp theo thời gian tăng dần
    entries.sort(key=lambda x: x.date)
    print(f"\n=== {name} ===")
    for i in range(1, len(entries)):
        prev = entries[i - 1].value
        curr = entries[i].value
        growth = (curr - prev) / prev * 100 if prev else 0
        print(f"  {entries[i].date}: {curr:>15,.2f}  (MoM: {growth:+.2f}%)")
```

---

## Use Case 5.3 — Kết hợp dữ liệu vĩ mô với dữ liệu cổ phiếu ngân hàng

Phân tích mối tương quan giữa tín dụng tăng trưởng và cổ phiếu ngân hàng:

```python
import openstockapi as osapi

# Lấy dữ liệu vĩ mô
macro_data = osapi.indicators()

# Lấy đồng thời giá cổ phiếu nhóm ngân hàng (ví dụ: VCB, BID, CTG)
vcb_ohlcv = osapi.ohlcv("VCB", resolution="1M", start="2024-01-01", end="2025-06-30")
bid_ohlcv = osapi.ohlcv("BID", resolution="1M", start="2024-01-01", end="2025-06-30")

print(f"Số điểm dữ liệu vĩ mô  : {len(macro_data)}")
print(f"Số tháng dữ liệu VCB   : {len(vcb_ohlcv)}")
print(f"Số tháng dữ liệu BID   : {len(bid_ohlcv)}")
print("\nSẵn sàng để thực hiện phân tích tương quan!")
```

> [!NOTE]
> Dữ liệu vĩ mô được cập nhật theo tháng từ báo cáo chính thức của NHNN. Độ trễ dữ liệu thường từ 1–2 tháng so với thời điểm thực tế.
