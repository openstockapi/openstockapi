---
id: financials-and-macro
title: "Module 02: Báo Cáo Tài Chính & Vĩ Mô (Financials & Macro)"
description: Hướng dẫn lấy dữ liệu báo cáo tài chính doanh nghiệp và các chỉ số kinh tế vĩ mô Việt Nam.
category: Financial
difficulty: Cơ bản
tier: Free
tags: [financial, balance-sheet, income-statement, cashflow, ratios, macro, economics]
---

# Module 02: Báo Cáo Tài Chính & Vĩ Mô (Financials & Macro)

Module này cung cấp đầy đủ dữ liệu báo cáo tài chính của các doanh nghiệp niêm yết (HOSE và HNX) cùng với các chỉ số kinh tế vĩ mô quan trọng của Việt Nam.

---

## 1. Báo Cáo Tài Chính (Financial Statements)

**Tier yêu cầu**: `Free`  
**Provider**: MAS (Mass Asset Securities) — GraphQL API hoặc TCBS (Hỗ trợ Auto-Switching tự động)

### Use Case 2.1 — Bảng cân đối kế toán (Balance Sheet)

```python
import openstockapi as osapi

# Lấy bảng cân đối kế toán theo năm (period="annual" hoặc "quarter", provider="mas")
data = osapi.balance_sheet(
    symbol="VNM",
    period="annual",      # "annual" (Năm) hoặc "quarter" (Quý)
    provider="mas"        # Tùy chọn nguồn thủ công: "mas", "tcbs" (Bỏ qua để dùng Auto-Switching)
)

for entry in data:
    print(f"Năm: {entry.year}")
    print(f"  Tổng tài sản     : {entry.total_assets:,.0f} VND")
    print(f"  Tổng nợ phải trả : {entry.total_liabilities:,.0f} VND")
    print(f"  Vốn chủ sở hữu  : {entry.equity:,.0f} VND")
```

**Tham số:**

| Tham số | Kiểu | Bắt buộc | Giá trị hợp lệ | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | **Có** | VD: `VNM` | Mã cổ phiếu |
| `period` | `str` | Không | `annual` (`Y`), `quarter` (`Q`) | Chu kỳ báo cáo (Mặc định: `quarter`) |
| `provider` | `str` | Không | Auto | Chỉ định nguồn dữ liệu thủ công: `"mas"`, `"tcbs"` |

---

### Use Case 2.2 — Kết quả kinh doanh (Income Statement)

```python
import openstockapi as osapi

# Lấy kết quả kinh doanh theo quý
data = osapi.income_statement("FPT", period="quarter")

for entry in data:
    print(f"Quý {entry.quarter}/{entry.year}")
    print(f"  Doanh thu thuần : {entry.net_revenue:,.0f} VND")
    print(f"  Lợi nhuận gộp   : {entry.gross_profit:,.0f} VND")
    print(f"  Lợi nhuận sau thuế: {entry.net_profit:,.0f} VND")
```

---

### Use Case 2.3 — Lưu chuyển tiền tệ (Cash Flow)

```python
import openstockapi as osapi

# Lấy dòng tiền theo năm
data = osapi.cashflow("VIC", period="annual")

for entry in data:
    print(f"Năm: {entry.year}")
    print(f"  Tiền từ hoạt động kinh doanh : {entry.operating_cashflow:,.0f} VND")
    print(f"  Tiền từ hoạt động đầu tư     : {entry.investing_cashflow:,.0f} VND")
    print(f"  Tiền từ hoạt động tài chính  : {entry.financing_cashflow:,.0f} VND")
```

---

### Use Case 2.4 — Chỉ số tài chính (Financial Ratios)

```python
import openstockapi as osapi

# Lấy các chỉ số tài chính quan trọng
data = osapi.ratios("HPG")

for entry in data:
    print(f"Năm {entry.year}:")
    print(f"  P/E  : {entry.pe:.2f}")
    print(f"  P/B  : {entry.pb:.2f}")
    print(f"  ROE  : {entry.roe:.2%}")
    print(f"  ROA  : {entry.roa:.2%}")
    print(f"  EPS  : {entry.eps:,.0f} VND")
```

---

### Use Case 2.5 — Phân tích toàn diện một doanh nghiệp

Kết hợp nhiều API để phân tích một công ty từ nhiều góc độ:

```python
import openstockapi as osapi

SYMBOL = "VNM"

# Lấy tất cả dữ liệu tài chính cùng lúc
balance  = osapi.balance_sheet(SYMBOL, period="annual")
income   = osapi.income_statement(SYMBOL, period="annual")
cashflow = osapi.cashflow(SYMBOL, period="annual")
ratios   = osapi.ratios(SYMBOL)

print(f"=== Phân tích tài chính: {SYMBOL} ===")
print(f"Số kỳ báo cáo (Balance Sheet) : {len(balance)}")
print(f"Số kỳ báo cáo (Income Stmt)  : {len(income)}")
print(f"Số kỳ báo cáo (Cash Flow)    : {len(cashflow)}")
print(f"Số kỳ báo cáo (Ratios)       : {len(ratios)}")
```

> [!TIP]
> Toàn bộ dữ liệu tài chính đều lấy từ Provider **MAS (Mass Asset Securities)** thông qua GraphQL, đảm bảo dữ liệu chuẩn hóa theo chuẩn IFRS/VAS.

---

## 2. Chỉ Số Vĩ Mô (Macro Economic Indicators)

**Tier yêu cầu**: `Free`  
**Provider**: MBK (Maybank Securities Vietnam) - Nguồn dữ liệu từ Ngân hàng Nhà nước (NHNN)

### Use Case 2.6 — Lấy các chỉ số vĩ mô

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

### Use Case 2.7 — Phân tích tốc độ tăng trưởng M2 và Tín dụng

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

### Use Case 2.8 — Kết hợp dữ liệu vĩ mô với dữ liệu cổ phiếu ngân hàng

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
