---
id: derivatives-and-funds
title: "Module 03: Phái Sinh & Quỹ Mở (Derivatives & Mutual Funds)"
description: Hướng dẫn lấy thông tin hợp đồng tương lai, chứng quyền và thông tin chứng chỉ quỹ mở tại Việt Nam.
category: Derivatives
difficulty: Trung bình
tier: Free / Pro
tags: [derivatives, futures, warrant, fund, mutual-fund, nav, holdings]
---

# Module 03: Phái Sinh & Quỹ Mở (Derivatives & Mutual Funds)

Module này cung cấp thông tin về các sản phẩm chứng khoán phái sinh (Hợp đồng tương lai, Chứng quyền có bảo đảm) và dữ liệu các quỹ mở hoạt động tại Việt Nam.

---

## 1. Chứng Khoán Phái Sinh (Vietnam Derivatives Data)

> [!NOTE]
> Chức năng này yêu cầu người dùng sở hữu Tier **PRO** trở lên.

### Use Case 3.1 — Lấy thông tin chi tiết (profile) của phái sinh / chứng quyền

Hàm `derivative_profile` cho phép lấy chi tiết thông tin của một mã hợp đồng tương lai (Futures) hoặc chứng quyền (Covered Warrants), bao gồm các biên dao động giá (trần, sàn, tham chiếu) và các thông số cụ thể của sản phẩm.

#### Tham số (Parameters)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | `str` | Yes | Mã hợp đồng tương lai (VD: `VN30F1M`) hoặc chứng quyền (VD: `CHPG2401`). |
| `provider` | `str` | No | Định danh provider. Mặc định là `kbs`. |
| `market` | `str` | No | Mã thị trường. Mặc định là `VN`. |

#### Ví dụ sử dụng (Python Example)

```python
import openstockapi as osapi

# Khởi động với API key Pro hoặc Premium
osapi.init(api_key="your_pro_api_key")

# 1. Lấy thông tin Hợp đồng tương lai chỉ số VN30
future_profile = osapi.derivative_profile("VN30F1M")
print("Future Profile:")
print(future_profile)

# 2. Lấy thông tin Chứng quyền có bảo đảm HPG
warrant_profile = osapi.derivative_profile("CHPG2401")
print("\nWarrant Profile:")
print(warrant_profile)
```

#### Dữ liệu mẫu trả về (Sample Output)

##### Hợp đồng tương lai (`VN30F1M`):
```json
{
  "symbol": "VN30F1M",
  "full_name": "VN30 Index Futures 082026",
  "underlying_symbol": "VN30",
  "exchange": "HNX",
  "first_trading_date": "2026-07-17T00:00:00",
  "last_trading_date": "2026-08-20T00:00:00",
  "reference_price": 1250.0,
  "ceiling_price": 1337.5,
  "floor_price": 1162.5,
  "open_interest": 45120,
  "warrant_type": null,
  "exercise_price": null,
  "conversion_ratio": null,
  "provider": "kbs",
  "market": "vn",
  "asset_class": "derivative"
}
```

##### Chứng quyền (`CHPG2401`):
```json
{
  "symbol": "CHPG2401",
  "full_name": "Warrant CHPG2401 (Underlying: HPG)",
  "underlying_symbol": "HPG",
  "exchange": "HOSE",
  "first_trading_date": null,
  "last_trading_date": null,
  "reference_price": 1.2,
  "ceiling_price": 1.28,
  "floor_price": 1.12,
  "open_interest": null,
  "warrant_type": "Call",
  "exercise_price": 26.0,
  "conversion_ratio": 4.0,
  "provider": "kbs",
  "market": "vn",
  "asset_class": "derivative"
}
```

---

## 2. Quỹ Mở (Mutual Funds)

**Tier yêu cầu**: `Free`  
**Provider**: Fmarket Vietnam

Để sử dụng API, bạn cần biết **Fund ID** của quỹ trên Fmarket. Một số quỹ phổ biến tại Việt Nam:

| Fund ID | Tên Quỹ | Công ty quản lý |
| :---: | :--- | :--- |
| `23` | VESAF (Vietnam Enterprise Securities Active Fund) | VinaCapital |
| `27` | VFMVSF (VFM VN30 ETF) | VFM |
| `35` | DCVFMVN30 | Dragon Capital |
| `9`  | BVPF (Bao Viet Balanced Fund) | Bao Viet Fund |

---

### Use Case 3.2 — Xem chi tiết một quỹ mở

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

### Use Case 3.3 — Xem danh mục nắm giữ (Top Holdings)

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

### Use Case 3.4 — So sánh nhiều quỹ

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
