import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiet lap session (tai khoan Free)
set_current_session("free")


# ============================================================
# Use Case 2.1 — Bang can doi ke toan (Balance Sheet)
# ============================================================

# period: "annual" = theo nam, "quarter" = theo quy
balance = osapi.balance_sheet("VNM", period="annual")

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in balance])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("VNM_balance_sheet.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_balance_sheet.xlsx'")


# ============================================================
# Use Case 2.2 — Ket qua kinh doanh (Income Statement)
# ============================================================

income = osapi.income_statement("FPT", period="quarter")

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in income])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("FPT_income_statement.xlsx", index=False)
print("Da luu du lieu vao file 'FPT_income_statement.xlsx'")


# ============================================================
# Use Case 2.3 — Luu chuyen tien te (Cash Flow)
# ============================================================

cashflow = osapi.cashflow("VIC", period="annual")

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in cashflow])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("VIC_cashflow.xlsx", index=False)
print("Da luu du lieu vao file 'VIC_cashflow.xlsx'")


# ============================================================
# Use Case 2.4 — Chi so tai chinh (Financial Ratios)
# ============================================================

ratios = osapi.ratios("HPG")

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in ratios])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("HPG_ratios.xlsx", index=False)
print("Da luu du lieu vao file 'HPG_ratios.xlsx'")


# ============================================================
# Use Case 2.5 — Phan tich toan dien mot doanh nghiep
# ============================================================

# Lay tat ca du lieu tai chinh cua VNM
balance  = osapi.balance_sheet("VNM", period="annual")
income   = osapi.income_statement("VNM", period="annual")
cashflow = osapi.cashflow("VNM", period="annual")
ratios   = osapi.ratios("VNM")

# Luu ra 4 sheet trong cung 1 file Excel
with pd.ExcelWriter("VNM_full_financial.xlsx") as writer:
    pd.DataFrame([e.model_dump() for e in balance]).to_excel(writer, sheet_name="Balance Sheet", index=False)
    pd.DataFrame([e.model_dump() for e in income]).to_excel(writer, sheet_name="Income Statement", index=False)
    pd.DataFrame([e.model_dump() for e in cashflow]).to_excel(writer, sheet_name="Cash Flow", index=False)
    pd.DataFrame([e.model_dump() for e in ratios]).to_excel(writer, sheet_name="Ratios", index=False)

print("Da luu du lieu vao file 'VNM_full_financial.xlsx'")
