---
id: financial-statements
title: "Module 02: Báo Cáo Tài Chính (Financial Statements)"
description: Hướng dẫn lấy bảng cân đối kế toán, kết quả kinh doanh, lưu chuyển tiền tệ và các chỉ số tài chính.
category: Financial
difficulty: Cơ bản
tier: Free
tags: [financial, balance-sheet, income-statement, cashflow, ratios]
---

# Module 02: Báo Cáo Tài Chính (Financial Statements)

Module này cung cấp đầy đủ dữ liệu báo cáo tài chính của các doanh nghiệp niêm yết trên HOSE và HNX.

**Tier yêu cầu**: `Free`  
**Provider**: MAS (Mass Asset Securities) — GraphQL API

---

**Provider hỗ trợ**: MAS / TCBS (Hỗ trợ Auto-Switching tự động)

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

## Use Case 2.2 — Kết quả kinh doanh (Income Statement)

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

## Use Case 2.3 — Lưu chuyển tiền tệ (Cash Flow)

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

## Use Case 2.4 — Chỉ số tài chính (Financial Ratios)

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

## Use Case 2.5 — Phân tích toàn diện một doanh nghiệp

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
