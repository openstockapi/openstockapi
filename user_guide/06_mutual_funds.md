---
id: mutual-funds
title: "Module 06: Quỹ Mở (Mutual Funds)"
description: Hướng dẫn lấy thông tin chi tiết quỹ mở tại Việt Nam bao gồm NAV, phí quản lý và danh mục cổ phiếu nắm giữ.
category: Fund
difficulty: Cơ bản
tier: Free
tags: [fund, mutual-fund, nav, holdings, fmarket]
---

# Module 06: Quỹ Mở (Mutual Funds)

Module này cung cấp thông tin chi tiết về các quỹ mở tại Việt Nam — bao gồm NAV (Giá trị tài sản ròng), phí quản lý và top 10 cổ phiếu nắm giữ trong danh mục.

**Tier yêu cầu**: `Free`  
**Provider**: Fmarket Vietnam

---

## Tìm hiểu về Fund ID trên Fmarket

Để sử dụng API, bạn cần biết **Fund ID** của quỹ trên Fmarket. Một số quỹ phổ biến tại Việt Nam:

| Fund ID | Tên Quỹ | Công ty quản lý |
| :---: | :--- | :--- |
| `23` | VESAF (Vietnam Enterprise Securities Active Fund) | VinaCapital |
| `27` | VFMVSF (VFM VN30 ETF) | VFM |
| `35` | DCVFMVN30 | Dragon Capital |
| `9`  | BVPF (Bao Viet Balanced Fund) | Bao Viet Fund |

---

## Use Case 6.1 — Xem chi tiết một quỹ mở

```python
import openstockapi as osapi

# VESAF - Fund ID = 23
fund = osapi.fund_details(23)

print(f"Tên quỹ     : {fund.name}")
print(f"NAV hiện tại: {fund.nav:,.0f} VND/CCQ")
print(f"Phí quản lý : {fund.management_fee:.2%}/năm")
print(f"Tổng tài sản: {fund.total_assets:,.0f} VND")
```

**Kết quả mẫu:**
```
Tên quỹ     : Vietnam Enterprise Securities Active Fund (VESAF)
NAV hiện tại: 28,450 VND/CCQ
Phí quản lý : 1.50%/năm
Tổng tài sản: 12,500,000,000,000 VND
```

---

## Use Case 6.2 — Xem danh mục nắm giữ (Top Holdings)

```python
import openstockapi as osapi

fund = osapi.fund_details(23)

print(f"=== Top Holdings của {fund.name} ===\n")
for i, holding in enumerate(fund.holdings, 1):
    print(f"  {i:2d}. {holding.symbol:<8} | Tỷ trọng: {holding.weight:.2%} | Giá trị: {holding.value:>20,.0f} VND")
```

**Kết quả mẫu:**
```
=== Top Holdings của Vietnam Enterprise Securities Active Fund (VESAF) ===

   1. VHM      | Tỷ trọng: 8.50% | Giá trị:    1,062,500,000,000 VND
   2. FPT      | Tỷ trọng: 7.20% | Giá trị:      900,000,000,000 VND
   3. MBB      | Tỷ trọng: 6.80% | Giá trị:      850,000,000,000 VND
   4. VNM      | Tỷ trọng: 5.90% | Giá trị:      737,500,000,000 VND
   5. HPG      | Tỷ trọng: 5.40% | Giá trị:      675,000,000,000 VND
```

---

## Use Case 6.3 — So sánh nhiều quỹ

So sánh NAV và phí quản lý của các quỹ để hỗ trợ quyết định đầu tư:

```python
import openstockapi as osapi

# Danh sách Fund ID cần so sánh
fund_ids = [23, 27, 35, 9]

print(f"{'STT':<5} {'Tên quỹ':<50} {'NAV':>15} {'Phí QL':>10}")
print("-" * 85)

for i, fund_id in enumerate(fund_ids, 1):
    fund = osapi.fund_details(fund_id)
    print(f"{i:<5} {fund.name:<50} {fund.nav:>15,.0f} {fund.management_fee:>10.2%}")
```

> [!NOTE]
> Danh sách Fund ID có thể xem trực tiếp trên trang web [fmarket.vn](https://fmarket.vn). Mỗi quỹ có một Fund ID duy nhất trong hệ thống Fmarket.
